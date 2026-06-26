"""Smoke of Deceit and vision-modifier extractors for Dota 2 replays.

These two extractors were previously inline closures in ``gem.api.parse``.
They follow the same ``attach()`` / ``finalize()`` contract as the other
extractors (``objectives.py``, ``wards.py``): ``attach`` registers combat-log
callbacks on the parser, and ``finalize`` (called after ``parser.parse()``)
back-fills team numbers from the :class:`PlayerExtractor` snapshots and returns
the collected events.

``SmokeExtractor`` takes a :class:`PlayerExtractor` because it needs live hero
positions (``hero_pos``) at modifier-arrival time and the NPC-name → team map
for the post-parse back-fill — the same dependency pattern as
``gem.combat.aggregator._CombatAggregator``.

Smoke edge case (documented in CLAUDE.md, not a bug): the ``ITEM`` event fires
when the item is consumed; one ``MODIFIER_ADD`` fires per hero that receives the
buff. If the smoke breaks instantly (the activator stands inside a sentry's
truesight at activation), no ``MODIFIER_ADD`` follows and the group is empty —
this is correct game behaviour (the item was wasted), so the event is kept with
an empty ``smoked`` list. ``MODIFIER_ADD`` is filtered by ``target_is_hero`` to
exclude summoned units (e.g. Beastmaster boars) from the group.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from gem.combat.log import CombatLogEntry
from gem.results.models import SmokeEvent, VisionModifierEvent

if TYPE_CHECKING:
    from gem.extractors.players import PlayerExtractor
    from gem.parser import ReplayParser

# Modifiers that reveal / grant vision of enemy heroes. Kept here (rather than
# in the catalog) because the set is small and specific to this extractor.
VISION_MODIFIER_NAMES: frozenset[str] = frozenset(
    {
        # Slardar — Corrosive Haze (ultimate): true sight of target
        "modifier_slardar_amplify_damage",
        # Bounty Hunter — Track: true sight + gold bounty
        "modifier_bounty_hunter_track",
        # Dust of Appearance — item AoE reveal
        "modifier_item_dustofappearance",
        # Gem of True Sight — carrier aura (hero-level modifier on target)
        "modifier_item_gem_of_true_sight",
        "modifier_gem_active_truesight",
        # Oracle — False Promise: not a reveal but often comboed; skip
        # Zeus — Thundergods Wrath: global, not a per-hero modifier; skip
    }
)

_SMOKE_ITEM = "item_smoke_of_deceit"
_SMOKE_MODIFIER = "modifier_smoke_of_deceit"


class VisionModifierExtractor:
    """Collects vision-granting modifier windows (Slardar ulti, Track, Dust, Gem).

    ``MODIFIER_ADD`` opens an event (``end_tick=None``); ``MODIFIER_REMOVE``
    closes the most recently opened matching event. The same hero can have the
    same modifier applied multiple times (e.g. refreshed Dust), so open events
    are keyed by ``(modifier_name, target_name)`` and stacked LIFO.

    Attach to a ``ReplayParser`` before calling ``parse()``, then call
    ``finalize()`` to back-fill caster teams and get the events:

    Example:
        >>> ext = VisionModifierExtractor(player_ext)
        >>> ext.attach(parser)
        >>> parser.parse()
        >>> events = ext.finalize()

    Attributes:
        events: All vision-modifier events in chronological open order.
    """

    events: list[VisionModifierEvent]

    def __init__(self, player_ext: PlayerExtractor) -> None:
        """Initialize the extractor.

        Args:
            player_ext: Attached ``PlayerExtractor``, used to map caster NPC
                names to team numbers during ``finalize``.
        """
        self._player_ext = player_ext
        self.events = []
        # (modifier_name, target_name) → stack of not-yet-closed events.
        self._open: dict[tuple[str, str], list[VisionModifierEvent]] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register the combat-log callback with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        parser.on_combat_log_entry(self._on_entry)

    def _on_entry(self, entry: CombatLogEntry) -> None:
        mod = entry.inflictor_name
        if mod not in VISION_MODIFIER_NAMES:
            return
        if entry.log_type == "MODIFIER_ADD":
            ev = VisionModifierEvent(
                tick=entry.tick,
                end_tick=None,
                modifier_name=mod,
                target_name=entry.target_name,
                caster_name=entry.attacker_name,
                caster_team=0,  # back-filled in finalize()
            )
            self.events.append(ev)
            self._open.setdefault((mod, entry.target_name), []).append(ev)
        elif entry.log_type == "MODIFIER_REMOVE":
            key = (mod, entry.target_name)
            stack = self._open.get(key)
            if stack:
                stack.pop().end_tick = entry.tick
                if not stack:
                    del self._open[key]

    def finalize(self) -> list[VisionModifierEvent]:
        """Back-fill caster teams from player snapshots and return the events.

        Call after ``parser.parse()``.

        Returns:
            The collected vision-modifier events.
        """
        team_by_npc = _team_by_npc(self._player_ext)
        for ev in self.events:
            ev.caster_team = team_by_npc.get(ev.caster_name, 0)
        return self.events


class SmokeExtractor:
    """Collects Smoke of Deceit activations with their smoked-hero groups.

    The ``ITEM`` event (item consumed) opens a pending event keyed by the
    activator's NPC name. Each subsequent ``MODIFIER_ADD`` on a hero target adds
    that hero to the group and captures its live position; the activation
    centroid is the mean of those positions. ``MODIFIER_REMOVE`` closes the
    pending event once at least one hero was smoked.

    Attach to a ``ReplayParser`` before calling ``parse()``, then call
    ``finalize()`` to back-fill teams / centroids and get the events:

    Example:
        >>> ext = SmokeExtractor(player_ext)
        >>> ext.attach(parser)
        >>> parser.parse()
        >>> events = ext.finalize()

    Attributes:
        events: All smoke activations in chronological order.
    """

    events: list[SmokeEvent]

    def __init__(self, player_ext: PlayerExtractor) -> None:
        """Initialize the extractor.

        Args:
            player_ext: Attached ``PlayerExtractor``, used for live hero
                positions and the NPC-name → team map during ``finalize``.
        """
        self._player_ext = player_ext
        self.events = []
        # activator NPC → pending (not-yet-closed) event.
        self._pending: dict[str, SmokeEvent] = {}
        # activator NPC → live (x, y) positions captured at MODIFIER_ADD time.
        self._positions: dict[str, list[tuple[float, float]]] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register the combat-log callback with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        parser.on_combat_log_entry(self._on_entry)

    def _on_entry(self, entry: CombatLogEntry) -> None:
        if entry.log_type == "ITEM" and entry.inflictor_name == _SMOKE_ITEM:
            ev = SmokeEvent(tick=entry.tick, activator=entry.attacker_name, team=0)
            self._pending[entry.attacker_name] = ev
            self._positions[entry.attacker_name] = []
            self.events.append(ev)
        elif (
            entry.log_type == "MODIFIER_ADD"
            and entry.inflictor_name == _SMOKE_MODIFIER
            and entry.target_is_hero
        ):
            pending = self._pending.get(entry.attacker_name)
            if pending is not None:
                pending.smoked.append(entry.target_name)
                # Capture this hero's live position at buff-arrival time.
                pos = self._player_ext.hero_pos(entry.target_name)
                if pos is not None:
                    self._positions[entry.attacker_name].append(pos)
        elif (
            entry.log_type == "MODIFIER_REMOVE"
            and entry.inflictor_name == _SMOKE_MODIFIER
            and entry.target_is_hero
        ):
            pending = self._pending.get(entry.attacker_name)
            if pending is not None and len(pending.smoked) >= 1:
                self._pending.pop(entry.attacker_name, None)

    def finalize(self) -> list[SmokeEvent]:
        """Back-fill team + centroid from player snapshots and return the events.

        Call after ``parser.parse()``. The centroid (x, y) is the mean of the
        live positions captured at each hero's ``MODIFIER_ADD``; an empty group
        leaves the position ``None``.

        Returns:
            The collected smoke events.
        """
        team_by_npc = _team_by_npc(self._player_ext)
        for ev in self.events:
            ev.team = team_by_npc.get(ev.activator, 0)
            positions = self._positions.get(ev.activator, [])
            if positions:
                ev.x = sum(p[0] for p in positions) / len(positions)
                ev.y = sum(p[1] for p in positions) / len(positions)
        return self.events


def _team_by_npc(player_ext: PlayerExtractor) -> dict[str, int]:
    """Build an NPC-name → team map from player snapshots (non-zero teams only)."""
    return {snap.npc_name: snap.team for snap in player_ext.snapshots if snap.team}

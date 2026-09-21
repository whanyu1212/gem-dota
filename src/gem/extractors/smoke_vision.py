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
from gem.results.models import SmokeEvent, SmokeParticipant, VisionModifierEvent

if TYPE_CHECKING:
    from gem.extractors.players import PlayerExtractor, PlayerStateSnapshot
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
# The canonical fixture contains a legitimate late join 82 ticks after item use
# with a correspondingly shortened reported duration (42.23s of the 45s buff).
# Three seconds keeps that evidence while still bounding stray historical adds.
_SMOKE_ADD_WINDOW_TICKS = 90
_SMOKE_DEFAULT_REMOVE_WINDOW_TICKS = 60 * 30
_SMOKE_REMOVE_GRACE_TICKS = 60
_SMOKE_DEFAULT_REMOVE_WINDOW_S = _SMOKE_DEFAULT_REMOVE_WINDOW_TICKS / 30
_SMOKE_REMOVE_GRACE_S = _SMOKE_REMOVE_GRACE_TICKS / 30


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
    """Collect Smoke activations and each hero's modifier lifecycle.

    Every ``ITEM`` event creates a distinct activation. A hero-targeted
    ``MODIFIER_ADD`` joins the most recent same-activator activation whose item
    tick is not later than the modifier tick. Duplicate adds for the same hero
    are folded into one participant. ``MODIFIER_REMOVE`` closes only the most
    recently applied still-open participant for its target, so one hero losing
    smoke does not close the rest of the group.

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
        self._parser: ReplayParser | None = None
        self.events = []
        # Retain all item uses in activation order. Incomplete/empty activations
        # are evidence too and must not be overwritten by a later use from the
        # same caster.
        self._open_activations: list[SmokeEvent] = []
        # Matching removals needs a pause-aware clock: raw replay ticks continue
        # while modifier duration is frozen. Keys are object identities because
        # participants are mutable public dataclasses retained for the parse.
        self._participant_applied_game_time_s: dict[int, int] = {}

    def attach(self, parser: ReplayParser) -> None:
        """Register the combat-log callback with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_combat_log_entry(self._on_entry)

    def _on_entry(self, entry: CombatLogEntry) -> None:
        if entry.log_type == "ITEM" and entry.inflictor_name == _SMOKE_ITEM:
            ev = SmokeEvent(tick=entry.tick, activator=entry.attacker_name, team=0)
            self.events.append(ev)
            self._open_activations.append(ev)
        elif (
            entry.log_type == "MODIFIER_ADD"
            and entry.inflictor_name == _SMOKE_MODIFIER
            and entry.target_is_hero
        ):
            activation = self._activation_for_add(entry)
            if activation is not None:
                existing = next(
                    (p for p in activation.participants if p.hero_name == entry.target_name),
                    None,
                )
                if existing is None:
                    new_participant = SmokeParticipant(
                        hero_name=entry.target_name,
                        player_id=None,
                        applied_tick=entry.tick,
                        modifier_duration_s=entry.modifier_duration_s,
                        modifier_elapsed_duration_s=entry.modifier_elapsed_duration_s,
                    )
                    activation.participants.append(new_participant)
                    applied_game_time_s = self._entry_game_time_s(entry)
                    if applied_game_time_s is not None:
                        self._participant_applied_game_time_s[id(new_participant)] = (
                            applied_game_time_s
                        )
                    activation.smoked.append(entry.target_name)
                elif entry.tick < existing.applied_tick:
                    # Combat-log batches can be delivered out of order. Keep the
                    # canonical earliest add tick without duplicating the hero.
                    existing.applied_tick = entry.tick
                    applied_game_time_s = self._entry_game_time_s(entry)
                    if applied_game_time_s is not None:
                        self._participant_applied_game_time_s[id(existing)] = applied_game_time_s
                    if entry.modifier_duration_s is not None:
                        existing.modifier_duration_s = entry.modifier_duration_s
                    if entry.modifier_elapsed_duration_s is not None:
                        existing.modifier_elapsed_duration_s = entry.modifier_elapsed_duration_s
                else:
                    if existing.modifier_duration_s is None:
                        existing.modifier_duration_s = entry.modifier_duration_s
                    if existing.modifier_elapsed_duration_s is None:
                        existing.modifier_elapsed_duration_s = entry.modifier_elapsed_duration_s
        elif (
            entry.log_type == "MODIFIER_REMOVE"
            and entry.inflictor_name == _SMOKE_MODIFIER
            and entry.target_is_hero
        ):
            participant = self._participant_for_remove(entry)
            if participant is not None:
                participant.removed_tick = entry.tick
                if entry.modifier_duration_s is not None:
                    participant.modifier_duration_s = entry.modifier_duration_s
                if entry.modifier_elapsed_duration_s is not None:
                    participant.modifier_elapsed_duration_s = entry.modifier_elapsed_duration_s

    def _activation_for_add(self, entry: CombatLogEntry) -> SmokeEvent | None:
        eligible = [
            (index, event)
            for index, event in enumerate(self._open_activations)
            if event.activator == entry.attacker_name
            and event.tick <= entry.tick
            and entry.tick - event.tick <= _SMOKE_ADD_WINDOW_TICKS
        ]
        if not eligible:
            return None
        # The list index breaks same-tick ties in favour of the latest item use.
        return max(eligible, key=lambda pair: (pair[1].tick, pair[0]))[1]

    def _participant_for_remove(self, entry: CombatLogEntry) -> SmokeParticipant | None:
        removal_game_time_s = self._entry_game_time_s(entry)
        eligible = [
            participant
            for event in self._open_activations
            for participant in event.participants
            if participant.hero_name == entry.target_name
            and participant.removed_tick is None
            and participant.applied_tick <= entry.tick
            and self._removal_is_within_window(
                participant,
                entry,
                removal_game_time_s,
            )
        ]
        if not eligible:
            return None
        return max(eligible, key=lambda participant: participant.applied_tick)

    def _entry_game_time_s(self, entry: CombatLogEntry) -> int | None:
        """Return the best pause-aware game clock available for an entry."""
        if entry.game_time_s is not None:
            return entry.game_time_s
        if self._parser is not None:
            return getattr(self._parser, "game_time_s", None)
        return None

    def _removal_is_within_window(
        self,
        participant: SmokeParticipant,
        entry: CombatLogEntry,
        removal_game_time_s: int | None,
    ) -> bool:
        """Return whether a removal plausibly belongs to ``participant``.

        Modifier elapsed time and the replay's game clock freeze during pauses,
        unlike raw replay ticks. Use either pause-aware source when possible and
        keep the historical raw-tick deadline only for evidence-poor entries.
        """
        duration_s = participant.modifier_duration_s
        if duration_s is None or duration_s <= 0:
            duration_s = entry.modifier_duration_s
        if duration_s is None or duration_s <= 0:
            duration_s = _SMOKE_DEFAULT_REMOVE_WINDOW_S
        deadline_s = duration_s + _SMOKE_REMOVE_GRACE_S

        applied_game_time_s = self._participant_applied_game_time_s.get(id(participant))
        if applied_game_time_s is not None and removal_game_time_s is not None:
            elapsed_game_time_s = removal_game_time_s - applied_game_time_s
            return 0 <= elapsed_game_time_s <= deadline_s

        elapsed_s = entry.modifier_elapsed_duration_s
        if elapsed_s is not None:
            return 0 <= elapsed_s <= deadline_s

        return entry.tick <= _participant_remove_deadline(participant)

    def finalize(self) -> list[SmokeEvent]:
        """Back-fill identities and exact-tick sampled positions.

        Call after ``parser.parse()``. ``activation_x``/``activation_y`` use the
        activator snapshot nearest the item-use tick. Participant coordinates
        use their own exact apply/remove ticks. Legacy ``x``/``y`` remain the
        centroid of available participant application positions; an empty group
        leaves that centroid ``None``.

        Returns:
            The collected smoke events.
        """
        snapshot_index = _snapshots_by_npc(self._player_ext)
        team_by_npc = _team_by_npc(self._player_ext)
        for ev in self.events:
            activation_snapshot = _snapshot_at_tick(snapshot_index, ev.activator, ev.tick)
            ev.team = (
                activation_snapshot.team
                if activation_snapshot is not None and activation_snapshot.team
                else team_by_npc.get(ev.activator, 0)
            )
            activation_pos = _snapshot_position(activation_snapshot)
            if activation_pos is not None:
                ev.activation_x, ev.activation_y = activation_pos

            positions: list[tuple[float, float]] = []
            for participant in ev.participants:
                applied_snapshot = _snapshot_at_tick(
                    snapshot_index, participant.hero_name, participant.applied_tick
                )
                if applied_snapshot is not None:
                    participant.player_id = applied_snapshot.player_id
                applied_pos = _snapshot_position(applied_snapshot)
                if applied_pos is not None:
                    participant.applied_x, participant.applied_y = applied_pos
                    positions.append(applied_pos)

                if participant.removed_tick is not None:
                    removed_snapshot = _snapshot_at_tick(
                        snapshot_index,
                        participant.hero_name,
                        participant.removed_tick,
                    )
                    removed_pos = _snapshot_position(removed_snapshot)
                    if removed_pos is not None:
                        participant.removed_x, participant.removed_y = removed_pos

            if positions:
                ev.x = sum(p[0] for p in positions) / len(positions)
                ev.y = sum(p[1] for p in positions) / len(positions)
        return self.events


def _team_by_npc(player_ext: PlayerExtractor) -> dict[str, int]:
    """Build an NPC-name → team map from player snapshots (non-zero teams only)."""
    return {snap.npc_name: snap.team for snap in player_ext.snapshots if snap.team}


def _snapshots_by_npc(
    player_ext: PlayerExtractor,
) -> dict[str, list[PlayerStateSnapshot]]:
    """Index position-capable player snapshots by NPC name."""
    result: dict[str, list[PlayerStateSnapshot]] = {}
    for snapshot in player_ext.snapshots:
        npc_name = getattr(snapshot, "npc_name", None)
        tick = getattr(snapshot, "tick", None)
        if not isinstance(npc_name, str) or not isinstance(tick, int):
            continue
        result.setdefault(npc_name, []).append(snapshot)
    for snapshots in result.values():
        snapshots.sort(key=lambda snapshot: snapshot.tick)
    return result


def _snapshot_at_tick(
    snapshot_index: dict[str, list[PlayerStateSnapshot]], npc_name: str, tick: int
) -> PlayerStateSnapshot | None:
    """Return the nearest sampled state for ``npc_name`` at a canonical tick."""
    snapshots = snapshot_index.get(npc_name)
    if not snapshots:
        return None
    return min(snapshots, key=lambda snapshot: abs(snapshot.tick - tick))


def _snapshot_position(
    snapshot: PlayerStateSnapshot | None,
) -> tuple[float, float] | None:
    """Return a snapshot's complete position pair, if available."""
    if snapshot is None:
        return None
    x = getattr(snapshot, "x", None)
    y = getattr(snapshot, "y", None)
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return None
    return (float(x), float(y))


def _participant_remove_deadline(participant: SmokeParticipant) -> int:
    """Return the latest plausible removal tick for a participant."""
    duration_s = participant.modifier_duration_s
    if duration_s is not None and duration_s > 0:
        duration_ticks = round(duration_s * 30)
        return participant.applied_tick + duration_ticks + _SMOKE_REMOVE_GRACE_TICKS
    return participant.applied_tick + _SMOKE_DEFAULT_REMOVE_WINDOW_TICKS

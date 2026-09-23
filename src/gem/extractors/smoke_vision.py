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

from dataclasses import dataclass
from typing import TYPE_CHECKING

from gem.combat.log import CombatLogEntry
from gem.results.models import (
    SmokeEvent,
    SmokeParticipant,
    VisionModifierCloseEvidence,
    VisionModifierEvent,
    VisionModifierLifecycleStatus,
    VisionModifierPairingIssue,
    VisionModifierPairingStatus,
    VisionModifierSemantic,
    VisionModifierTeamSource,
)

if TYPE_CHECKING:
    from gem.extractors.players import PlayerExtractor, PlayerStateSnapshot
    from gem.parser import ReplayParser


@dataclass(frozen=True, slots=True)
class VisionModifierDescriptor:
    """Static meaning assigned to one tracked modifier name."""

    semantic: VisionModifierSemantic


# This deliberately distinguishes target reveals from carrier/aura evidence.
# Consumers that answer point-vision questions may use only direct target
# reveals; the remaining descriptors are preserved for later structured aura
# analysis rather than being silently misinterpreted.
VISION_MODIFIER_DESCRIPTORS: dict[str, VisionModifierDescriptor] = {
    "modifier_slardar_amplify_damage": VisionModifierDescriptor(
        VisionModifierSemantic.DIRECT_TARGET_REVEAL
    ),
    "modifier_bounty_hunter_track": VisionModifierDescriptor(
        VisionModifierSemantic.DIRECT_TARGET_REVEAL
    ),
    "modifier_item_dustofappearance": VisionModifierDescriptor(
        VisionModifierSemantic.DIRECT_TARGET_REVEAL
    ),
    "modifier_item_gem_of_true_sight": VisionModifierDescriptor(
        VisionModifierSemantic.AURA_CARRIER
    ),
    "modifier_gem_active_truesight": VisionModifierDescriptor(VisionModifierSemantic.REVEAL_AURA),
}

_VISION_EXPIRY_TOLERANCE_S = 1.5


@dataclass(frozen=True, slots=True)
class _VisionObservation:
    entry: CombatLogEntry
    ingestion_order: int


@dataclass(slots=True)
class _PendingVisionRemoval:
    """An ambiguous removal and the applications eligible when it occurred."""

    entry: CombatLogEntry
    candidates: list[VisionModifierEvent]


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
    """Collect evidence-preserving vision-modifier application lifecycles.

    Relevant observations are buffered and resolved deterministically in
    ``finalize()``. A removal is never assigned by stack order when several
    prior applications remain plausible; ambiguous and orphan removals are
    retained separately as :class:`VisionModifierPairingIssue` objects.

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
    pairing_issues: list[VisionModifierPairingIssue]

    def __init__(self, player_ext: PlayerExtractor) -> None:
        """Initialize the extractor.

        Args:
            player_ext: Attached ``PlayerExtractor``, used to map caster NPC
                names to team numbers during ``finalize``.
        """
        self._player_ext = player_ext
        self._parser: ReplayParser | None = None
        self.events = []
        self.pairing_issues = []
        self._observations: list[_VisionObservation] = []
        self._finalized = False

    def attach(self, parser: ReplayParser) -> None:
        """Register the combat-log callback with the parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_combat_log_entry(self._on_entry)

    def _on_entry(self, entry: CombatLogEntry) -> None:
        mod = entry.inflictor_name
        if mod not in VISION_MODIFIER_DESCRIPTORS:
            return
        if entry.log_type in ("MODIFIER_ADD", "MODIFIER_REMOVE"):
            self._observations.append(_VisionObservation(entry, len(self._observations)))

    def finalize(self) -> list[VisionModifierEvent]:
        """Resolve pairing, lifecycle, and team evidence and return applications.

        Call after ``parser.parse()``.

        Returns:
            The collected vision-modifier events.
        """
        if self._finalized:
            return self.events
        self._finalized = True

        team_by_npc, ambiguous_team_npcs = _team_evidence_by_npc(self._player_ext)
        open_events: dict[tuple[str, str], list[VisionModifierEvent]] = {}
        pending_removals: dict[tuple[str, str], list[_PendingVisionRemoval]] = {}
        ambiguous_ids: set[int] = set()

        for observation in self._ordered_observations():
            entry = observation.entry
            key = (entry.inflictor_name, entry.target_name)
            if entry.log_type == "MODIFIER_ADD":
                added_event = self._event_from_add(entry)
                self.events.append(added_event)
                open_events.setdefault(key, []).append(added_event)
                continue

            candidates = list(open_events.get(key, []))
            paired_event, status = self._select_candidate(entry, candidates)
            if paired_event is None:
                if status is VisionModifierPairingStatus.AMBIGUOUS:
                    pending_removals.setdefault(key, []).append(
                        _PendingVisionRemoval(entry, candidates)
                    )
                else:
                    self.pairing_issues.append(self._pairing_issue(entry, "unmatched", []))
                continue

            self._close_event(open_events, key, paired_event, entry, status)
            self._retry_pending_removals(open_events, pending_removals, key)

        for key in list(pending_removals):
            self._retry_pending_removals(open_events, pending_removals, key)
            for pending in pending_removals.get(key, []):
                candidates = self._still_open_candidates(
                    open_events,
                    key,
                    pending.candidates,
                )
                status = self._select_candidate(pending.entry, candidates)[1]
                reason = (
                    "ambiguous" if status is VisionModifierPairingStatus.AMBIGUOUS else "unmatched"
                )
                issue_candidates = candidates if reason == "ambiguous" else []
                self.pairing_issues.append(
                    self._pairing_issue(pending.entry, reason, issue_candidates)
                )
                if reason == "ambiguous":
                    for candidate in candidates:
                        candidate.pairing_status = VisionModifierPairingStatus.AMBIGUOUS
                        candidate.lifecycle_status = VisionModifierLifecycleStatus.INCOMPLETE
                        candidate.close_evidence = VisionModifierCloseEvidence.AMBIGUOUS
                        if "ambiguous_removal" not in candidate.evidence_gaps:
                            candidate.evidence_gaps.append("ambiguous_removal")
                        ambiguous_ids.add(id(candidate))

        final_game_time_s = self._final_game_time_s()
        for event in self.events:
            self._attribute_teams(event, team_by_npc, ambiguous_team_npcs)
            if event.end_tick is None:
                self._classify_unclosed(event, final_game_time_s, id(event) in ambiguous_ids)
        return self.events

    def _retry_pending_removals(
        self,
        open_events: dict[tuple[str, str], list[VisionModifierEvent]],
        pending_removals: dict[tuple[str, str], list[_PendingVisionRemoval]],
        key: tuple[str, str],
    ) -> None:
        """Resolve removals made unique by later, stronger pairing evidence."""
        pending = pending_removals.get(key)
        if not pending:
            return

        made_progress = True
        while made_progress:
            made_progress = False
            for removal in list(pending):
                candidates = self._still_open_candidates(
                    open_events,
                    key,
                    removal.candidates,
                )
                event, status = self._select_candidate(removal.entry, candidates)
                if event is None:
                    continue
                self._close_event(open_events, key, event, removal.entry, status)
                pending.remove(removal)
                made_progress = True
                break

        if not pending:
            del pending_removals[key]

    @staticmethod
    def _still_open_candidates(
        open_events: dict[tuple[str, str], list[VisionModifierEvent]],
        key: tuple[str, str],
        original_candidates: list[VisionModifierEvent],
    ) -> list[VisionModifierEvent]:
        current_ids = {id(event) for event in open_events.get(key, [])}
        return [event for event in original_candidates if id(event) in current_ids]

    def _close_event(
        self,
        open_events: dict[tuple[str, str], list[VisionModifierEvent]],
        key: tuple[str, str],
        event: VisionModifierEvent,
        remove: CombatLogEntry,
        status: VisionModifierPairingStatus,
    ) -> None:
        remaining = [candidate for candidate in open_events[key] if candidate is not event]
        if remaining:
            open_events[key] = remaining
        else:
            del open_events[key]
        self._apply_remove(event, remove, status)

    def _event_from_add(self, entry: CombatLogEntry) -> VisionModifierEvent:
        descriptor = VISION_MODIFIER_DESCRIPTORS[entry.inflictor_name]
        gaps: list[str] = []
        if not entry.target_name:
            gaps.append("missing_target_name")
        if not entry.attacker_name:
            gaps.append("missing_caster_name")
        return VisionModifierEvent(
            tick=entry.tick,
            end_tick=None,
            modifier_name=entry.inflictor_name,
            target_name=entry.target_name,
            caster_name=entry.attacker_name,
            caster_team=0,
            semantic=descriptor.semantic,
            pairing_status=VisionModifierPairingStatus.UNMATCHED,
            target_is_hero=entry.target_is_hero,
            caster_is_hero=entry.attacker_is_hero,
            caster_is_illusion=entry.attacker_is_illusion,
            target_is_illusion=entry.target_is_illusion,
            caster_is_hero_present=entry.attacker_is_hero_present,
            target_is_hero_present=entry.target_is_hero_present,
            caster_is_illusion_present=entry.attacker_is_illusion_present,
            target_is_illusion_present=entry.target_is_illusion_present,
            add_attacker_team=entry.attacker_team,
            add_target_team=entry.target_team,
            add_source=entry.source,
            add_game_time_s=entry.game_time_s,
            add_modifier_duration_s=entry.modifier_duration_s,
            add_modifier_elapsed_duration_s=entry.modifier_elapsed_duration_s,
            add_aura_modifier=entry.aura_modifier,
            evidence_gaps=gaps,
        )

    def _select_candidate(
        self,
        remove: CombatLogEntry,
        candidates: list[VisionModifierEvent],
    ) -> tuple[VisionModifierEvent | None, VisionModifierPairingStatus]:
        if not candidates:
            return None, VisionModifierPairingStatus.UNMATCHED

        narrowed = candidates
        if remove.attacker_name:
            caster_compatible = [
                event
                for event in candidates
                if not event.caster_name or event.caster_name == remove.attacker_name
            ]
            if not caster_compatible:
                return None, VisionModifierPairingStatus.UNMATCHED
            narrowed = caster_compatible

        identity_matches = [
            event for event in narrowed if self._identity_flags_match(event, remove)
        ]
        if not identity_matches:
            return None, VisionModifierPairingStatus.UNMATCHED
        narrowed = identity_matches
        if (
            remove.attacker_name
            and len(narrowed) == 1
            and narrowed[0].caster_name == remove.attacker_name
        ):
            return narrowed[0], VisionModifierPairingStatus.EXACT

        timed = self._duration_match(remove, narrowed)
        if timed is not None:
            return timed, VisionModifierPairingStatus.EXACT
        if len(narrowed) == 1:
            return narrowed[0], VisionModifierPairingStatus.UNIQUE_FALLBACK
        return None, VisionModifierPairingStatus.AMBIGUOUS

    @staticmethod
    def _duration_match(
        remove: CombatLogEntry,
        candidates: list[VisionModifierEvent],
    ) -> VisionModifierEvent | None:
        elapsed = remove.modifier_elapsed_duration_s
        if elapsed is None:
            return None

        scored: list[tuple[float, VisionModifierEvent]] = []
        for event in candidates:
            if remove.game_time_s is None or event.add_game_time_s is None:
                continue
            observed_age = float(remove.game_time_s - event.add_game_time_s)
            scored.append((abs(observed_age - elapsed), event))
        scored.sort(key=lambda item: item[0])
        if not scored or scored[0][0] > _VISION_EXPIRY_TOLERANCE_S:
            return None
        if len(scored) > 1 and abs(scored[1][0] - scored[0][0]) < 1e-6:
            return None
        return scored[0][1]

    @staticmethod
    def _identity_flags_match(
        event: VisionModifierEvent,
        remove: CombatLogEntry,
    ) -> bool:
        """Return whether explicit add/remove identity flags are compatible."""
        checks = (
            (
                event.caster_is_hero_present,
                event.caster_is_hero,
                remove.attacker_is_hero_present,
                remove.attacker_is_hero,
            ),
            (
                event.target_is_hero_present,
                event.target_is_hero,
                remove.target_is_hero_present,
                remove.target_is_hero,
            ),
            (
                event.caster_is_illusion_present,
                event.caster_is_illusion,
                remove.attacker_is_illusion_present,
                remove.attacker_is_illusion,
            ),
            (
                event.target_is_illusion_present,
                event.target_is_illusion,
                remove.target_is_illusion_present,
                remove.target_is_illusion,
            ),
        )
        return all(
            not (add_present and remove_present) or add_value == remove_value
            for add_present, add_value, remove_present, remove_value in checks
        )

    def _ordered_observations(self) -> list[_VisionObservation]:
        """Return deterministic tick order, using timestamps only for complete ties."""
        by_tick: dict[int, list[_VisionObservation]] = {}
        for observation in self._observations:
            by_tick.setdefault(observation.entry.tick, []).append(observation)

        ordered: list[_VisionObservation] = []
        for tick in sorted(by_tick):
            group = by_tick[tick]
            if all(item.entry.timestamp_s is not None for item in group):
                group = sorted(
                    group,
                    key=lambda item: (item.entry.timestamp_s, item.ingestion_order),
                )
            else:
                group = sorted(group, key=lambda item: item.ingestion_order)
            ordered.extend(group)
        return ordered

    def _apply_remove(
        self,
        event: VisionModifierEvent,
        remove: CombatLogEntry,
        pairing_status: VisionModifierPairingStatus,
    ) -> None:
        event.end_tick = remove.tick
        event.pairing_status = pairing_status
        event.close_evidence = VisionModifierCloseEvidence.OBSERVED
        event.remove_source = remove.source
        event.remove_attacker_team = remove.attacker_team
        event.remove_target_team = remove.target_team
        event.remove_game_time_s = remove.game_time_s
        event.remove_modifier_duration_s = remove.modifier_duration_s
        event.remove_modifier_elapsed_duration_s = remove.modifier_elapsed_duration_s
        event.remove_aura_modifier = remove.aura_modifier
        event.remove_modifier_purged = remove.modifier_purged
        event.remove_modifier_purged_duration_s = remove.modifier_purged_duration_s
        event.remove_caster_name = remove.attacker_name
        event.remove_caster_is_hero = (
            remove.attacker_is_hero if remove.attacker_is_hero_present else None
        )
        event.remove_target_is_hero = (
            remove.target_is_hero if remove.target_is_hero_present else None
        )
        event.remove_caster_is_illusion = (
            remove.attacker_is_illusion if remove.attacker_is_illusion_present else None
        )
        event.remove_target_is_illusion = (
            remove.target_is_illusion if remove.target_is_illusion_present else None
        )
        if not event.modifier_name or not event.target_name or not event.caster_name:
            event.lifecycle_status = VisionModifierLifecycleStatus.INCOMPLETE
            return
        event.lifecycle_status = (
            VisionModifierLifecycleStatus.EXPIRED
            if self._observed_near_expiry(event)
            else VisionModifierLifecycleStatus.REMOVED
        )

    @staticmethod
    def _observed_near_expiry(event: VisionModifierEvent) -> bool:
        if event.remove_modifier_purged is True:
            return False
        intended = (
            event.remove_modifier_duration_s
            if event.remove_modifier_duration_s is not None
            else event.add_modifier_duration_s
        )
        if intended is None or intended <= 0:
            return False
        elapsed = event.remove_modifier_elapsed_duration_s
        if (
            elapsed is None
            and event.add_game_time_s is not None
            and event.remove_game_time_s is not None
        ):
            elapsed = float(event.remove_game_time_s - event.add_game_time_s)
        if elapsed is None:
            return False
        tolerance = max(_VISION_EXPIRY_TOLERANCE_S, intended * 0.03)
        return abs(elapsed - intended) <= tolerance

    def _attribute_teams(
        self,
        event: VisionModifierEvent,
        team_by_npc: dict[str, int],
        ambiguous_team_npcs: set[str],
    ) -> None:
        caster_protocol = self._valid_team(event.add_attacker_team)
        if caster_protocol == 0:
            caster_protocol = self._valid_team(event.remove_attacker_team)
        if caster_protocol:
            event.caster_team = caster_protocol
            event.caster_team_source = VisionModifierTeamSource.PROTOCOL
        else:
            event.caster_team = self._valid_team(team_by_npc.get(event.caster_name))
            if event.caster_team:
                event.caster_team_source = VisionModifierTeamSource.SNAPSHOT_FALLBACK
            else:
                gap = (
                    "caster_team_ambiguous"
                    if event.caster_name in ambiguous_team_npcs
                    else "caster_team_unknown"
                )
                event.evidence_gaps.append(gap)

        target_protocol = self._valid_team(event.add_target_team)
        if target_protocol == 0:
            target_protocol = self._valid_team(event.remove_target_team)
        if target_protocol:
            event.target_team = target_protocol
            event.target_team_source = VisionModifierTeamSource.PROTOCOL
        else:
            event.target_team = self._valid_team(team_by_npc.get(event.target_name))
            if event.target_team:
                event.target_team_source = VisionModifierTeamSource.SNAPSHOT_FALLBACK
            else:
                gap = (
                    "target_team_ambiguous"
                    if event.target_name in ambiguous_team_npcs
                    else "target_team_unknown"
                )
                event.evidence_gaps.append(gap)

    @staticmethod
    def _valid_team(team: int | None) -> int:
        return team if team in (2, 3) else 0

    def _classify_unclosed(
        self,
        event: VisionModifierEvent,
        final_game_time_s: int | None,
        ambiguous: bool,
    ) -> None:
        if ambiguous or not event.modifier_name or not event.target_name or not event.caster_name:
            event.lifecycle_status = VisionModifierLifecycleStatus.INCOMPLETE
            if ambiguous:
                event.pairing_status = VisionModifierPairingStatus.AMBIGUOUS
                event.close_evidence = VisionModifierCloseEvidence.AMBIGUOUS
            else:
                event.close_evidence = VisionModifierCloseEvidence.UNOBSERVED
            return
        duration = event.add_modifier_duration_s
        if (
            duration is not None
            and duration > 0
            and event.add_game_time_s is not None
            and final_game_time_s is not None
            and final_game_time_s - event.add_game_time_s >= duration + _VISION_EXPIRY_TOLERANCE_S
        ):
            event.lifecycle_status = VisionModifierLifecycleStatus.EXPIRED
            event.close_evidence = VisionModifierCloseEvidence.DURATION_INFERRED
            event.evidence_gaps.append("removal_not_observed")
            return
        event.lifecycle_status = VisionModifierLifecycleStatus.OPEN
        event.close_evidence = VisionModifierCloseEvidence.UNOBSERVED
        event.evidence_gaps.append("removal_not_observed")

    def _final_game_time_s(self) -> int | None:
        if self._parser is None:
            return None
        duration = getattr(self._parser, "duration_s", None)
        if duration is not None:
            return duration
        return getattr(self._parser, "combat_log_time_s", None)

    @staticmethod
    def _pairing_issue(
        remove: CombatLogEntry,
        reason: str,
        candidates: list[VisionModifierEvent],
    ) -> VisionModifierPairingIssue:
        return VisionModifierPairingIssue(
            tick=remove.tick,
            reason=reason,
            modifier_name=remove.inflictor_name,
            caster_name=remove.attacker_name,
            target_name=remove.target_name,
            source=remove.source,
            candidate_add_ticks=[event.tick for event in candidates],
            game_time_s=remove.game_time_s,
            modifier_duration_s=remove.modifier_duration_s,
            modifier_elapsed_duration_s=remove.modifier_elapsed_duration_s,
            attacker_team=remove.attacker_team,
            target_team=remove.target_team,
            caster_is_hero=(remove.attacker_is_hero if remove.attacker_is_hero_present else None),
            target_is_hero=(remove.target_is_hero if remove.target_is_hero_present else None),
            caster_is_illusion=(
                remove.attacker_is_illusion if remove.attacker_is_illusion_present else None
            ),
            target_is_illusion=(
                remove.target_is_illusion if remove.target_is_illusion_present else None
            ),
            aura_modifier=remove.aura_modifier,
            modifier_purged=remove.modifier_purged,
            modifier_purged_duration_s=remove.modifier_purged_duration_s,
        )


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
            ev = SmokeEvent(
                tick=entry.tick,
                activator=entry.attacker_name,
                team=0,
                activation_game_time_s=self._entry_game_time_s(entry),
            )
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
                        applied_game_time_s=self._entry_game_time_s(entry),
                    )
                    activation.participants.append(new_participant)
                    applied_game_time_s = new_participant.applied_game_time_s
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
                    existing.applied_game_time_s = applied_game_time_s
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
                participant.removed_game_time_s = self._entry_game_time_s(entry)
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


def _team_evidence_by_npc(
    player_ext: PlayerExtractor,
) -> tuple[dict[str, int], set[str]]:
    """Return consensus snapshot teams and names with conflicting evidence."""
    teams_by_npc: dict[str, set[int]] = {}
    for snapshot in player_ext.snapshots:
        npc_name = getattr(snapshot, "npc_name", None)
        team = getattr(snapshot, "team", None)
        if isinstance(npc_name, str) and npc_name and team in (2, 3):
            teams_by_npc.setdefault(npc_name, set()).add(team)

    resolved = {
        npc_name: next(iter(teams)) for npc_name, teams in teams_by_npc.items() if len(teams) == 1
    }
    ambiguous = {npc_name for npc_name, teams in teams_by_npc.items() if len(teams) > 1}
    return resolved, ambiguous


def _team_by_npc(player_ext: PlayerExtractor) -> dict[str, int]:
    """Build an NPC-name → consensus team map from player snapshots."""
    resolved, _ambiguous = _team_evidence_by_npc(player_ext)
    return resolved


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

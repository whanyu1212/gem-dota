"""Tests for evidence-first Smoke of Deceit lifecycle analysis."""

from __future__ import annotations

import pytest

from gem.analysis.smoke import (
    SmokeGroupStatus,
    SmokeLifecycleStatus,
    build_smoke_analysis,
)
from gem.combat.log import CombatLogEntry
from gem.extractors.teamfights import Teamfight
from gem.results.models import (
    HeroVisibilityEvent,
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisibilityState,
)


def _participant(**kwargs: object) -> SmokeParticipant:
    values: dict[str, object] = {
        "hero_name": "npc_dota_hero_axe",
        "player_id": 0,
        "applied_tick": 100,
        "removed_tick": 1_450,
        "modifier_duration_s": 45.0,
    }
    values.update(kwargs)
    return SmokeParticipant(**values)  # type: ignore[arg-type]


def _visibility(
    *,
    tick: int,
    player_id: int,
    dire_state: VisibilityState,
) -> HeroVisibilityEvent:
    return HeroVisibilityEvent(
        tick=tick,
        player_id=player_id,
        hero_name=f"hero_{player_id}",
        entity_index=player_id,
        entity_serial=1,
        radiant_state=VisibilityState.UNKNOWN,
        dire_state=dire_state,
    )


def test_group_statuses_and_duration_tolerance() -> None:
    match = ParsedMatch(
        smoke_events=[
            SmokeEvent(tick=10, activator="empty", team=2),
            SmokeEvent(
                tick=90,
                activator="expired",
                team=2,
                participants=[_participant(removed_tick=1_450)],
            ),
            SmokeEvent(
                tick=190,
                activator="tolerance",
                team=2,
                participants=[
                    _participant(
                        applied_tick=200,
                        removed_tick=500,
                        modifier_elapsed_duration_s=44.75,
                    )
                ],
            ),
            SmokeEvent(
                tick=290,
                activator="early",
                team=2,
                participants=[
                    _participant(
                        applied_tick=300,
                        removed_tick=600,
                        modifier_elapsed_duration_s=44.74,
                    )
                ],
            ),
            SmokeEvent(
                tick=390,
                activator="incomplete",
                team=2,
                participants=[_participant(applied_tick=400, removed_tick=None)],
            ),
        ]
    )

    analyses = build_smoke_analysis(match)

    assert analyses[0].status is SmokeGroupStatus.NO_MEMBERS_OBSERVED
    assert analyses[1].members[0].lifecycle_status is SmokeLifecycleStatus.EXPIRED
    assert analyses[1].status is SmokeGroupStatus.EXPIRED
    assert analyses[2].members[0].lifecycle_status is SmokeLifecycleStatus.EXPIRED
    assert analyses[3].members[0].lifecycle_status is SmokeLifecycleStatus.EARLY
    assert analyses[3].status is SmokeGroupStatus.EARLY_REMOVAL
    assert analyses[4].members[0].lifecycle_status is SmokeLifecycleStatus.UNOBSERVED
    assert analyses[4].status is SmokeGroupStatus.INCOMPLETE


def test_visibility_preserves_hidden_visible_unknown_and_first_transition() -> None:
    participants = [
        _participant(hero_name="hero_hidden", player_id=0, removed_tick=300),
        _participant(hero_name="hero_visible", player_id=1, removed_tick=300),
        _participant(hero_name="hero_unknown", player_id=2, removed_tick=300),
    ]
    match = ParsedMatch(
        players=[
            ParsedPlayer(player_id=0, hero_name="hero_hidden", team=2),
            ParsedPlayer(player_id=1, hero_name="hero_visible", team=2),
            ParsedPlayer(player_id=2, hero_name="hero_unknown", team=2),
        ],
        smoke_events=[
            SmokeEvent(
                tick=99,
                activator="hero_hidden",
                team=2,
                participants=participants,
            )
        ],
        hero_visibility_events=[
            _visibility(tick=90, player_id=0, dire_state=VisibilityState.HIDDEN),
            _visibility(tick=200, player_id=0, dire_state=VisibilityState.VISIBLE),
            _visibility(tick=250, player_id=0, dire_state=VisibilityState.HIDDEN),
            _visibility(tick=90, player_id=1, dire_state=VisibilityState.HIDDEN),
            _visibility(tick=200, player_id=1, dire_state=VisibilityState.VISIBLE),
        ],
    )

    members = {member.hero_name: member for member in build_smoke_analysis(match)[0].members}

    hidden = members["hero_hidden"]
    assert hidden.visibility_at_apply is VisibilityState.HIDDEN
    assert hidden.visibility_at_remove is VisibilityState.HIDDEN
    assert hidden.first_visible_tick == 200
    visible = members["hero_visible"]
    assert visible.visibility_at_apply is VisibilityState.HIDDEN
    assert visible.visibility_at_remove is VisibilityState.VISIBLE
    assert visible.first_visible_tick == 200
    unknown = members["hero_unknown"]
    assert unknown.visibility_at_apply is VisibilityState.UNKNOWN
    assert unknown.visibility_at_remove is VisibilityState.UNKNOWN
    assert unknown.first_visible_tick is None


def test_removal_evidence_and_followup_teamfight_remain_factual() -> None:
    participant = _participant(
        hero_name="npc_dota_hero_axe",
        player_id=0,
        applied_tick=101,
        removed_tick=300,
        removed_x=0.0,
        removed_y=0.0,
    )
    ability = CombatLogEntry(
        tick=300,
        log_type="ABILITY",
        attacker_name="npc_dota_hero_axe",
        inflictor_name="axe_berserkers_call",
    )
    death = CombatLogEntry(
        tick=300,
        log_type="DEATH",
        target_name="npc_dota_hero_axe",
    )
    later_action = CombatLogEntry(
        tick=301,
        log_type="ABILITY",
        attacker_name="npc_dota_hero_axe",
    )
    first_fight = Teamfight(
        start_tick=1_700,
        end_tick=2_000,
        last_death_tick=1_950,
        deaths=3,
        first_death_tick=1_900,
    )
    out_of_window_fight = Teamfight(
        start_tick=2_000,
        end_tick=2_300,
        last_death_tick=2_200,
        deaths=3,
        first_death_tick=2_001,
    )
    match = ParsedMatch(
        players=[
            ParsedPlayer(
                player_id=0,
                hero_name="npc_dota_hero_axe",
                team=2,
                position_log=[(300, 0.0, 0.0)],
            ),
            ParsedPlayer(
                player_id=5,
                hero_name="npc_dota_hero_lina",
                team=3,
                position_log=[(300, 3.0, 4.0)],
            ),
            ParsedPlayer(
                player_id=6,
                hero_name="npc_dota_hero_invoker",
                team=3,
                position_log=[(300, 30.0, 40.0)],
            ),
        ],
        smoke_events=[
            SmokeEvent(
                tick=100,
                activator="npc_dota_hero_axe",
                team=2,
                participants=[participant],
            )
        ],
        combat_log=[ability, death, later_action],
        teamfights=[out_of_window_fight, first_fight],
    )

    analysis = build_smoke_analysis(match)[0]
    member = analysis.members[0]

    assert analysis.activation_tick == 100
    assert member.applied_tick == 101
    assert member.removed_tick == 300
    assert member.nearest_enemy_hero == "npc_dota_hero_lina"
    assert member.nearest_enemy_player_id == 5
    assert member.nearest_enemy_distance == pytest.approx(5.0)
    assert member.same_tick_actions == [ability]
    assert member.same_tick_deaths == [death]
    assert analysis.first_teamfight is first_fight


def test_teamfight_window_includes_exact_sixty_second_boundary() -> None:
    boundary_fight = Teamfight(
        start_tick=1_600,
        end_tick=2_000,
        last_death_tick=1_950,
        deaths=3,
        first_death_tick=1_900,
    )
    match = ParsedMatch(
        smoke_events=[SmokeEvent(tick=100, activator="hero", team=2)],
        teamfights=[boundary_fight],
    )

    assert build_smoke_analysis(match)[0].first_teamfight is boundary_fight

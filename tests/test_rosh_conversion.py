from __future__ import annotations

import pytest

from gem.analysis.roshan import (
    AegisFateSource,
    RoshConversion,
    RoshFightRelation,
    RoshTagThresholds,
    RoshTeamAttributionSource,
    _rax_lane,
    build_rosh_conversions,
)
from gem.combat.log import CombatLogEntry
from gem.extractors.objectives import (
    AegisEvent,
    BannerPlant,
    BarracksKill,
    RoshanKill,
    TormentorKill,
    TowerKill,
)
from gem.extractors.teamfights import Teamfight, TeamfightPlayer
from gem.extractors.wards import WardEvent
from gem.reports._sections import build_rosh_conversion
from gem.results.models import ParsedMatch, ParsedPlayer


def _make_players() -> list[ParsedPlayer]:
    players: list[ParsedPlayer] = []
    for pid in range(10):
        team = 2 if pid < 5 else 3
        players.append(
            ParsedPlayer(
                player_id=pid,
                hero_name=f"npc_dota_hero_hero_{pid}",
                team=team,
            )
        )
    return players


def _make_fight(start: int, end: int, winner: str, deaths: int = 2) -> Teamfight:
    return Teamfight(
        start_tick=start,
        end_tick=end,
        last_death_tick=end - 60,
        deaths=deaths,
        winner=winner,
        players=[TeamfightPlayer(player_id=i) for i in range(10)],
    )


def test_build_rosh_conversions_objective_conversion() -> None:
    players = _make_players()
    players[0].position_log = [(800, 9800.0, 9800.0), (1300, 24500.0, 22000.0)]
    players[1].position_log = [(820, 9900.0, 9850.0), (1320, 23850.0, 21400.0)]
    players[5].buyback_log = [CombatLogEntry(tick=1500, log_type="BUYBACK")]

    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        towers=[
            TowerKill(
                tick=1600,
                team=3,
                killer="npc_dota_hero_hero_0",
                tower_name="npc_dota_badguys_tower2_mid",
            ),
            TowerKill(
                tick=1700,
                team=3,
                killer="npc_dota_hero_hero_1",
                tower_name="npc_dota_badguys_tower2_top",
            ),
        ],
        barracks=[
            BarracksKill(
                tick=2000,
                team=3,
                killer="npc_dota_hero_hero_0",
                barracks_name="npc_dota_badguys_melee_rax_mid",
            )
        ],
        wards=[
            WardEvent(
                tick=1400,
                player_id=0,
                placer="npc_dota_hero_hero_0",
                ward_type="observer",
                team=2,
                x=24500.0,
                y=22000.0,
                expires_tick=None,
                killed_tick=None,
                killer="",
            )
        ],
        teamfights=[_make_fight(1200, 1450, "radiant")],
        combat_log=[],
    )

    conversions = build_rosh_conversions(match)
    assert len(conversions) == 1
    conversion = conversions[0]
    assert conversion.conversion_label == "objective_conversion"
    assert conversion.fights_won == 1
    assert conversion.towers_taken == 2
    assert conversion.barracks_taken == 1
    assert conversion.enemy_buybacks_forced == 1
    assert conversion.enemy_half_observer_delta == 1
    assert conversion.enemy_half_farm_share_delta > 0.0
    assert any(event.kind == "barracks" for event in conversion.timeline_events)


def test_build_rosh_conversions_failed_aegis_on_lost_fight() -> None:
    players = _make_players()
    players[5].position_log = [(1800, 23000.0, 22000.0), (2250, 15000.0, 15000.0)]

    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=9000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=2000, killer="npc_dota_hero_hero_5", kill_number=1)],
        aegis_events=[AegisEvent(tick=2010, player_id=5, event_type="pickup")],
        teamfights=[_make_fight(2200, 2600, "radiant")],
        combat_log=[
            CombatLogEntry(
                tick=2300,
                log_type="DEATH",
                target_name="npc_dota_hero_hero_5",
                target_is_hero=True,
                target_is_illusion=False,
            )
        ],
    )

    conversions = build_rosh_conversions(match)
    assert len(conversions) == 1
    conversion = conversions[0]
    assert conversion.aegis_fate == "consumed"
    assert conversion.conversion_label == "low_conversion"
    assert conversion.aegis_outcome == "window_lost"
    assert conversion.fights_lost == 1
    assert conversion.towers_taken == 0
    assert conversion.barracks_taken == 0
    assert any(event.kind == "aegis_end" for event in conversion.timeline_events)


def test_build_rosh_conversions_uses_first_death_for_fight_timing() -> None:
    players = _make_players()
    fight = Teamfight(
        start_tick=500,
        end_tick=1300,
        last_death_tick=850,
        deaths=2,
        first_death_tick=950,
        winner="radiant",
        players=[TeamfightPlayer(player_id=i) for i in range(10)],
    )
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=4000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        teamfights=[fight],
    )

    conversion = build_rosh_conversions(match)[0]
    assert conversion.first_fight_tick == 1010
    fight_events = [
        event for event in conversion.timeline_events if event.kind.startswith("fight_")
    ]
    assert fight_events
    assert fight_events[0].tick == 1010
    assert "already underway" in fight_events[0].label.lower()
    assert fight_events[0].fight_index == 0
    assert conversion.first_engagement_tick is not None
    assert conversion.fight_evidence[0].relation is RoshFightRelation.PREEXISTING


def test_holder_window_clamped_to_next_roshan_no_double_count() -> None:
    # Two back-to-back Roshans. The first aegis is consumed (holder dies), which
    # extends the holder window by the post-consume grace. That grace must NOT
    # bleed past the next Roshan kill, or a tower destroyed after Rosh #2 is
    # counted in BOTH conversion records. Regression for the missing clamp to
    # extended_end_tick (next_rosh_tick - 1).
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        radiant_win=None,
        players=players,
        # Both holders are Radiant (hero_0, hero_1) so the lone Dire tower is a
        # valid objective for whichever Roshan window contains it — isolating the
        # double-count from team-attribution effects.
        roshans=[
            RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1),
            RoshanKill(tick=1500, killer="npc_dota_hero_hero_1", kill_number=2),
        ],
        aegis_events=[
            AegisEvent(tick=1010, player_id=0, event_type="pickup"),
            AegisEvent(tick=1510, player_id=1, event_type="pickup"),
        ],
        # Holder of aegis #1 (hero_0) dies at 1050 -> aegis consumed -> grace
        # pushes the raw window end well past Rosh #2's 1500 kill.
        combat_log=[
            CombatLogEntry(
                tick=1050,
                log_type="DEATH",
                target_name="npc_dota_hero_hero_0",
                target_is_hero=True,
            )
        ],
        # A single Dire tower at 1800 — after Rosh #2, so it belongs only to the
        # second Roshan's window, never the first.
        towers=[
            TowerKill(
                tick=1800,
                team=3,
                killer="npc_dota_hero_hero_1",
                tower_name="npc_dota_badguys_tower2_mid",
            )
        ],
    )

    conversions = build_rosh_conversions(match)
    assert len(conversions) == 2
    # The lone tower must be attributed to exactly one Roshan, not both.
    total_towers = sum(c.towers_taken for c in conversions)
    assert total_towers == 1, f"tower double-counted across Roshans: {total_towers}"
    assert conversions[0].towers_taken == 0
    assert conversions[1].towers_taken == 1


def test_rosh_conversion_legacy_constructor_keeps_working() -> None:
    # RoshConversion is part of the public ``gem`` API, so the drops + banner→rax
    # fields must stay optional: a caller using the pre-drops keyword set must
    # still construct without a missing-argument TypeError, and the new fields
    # must fall back to safe legacy defaults.
    conversion = RoshConversion(
        rosh_number=1,
        rosh_tick=1000,
        killer_name="npc_dota_hero_x",
        holder_team=2,
        holder_player_id=0,
        holder_name="npc_dota_hero_x",
        aegis_pickup_tick=1010,
        immediate_end_tick=6400,
        aegis_end_tick=10000,
        aegis_eval_end_tick=10000,
        extended_end_tick=10000,
        aegis_fate="expired",
        first_fight_tick=None,
        first_objective_tick=None,
        fight_count=0,
        fights_won=0,
        fights_lost=0,
        fights_drawn=0,
        towers_taken=0,
        barracks_taken=0,
        enemy_buybacks_forced=0,
        enemy_half_observer_delta=0,
        enemy_half_farm_share_before=0.0,
        enemy_half_farm_share_during=0.0,
        enemy_half_farm_share_delta=0.0,
        conversion_score=25,
        conversion_label="low_conversion",
        aegis_outcome="expired_unused",
    )
    assert conversion.drops == []
    assert conversion.had_high_value_drop is False
    assert conversion.banner_planted is False
    assert conversion.banner_rax_conversion is False
    assert conversion.banner_rax_lane is None
    assert conversion.roshan_team is None
    assert conversion.conversion_team is None
    assert conversion.aegis_fate_inferred is False
    assert conversion.conversion_tags == []
    assert conversion.analysis_status == "unavailable"
    assert conversion.differential_profile.conversion_team is None


def test_rax_lane_parses_known_suffixes() -> None:
    assert _rax_lane("npc_dota_badguys_melee_rax_mid") == "mid"
    assert _rax_lane("npc_dota_goodguys_range_rax_top") == "top"
    assert _rax_lane("npc_dota_badguys_melee_rax_bot") == "bot"
    # No lane suffix (or an unknown one) yields None rather than guessing.
    assert _rax_lane("npc_dota_badguys_fort") is None


def test_banner_rax_conversion_links_plant_to_barracks() -> None:
    # Radiant (hero_0) holds the Aegis, plants a banner, then an enemy (Dire)
    # mid rax falls after the plant -> banner_rax_conversion on the mid lane.
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        banner_plants=[BannerPlant(tick=1200, team=2, player_id=0, x=22000.0, y=18000.0)],
        barracks=[
            BarracksKill(
                tick=1500,
                team=3,
                killer="npc_dota_hero_hero_0",
                barracks_name="npc_dota_badguys_melee_rax_mid",
            )
        ],
    )

    conversion = build_rosh_conversions(match)[0]
    assert conversion.banner_planted is True
    assert conversion.banner_rax_conversion is True
    assert conversion.banner_rax_lane == "mid"
    assert any("Banner" in driver for driver in conversion.drivers)


def test_banner_planted_without_rax_is_not_a_conversion() -> None:
    # A banner planted in the window but with no enemy rax falling afterwards is
    # surfaced as planted-only — never asserted as a rax conversion.
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        banner_plants=[BannerPlant(tick=1200, team=2, player_id=0, x=22000.0, y=18000.0)],
    )

    conversion = build_rosh_conversions(match)[0]
    assert conversion.banner_planted is True
    assert conversion.banner_rax_conversion is False
    assert conversion.banner_rax_lane is None


def test_banner_rax_ignores_rax_before_plant_and_enemy_banner() -> None:
    # Two guards in one: a rax that fell BEFORE the plant must not count, and an
    # enemy-team banner must not attribute to the Radiant holder.
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        radiant_win=None,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        # Enemy (Dire) banner — wrong team for the Radiant holder.
        banner_plants=[BannerPlant(tick=1300, team=3, player_id=5, x=8000.0, y=8000.0)],
        # Rax fell at 1100, before any (hypothetical) Radiant plant.
        barracks=[
            BarracksKill(
                tick=1100,
                team=3,
                killer="npc_dota_hero_hero_0",
                barracks_name="npc_dota_badguys_melee_rax_mid",
            )
        ],
    )

    conversion = build_rosh_conversions(match)[0]
    assert conversion.banner_planted is False
    assert conversion.banner_rax_conversion is False


def test_build_rosh_conversion_html_banner_badge() -> None:
    # A banner→rax conversion renders the planted line and the "→ Rax" badge with
    # the lane in the card.
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=6000,
        radiant_win=None,
        players=players,
        roshans=[
            RoshanKill(
                tick=1000,
                killer="npc_dota_hero_hero_0",
                kill_number=1,
                drops=["aegis", "banner"],
            )
        ],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        banner_plants=[BannerPlant(tick=1200, team=2, player_id=0, x=22000.0, y=18000.0)],
        barracks=[
            BarracksKill(
                tick=1500,
                team=3,
                killer="npc_dota_hero_hero_0",
                barracks_name="npc_dota_badguys_melee_rax_mid",
            )
        ],
    )

    html = build_rosh_conversion(match)
    assert "Banner planted" in html
    assert "rosh-banner-badge" in html
    assert "Rax" in html  # the lane-tagged badge text
    # The summary-table Rax cell gains the banner flag marker.
    assert "⚑" in html


def test_build_rosh_conversion_html_smoke() -> None:
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=6000,
        radiant_win=None,
        players=players,
        roshans=[
            RoshanKill(
                tick=1000,
                killer="npc_dota_hero_hero_0",
                kill_number=1,
                drops=["aegis", "cheese", "banner"],
            )
        ],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
    )

    html = build_rosh_conversion(match)
    assert "Roshan Conversion" in html
    assert "Roshan #1" in html
    # Drops surface on the card (human-readable) and the summary table gains a
    # Drops column; a non-Aegis premium drop flips the high-value badge on.
    assert "Drops:" in html
    assert "Aegis, Cheese, Banner" in html
    assert "rosh-hv-badge" in html
    assert "<th>Drops</th>" in html


def test_build_rosh_conversion_html_no_high_value_badge_for_aegis_only() -> None:
    # An Aegis-only kill must NOT show the high-value badge — guards against the
    # badge firing on every Roshan regardless of drop contents.
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=6000,
        radiant_win=None,
        players=players,
        roshans=[
            RoshanKill(
                tick=1000,
                killer="npc_dota_hero_hero_0",
                kill_number=1,
                drops=["aegis"],
            )
        ],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
    )

    html = build_rosh_conversion(match)
    assert "rosh-hv-badge" not in html


@pytest.mark.parametrize(
    ("holder_id", "expected_sign"),
    [(0, 1), (5, -1)],
)
def test_differential_resource_curves_are_signed_to_conversion_team(
    holder_id: int, expected_sign: int
) -> None:
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=players,
        roshans=[
            RoshanKill(
                tick=1000,
                killer=f"npc_dota_hero_hero_{holder_id}",
                kill_number=1,
            )
        ],
        aegis_events=[AegisEvent(tick=1010, player_id=holder_id, event_type="pickup")],
        game_times_min=[0, 60, 120, 180, 240, 300, 360, 420],
        radiant_gold_adv=[0, 100, 300, 700, 1300, 2200, 3300, 4700],
        radiant_xp_adv=[0, 50, 150, 350, 700, 1200, 1800, 2500],
    )

    profile = build_rosh_conversions(match)[0].differential_profile
    assert profile.net_worth_advantage_start == 100 * expected_sign
    assert profile.net_worth_swing is not None
    assert profile.net_worth_swing * expected_sign > 0
    assert profile.xp_swing is not None
    assert profile.xp_swing * expected_sign > 0


def test_missing_resource_curves_remain_unavailable() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
    )
    profile = build_rosh_conversions(match)[0].differential_profile
    assert profile.net_worth_advantage_start is None
    assert profile.net_worth_advantage_end is None
    assert profile.net_worth_swing is None
    assert profile.xp_swing is None
    assert "net_worth_series_unavailable" in profile.status_reasons


def test_differential_counts_both_sides_and_tormentor_timeline() -> None:
    players = _make_players()
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=15000,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        teamfights=[
            _make_fight(1200, 1400, "radiant"),
            _make_fight(1600, 1800, "radiant"),
            _make_fight(2000, 2200, "dire"),
        ],
        towers=[
            TowerKill(2400, 3, "", "npc_dota_badguys_tower2_mid", killer_team=2),
            TowerKill(2500, 2, "", "npc_dota_goodguys_tower1_mid", killer_team=3),
        ],
        barracks=[
            BarracksKill(
                2600,
                3,
                "",
                "npc_dota_badguys_melee_rax_mid",
                killer_team=2,
            ),
        ],
        wards=[
            WardEvent(2700, 0, "", "observer", 2, 24000.0, 21000.0, None, None, ""),
            WardEvent(2800, 5, "", "observer", 3, 8804.0, 11034.0, None, None, ""),
        ],
        tormentors=[
            TormentorKill(2900, "", 0, 1),
            TormentorKill(3000, "", 5, 2),
        ],
    )

    conversion = build_rosh_conversions(match)[0]
    profile = conversion.differential_profile
    assert profile.fight_differential == 1
    assert profile.conversion_towers == 1
    assert profile.opponent_towers == 1
    assert profile.conversion_barracks == 1
    assert profile.structure_delta == 5
    assert profile.forward_ward_delta == 0
    assert profile.tormentor_delta == 0
    kinds = {event.kind for event in conversion.timeline_events}
    assert {"tower", "tower_lost", "barracks", "tormentor", "opponent_tormentor"} <= kinds


def test_structure_denies_are_not_credited_to_either_team() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        towers=[
            TowerKill(
                tick=1500,
                team=2,
                killer="npc_dota_hero_hero_0",
                tower_name="npc_dota_goodguys_tower3_mid",
            ),
            TowerKill(
                tick=1550,
                team=3,
                killer="npc_dota_hero_hero_5",
                tower_name="npc_dota_badguys_tower3_mid",
            ),
        ],
        barracks=[
            BarracksKill(
                tick=1600,
                team=2,
                killer="npc_dota_hero_hero_1",
                barracks_name="npc_dota_goodguys_melee_rax_mid",
            ),
            BarracksKill(
                tick=1650,
                team=3,
                killer="npc_dota_hero_hero_6",
                barracks_name="npc_dota_badguys_melee_rax_mid",
            ),
        ],
    )

    conversion = build_rosh_conversions(match)[0]
    profile = conversion.differential_profile
    assert profile.conversion_towers == 0
    assert profile.opponent_towers == 0
    assert profile.conversion_barracks == 0
    assert profile.opponent_barracks == 0
    assert profile.structure_delta == 0
    assert conversion.towers_taken == 0
    assert conversion.barracks_taken == 0
    assert conversion.first_objective_tick is None
    assert not {"tower", "tower_lost", "barracks", "barracks_lost"} & {
        event.kind for event in conversion.timeline_events
    }


def test_tormentor_attribution_falls_back_to_killer_hero() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        tormentors=[
            TormentorKill(
                tick=1500,
                killer="npc_dota_hero_hero_0",
                killer_player_id=-1,
                kill_number=1,
            )
        ],
    )

    conversion = build_rosh_conversions(match)[0]
    profile = conversion.differential_profile
    assert profile.conversion_tormentors == 1
    assert profile.opponent_tormentors == 0
    assert profile.tormentor_delta == 1
    assert "tormentor_attribution_unavailable" not in profile.status_reasons
    assert any(event.kind == "tormentor" for event in conversion.timeline_events)
    assert all(event.kind != "tormentor_unknown" for event in conversion.timeline_events)


def test_consumed_aegis_is_inferred_only_inside_ownership_horizon() -> None:
    players = _make_players()
    inside = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        combat_log=[
            CombatLogEntry(
                tick=2000,
                log_type="DEATH",
                target_name="npc_dota_hero_hero_0",
                target_is_hero=True,
            )
        ],
    )
    conversion = build_rosh_conversions(inside)[0]
    assert conversion.aegis_fate == "consumed"
    assert conversion.aegis_fate_inferred is True
    assert conversion.aegis_fate_source is AegisFateSource.HOLDER_DEATH_INFERENCE

    outside = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        combat_log=[
            CombatLogEntry(
                tick=1010 + 5 * 60 * 30 + 1,
                log_type="DEATH",
                target_name="npc_dota_hero_hero_0",
                target_is_hero=True,
            )
        ],
    )
    conversion = build_rosh_conversions(outside)[0]
    assert conversion.aegis_fate == "expired"
    assert conversion.aegis_fate_inferred is False
    assert conversion.aegis_fate_source is AegisFateSource.NOMINAL_EXPIRY


def test_conversion_team_attribution_for_stolen_denied_missing_and_unknown() -> None:
    players = _make_players()
    stolen = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=players,
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=5, event_type="stolen")],
    )
    conversion = build_rosh_conversions(stolen)[0]
    assert conversion.roshan_team == 2
    assert conversion.holder_team == 3
    assert conversion.conversion_team == 3

    denied = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=5, event_type="denied")],
    )
    conversion = build_rosh_conversions(denied)[0]
    assert conversion.holder_team is None
    assert conversion.conversion_team == 2
    assert conversion.aegis_eval_end_tick == 1000 + 3 * 60 * 30
    assert conversion.analysis_status == "partial"

    missing = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
    )
    assert build_rosh_conversions(missing)[0].conversion_team == 2

    unknown = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_roshan", kill_number=1)],
    )
    conversion = build_rosh_conversions(unknown)[0]
    assert conversion.roshan_team is None
    assert conversion.conversion_team is None
    assert conversion.analysis_status == "unavailable"
    assert conversion.differential_profile.fight_differential is None


def test_game_closing_uses_hardened_window_and_multiple_tags_are_nonexclusive() -> None:
    players = _make_players()
    common = {
        "game_start_tick": 0,
        "radiant_win": True,
        "players": players,
        "roshans": [RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        "aegis_events": [AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        "teamfights": [
            _make_fight(1200, 1400, "radiant"),
            _make_fight(1600, 1800, "radiant"),
        ],
        "towers": [
            TowerKill(
                2000,
                3,
                "",
                "npc_dota_badguys_tower3_mid",
                killer_team=2,
            )
        ],
        "wards": [
            WardEvent(2100, 0, "", "observer", 2, 24000.0, 21000.0, None, None, ""),
            WardEvent(2200, 1, "", "observer", 2, 24000.0, 21000.0, None, None, ""),
        ],
        "tormentors": [TormentorKill(2300, "", 0, 1)],
        "game_times_min": [0, 60, 120, 180, 240],
        "radiant_gold_adv": [0, 0, 500, 3000, 5000],
        "radiant_xp_adv": [0, 0, 400, 2000, 3000],
    }
    closing = build_rosh_conversions(ParsedMatch(game_end_tick=7000, **common))[0]
    assert {
        "fight_advantage",
        "objective_gain",
        "resource_gain",
        "vision_expansion",
        "tormentor_secured",
        "game_closing",
    } <= set(closing.conversion_tags)

    late = build_rosh_conversions(ParsedMatch(game_end_tick=20000, **common))[0]
    assert "game_closing" not in late.conversion_tags


def test_counter_conversion_requires_dominant_opponent_evidence() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=_make_players(),
        roshans=[RoshanKill(tick=1000, killer="npc_dota_hero_hero_0", kill_number=1)],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        teamfights=[
            _make_fight(1200, 1400, "dire"),
            _make_fight(1600, 1800, "dire"),
        ],
        towers=[
            TowerKill(
                2000,
                2,
                "",
                "npc_dota_goodguys_tower3_mid",
                killer_team=3,
            )
        ],
        game_times_min=[0, 60, 120, 180, 240, 300, 360, 420],
        radiant_gold_adv=[0, 2000, 1500, 500, -1000, -2500, -4000, -5000],
        radiant_xp_adv=[0, 1000, 500, 0, -500, -1500, -2500, -3000],
    )
    conversion = build_rosh_conversions(match)[0]
    assert conversion.differential_profile.fight_differential == -2
    assert conversion.differential_profile.structure_delta == -3
    assert "counter_conversion" in conversion.conversion_tags


def test_protocol_team_is_preferred_and_unknown_objectives_are_not_credited() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[
            RoshanKill(
                tick=1000,
                killer="npc_dota_neutral_centaur_khan",
                kill_number=1,
                killer_team=2,
            )
        ],
        towers=[
            TowerKill(1500, 3, "", "npc_dota_badguys_tower2_mid"),
            TowerKill(
                1550,
                2,
                "",
                "npc_dota_goodguys_tower2_mid",
                killer_team=2,
            ),
        ],
        barracks=[BarracksKill(1600, 3, "", "npc_dota_badguys_melee_rax_mid")],
        tormentors=[TormentorKill(1700, "", -1, 1)],
    )

    conversion = build_rosh_conversions(match)[0]
    profile = conversion.differential_profile
    assert conversion.roshan_team == 2
    assert conversion.roshan_team_source is RoshTeamAttributionSource.PROTOCOL
    assert conversion.conversion_team_source is RoshTeamAttributionSource.PROTOCOL
    assert profile.conversion_towers == 0
    assert profile.opponent_towers == 0
    assert profile.unattributed_towers == 1
    assert profile.unattributed_barracks == 1
    assert profile.unattributed_tormentors == 1
    assert "structure_attribution_unavailable" in profile.status_reasons
    assert "tormentor_attribution_unavailable" in profile.status_reasons
    kinds = {event.kind for event in conversion.timeline_events}
    assert {"tower_unknown", "barracks_unknown", "tormentor_unknown"} <= kinds


def test_creep_and_summon_structure_kills_use_explicit_name_evidence() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2)],
        towers=[
            TowerKill(
                1500,
                3,
                "npc_dota_creep_goodguys_melee",
                "npc_dota_badguys_tower1_mid",
            ),
            TowerKill(
                1600,
                3,
                "npc_dota_beastmaster_boar_4",
                "npc_dota_badguys_tower1_top",
                killer_source="npc_dota_hero_hero_0",
            ),
            TowerKill(
                1700,
                2,
                "npc_dota_creep_goodguys_ranged",
                "npc_dota_goodguys_tower3_mid",
            ),
        ],
    )

    conversion = build_rosh_conversions(match)[0]
    profile = conversion.differential_profile
    assert profile.conversion_towers == 2
    assert profile.opponent_towers == 0
    assert profile.unattributed_towers == 0
    assert conversion.towers_taken == 2


def test_tag_thresholds_are_configurable_at_the_boundary() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[
            RoshanKill(
                tick=1000,
                killer="npc_dota_hero_hero_0",
                kill_number=1,
                killer_team=2,
            )
        ],
        aegis_events=[AegisEvent(tick=1010, player_id=0, event_type="pickup")],
        teamfights=[_make_fight(1200, 1400, "radiant")],
        towers=[
            TowerKill(
                1500,
                3,
                "",
                "npc_dota_badguys_tower1_mid",
                killer_team=2,
            )
        ],
    )

    default = build_rosh_conversions(match)[0]
    calibrated = build_rosh_conversions(
        match,
        tag_thresholds=RoshTagThresholds(
            fight_advantage=1,
            objective_gain=1,
            ruleset="boundary-test",
        ),
    )[0]

    assert "fight_advantage" not in default.conversion_tags
    assert "objective_gain" not in default.conversion_tags
    assert {"fight_advantage", "objective_gain"} <= set(calibrated.conversion_tags)
    assert calibrated.differential_profile.tag_ruleset == "boundary-test"


def test_tag_thresholds_reject_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        RoshTagThresholds(fight_advantage=-1)
    with pytest.raises(ValueError, match="must not be empty"):
        RoshTagThresholds(ruleset="")


def test_fight_spanning_next_roshan_is_never_double_counted() -> None:
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=10000,
        players=_make_players(),
        roshans=[
            RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2),
            RoshanKill(1500, "npc_dota_hero_hero_1", 2, killer_team=2),
        ],
        aegis_events=[
            AegisEvent(1010, 0, "pickup"),
            AegisEvent(1510, 1, "pickup"),
        ],
        teamfights=[_make_fight(1400, 1600, "radiant")],
    )

    conversions = build_rosh_conversions(match)

    assert sum(conversion.fight_count for conversion in conversions) == 1
    assert sum(len(conversion.fight_evidence) for conversion in conversions) == 1


def test_aegis_association_window_is_inclusive_at_thirty_seconds() -> None:
    exact = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=_make_players(),
        roshans=[RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2)],
        aegis_events=[AegisEvent(1900, 0, "pickup")],
    )
    late = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=_make_players(),
        roshans=[RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2)],
        aegis_events=[AegisEvent(1901, 0, "pickup")],
    )

    exact_conversion = build_rosh_conversions(exact)[0]
    late_conversion = build_rosh_conversions(late)[0]

    assert exact_conversion.aegis_pickup_tick == 1900
    assert exact_conversion.aegis_fate_source is AegisFateSource.NOMINAL_EXPIRY
    assert late_conversion.aegis_pickup_tick is None
    assert late_conversion.aegis_fate == "unknown"
    assert late_conversion.aegis_fate_source is AegisFateSource.MISSING_EVENT


def test_aegis_lifecycle_boundary_sources_are_explicit() -> None:
    game_end = ParsedMatch(
        game_start_tick=0,
        game_end_tick=5000,
        players=_make_players(),
        roshans=[RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2)],
        aegis_events=[AegisEvent(1010, 0, "pickup")],
    )
    next_roshan = ParsedMatch(
        game_start_tick=0,
        game_end_tick=20000,
        players=_make_players(),
        roshans=[
            RoshanKill(1000, "npc_dota_hero_hero_0", 1, killer_team=2),
            RoshanKill(5000, "npc_dota_hero_hero_1", 2, killer_team=2),
        ],
        aegis_events=[AegisEvent(1010, 0, "pickup")],
    )

    ended = build_rosh_conversions(game_end)[0]
    bounded = build_rosh_conversions(next_roshan)[0]

    assert ended.aegis_fate == "game_end"
    assert ended.aegis_fate_source is AegisFateSource.GAME_END_BOUNDARY
    assert bounded.aegis_fate == "unknown"
    assert bounded.aegis_fate_source is AegisFateSource.NEXT_ROSHAN_BOUNDARY

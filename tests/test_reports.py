from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from gem.analysis import FarmingBoundaryReason, FarmingRoutePoint
from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.teamfights import Teamfight, TeamfightPlayer
from gem.reports import (
    ReportOptions,
    apply_opendota_player_names,
    build_html_report,
    is_displayable_player_name,
    write_html_report,
)
from gem.reports.sections.combat import _fight_reveals_html, build_kill_feed, build_teamfights
from gem.reports.sections.vision import (
    _downsample_farming_route_points,
    _insight_delta,
    build_farming,
)
from gem.results.models import (
    HeroVisibilityEvent,
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisibilityState,
    VisionModifierEvent,
    VisionModifierLifecycleStatus,
    VisionModifierPairingStatus,
    VisionModifierSemantic,
)


def _minimal_match() -> ParsedMatch:
    return ParsedMatch(
        match_id=123456789,
        game_mode=22,
        radiant_win=True,
        game_start_tick=0,
        game_end_tick=1800,
        players=[
            ParsedPlayer(player_id=0, hero_name="npc_dota_hero_axe", team=2, kills=1),
            ParsedPlayer(player_id=5, hero_name="npc_dota_hero_bane", team=3, deaths=1),
        ],
    )


def _positioning_match(*, missing_position: bool = False) -> ParsedMatch:
    players = [
        ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_axe",
            player_name="Radiant One",
            team=2,
            position_log=[(700, 10_000.0, 10_000.0), (1_000, 11_000.0, 11_000.0)],
        ),
        ParsedPlayer(
            player_id=5,
            hero_name="npc_dota_hero_bane",
            player_name="Dire One",
            team=3,
            position_log=(
                [] if missing_position else [(700, 10_400.0, 10_000.0), (1_000, 11_400.0, 11_000.0)]
            ),
        ),
        ParsedPlayer(
            player_id=1,
            hero_name="npc_dota_hero_crystal_maiden",
            player_name="Nearby Support",
            team=2,
            position_log=[(700, 10_100.0, 10_100.0), (1_000, 11_100.0, 11_100.0)],
        ),
    ]
    fight_players = [TeamfightPlayer(player_id=i) for i in range(10)]
    fight_players[0].damage_dealt = 100
    fight_players[5].damage_taken = 100
    fight = Teamfight(
        start_tick=550,
        end_tick=1_450,
        first_death_tick=1_000,
        last_death_tick=1_000,
        deaths=1,
        players=fight_players,
    )
    return ParsedMatch(
        game_end_tick=1_500,
        players=players,
        teamfights=[fight],
        hero_visibility_events=[
            HeroVisibilityEvent(
                tick=700,
                player_id=0,
                hero_name="npc_dota_hero_axe",
                entity_index=1,
                entity_serial=1,
                radiant_state=VisibilityState.UNKNOWN,
                dire_state=VisibilityState.VISIBLE,
            ),
            HeroVisibilityEvent(
                tick=700,
                player_id=5,
                hero_name="npc_dota_hero_bane",
                entity_index=2,
                entity_serial=1,
                radiant_state=VisibilityState.HIDDEN,
                dire_state=VisibilityState.UNKNOWN,
            ),
        ],
    )


def _linked_smoke_match(*, multiple_fights: bool = False) -> ParsedMatch:
    match = _positioning_match()
    match.smoke_events = [
        SmokeEvent(
            tick=900,
            activator="npc_dota_hero_axe",
            team=2,
            activation_game_time_s=30,
            participants=[
                SmokeParticipant(
                    hero_name="npc_dota_hero_axe",
                    player_id=0,
                    applied_tick=901,
                    removed_tick=1_100,
                    modifier_duration_s=45.0,
                    modifier_elapsed_duration_s=7.0,
                    applied_game_time_s=30,
                    removed_game_time_s=37,
                )
            ],
        )
    ]
    if multiple_fights:
        fight_players = [TeamfightPlayer(player_id=i) for i in range(10)]
        fight_players[0].damage_dealt = 50
        fight_players[5].damage_taken = 50
        match.teamfights.append(
            Teamfight(
                start_tick=1_300,
                end_tick=1_600,
                first_death_tick=1_400,
                last_death_tick=1_400,
                deaths=1,
                players=fight_players,
            )
        )
        match.game_end_tick = 1_700
        match.players[0].position_log.append((1_400, 12_000.0, 12_000.0))
        match.players[1].position_log.append((1_400, 12_100.0, 12_100.0))
        match.players[2].position_log.append((1_400, 12_400.0, 12_000.0))
    return match


def test_build_html_report_smoke_without_assets() -> None:
    html = build_html_report(
        _minimal_match(),
        options=ReportOptions(title="Smoke Report", include_movement=False),
    )

    assert "<!DOCTYPE html>" in html
    assert "<title>Smoke Report</title>" in html
    assert "Match ID" in html
    assert "123456789" in html


def test_farming_report_leads_with_evidence_and_preserves_missing_context() -> None:
    hero_name = "npc_dota_hero_axe"
    match = ParsedMatch(
        game_start_tick=0,
        game_end_tick=600,
        players=[
            ParsedPlayer(
                player_id=0,
                hero_name=hero_name,
                team=2,
                position_log=[
                    (0, 8_647.0, 15_564.0),
                    (150, 8_650.0, 15_560.0),
                    (500, 8_647.0, 15_564.0),
                ],
            )
        ],
        combat_log=[
            CombatLogEntry(
                tick=90,
                log_type=CombatLogType.DEATH,
                attacker_name=hero_name,
                target_name="npc_dota_neutral_centaur_khan",
                location_x=8_647.0,
                location_y=15_564.0,
            )
        ],
    )

    html = build_farming(match, None)

    assert "Strong Farm Evidence" in html
    assert "Incomplete Context" in html
    assert "XP unavailable" in html
    assert "Why these tags?" in html
    assert "team_3_roster_unavailable" in html
    assert "1 neutral kill(s)" in html
    assert "units travelled" in html
    assert "Context Tags" in html
    assert "Legacy Context</th>" not in html
    assert '"break_before": true' in html
    assert "S:0.50 P:0.50 V:0.50" not in html
    assert html.index("Strong Farm Evidence") < html.index("Legacy context heuristic reference")


@pytest.mark.parametrize(
    "boundary",
    [FarmingBoundaryReason.SAMPLE_GAP, FarmingBoundaryReason.LARGE_JUMP],
)
def test_farming_route_downsampling_preserves_discontinuities(
    boundary: FarmingBoundaryReason,
) -> None:
    points = [
        FarmingRoutePoint(
            tick=index * 30,
            x=float(index),
            y=0.0,
            camp_id=None,
            camp_type=None,
            inside_base_zone=False,
            boundary_before=(boundary if index == 701 else None),
        )
        for index in range(1405)
    ]

    sampled = _downsample_farming_route_points(points)

    assert points[700] in sampled
    assert points[701] in sampled
    assert sampled[-1] is points[-1]


def test_teamfight_report_renders_four_evidence_snapshots_on_one_map() -> None:
    html = build_teamfights(_positioning_match(), "ZmFrZQ==")

    assert html.count('class="tf-snapshot-btn') == 4
    assert html.count('class="tf-position-layer"') == 4
    assert html.count('class="gem-map-bg"') == 1
    assert "Pre-engagement" in html
    assert "Engagement start" in html
    assert "First death" in html
    assert "Fight end" in html
    assert "visible to opponents" in html
    assert "hidden to opponents" in html
    assert "dimmed = nonparticipant" in html
    assert "conservative fallback" in html
    assert "bad positioning" not in html.lower()
    assert "outplayed" not in html.lower()


def test_teamfight_report_surfaces_partial_position_evidence() -> None:
    html = build_teamfights(_positioning_match(missing_position=True), None)

    assert "fresh positions" in html
    assert "missing" in html
    assert "position sample unavailable" not in html  # absent heroes do not get map markers


def test_teamfight_report_uses_first_player_for_duplicate_slots() -> None:
    match = _positioning_match()
    match.players.append(
        ParsedPlayer(
            player_id=0,
            hero_name="npc_dota_hero_drow_ranger",
            player_name="Duplicate",
            team=2,
            position_log=[(700, 5_000.0, 5_000.0), (1_000, 5_100.0, 5_100.0)],
        )
    )

    html = build_teamfights(match, None)

    assert "Radiant One" in html
    assert "Axe" in html
    assert "Duplicate" not in html
    assert "Drow Ranger" not in html


def test_teamfight_report_discloses_missing_first_death_tick_fallback() -> None:
    match = _positioning_match()
    match.teamfights[0].first_death_tick = 0

    html = build_teamfights(match, None)

    assert "Death fallback" in html
    assert "use the observed last-death tick" in html
    assert ">00:00<" not in html


def test_full_report_wires_teamfight_snapshot_controls() -> None:
    html = build_html_report(
        _positioning_match(),
        options=ReportOptions(include_movement=False),
    )

    assert "document.querySelectorAll('.tf-snapshot-btn')" in html
    assert "tf-position-layer, .tf-position-note" in html


def test_smoke_insight_delta_formats_preexisting_events_as_negative() -> None:
    assert _insight_delta(SimpleNamespace(game_time_delta_s=-3, tick_delta=-90)) == "-3s"
    assert "-3.0s*" in _insight_delta(SimpleNamespace(game_time_delta_s=None, tick_delta=-90))


def test_full_report_cross_links_smoke_and_unique_fight_evidence() -> None:
    html = build_html_report(
        _linked_smoke_match(),
        options=ReportOptions(include_movement=False),
    )

    assert 'id="smoke-operation-1"' in html
    assert 'id="fight-1"' in html
    assert 'data-report-target="fight-1"' in html
    assert 'data-report-snapshot="engagement_start"' in html
    assert 'data-report-target="smoke-operation-1"' in html
    assert "Linked" in html
    assert "Visible 1 · Hidden 0 · Unknown 0" in html
    assert "document.querySelectorAll('[data-report-target]')" in html
    smoke_sequence = html[html.index('class="smoke-fight-sequence"') :]
    assert smoke_sequence.index("First death") < smoke_sequence.index("Removal")
    assert "successful smoke" not in html.lower()
    assert "ward broke the smoke" not in html.lower()


def test_smoke_report_keeps_multiple_fight_links_distinct() -> None:
    html = build_html_report(
        _linked_smoke_match(multiple_fights=True),
        options=ReportOptions(include_movement=False),
    )

    assert html.count("View Fight #") == 2
    assert 'data-report-target="fight-1"' in html
    assert 'data-report-target="fight-2"' in html
    assert html.count('data-report-target="smoke-operation-1"') == 2


def test_player_name_display_gate_rejects_binary_looking_text() -> None:
    assert is_displayable_player_name("叽叽喳喳")
    assert is_displayable_player_name("宇宙にきらめく エメラルド")
    assert not is_displayable_player_name("0�ɛ�\x01")
    assert not is_displayable_player_name("�\x17�#�\x01")


def test_build_html_report_omits_malformed_replay_player_names() -> None:
    match = _minimal_match()
    match.players[0].player_name = "0�ɛ�\x01"

    html = build_html_report(match, options=ReportOptions(include_movement=False))

    assert "\ufffd" not in html
    assert "\x01" not in html


def test_opendota_player_names_make_reports_display_clean_cjk_names() -> None:
    match = _minimal_match()
    match.players[0].player_name = "0�ɛ�\x01"
    match.players[1].player_name = "�\x17�#�\x01"

    apply_opendota_player_names(
        match,
        {
            "players": [
                {"player_slot": 0, "personaname": "烟弹漏油"},
                {"player_slot": 128, "personaname": "李火旺"},
            ],
        },
    )
    html = build_html_report(match, options=ReportOptions(include_movement=False))

    assert match.players[0].player_name == "烟弹漏油"
    assert match.players[1].player_name == "李火旺"
    assert "烟弹漏油" in html
    assert "李火旺" in html
    assert "\ufffd" not in html


def test_write_html_report_returns_written_path(tmp_path: Path) -> None:
    output = tmp_path / "report.html"

    written = write_html_report(
        _minimal_match(),
        output,
        options=ReportOptions(include_movement=False),
    )

    assert written == output
    assert output.exists()
    assert "Dota 2 Match Report" in output.read_text(encoding="utf-8")


def test_report_without_icons_falls_back_to_hero_names() -> None:
    """Without an icon cache the report must stay readable via hero names.

    The scoreboard renders each hero's display name as text, and no grey 1×1
    placeholder data URI leaks into the output in place of a missing portrait.
    """
    from gem.reports.assets import HERO_PLACEHOLDER_B64, ReportAssets, configure_assets

    configure_assets(ReportAssets())  # explicitly no icon cache
    html = build_html_report(
        _minimal_match(),
        options=ReportOptions(include_movement=False),
        assets=ReportAssets(),
    )

    assert "Axe" in html
    assert "Bane" in html
    # The grey placeholder square must not stand in for a missing portrait.
    assert HERO_PLACEHOLDER_B64 not in html


def test_item_icon_tag_is_icon_only_when_uncached() -> None:
    """``item_icon_tag`` is an icon prefix only.

    Every call site appends its own item label, so an uncached item must
    return an empty string (degrading to the adjacent text) rather than a
    name chip — otherwise the name would render twice (e.g. "BlinkBlink").
    """
    from gem.reports.assets import ITEM_ICON_B64, item_icon_tag

    ITEM_ICON_B64.clear()
    assert item_icon_tag("item_blink") == ""
    assert item_icon_tag("") == ""

    ITEM_ICON_B64["blink"] = "data:image/png;base64,AAAA"
    assert "<img" in item_icon_tag("item_blink")
    ITEM_ICON_B64.clear()


def test_purchase_rows_show_item_name_once_without_icons() -> None:
    """A purchase entry with no icon cache must not duplicate the item name."""
    from gem.combat.log import CombatLogEntry
    from gem.reports.assets import ReportAssets, configure_assets

    match = _minimal_match()
    match.players[0].purchase_log = [
        CombatLogEntry(
            tick=600,
            log_type=CombatLogType.PURCHASE,
            value_name="item_blink",
        ),
    ]

    configure_assets(ReportAssets())
    html = build_html_report(
        match,
        options=ReportOptions(include_movement=False),
        assets=ReportAssets(),
    )

    # The item label appears, but never doubled up (no "Blink DaggerBlink Dagger").
    assert "Blink DaggerBlink Dagger" not in html
    assert "Blink Dagger" in html


def test_has_hero_icon_tracks_loaded_cache() -> None:
    from gem.reports.assets import HERO_ICON_B64, has_hero_icon

    HERO_ICON_B64.clear()
    assert not has_hero_icon("npc_dota_hero_axe")

    HERO_ICON_B64["axe"] = "data:image/png;base64,AAAA"
    assert has_hero_icon("npc_dota_hero_axe")
    assert has_hero_icon("axe")
    HERO_ICON_B64.clear()


def test_fight_reveal_badges_use_only_bounded_direct_hero_reveals() -> None:
    direct = VisionModifierEvent(
        100,
        250,
        "modifier_slardar_amplify_damage",
        "npc_dota_hero_bane",
        "npc_dota_hero_slardar",
        2,
        add_modifier_duration_s=10.0,
    )
    gem_carrier = VisionModifierEvent(
        100,
        None,
        "modifier_item_gem_of_true_sight",
        "npc_dota_hero_axe",
        "npc_dota_hero_axe",
        2,
        semantic=VisionModifierSemantic.AURA_CARRIER,
        add_modifier_duration_s=10.0,
    )
    ambiguous = VisionModifierEvent(
        100,
        None,
        "modifier_bounty_hunter_track",
        "npc_dota_hero_bane",
        "npc_dota_hero_bounty_hunter",
        2,
        lifecycle_status=VisionModifierLifecycleStatus.INCOMPLETE,
        pairing_status=VisionModifierPairingStatus.AMBIGUOUS,
        add_modifier_duration_s=10.0,
    )
    illusion = VisionModifierEvent(
        100,
        250,
        "modifier_item_dustofappearance",
        "npc_dota_hero_bane",
        "npc_dota_hero_slardar",
        2,
        target_is_illusion=True,
    )
    match = _minimal_match()
    match.vision_modifiers = [direct, gem_carrier, ambiguous, illusion]

    html = _fight_reveals_html(150, 200, match)

    assert "Corrosive Haze" in html
    assert "Gem of True Sight" not in html
    assert "Track" not in html
    assert "Dust of Appearance" not in html


def test_fight_reveal_badges_skip_duration_only_boundaries() -> None:
    inferred = VisionModifierEvent(
        100,
        None,
        "modifier_slardar_amplify_damage",
        "npc_dota_hero_bane",
        "npc_dota_hero_slardar",
        2,
        lifecycle_status=VisionModifierLifecycleStatus.EXPIRED,
        add_modifier_duration_s=10.0,
    )
    match = _minimal_match()
    match.vision_modifiers = [inferred]

    assert _fight_reveals_html(150, 200, match) == ""


def test_kill_feed_uses_authoritative_visible_hidden_unknown_labels() -> None:
    match = _minimal_match()
    match.combat_log = [
        CombatLogEntry(
            tick=tick,
            log_type=CombatLogType.DEATH,
            attacker_name="npc_dota_hero_axe",
            target_name="npc_dota_hero_bane",
            attacker_is_hero=True,
            target_is_hero=True,
        )
        for tick in (10, 20, 30)
    ]
    match.hero_visibility_events = [
        HeroVisibilityEvent(
            tick=10,
            player_id=5,
            hero_name="npc_dota_hero_bane",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.VISIBLE,
            dire_state=VisibilityState.UNKNOWN,
        ),
        HeroVisibilityEvent(
            tick=20,
            player_id=5,
            hero_name="npc_dota_hero_bane",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.HIDDEN,
            dire_state=VisibilityState.UNKNOWN,
        ),
        HeroVisibilityEvent(
            tick=30,
            player_id=5,
            hero_name="npc_dota_hero_bane",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.UNKNOWN,
            dire_state=VisibilityState.UNKNOWN,
        ),
    ]

    html = build_kill_feed(match)

    assert "visible" in html
    assert "hidden" in html
    assert "unknown" in html
    assert "blind" not in html.lower()


def test_kill_feed_prefers_event_visibility_over_same_tick_hero_state() -> None:
    match = _minimal_match()
    match.combat_log = [
        CombatLogEntry(
            tick=10,
            log_type=CombatLogType.DEATH,
            attacker_name="npc_dota_hero_axe",
            target_name="npc_dota_hero_bane",
            attacker_is_hero=True,
            target_is_hero=True,
            visible_radiant=False,
        )
    ]
    match.hero_visibility_events = [
        HeroVisibilityEvent(
            tick=10,
            player_id=5,
            hero_name="npc_dota_hero_bane",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.VISIBLE,
            dire_state=VisibilityState.UNKNOWN,
        )
    ]

    html = build_kill_feed(match)

    assert "◌ hidden" in html
    assert "👁 visible" not in html


def test_kill_feed_does_not_apply_canonical_visibility_to_illusion_death() -> None:
    match = _minimal_match()
    match.combat_log = [
        CombatLogEntry(
            tick=10,
            log_type=CombatLogType.DEATH,
            attacker_name="npc_dota_hero_axe",
            target_name="npc_dota_hero_bane",
            attacker_is_hero=True,
            target_is_hero=True,
            target_is_illusion=True,
        )
    ]
    match.hero_visibility_events = [
        HeroVisibilityEvent(
            tick=10,
            player_id=5,
            hero_name="npc_dota_hero_bane",
            entity_index=7,
            entity_serial=1,
            radiant_state=VisibilityState.VISIBLE,
            dire_state=VisibilityState.UNKNOWN,
        )
    ]

    html = build_kill_feed(match)

    assert "Bane" in html
    assert "👁 visible" not in html

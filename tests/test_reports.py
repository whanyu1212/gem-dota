from __future__ import annotations

from gem.reports import (
    ReportOptions,
    apply_opendota_player_names,
    build_html_report,
    is_displayable_player_name,
    write_html_report,
)
from gem.reports.sections.combat import _fight_reveals_html
from gem.results.models import (
    ParsedMatch,
    ParsedPlayer,
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


def test_build_html_report_smoke_without_assets() -> None:
    html = build_html_report(
        _minimal_match(),
        options=ReportOptions(title="Smoke Report", include_movement=False),
    )

    assert "<!DOCTYPE html>" in html
    assert "<title>Smoke Report</title>" in html
    assert "Match ID" in html
    assert "123456789" in html


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


def test_write_html_report_returns_written_path(tmp_path) -> None:
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
        CombatLogEntry(tick=600, log_type="PURCHASE", value_name="item_blink"),
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

"""The cookbook recipes in examples/cookbook answer their questions from gem's facts (HY-102)."""

from __future__ import annotations

import importlib.util
import warnings
from pathlib import Path
from types import ModuleType

import pandas as pd
import pytest

from gem.combat.log import CombatLogEntry, CombatLogType
from gem.extractors.fights import Fight, FightPlayer
from gem.extractors.objectives import AegisEvent, BarracksKill, RoshanKill, TormentorKill, TowerKill
from gem.extractors.wards import WardEvent
from gem.results.models import (
    GoldLedger,
    GoldLedgerSnapshot,
    HeroVisibilityEvent,
    ParsedMatch,
    ParsedPlayer,
    SmokeEvent,
    SmokeParticipant,
    VisibilityState,
)
from gem.state.game_clock import GameClock, GamePause
from tests._lanes import MID as MID_CELL, TOP as TOP_CELL, lanes_match as _lanes_match
from tests._runes import AXE, LINA, PUDGE, SF, runes_match as _runes_match

COOKBOOK = Path(__file__).resolve().parent.parent / "examples" / "cookbook"


def _recipe(name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, COOKBOOK / f"{name}.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


roshan_next_fight = _recipe("roshan_next_fight")
core_farm_10_to_20 = _recipe("core_farm_10_to_20")
smoke_to_kill = _recipe("smoke_to_kill")
wards = _recipe("wards")
fights = _recipe("fights")
objectives = _recipe("objectives")
lead = _recipe("lead")
lanes = _recipe("lanes")
runes = _recipe("runes")


def _fight(first_death_tick: int, winner: str) -> Fight:
    return Fight(
        start_tick=first_death_tick - 300,
        end_tick=first_death_tick + 300,
        last_death_tick=first_death_tick,
        deaths=1,
        first_death_tick=first_death_tick,
        winner=winner,
        players=[FightPlayer(player_id=i) for i in range(10)],
    )


def _hero_death(
    game_time_s: int, killer_team: int, victim_team: int, **flags: bool
) -> CombatLogEntry:
    return CombatLogEntry(
        tick=game_time_s * 30,
        log_type=CombatLogType.DEATH,
        attacker_name="npc_dota_hero_axe",
        target_name="npc_dota_hero_lina",
        target_is_hero=True,
        attacker_team=killer_team,
        target_team=victim_team,
        game_time_s=game_time_s,
        **flags,
    )


def test_roshan_next_fight_pairs_each_kill_with_its_aegis_and_next_fight() -> None:
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(
            game_start_tick=0, pauses=[GamePause(start_tick=3_100, end_tick=6_100)]
        ),
        players=[ParsedPlayer(player_id=6, team=3, hero_name="npc_dota_hero_huskar")],
        roshans=[
            RoshanKill(tick=3_000, killer="npc_dota_hero_huskar", kill_number=1, killer_team=3),
            RoshanKill(tick=30_000, killer="npc_dota_hero_huskar", kill_number=2, killer_team=3),
        ],
        aegis_events=[
            AegisEvent(tick=3_010, player_id=6, event_type="denied"),
            AegisEvent(tick=30_020, player_id=6, event_type="pickup"),
        ],
        # 100 s of a 3,000-tick pause sit between the first kill and this fight.
        fights=[_fight(7_000, "dire"), _fight(50_000, "radiant")],
    )

    table = roshan_next_fight.roshan_next_fight(match)

    first, second = table.to_dict("records")
    assert (first["aegis"], first["aegis_by"]) == ("denied", "huskar")
    assert first["next_fight"] == 1
    # 4,000 ticks apart, of which 3,000 are paused: 33 s of game time.
    assert first["seconds_to_fight"] == 33
    assert first["killer_team_won"] is True
    # The second kill's only later fight is 667 s away, past the Aegis's 5 minutes.
    assert pd.isna(second["next_fight"])
    assert second["killer_team_won"] is None


def test_smoke_to_kill_counts_real_hero_kills_in_the_window() -> None:
    participant = SmokeParticipant(
        hero_name="npc_dota_hero_axe", player_id=0, applied_tick=600, removed_tick=900
    )
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        smoke_events=[
            SmokeEvent(tick=600, activator="npc_dota_hero_axe", team=2, participants=[participant])
        ],
        combat_log=[
            _hero_death(
                25, killer_team=2, victim_team=3, will_reincarnate=True
            ),  # Aegis: not a kill
            _hero_death(28, killer_team=2, victim_team=3, target_is_illusion=True),  # illusion
            _hero_death(40, killer_team=2, victim_team=3),
            _hero_death(45, killer_team=3, victim_team=2),
            _hero_death(200, killer_team=2, victim_team=3),  # outside the window
        ],
    )

    row = smoke_to_kill.smoke_to_kill(match).iloc[0]

    assert row["team"] == "radiant"
    assert row["first_kill_after_s"] == 20
    assert row["first_loss_after_s"] == 25


def test_core_farm_reports_the_window_for_each_core() -> None:
    minutes = list(range(25))

    def laner(player_id: int, team: int, lane_role: int, lh_at_10: int) -> ParsedPlayer:
        return ParsedPlayer(
            player_id=player_id,
            team=team,
            hero_name=f"npc_dota_hero_{player_id}",
            lane_role=lane_role,
            lane_last_hits=lh_at_10,
            total_earned_gold_t_min=[600 * m for m in minutes],
            lh_t_min=[10 * m for m in minutes],
            # Inside the Radiant half for the whole window.
            position_log=[(tick, 10_000.0, 10_000.0) for tick in range(18_000, 36_000, 30)],
        )

    carry, support = laner(0, 2, 1, 60), laner(1, 2, 1, 5)
    neutral = CombatLogEntry(
        tick=20_000,
        log_type=CombatLogType.DEATH,
        attacker_name=carry.hero_name,
        target_name="npc_dota_neutral_kobold",
        game_time_s=700,
    )
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[carry, support],
        combat_log=[neutral],
    )

    row = core_farm_10_to_20.core_farm(match).iloc[0]

    assert (row["hero"], row["role"]) == ("0", "carry")  # the support laner is not a core
    assert row["gold_per_min"] == 600
    assert row["last_hits"] == 100
    assert row["neutral_kills"] == 1
    assert row["own_half"] == 1.0


@pytest.mark.integration
@pytest.mark.slow
def test_recipes_run_on_a_replay_without_deprecation_warnings(canonical_parsed_match) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        rosh = roshan_next_fight.roshan_next_fight(canonical_parsed_match)
        farm = core_farm_10_to_20.core_farm(canonical_parsed_match)
        smokes = smoke_to_kill.smoke_to_kill(canonical_parsed_match)
        ward_rows = wards.ward_table(canonical_parsed_match)
        samples = wards.circle_samples(canonical_parsed_match, ward_rows)
        fight_rows = fights.fight_table(canonical_parsed_match)
        objective_rows = objectives.objective_table(canonical_parsed_match)
        edge_rows = objectives.edges(canonical_parsed_match, objective_rows)
        gold_lead = lead.lead_by_source(lead.gold_sources(canonical_parsed_match))
        xp_lead = lead.lead_by_source(lead.xp_sources(canonical_parsed_match))
        hero_lanes = lanes.hero_lanes(canonical_parsed_match)
        lane_rows = lanes.lane_table(canonical_parsed_match, hero_lanes)
        lane_events = lanes.lane_events(canonical_parsed_match, hero_lanes)
        rune_rows = runes.rune_table(canonical_parsed_match)
        openers = runes.opening_bounties(canonical_parsed_match, rune_rows)
        windows = runes.rune_windows(canonical_parsed_match)

    assert len(rosh) == len(canonical_parsed_match.roshans)
    assert list(rosh.columns) == roshan_next_fight.COLUMNS
    # The canonical replay's minute curves end before 20:00, so no core has the window.
    assert list(farm.columns) == core_farm_10_to_20.COLUMNS
    assert set(farm["role"]) <= {"carry", "mid", "offlane"}
    assert list(smokes.columns) == smoke_to_kill.COLUMNS
    assert len(smokes) > 0
    placed = [w for w in canonical_parsed_match.wards if w.x is not None and w.team in (2, 3)]
    assert list(ward_rows.columns) == wards.WARD_COLUMNS and len(ward_rows) == len(placed)
    heroes = {p.hero_name for p in canonical_parsed_match.players}
    assert set(ward_rows["placer"]) <= heroes
    assert set(samples["state"]) <= set(wards.STATES) and (samples["distance"] <= 1600).all()
    assert list(fight_rows.columns) == fights.COLUMNS
    assert len(fight_rows) == len(canonical_parsed_match.fights)
    assert set(fight_rows["more_kills"]) <= {"radiant", "dire", "even"}
    assert list(objective_rows.columns) == objectives.OBJECTIVE_COLUMNS
    match = canonical_parsed_match
    pickups = [e for e in match.combat_log if e.log_type == "PICKUP_RUNE" and e.rune_type == 8]
    assert len(objective_rows) == len(match.towers) + len(match.barracks) + len(
        match.roshans
    ) + len(match.tormentors) + len(pickups)
    # Every wisdom rune taken is on one of the two shrines' halves, with its XP.
    wisdom = objectives.wisdom_runes(match)
    assert wisdom["taken_by"].notna().sum() == len(pickups)
    assert set(wisdom["outcome"]) <= {"own side", "other side", "not taken", "game ended"}
    assert (wisdom.dropna(subset=["taken_by"])["xp"] > 0).all()
    assert set(edge_rows["outcome"]) <= {"converted", "other side first", "nothing"}
    # The sources add up to the lead, which is the match's own curve at every minute.
    for frame, curve in ((gold_lead, match.radiant_gold_adv), (xp_lead, match.radiant_xp_adv)):
        sources = frame.drop(columns=["match_id", "tick", "time_s", "lead"])
        assert (sources.sum(axis=1) == frame["lead"]).all()
        assert frame["lead"].tolist()[: len(curve)] == curve
    assert len(gold_lead) == len(match.radiant_gold_adv) + 1  # and the end of the game
    # Every hero gets a lane; each lane and side has a row at both readings.
    assert set(hero_lanes["lane"]) <= {"top", "mid", "bot"} and len(hero_lanes) == 10
    assert list(lane_rows.columns) == lanes.LANE_COLUMNS and len(lane_rows) == 3 * 2 * 2
    assert lane_rows["net_worth"].sum() > 0
    assert list(lane_events.columns) == lanes.EVENT_COLUMNS
    assert set(lane_events["kind"]) <= {"death", "teleport", "visit"}
    # Every rune is at one of the four spots, and every pickup keeps its own time.
    assert list(rune_rows.columns) == runes.RUNE_COLUMNS and len(rune_rows) == len(match.runes)
    assert set(rune_rows["spot"]) <= {"top_river", "bot_river", "radiant_jungle", "dire_jungle"}
    picked = [r for r in match.runes if r.outcome == "picked_up"]
    used = [r for r in match.runes if r.used_tick is not None]
    assert len(runes._pickup_times(match)) == len(picked) + len(used)
    assert len(openers) == 4 and (openers["after_horn_s"] < 30).all()
    # Every power rune taken or used from a Bottle has its window.
    power = [
        r for r in picked + used if r.rune_type in runes.BUFFS or r.rune_type == runes.ILLUSION
    ]
    assert list(windows.columns) == runes.WINDOW_COLUMNS and len(windows) == len(power)
    assert (windows["end_s"] >= windows["start_s"]).all()


def test_recipes_fall_back_to_hero_teams_without_combat_log_teams() -> None:
    # Source 1 replays record no attacker/target team on the combat log or Roshan kill.
    axe = ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe")
    lina = ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_lina")
    match = ParsedMatch(
        match_id=1,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[axe, lina],
        roshans=[
            RoshanKill(
                tick=3_000,
                killer="npc_dota_roshan_minion",
                kill_number=1,
                killer_source="npc_dota_hero_axe",
            )
        ],
        fights=[_fight(4_000, "radiant")],
        smoke_events=[SmokeEvent(tick=600, activator="npc_dota_hero_axe", team=2)],
        combat_log=[
            CombatLogEntry(
                tick=1_200,
                log_type=CombatLogType.DEATH,
                attacker_name="npc_dota_axe_summon",
                damage_source_name="npc_dota_hero_axe",
                target_name="npc_dota_hero_lina",
                target_is_hero=True,
                game_time_s=40,
            )
        ],
    )

    rosh = roshan_next_fight.roshan_next_fight(match).iloc[0]
    smoke = smoke_to_kill.smoke_to_kill(match).iloc[0]

    assert (rosh["killed_by"], rosh["killer_team_won"]) == ("radiant", True)
    assert smoke["first_kill_after_s"] == 20


def _ward_match() -> ParsedMatch:
    """Lion (Radiant) wards; Axe (Dire) walks through Lion's observer circle."""
    lion = ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_lion")
    axe = ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_axe")
    axe.position_log = [
        (30, 16100.0, 16000.0),  # 100 from the observer: inside, seen
        (60, 17000.0, 16000.0),  # 1,000: inside, hidden
        (90, 20000.0, 16000.0),  # 4,000: outside
        (120, 16000.0, 16000.0),  # inside, but dead
        (150, 16000.0, 16000.0),  # inside, but smoked
    ]
    axe.times = [tick for tick, _, _ in axe.position_log]
    axe.hp_t = [700, 700, 700, 0, 700]
    visible, hidden = VisibilityState.VISIBLE, VisibilityState.HIDDEN

    def seen(tick: int, radiant: VisibilityState) -> HeroVisibilityEvent:
        return HeroVisibilityEvent(tick, 5, "npc_dota_hero_axe", 9, 1, radiant, visible)

    def ward(tick: int, kind: str, team: int, **end: object) -> WardEvent:
        return WardEvent(
            tick=tick,
            player_id=0 if team == 2 else 5,
            placer="npc_dota_hero_lionx",  # the slot decides, not this name
            ward_type=kind,  # type: ignore[arg-type]
            team=team,
            x=16000.0,
            y=16000.0,
            expires_tick=end.get("expires"),  # type: ignore[arg-type]
            killed_tick=end.get("killed"),  # type: ignore[arg-type]
            killer=str(end.get("killer", "")),
        )

    return ParsedMatch(
        match_id=7,
        game_start_tick=0,
        post_game_tick=20_000,
        game_clock=GameClock(game_start_tick=0),
        players=[lion, axe],
        wards=[
            ward(0, "observer", 2, expires=10_800),
            ward(10, "sentry", 3, killed=310, killer="npc_dota_hero_lion"),
            ward(5_000, "observer", 2),  # still up when the recording ends
        ],
        # Two events on tick 60: the later one wins.
        hero_visibility_events=[seen(0, visible), seen(60, visible), seen(60, hidden)],
        smoke_events=[
            SmokeEvent(
                tick=140,
                activator="npc_dota_hero_axe",
                team=3,
                participants=[
                    SmokeParticipant(
                        hero_name="npc_dota_hero_axe",
                        player_id=5,
                        applied_tick=140,
                        removed_tick=200,
                    )
                ],
            )
        ],
    )


def test_wards_lists_each_ward_with_how_it_ended() -> None:
    table = wards.ward_table(_ward_match())

    assert list(table["how"]) == ["expired", "killed", "up at the end"]
    assert list(table["placer"]) == [
        "npc_dota_hero_lion",
        "npc_dota_hero_axe",
        "npc_dota_hero_lion",
    ]
    assert list(table["lasted_s"].round(1)) == [360.0, 10.0, 500.0]
    assert table["killer"].tolist() == ["", "npc_dota_hero_lion", ""]
    # The side is the warding team's: the same spot is one team's half, the other's enemy half.
    radiant_side, dire_side = table["side"].iloc[0], table["side"].iloc[1]
    if table["region"].iloc[0].endswith("_half"):
        assert {radiant_side, dire_side} == {"own half", "enemy half"}
    lifetimes = wards.observer_lifetimes(table)
    assert lifetimes["placed"].sum() == 2 and lifetimes["killed"].sum() == 0


def test_wards_reads_visibility_as_hero_visibility_at_does() -> None:
    import gem

    match = _ward_match()
    lookup = wards._states(match)
    for tick in (-1, 0, 59, 60, 61):
        expected = gem.hero_visibility_at(match, player_id=5, observing_team=2, tick=tick)
        assert wards.visibility_at(lookup, 5, 2, tick) == expected.value


def test_wards_checks_the_circle_against_the_replays_visibility() -> None:
    samples = wards.circle_samples(_ward_match())

    # Inside: seen at 100, hidden at 1,000, smoked at 150; outside and dead are left out.
    assert samples[["tick", "state"]].values.tolist() == [
        [30, "visible"],
        [60, "hidden"],
        [150, "smoked"],
    ]
    assert samples["team"].unique().tolist() == ["radiant"]  # Dire placed no observer
    assert samples["distance"].round().tolist() == [100, 1000, 0]
    summary = wards.circle_summary(samples).iloc[0]
    assert (summary["seconds"], summary["visible"], summary["hidden"], summary["smoked"]) == (
        2,
        1,
        1,
        1,
    )
    bands = wards.by_distance(samples).set_index("distance")
    assert (
        bands.loc["0-400", "visible_pct"] == 100.0 and bands.loc["800-1200", "visible_pct"] == 0.0
    )


def test_fights_lists_each_fight_and_what_fell_next() -> None:
    def fight(start: int, end: int, radiant: int, dire: int) -> Fight:
        return Fight(
            start_tick=start,
            end_tick=end,
            last_death_tick=end - 30,
            deaths=radiant + dire,
            radiant_kills=radiant,
            dire_kills=dire,
            centroid_x=16000.0,
            centroid_y=16000.0,
            players=[
                FightPlayer(player_id=0, gold_delta=300),
                FightPlayer(player_id=5, gold_delta=-50),
            ],
        )

    match = ParsedMatch(
        match_id=3,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe"),
            ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_lina"),
        ],
        fights=[
            fight(9_000, 9_900, 0, 2),  # Dire more kills; nothing falls within 120 s
            fight(3_000, 3_900, 2, 1),  # Radiant more kills; Dire's tower falls 60 s later
            fight(6_000, 6_900, 1, 1),  # even
        ],
        towers=[
            TowerKill(
                tick=5_700,
                team=3,
                killer="npc_dota_hero_axe",
                tower_name="npc_dota_badguys_tower1_mid",
            )
        ],
        barracks=[
            # Radiant denies its own barracks: it still counts for Dire.
            BarracksKill(
                tick=7_000,
                team=2,
                killer="npc_dota_hero_axe",
                barracks_name="npc_dota_goodguys_melee_rax_mid",
                killer_team=2,
            )
        ],
        roshans=[
            RoshanKill(tick=20_000, killer="npc_dota_hero_lina", kill_number=1, killer_team=3)
        ],
    )

    table = fights.fight_table(match)

    assert list(table["fight"]) == [1, 2, 3] and list(table["start"]) == ["01:40", "03:20", "05:00"]
    assert list(table["more_kills"]) == ["radiant", "even", "dire"]
    first = table.iloc[0]
    assert (first["next"], first["next_for"], first["next_after_s"]) == (
        "badguys_tower1_mid",
        "radiant",
        60,
    )
    assert table.iloc[1]["next_for"] == "dire"  # the deny, 3 s after the even fight
    assert pd.isna(table.iloc[2]["next"])  # Roshan is too late
    assert (first["radiant_gold"], first["dire_gold"]) == (300, -50)
    assert fights.next_objective_summary(table) == {
        "fights": 3,
        "more_kills": 2,
        "followed": 1,
        "same_side": 1,
    }


def test_objectives_lists_each_objective_who_damaged_it_and_each_teams_edges() -> None:
    def fight(start: int, end: int, radiant: int, dire: int) -> Fight:
        return Fight(
            start_tick=start,
            end_tick=end,
            last_death_tick=end - 30,
            deaths=radiant + dire,
            radiant_kills=radiant,
            dire_kills=dire,
        )

    def hit(tick: int, source: str, attacker: str, value: int) -> CombatLogEntry:
        return CombatLogEntry(
            tick=tick,
            log_type=CombatLogType.DAMAGE,
            attacker_name=attacker,
            damage_source_name=source,
            target_name="npc_dota_badguys_tower1_mid",
            value=value,
        )

    axe = "npc_dota_hero_axe"
    match = ParsedMatch(
        match_id=4,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            ParsedPlayer(player_id=0, team=2, hero_name=axe),
            ParsedPlayer(player_id=5, team=3, hero_name="npc_dota_hero_lina"),
        ],
        fights=[
            fight(3_000, 3_900, 2, 0),  # Radiant ahead; Dire's tower falls 60 s later: converted
            fight(6_000, 6_900, 0, 1),  # Dire ahead; Radiant denies its own barracks: still Dire's
            fight(12_000, 12_900, 1, 0),  # Radiant ahead; nothing within 120 s
        ],
        towers=[
            TowerKill(
                tick=5_700,
                team=3,
                killer=axe,
                tower_name="npc_dota_badguys_tower1_mid",
                killer_team=2,
            )
        ],
        barracks=[
            BarracksKill(
                tick=7_000,
                team=2,
                killer=axe,
                barracks_name="npc_dota_goodguys_melee_rax_mid",
                killer_team=2,
            )
        ],
        roshans=[
            RoshanKill(tick=4_000, killer=axe, kill_number=1, killer_team=2)
        ],  # its Aegis: the tower at +57 s
        tormentors=[
            # No player slot from the chat event: the protocol's team decides.
            TormentorKill(
                tick=20_000,
                killer="npc_dota_hero_lina",
                killer_player_id=-1,
                kill_number=1,
                killer_team=3,
            )
        ],
        combat_log=[
            hit(5_000, axe, axe, 300),
            hit(5_500, axe, "npc_dota_necronomicon_warrior_1", 200),  # a summon: its owner's
            hit(5_600, "npc_dota_creep_goodguys_melee", "npc_dota_creep_goodguys_melee", 100),
            hit(1_000, axe, axe, 999),  # more than 90 s before it fell
        ],
    )

    table = objectives.objective_table(match)
    assert list(table["kind"]) == ["roshan", "tower", "barracks", "tormentor"]
    assert list(table["for_side"]) == ["radiant", "radiant", "dire", "dire"]
    assert list(table["after_fight"].fillna(0)) == [1, 1, 2, 0]  # 0: no fight in the 120 s before
    damage = objectives.building_damage(match).set_index("attacker")["damage"].to_dict()
    assert damage == {axe: 500, "creeps": 100}

    rows = objectives.edges(match, table)
    fights_ = rows[rows["edge"] == "fight"]
    assert list(fights_["outcome"]) == ["converted", "converted", "nothing"]
    assert list(fights_["team"]) == ["radiant", "dire", "radiant"]
    aegis = rows[rows["edge"] == "aegis"].iloc[0]
    assert (aegis["team"], aegis["outcome"], aegis["took"], aegis["after_s"]) == (
        "radiant",
        "converted",
        "badguys_tower1_mid",
        57,
    )
    summary = objectives.conversion_summary(rows).set_index(["team", "edge"])
    assert (
        summary.loc[("radiant", "fight"), "converted"] == 1
        and summary.loc[("radiant", "fight"), "nothing"] == 1
    )


def test_objectives_damage_window_is_in_game_seconds() -> None:
    # 100 s paused between the hit and the fall: 190 s of ticks, 90 s of game time.
    match = ParsedMatch(
        match_id=5,
        game_start_tick=0,
        game_clock=GameClock(
            game_start_tick=0, pauses=[GamePause(start_tick=2_000, end_tick=5_000)]
        ),
        players=[ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe")],
        towers=[
            TowerKill(
                tick=5_700,
                team=3,
                killer="npc_dota_hero_axe",
                tower_name="npc_dota_badguys_tower1_mid",
                killer_team=2,
            )
        ],
        combat_log=[
            CombatLogEntry(
                tick=1_000,
                log_type=CombatLogType.DAMAGE,
                attacker_name="npc_dota_hero_axe",
                damage_source_name="npc_dota_hero_axe",
                target_name="npc_dota_badguys_tower1_mid",
                value=250,
            )
        ],
    )
    damage = objectives.building_damage(match)
    assert damage["damage"].tolist() == [250]


def _ledger(tick: int, time_s: int, **gold: int) -> GoldLedgerSnapshot:
    return GoldLedgerSnapshot(tick=tick, game_time_s=time_s, **gold)


def _lead_match() -> ParsedMatch:
    axe, lina = "npc_dota_hero_axe", "npc_dota_hero_lina"

    def xp(tick: int, hero: str, reason: int, value: int) -> CombatLogEntry:
        return CombatLogEntry(
            tick=tick, log_type=CombatLogType.XP, target_name=hero, xp_reason=reason, value=value
        )

    def died(tick: int, unit: str) -> CombatLogEntry:
        return CombatLogEntry(tick=tick, log_type=CombatLogType.DEATH, target_name=unit)

    return ParsedMatch(
        match_id=6,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            ParsedPlayer(
                player_id=0,
                team=2,
                hero_name=axe,
                times=[0, 1_800, 1_860],
                times_min=[0, 1_800],
                total_earned_gold_t=[0, 700, 800],
                total_earned_gold_t_min=[0, 700],
                total_earned_xp_t=[0, 190, 220],
                total_earned_xp_t_min=[0, 190],
                gold_ledger=GoldLedger(
                    per_minute=[
                        _ledger(0, 0),
                        _ledger(
                            1_800, 60, hero_kill_gold=200, creep_kill_gold=300, income_gold=200
                        ),
                    ],
                    # 50 of the 800 earned has no ledger field.
                    final=_ledger(
                        1_860,
                        62,
                        hero_kill_gold=200,
                        creep_kill_gold=300,
                        income_gold=210,
                        bounty_gold=40,
                    ),
                ),
            ),
            ParsedPlayer(
                player_id=5,
                team=3,
                hero_name=lina,
                times=[0, 1_800, 1_860],
                times_min=[0, 1_800],
                total_earned_gold_t=[0, 700, 1_010],
                total_earned_gold_t_min=[0, 700],
                total_earned_xp_t=[0, 270, 280],
                total_earned_xp_t_min=[0, 270],
                gold_ledger=GoldLedger(
                    per_minute=[
                        _ledger(0, 0),
                        _ledger(1_800, 60, neutral_kill_gold=500, income_gold=200),
                    ],
                    final=_ledger(
                        1_860, 62, neutral_kill_gold=500, income_gold=210, roshan_gold=300
                    ),
                ),
            ),
        ],
        combat_log=[
            xp(100, axe, 1, 100),
            died(200, "npc_dota_creep_badguys_melee"),
            xp(200, axe, 2, 50),
            # A neutral and a lane creep died on the tick: which one gave it is unclear.
            died(300, "npc_dota_neutral_kobold"),
            died(300, "npc_dota_creep_goodguys_ranged"),
            xp(300, axe, 2, 40),
            died(400, "npc_dota_neutral_kobold"),
            xp(400, lina, 2, 60),
            xp(500, lina, 3, 200),
            xp(600, lina, 0, 10),
            # On the minute's tick: the minute's reading doesn't count it yet.
            xp(1_800, axe, 4, 30),
        ],
    )


def test_lead_splits_the_gold_lead_into_ledger_sources() -> None:
    gold = lead.lead_by_source(lead.gold_sources(_lead_match()))

    assert gold["time_s"].tolist() == [0, 60, 62]
    assert gold["lead"].tolist() == [0, 0, -210]
    moved = lead.what_moved(gold)
    assert moved.to_dict() == {
        "hero_kills": 200,
        "lane_creeps": 300,
        "neutral_creeps": -500,
        "buildings": 0,
        "roshan": -300,
        "bounty_runes": 40,
        "passive_income": 0,
        "other": 0,
        "unlisted": 50,
        "lead": -210,
    }
    # A stretch: from the minute to the end.
    assert lead.what_moved(gold, start_s=60)["roshan"] == -300
    assert lead.what_moved(gold, end_s=60)["lead"] == 0


def test_lead_splits_the_xp_lead_by_reason_and_what_died() -> None:
    xp = lead.lead_by_source(lead.xp_sources(_lead_match()))

    minute = xp[xp["time_s"] == 60].iloc[0]
    assert minute["lead"] == 190 - 270
    assert (minute["hero_kills"], minute["lane_creeps"], minute["unclear_creeps"]) == (100, 50, 40)
    assert (minute["neutral_creeps"], minute["roshan"], minute["other"]) == (-60, -200, -10)
    assert minute["wisdom_runes"] == 0 and minute["unlisted"] == 0
    end = xp.iloc[-1]
    assert (end["wisdom_runes"], end["unlisted"], end["lead"]) == (30, -10, 220 - 280)


def test_lead_changes_hands_only_across_zero() -> None:
    frame = pd.DataFrame(
        {
            "match_id": 1,
            "tick": range(5),
            "time_s": [0, 60, 120, 180, 240],
            "lead": [0, 100, -50, 0, 20],
        }
    )
    changes = lead.lead_changes(frame)
    assert changes[["time_s", "ahead"]].values.tolist() == [[120, "dire"], [240, "radiant"]]


def test_lead_is_empty_without_a_gold_ledger() -> None:
    match = ParsedMatch(
        match_id=7, players=[ParsedPlayer(player_id=0, team=2, hero_name="npc_dota_hero_axe")]
    )
    assert lead.gold_sources(match).empty and lead.xp_sources(match).empty
    assert list(lead.gold_sources(match).columns) == [
        *lead.READING_COLUMNS,
        *lead.GOLD_SOURCES,
        "unlisted",
        "total",
    ]


def test_lanes_puts_each_hero_where_it_spent_the_laning_stage() -> None:
    hero_lanes = lanes.hero_lanes(_lanes_match()).set_index("hero")

    assert hero_lanes["lane"].to_dict() == {
        "npc_dota_hero_axe": "top",
        "npc_dota_hero_lina": "mid",
        "npc_dota_hero_pudge": "top",
        "npc_dota_hero_nevermore": "mid",
    }
    # 65 of the 360 seconds in mid: walking out of base and the visit.
    assert hero_lanes.loc["npc_dota_hero_axe", "share"] == round(295 / 360, 2)
    assert hero_lanes.loc["npc_dota_hero_nevermore", "jungle"] == 21


def test_lanes_reads_each_side_of_each_lane_at_both_readings() -> None:
    table = lanes.lane_table(_lanes_match())
    top = table[(table["lane"] == "top") & (table["side"] == "radiant")].set_index("reading_s")

    assert top.loc[360, "heroes"] == "npc_dota_hero_axe"
    assert (top.loc[360, "net_worth"], top.loc[600, "net_worth"]) == (1000 + 3600, 1000 + 6000)
    assert (top.loc[360, "last_hits"], top.loc[360, "denies"]) == (36, 6)
    # Earned 600 + 4 * 360 by 6:00: 720 from lane creeps, 180 from neutrals, the rest other.
    assert (top.loc[360, "lane_creep_gold"], top.loc[360, "neutral_gold"]) == (720, 180)
    assert top.loc[360, "other_gold"] == 600 + 4 * 360 - 720 - 180
    gaps = lanes.lane_gaps(table).set_index("lane")
    assert gaps.loc["mid", "gap_360"] == (1000 + 20 * 360) - (1000 + 70 * 360)


def test_lanes_lists_deaths_teleports_and_visits_by_lane() -> None:
    events = lanes.lane_events(_lanes_match())
    rows = [
        (e.time_s, e.kind, e.lane, e.hero, e.by, e.from_lane, None if pd.isna(e.end_s) else e.end_s)
        for e in events.itertuples(index=False)
    ]

    assert rows == [
        (100, "death", "jungle", "npc_dota_hero_nevermore", "npc_dota_hero_axe", "top", None),
        (300, "visit", "mid", "npc_dota_hero_axe", None, "top", 340),
        (400, "teleport", "top", "npc_dota_hero_lina", None, "mid", None),
        (401, "visit", "top", "npc_dota_hero_lina", None, "mid", 431),
        # A summon's kill counts for its owner, from the owner's lane.
        (410, "death", "top", "npc_dota_hero_pudge", "npc_dota_hero_lina", "mid", None),
    ]


def test_lanes_rounds_cells_as_opendota_does() -> None:
    # 90.46 cells is 91 for OpenDota (one decimal, then half up): mid, not top.
    assert lanes.lane_at(90.46 * 128, 128 * 128) == "mid"


def test_lanes_finds_a_teleport_that_lands_after_a_pause() -> None:
    lina = "npc_dota_hero_lina"
    match = ParsedMatch(
        match_id=9,
        game_start_tick=0,
        # 30 s paused one second into the channel (cast at 6:40, tick 12,000).
        game_clock=GameClock(
            game_start_tick=0, pauses=[GamePause(start_tick=12_030, end_tick=12_930)]
        ),
        players=[
            ParsedPlayer(
                player_id=1,
                team=2,
                hero_name=lina,
                position_log=[
                    (t, *(TOP_CELL if t >= 12_960 else MID_CELL)) for t in range(0, 20_000, 30)
                ],
            )
        ],
        combat_log=[
            CombatLogEntry(
                tick=12_000,
                log_type=CombatLogType.ITEM,
                attacker_name=lina,
                inflictor_name="item_tpscroll",
            )
        ],
    )
    events = lanes.lane_events(match)
    teleports = events[events["kind"] == "teleport"]
    assert teleports[["time_s", "lane"]].values.tolist() == [[400, "top"]]


def test_lanes_reads_a_ledger_without_minute_readings() -> None:
    match = _lanes_match()
    for player in match.players:
        assert player.gold_ledger is not None
        player.gold_ledger = GoldLedger(final=player.gold_ledger.per_minute[-1])
    table = lanes.lane_table(match)
    assert table["net_worth"].sum() > 0 and table["lane_creep_gold"].sum() == 0


def test_objectives_lists_each_wisdom_rune_and_who_took_each_shrines() -> None:
    lion, rubick = "npc_dota_hero_lion", "npc_dota_hero_rubick"
    radiant_shrine, dire_shrine = (8296.0, 17152.0), (24551.0, 15241.0)

    def pickup(second: int, slot: int) -> CombatLogEntry:
        return CombatLogEntry(
            tick=second * 30, log_type=CombatLogType.PICKUP_RUNE, value=slot, rune_type=8
        )

    def xp(second: int, hero: str, value: int) -> CombatLogEntry:
        return CombatLogEntry(
            tick=second * 30 + 1,
            log_type=CombatLogType.XP,
            target_name=hero,
            xp_reason=4,
            value=value,
        )

    def where(spots: dict[int, tuple[float, float]]) -> list[tuple[int, float, float]]:
        return [
            (
                s * 30,
                *next(spot for start, spot in sorted(spots.items(), reverse=True) if s >= start),
            )
            for s in range(0, 1500)
        ]

    match = ParsedMatch(
        match_id=10,
        game_start_tick=0,
        post_game_tick=1450 * 30,  # the game ends after the 21:00 spawn
        game_clock=GameClock(game_start_tick=0),
        players=[
            # Lion takes Radiant's 7:00 rune; Rubick takes Dire's, then Radiant's at 14:00.
            ParsedPlayer(
                player_id=0, team=2, hero_name=lion, position_log=where({0: radiant_shrine})
            ),
            ParsedPlayer(
                player_id=5,
                team=3,
                hero_name=rubick,
                position_log=where({0: dire_shrine, 900: radiant_shrine}),
            ),
        ],
        combat_log=[
            # Both 7:00 runes on the same tick: each team's XP stays its own.
            pickup(425, 0),
            pickup(425, 5),
            xp(425, lion, 200),
            xp(425, rubick, 200),
            # Radiant's 14:00 rune, taken by Rubick at its shrine.
            pickup(905, 5),
            xp(905, rubick, 500),
        ],
    )
    table = objectives.objective_table(match)
    runes = table[table["kind"] == "wisdom_rune"]
    assert runes[["name", "for_side", "last_hit"]].values.tolist() == [
        ["radiant_wisdom_rune", "radiant", lion],
        ["dire_wisdom_rune", "dire", rubick],
        ["radiant_wisdom_rune", "dire", rubick],
    ]
    pickups = objectives.wisdom_pickups(match)
    assert [p["xp"] for p in pickups] == [200, 200, 500]

    spawns = objectives.wisdom_runes(match)
    assert spawns[["spawn_s", "spot", "taken_by", "after_s", "outcome"]].values.tolist() == [
        [420, "radiant", "radiant", 5, "own side"],
        [420, "dire", "dire", 5, "own side"],
        [840, "radiant", "dire", 65, "other side"],
        [840, "dire", None, pd.NA, "not taken"],
        [1260, "radiant", None, pd.NA, "game ended"],
        [1260, "dire", None, pd.NA, "game ended"],
    ]
    summary = objectives.wisdom_summary(spawns).set_index("spot")
    assert summary.loc["radiant", ["own side", "other side", "game ended"]].tolist() == [1, 1, 1]


def test_objectives_times_a_wisdom_rune_by_its_own_chat_event_clock() -> None:
    lion = "npc_dota_hero_lion"
    shrine = (8296.0, 17152.0)
    match = ParsedMatch(
        match_id=11,
        game_start_tick=0,
        post_game_tick=1300 * 30,  # after the 21:00 spawn
        game_clock=GameClock(game_start_tick=0),
        players=[
            ParsedPlayer(
                player_id=0,
                team=2,
                hero_name=lion,
                position_log=[(s * 30, *shrine) for s in range(0, 1301)],
            )
        ],
        combat_log=[
            # OpenDota's clock reads 433 and 839 for pickups whose ticks read 434 and 841.
            CombatLogEntry(
                tick=434 * 30,
                log_type=CombatLogType.PICKUP_RUNE,
                value=0,
                rune_type=8,
                game_time_s=433,
            ),
            CombatLogEntry(
                tick=841 * 30,
                log_type=CombatLogType.PICKUP_RUNE,
                value=0,
                rune_type=8,
                game_time_s=839,
            ),
        ],
    )
    table = objectives.objective_table(match)
    assert table[["time", "time_s"]].values.tolist() == [["07:13", 433], ["13:59", 839]]
    # 13:59 is still the 7:00 spawn's window: no rune is taken twice in one.
    runes = objectives.wisdom_runes(match)
    radiant = runes[runes["spot"] == "radiant"]
    assert radiant[["spawn_s", "outcome", "after_s"]].values.tolist() == [
        [420, "own side", 13],
        [840, "not taken", pd.NA],
        [1260, "game ended", pd.NA],
    ]


def test_objectives_shares_wisdom_xp_when_one_team_takes_both_runes_at_once() -> None:
    lion, tiny = "npc_dota_hero_lion", "npc_dota_hero_tiny"
    match = ParsedMatch(
        match_id=12,
        game_start_tick=0,
        game_clock=GameClock(game_start_tick=0),
        players=[
            ParsedPlayer(
                player_id=0,
                team=2,
                hero_name=lion,
                position_log=[(s * 30, 8296.0, 17152.0) for s in range(0, 500)],
            ),
            ParsedPlayer(
                player_id=1,
                team=2,
                hero_name=tiny,
                position_log=[(s * 30, 24551.0, 15241.0) for s in range(0, 500)],
            ),
        ],
        combat_log=[
            CombatLogEntry(tick=12_750, log_type=CombatLogType.PICKUP_RUNE, value=slot, rune_type=8)
            for slot in (0, 1)
        ]
        + [
            CombatLogEntry(
                tick=12_751,
                log_type=CombatLogType.XP,
                target_name=hero,
                xp_reason=4,
                value=200,
            )
            for hero in (lion, tiny, lion, tiny)
        ],
    )
    # Four entries of 200 for two runes: 400 each, not 800 each.
    assert [p["xp"] for p in objectives.wisdom_pickups(match)] == [400, 400]


def test_runes_lists_each_rune_with_its_spot_taker_and_time() -> None:
    table = runes.rune_table(_runes_match())

    assert list(table.columns) == runes.RUNE_COLUMNS
    rows = table[["rune", "spot", "outcome", "hero", "whose", "time_s", "used_s", "stage"]]
    assert rows.astype(object).where(rows.notna(), None).values.tolist() == [
        ["bounty", "dire_jungle", "picked_up", AXE, "other", 3.0, None, "0:00-6:00"],
        # The pickup's own time (the chat clock's 5), not the rune's removal at 5.1 s.
        ["bounty", "top_river", "picked_up", LINA, "river", 5.0, None, "0:00-6:00"],
        ["bounty", "radiant_jungle", "not_taken", None, None, 120.0, None, "0:00-6:00"],
        ["water", "top_river", "picked_up", LINA, None, 125.0, None, "0:00-6:00"],
        ["double_damage", "top_river", "picked_up", SF, None, 400.0, None, "6:00-20:00"],
        ["illusion", "bot_river", "bottled", AXE, None, 500.0, 600.0, "6:00-20:00"],
        ["shield", "bot_river", "denied", PUDGE, None, 1210.0, None, "20:00-end"],
        ["haste", "top_river", "still_there", None, None, None, None, "20:00-end"],
    ]


def test_runes_counts_each_sides_runes_by_stage() -> None:
    summary = runes.rune_summary(runes.rune_table(_runes_match())).set_index(["stage", "side"])

    assert summary.loc[("0:00-6:00", "radiant")].drop("match_id").to_dict() == {
        "power": 0,
        "water": 1,
        "bounty_own_jungle": 0,
        "bounty_other_jungle": 1,
        "bounty_river": 1,
        "denied": 0,
    }
    assert summary.loc[("6:00-20:00", "radiant"), "power"] == 1  # the bottled illusion rune
    assert summary.loc[("6:00-20:00", "dire"), "power"] == 1
    assert summary.loc[("20:00-end", "dire"), "denied"] == 1


def test_runes_lists_the_0_00_bounties_and_the_deaths_before_1_30() -> None:
    match = _runes_match()
    openers = runes.opening_bounties(match)
    deaths = runes.opening_deaths(match)

    assert openers[["hero", "whose", "after_horn_s", "enemies_near"]].values.tolist() == [
        [AXE, "other", 3.0, PUDGE],
        [LINA, "river", 5.0, ""],
    ]
    # Pudge's death before the horn counts; Lina's at 1:40 doesn't.
    assert deaths[["time_s", "hero", "by"]].values.tolist() == [[-10.0, PUDGE, AXE]]


def test_runes_reads_each_power_runes_window_and_what_followed() -> None:
    windows = runes.rune_windows(_runes_match())

    double, illusion = windows.to_dict("records")
    assert (double["rune"], double["start_s"], double["end_s"]) == ("double_damage", 400.0, 445.0)
    assert (double["kills"], double["killed"], double["building_damage"]) == (1, LINA, 300)
    # The tower fell 15 s after the buff ended: within AFTER_S.
    assert (double["took"], double["took_s"], double["died"]) == (
        "goodguys_tower1_top",
        "60",
        False,
    )
    # Axe's Aegis trigger at 7:05 is no kill. The rune's illusions lasted 30 and 100 s
    # (the 9:50 illusion's remove isn't theirs); the window stops at ILLUSION_S.
    assert illusion["rune"] == "illusion" and illusion["from_bottle"]
    assert illusion["end_s"] - illusion["start_s"] == pytest.approx(runes.ILLUSION_S, abs=0.05)
    assert (illusion["roshan_damage"], illusion["took"], illusion["took_s"]) == (
        200,
        "roshan",
        "40",
    )


def test_runes_puts_each_spot_on_the_map() -> None:
    assert runes.spot_of(14700, 17500) == "top_river"
    assert runes.spot_of(17600, 15200) == "bot_river"
    assert runes.spot_of(15400, 20800) == "dire_jungle"
    assert runes.spot_of(17000, 11700) == "radiant_jungle"

"""DataFrame conversion for :class:`ParsedMatch` output.

Converts the structured output of :func:`gem.parse` into pandas DataFrames
suitable for tabular analysis.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

    from gem.results.models import ParsedMatch


def build_dataframes(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    """Convert a :class:`ParsedMatch` into a dict of pandas DataFrames.

    Args:
        match: Fully populated :class:`ParsedMatch`.

    Returns:
        Dictionary with tabular projections of match-level, player-level,
        and event-level data. Existing keys are preserved:
        ``players``, ``positions``, ``combat_log``, ``wards``,
        ``objectives``, and ``chat``.
    """
    from dataclasses import asdict, fields
    from enum import Enum

    import pandas as pd

    from gem.analysis.roshan import build_rosh_conversions
    from gem.analysis.smoke_fight import build_smoke_fight_insights
    from gem.analysis.teamfight_positioning import build_teamfight_positioning
    from gem.results.models import (
        EntityVisibilityEvent,
        VisionModifierEvent,
        VisionModifierPairingIssue,
    )

    def _plain_row(item: Any) -> dict:
        """``asdict`` an item, demoting Enum field values to their raw value.

        Keeps DataFrame cells as primitives (e.g. ``"DAMAGE"`` rather than a
        ``CombatLogType`` member) so the exported schema stays backward
        compatible regardless of how internal fields are typed.
        """
        row = asdict(item)
        for key, value in row.items():
            if isinstance(value, Enum):
                row[key] = value.value
        return row

    def _plain_rows(items: list) -> list[dict]:
        """``asdict`` each item with Enum field values demoted to primitives."""
        return [_plain_row(it) for it in items]

    # --- players (per sample tick) ---
    player_rows: list[dict] = []
    player_min_rows: list[dict] = []
    player_kills_rows: list[dict] = []
    player_purchase_rows: list[dict] = []
    player_runes_rows: list[dict] = []
    player_buyback_rows: list[dict] = []

    for pp in match.players:
        n = len(pp.times)
        for i in range(n):
            player_rows.append(
                {
                    "player_id": pp.player_id,
                    "player_name": pp.player_name,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times[i],
                    "gold": pp.gold_t[i] if i < len(pp.gold_t) else 0,
                    "total_earned_gold": (
                        pp.total_earned_gold_t[i] if i < len(pp.total_earned_gold_t) else 0
                    ),
                    "net_worth": pp.net_worth_t[i] if i < len(pp.net_worth_t) else 0,
                    "lh": pp.lh_t[i] if i < len(pp.lh_t) else 0,
                    "dn": pp.dn_t[i] if i < len(pp.dn_t) else 0,
                    "xp": pp.xp_t[i] if i < len(pp.xp_t) else 0,
                    "kills": pp.kills,
                    "deaths": pp.deaths,
                    "assists": pp.assists,
                    "stuns_dealt": pp.stuns_dealt,
                    "lane_role": pp.lane_role,
                    "lane_last_hits": pp.lane_last_hits,
                    "lane_denies": pp.lane_denies,
                    "lane_total_gold": pp.lane_total_gold,
                    "lane_total_xp": pp.lane_total_xp,
                    "lane_efficiency_pct": pp.lane_efficiency_pct,
                    "lane_gold_adv": pp.lane_gold_adv,
                    "lane_xp_adv": pp.lane_xp_adv,
                    # Per-player end-of-game terminal scalars (constant across the
                    # player's rows). Named ``final_*`` to avoid shadowing the
                    # per-tick ``net_worth``/``lh``/``dn`` columns above.
                    "final_net_worth": pp.net_worth,
                    "final_last_hits": pp.last_hits,
                    "final_denies": pp.denies,
                    "camps_stacked": pp.camps_stacked,
                    "creeps_stacked": pp.creeps_stacked,
                    "obs_placed": pp.obs_placed,
                    "sen_placed": pp.sen_placed,
                    "rune_pickups": pp.rune_pickups,
                    "tower_kills": pp.tower_kills,
                    "kda": pp.kda,
                    "buyback_count": pp.buyback_count,
                    "is_radiant": pp.is_radiant,
                    "win": pp.win,
                    "kills_per_min": pp.kills_per_min,
                    "gold_per_min": pp.gold_per_min,
                    "xp_per_min": pp.xp_per_min,
                    "total_gold": pp.total_gold,
                    "total_xp": pp.total_xp,
                    "hero_damage": pp.hero_damage,
                    "tower_damage": pp.tower_damage,
                    "hero_healing": pp.hero_healing,
                    "aghanims_scepter": pp.aghanims_scepter,
                    "aghanims_shard": pp.aghanims_shard,
                    "moonshard": pp.moonshard,
                    "damage_physical": pp.damage_by_type.get("physical", 0),
                    "damage_magical": pp.damage_by_type.get("magical", 0),
                    "damage_pure": pp.damage_by_type.get("pure", 0),
                    "damage_taken_physical": pp.damage_taken_by_type.get("physical", 0),
                    "damage_taken_magical": pp.damage_taken_by_type.get("magical", 0),
                    "damage_taken_pure": pp.damage_taken_by_type.get("pure", 0),
                    "damage": dict(pp.damage),
                    "damage_taken": dict(pp.damage_taken),
                    "damage_inflictor": dict(pp.damage_inflictor),
                    "damage_inflictor_received": dict(pp.damage_inflictor_received),
                    "damage_targets": {k: dict(v) for k, v in pp.damage_targets.items()},
                    "ability_targets": {k: dict(v) for k, v in pp.ability_targets.items()},
                    "hero_hits": dict(pp.hero_hits),
                    "max_hero_hit": pp.max_hero_hit,
                    "healing": dict(pp.healing),
                    "ability_uses": dict(pp.ability_uses),
                    "item_uses": dict(pp.item_uses),
                    "purchase": dict(pp.purchase),
                    "purchase_time": dict(pp.purchase_time),
                    "first_purchase_time": dict(pp.first_purchase_time),
                    "purchase_tpscroll": pp.purchase_tpscroll,
                    "purchase_ward_observer": pp.purchase_ward_observer,
                    "purchase_ward_sentry": pp.purchase_ward_sentry,
                    "observer_uses": pp.observer_uses,
                    "sentry_uses": pp.sentry_uses,
                    "observers_placed": pp.observers_placed,
                    "gold_reasons": dict(pp.gold_reasons),
                    "xp_reasons": dict(pp.xp_reasons),
                    "lane_pos": dict(pp.lane_pos),
                }
            )

        m = len(pp.times_min)
        for i in range(m):
            game_time_s = pp.game_times_min[i] if i < len(pp.game_times_min) else None
            player_min_rows.append(
                {
                    "player_id": pp.player_id,
                    "player_name": pp.player_name,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times_min[i],
                    "game_time_s": game_time_s,
                    "minute": game_time_s // 60 if game_time_s is not None else None,
                    "gold": pp.gold_t_min[i] if i < len(pp.gold_t_min) else 0,
                    "total_earned_gold": (
                        pp.total_earned_gold_t_min[i] if i < len(pp.total_earned_gold_t_min) else 0
                    ),
                    "total_earned_xp": (
                        pp.total_earned_xp_t_min[i] if i < len(pp.total_earned_xp_t_min) else 0
                    ),
                    "net_worth": pp.net_worth_t_min[i] if i < len(pp.net_worth_t_min) else 0,
                    "lh": pp.lh_t_min[i] if i < len(pp.lh_t_min) else 0,
                    "dn": pp.dn_t_min[i] if i < len(pp.dn_t_min) else 0,
                    "xp": pp.xp_t_min[i] if i < len(pp.xp_t_min) else 0,
                }
            )

        for entry in pp.kills_log:
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            player_kills_rows.append(row)

        for entry in pp.purchase_log:
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            player_purchase_rows.append(row)

        for entry in pp.runes_log:
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            player_runes_rows.append(row)

        # Buyback rows carry the estimated cost / net worth from the structured
        # BuybackEvent (built 1:1 with buyback_log) so the DataFrame surfaces cost
        # too. Iterate buyback_log (the source of truth that a buyback happened)
        # and pull cost from the aligned BuybackEvent when present, so a row is
        # never dropped if buybacks is unset.
        for i, entry in enumerate(pp.buyback_log):
            row = _plain_row(entry)
            row["player_id"] = pp.player_id
            bb = pp.buybacks[i] if i < len(pp.buybacks) else None
            row["cost"] = bb.cost if bb is not None else None
            row["net_worth"] = bb.net_worth if bb is not None else None
            player_buyback_rows.append(row)

    players_df = pd.DataFrame(player_rows)
    players_min_df = pd.DataFrame(player_min_rows)

    # --- combat_log ---
    combat_df = pd.DataFrame(_plain_rows(match.combat_log))

    # --- wards ---
    wards_df = pd.DataFrame([asdict(w) for w in match.wards]) if match.wards else pd.DataFrame()

    # --- objectives ---
    obj_rows: list[dict] = []
    for t in match.towers:
        obj_rows.append(
            {
                "type": "tower",
                "tick": t.tick,
                "team": t.team,
                "name": t.tower_name,
                "killer": t.killer,
                "killer_source": t.killer_source,
                "killer_team": t.killer_team,
            }
        )
    for b in match.barracks:
        obj_rows.append(
            {
                "type": "barracks",
                "tick": b.tick,
                "team": b.team,
                "name": b.barracks_name,
                "killer": b.killer,
                "killer_source": b.killer_source,
                "killer_team": b.killer_team,
            }
        )
    for r in match.roshans:
        obj_rows.append(
            {
                "type": "roshan",
                "tick": r.tick,
                "team": 0,
                "name": "roshan",
                "killer": r.killer,
                "killer_source": r.killer_source,
                "killer_team": r.killer_team,
                "kill_number": r.kill_number,
                # Comma-joined raw drop tokens (e.g. "aegis,cheese,banner"). A
                # string keeps the cell filterable (df.drops.str.contains(...))
                # and round-trips cleanly to Parquet/CSV/JSON, unlike a list cell.
                "drops": ",".join(r.drops),
            }
        )
    for tm in match.tormentors:
        obj_rows.append(
            {
                "type": "tormentor",
                "tick": tm.tick,
                "team": 0,
                "name": "npc_dota_miniboss",
                "killer": tm.killer,
                "killer_team": tm.killer_team,
                "killer_player_id": tm.killer_player_id,
                "kill_number": tm.kill_number,
            }
        )
    for s in match.shrines:
        obj_rows.append(
            {
                "type": "shrine",
                "tick": s.tick,
                "team": s.team,
                "name": "shrine_of_wisdom",
                "killer": "",
            }
        )
    for a in match.aegis_events:
        obj_rows.append(
            {
                "type": "aegis",
                "tick": a.tick,
                "team": 0,
                "name": a.event_type,
                "killer": "",
                "player_id": a.player_id,
                "event_type": a.event_type,
            }
        )
    for cd in match.courier_deaths:
        obj_rows.append(
            {
                "type": "courier_death",
                "tick": cd.tick,
                "team": 0,
                "name": "npc_dota_courier",
                "killer": cd.killer,
            }
        )
    for bp in match.banner_plants:
        obj_rows.append(
            {
                "type": "banner_plant",
                "tick": bp.tick,
                "team": bp.team,
                "name": "roshans_banner",
                "killer": "",
                "player_id": bp.player_id,
                # World plant position (None when the banner unit carried no
                # readable coordinates); enables spatial filtering downstream.
                "x": bp.x,
                "y": bp.y,
            }
        )
    objectives_df = pd.DataFrame(obj_rows)

    # OpenDota-shaped unified objectives timeline (separate from the native
    # per-type objectives_df above).
    opendota_objectives_df = pd.DataFrame(match.objectives) if match.objectives else pd.DataFrame()

    # --- positions ---
    pos_rows: list[dict] = []
    for pp in match.players:
        for tick, x, y in pp.position_log:
            pos_rows.append(
                {
                    "player_id": pp.player_id,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": tick,
                    "x": x,
                    "y": y,
                }
            )
    positions_df = pd.DataFrame(pos_rows)

    # --- chat ---
    chat_df = pd.DataFrame([asdict(c) for c in match.chat]) if match.chat else pd.DataFrame()

    # --- match metadata ---
    match_df = pd.DataFrame(
        [
            {
                "match_id": match.match_id,
                "game_mode": match.game_mode,
                "leagueid": match.leagueid,
                "radiant_win": match.radiant_win,
                "game_start_tick": match.game_start_tick,
                "game_end_tick": match.game_end_tick,
                "tower_status_radiant": match.tower_status_radiant,
                "tower_status_dire": match.tower_status_dire,
                "barracks_status_radiant": match.barracks_status_radiant,
                "barracks_status_dire": match.barracks_status_dire,
            }
        ]
    )

    # --- radiant advantages ---
    adv_len = max(len(match.radiant_gold_adv), len(match.radiant_xp_adv))
    advantage_rows = [
        {
            "game_time_s": (match.game_times_min[i] if i < len(match.game_times_min) else i * 60),
            "minute": (match.game_times_min[i] // 60 if i < len(match.game_times_min) else i),
            "radiant_gold_adv": match.radiant_gold_adv[i] if i < len(match.radiant_gold_adv) else 0,
            "radiant_xp_adv": match.radiant_xp_adv[i] if i < len(match.radiant_xp_adv) else 0,
        }
        for i in range(adv_len)
    ]
    advantage_df = pd.DataFrame(advantage_rows)

    # --- list-based domains ---
    draft_df = pd.DataFrame([asdict(d) for d in match.draft]) if match.draft else pd.DataFrame()
    teamfights_df = (
        pd.DataFrame([asdict(tf) for tf in match.teamfights])
        if match.teamfights
        else pd.DataFrame()
    )
    opendota_teamfights_df = (
        pd.DataFrame([asdict(tf) for tf in match.opendota_teamfights])
        if match.opendota_teamfights
        else pd.DataFrame()
    )
    smoke_df = (
        pd.DataFrame([asdict(se) for se in match.smoke_events])
        if match.smoke_events
        else pd.DataFrame()
    )
    smoke_member_columns = [
        "smoke_event_index",
        "activation_tick",
        "activation_game_time_s",
        "activator",
        "team",
        "hero_name",
        "player_id",
        "applied_tick",
        "removed_tick",
        "modifier_duration_s",
        "modifier_elapsed_duration_s",
        "applied_x",
        "applied_y",
        "removed_x",
        "removed_y",
        "applied_game_time_s",
        "removed_game_time_s",
    ]
    smoke_member_rows = [
        {
            "smoke_event_index": event_index,
            "activation_tick": smoke.tick,
            "activation_game_time_s": smoke.activation_game_time_s,
            "activator": smoke.activator,
            "team": smoke.team,
            **asdict(participant),
        }
        for event_index, smoke in enumerate(match.smoke_events)
        for participant in smoke.participants
    ]
    smoke_members_df = pd.DataFrame(smoke_member_rows, columns=smoke_member_columns)
    courier_df = (
        pd.DataFrame([asdict(cs) for cs in match.courier_snapshots])
        if match.courier_snapshots
        else pd.DataFrame()
    )
    neutral_item_finds_df = (
        pd.DataFrame([asdict(event) for event in match.neutral_item_finds])
        if match.neutral_item_finds
        else pd.DataFrame()
    )
    hero_visibility_df = pd.DataFrame(_plain_rows(match.hero_visibility_events))
    entity_visibility_columns = [item.name for item in fields(EntityVisibilityEvent)]
    entity_visibility_df = pd.DataFrame(
        _plain_rows(match.entity_visibility_events), columns=entity_visibility_columns
    )
    vision_modifier_columns = [item.name for item in fields(VisionModifierEvent)]
    vision_modifiers_df = pd.DataFrame(
        _plain_rows(match.vision_modifiers), columns=vision_modifier_columns
    )
    vision_pairing_issue_columns = [item.name for item in fields(VisionModifierPairingIssue)]
    vision_modifier_pairing_issues_df = pd.DataFrame(
        _plain_rows(match.vision_modifier_pairing_issues),
        columns=vision_pairing_issue_columns,
    )

    positioning_columns = [
        "fight_index",
        "fight_start_tick",
        "engagement_start_tick",
        "first_death_tick",
        "fight_end_tick",
        "engagement_start_source",
        "snapshot_kind",
        "snapshot_tick",
        "player_id",
        "player_name",
        "hero_name",
        "team",
        "active_participant",
        "near_fight",
        "x",
        "y",
        "sample_tick",
        "sample_age_ticks",
        "visibility",
        "distance_to_team_centroid",
        "nearest_ally_distance",
        "nearest_enemy_distance",
        "active_smoke_activation_tick",
        "active_reveal_modifiers",
        "evidence_gaps",
        "radiant_expected_count",
        "radiant_positioned_count",
        "radiant_unpositioned_count",
        "radiant_completeness",
        "radiant_centroid_x",
        "radiant_centroid_y",
        "radiant_rms_spread",
        "dire_expected_count",
        "dire_positioned_count",
        "dire_unpositioned_count",
        "dire_completeness",
        "dire_centroid_x",
        "dire_centroid_y",
        "dire_rms_spread",
        "centroid_distance",
        "active_participant_centroid_x",
        "active_participant_centroid_y",
    ]
    positioning_rows: list[dict[str, Any]] = []
    for fight in build_teamfight_positioning(match):
        for snapshot in fight.snapshots:
            for hero in snapshot.heroes:
                positioning_rows.append(
                    {
                        "fight_index": fight.fight_index,
                        "fight_start_tick": fight.start_tick,
                        "engagement_start_tick": fight.engagement_start_tick,
                        "first_death_tick": fight.first_death_tick,
                        "fight_end_tick": fight.end_tick,
                        "engagement_start_source": fight.engagement_start_source.value,
                        "snapshot_kind": snapshot.kind.value,
                        "snapshot_tick": snapshot.tick,
                        "player_id": hero.player_id,
                        "player_name": hero.player_name,
                        "hero_name": hero.hero_name,
                        "team": hero.team,
                        "active_participant": hero.active_participant,
                        "near_fight": hero.near_fight,
                        "x": hero.x,
                        "y": hero.y,
                        "sample_tick": hero.sample_tick,
                        "sample_age_ticks": hero.sample_age_ticks,
                        "visibility": hero.visibility.value,
                        "distance_to_team_centroid": hero.distance_to_team_centroid,
                        "nearest_ally_distance": hero.nearest_ally_distance,
                        "nearest_enemy_distance": hero.nearest_enemy_distance,
                        "active_smoke_activation_tick": hero.active_smoke_activation_tick,
                        "active_reveal_modifiers": hero.active_reveal_modifiers,
                        "evidence_gaps": hero.evidence_gaps,
                        "radiant_expected_count": snapshot.radiant.expected_count,
                        "radiant_positioned_count": snapshot.radiant.positioned_count,
                        "radiant_unpositioned_count": snapshot.radiant.unpositioned_count,
                        "radiant_completeness": snapshot.radiant.completeness.value,
                        "radiant_centroid_x": snapshot.radiant.centroid_x,
                        "radiant_centroid_y": snapshot.radiant.centroid_y,
                        "radiant_rms_spread": snapshot.radiant.rms_spread,
                        "dire_expected_count": snapshot.dire.expected_count,
                        "dire_positioned_count": snapshot.dire.positioned_count,
                        "dire_unpositioned_count": snapshot.dire.unpositioned_count,
                        "dire_completeness": snapshot.dire.completeness.value,
                        "dire_centroid_x": snapshot.dire.centroid_x,
                        "dire_centroid_y": snapshot.dire.centroid_y,
                        "dire_rms_spread": snapshot.dire.rms_spread,
                        "centroid_distance": snapshot.centroid_distance,
                        "active_participant_centroid_x": (snapshot.active_participant_centroid_x),
                        "active_participant_centroid_y": (snapshot.active_participant_centroid_y),
                    }
                )
    teamfight_positioning_df = pd.DataFrame(positioning_rows, columns=positioning_columns)

    # --- evidence-first Roshan conversions ---
    roshan_conversion_columns = [
        "rosh_number",
        "rosh_tick",
        "killer_name",
        "roshan_team",
        "roshan_team_source",
        "conversion_team",
        "conversion_team_source",
        "holder_player_id",
        "holder_name",
        "aegis_pickup_tick",
        "aegis_end_tick",
        "aegis_eval_end_tick",
        "aegis_fate",
        "aegis_fate_source",
        "aegis_fate_inferred",
        "aegis_outcome",
        "first_engagement_tick",
        "first_fight_tick",
        "first_objective_tick",
        "fight_count",
        "fight_differential",
        "conversion_towers",
        "opponent_towers",
        "unattributed_towers",
        "conversion_barracks",
        "opponent_barracks",
        "unattributed_barracks",
        "conversion_structure_value",
        "opponent_structure_value",
        "structure_delta",
        "net_worth_advantage_start",
        "net_worth_advantage_end",
        "net_worth_swing",
        "net_worth_swing_per_minute",
        "xp_advantage_start",
        "xp_advantage_end",
        "xp_swing",
        "xp_swing_per_minute",
        "before_conversion_coverage_pct",
        "before_opponent_coverage_pct",
        "during_conversion_coverage_pct",
        "during_opponent_coverage_pct",
        "coverage_swing_pct",
        "depth_swing",
        "conversion_forward_wards",
        "opponent_forward_wards",
        "forward_ward_delta",
        "conversion_tormentors",
        "opponent_tormentors",
        "unattributed_tormentors",
        "tormentor_delta",
        "conversion_tags",
        "tag_ruleset",
        "analysis_status",
        "analysis_status_reasons",
        "drops",
        "legacy_conversion_score",
        "legacy_conversion_label",
    ]
    roshan_fight_columns = [
        "rosh_number",
        "fight_index",
        "relation",
        "engagement_start_tick",
        "engagement_start_source",
        "first_death_tick",
        "fight_end_tick",
        "winner",
        "deaths",
        "conversion_participant_ids",
        "opponent_participant_ids",
        "unknown_participant_ids",
    ]
    roshan_conversion_rows: list[dict[str, Any]] = []
    roshan_fight_rows: list[dict[str, Any]] = []
    for conversion in build_rosh_conversions(match):
        profile = conversion.differential_profile
        roshan_conversion_rows.append(
            {
                "rosh_number": conversion.rosh_number,
                "rosh_tick": conversion.rosh_tick,
                "killer_name": conversion.killer_name,
                "roshan_team": conversion.roshan_team,
                "roshan_team_source": conversion.roshan_team_source.value,
                "conversion_team": conversion.conversion_team,
                "conversion_team_source": conversion.conversion_team_source.value,
                "holder_player_id": conversion.holder_player_id,
                "holder_name": conversion.holder_name,
                "aegis_pickup_tick": conversion.aegis_pickup_tick,
                "aegis_end_tick": conversion.aegis_end_tick,
                "aegis_eval_end_tick": conversion.aegis_eval_end_tick,
                "aegis_fate": conversion.aegis_fate,
                "aegis_fate_source": conversion.aegis_fate_source.value,
                "aegis_fate_inferred": conversion.aegis_fate_inferred,
                "aegis_outcome": conversion.aegis_outcome,
                "first_engagement_tick": conversion.first_engagement_tick,
                "first_fight_tick": conversion.first_fight_tick,
                "first_objective_tick": conversion.first_objective_tick,
                "fight_count": conversion.fight_count,
                "fight_differential": profile.fight_differential,
                "conversion_towers": profile.conversion_towers,
                "opponent_towers": profile.opponent_towers,
                "unattributed_towers": profile.unattributed_towers,
                "conversion_barracks": profile.conversion_barracks,
                "opponent_barracks": profile.opponent_barracks,
                "unattributed_barracks": profile.unattributed_barracks,
                "conversion_structure_value": profile.conversion_structure_value,
                "opponent_structure_value": profile.opponent_structure_value,
                "structure_delta": profile.structure_delta,
                "net_worth_advantage_start": profile.net_worth_advantage_start,
                "net_worth_advantage_end": profile.net_worth_advantage_end,
                "net_worth_swing": profile.net_worth_swing,
                "net_worth_swing_per_minute": profile.net_worth_swing_per_minute,
                "xp_advantage_start": profile.xp_advantage_start,
                "xp_advantage_end": profile.xp_advantage_end,
                "xp_swing": profile.xp_swing,
                "xp_swing_per_minute": profile.xp_swing_per_minute,
                "before_conversion_coverage_pct": (
                    profile.before_territory.conversion_coverage_pct
                ),
                "before_opponent_coverage_pct": (profile.before_territory.opponent_coverage_pct),
                "during_conversion_coverage_pct": (
                    profile.during_territory.conversion_coverage_pct
                ),
                "during_opponent_coverage_pct": (profile.during_territory.opponent_coverage_pct),
                "coverage_swing_pct": profile.coverage_swing_pct,
                "depth_swing": profile.depth_swing,
                "conversion_forward_wards": profile.conversion_forward_wards,
                "opponent_forward_wards": profile.opponent_forward_wards,
                "forward_ward_delta": profile.forward_ward_delta,
                "conversion_tormentors": profile.conversion_tormentors,
                "opponent_tormentors": profile.opponent_tormentors,
                "unattributed_tormentors": profile.unattributed_tormentors,
                "tormentor_delta": profile.tormentor_delta,
                "conversion_tags": ",".join(conversion.conversion_tags),
                "tag_ruleset": profile.tag_ruleset,
                "analysis_status": conversion.analysis_status,
                "analysis_status_reasons": ";".join(conversion.analysis_status_reasons),
                "drops": ",".join(conversion.drops),
                "legacy_conversion_score": conversion.conversion_score,
                "legacy_conversion_label": conversion.conversion_label,
            }
        )
        for evidence in conversion.fight_evidence:
            roshan_fight_rows.append(
                {
                    "rosh_number": conversion.rosh_number,
                    "fight_index": evidence.fight_index,
                    "relation": evidence.relation.value,
                    "engagement_start_tick": evidence.engagement_start_tick,
                    "engagement_start_source": evidence.engagement_start_source.value,
                    "first_death_tick": evidence.first_death_tick,
                    "fight_end_tick": evidence.end_tick,
                    "winner": evidence.winner,
                    "deaths": evidence.deaths,
                    "conversion_participant_ids": ",".join(
                        str(player_id) for player_id in evidence.conversion_participant_ids
                    ),
                    "opponent_participant_ids": ",".join(
                        str(player_id) for player_id in evidence.opponent_participant_ids
                    ),
                    "unknown_participant_ids": ",".join(
                        str(player_id) for player_id in evidence.unknown_participant_ids
                    ),
                }
            )
    roshan_conversions_df = pd.DataFrame(roshan_conversion_rows, columns=roshan_conversion_columns)
    roshan_conversion_fights_df = pd.DataFrame(roshan_fight_rows, columns=roshan_fight_columns)

    # --- bounded smoke/fight insights ---
    insight_columns = [
        "smoke_index",
        "fight_index",
        "status",
        "evidence_completeness",
        "smoke_team",
        "activator",
        "smoke_lifecycle_status",
        "activation_tick",
        "activation_game_time_s",
        "first_member_removal_tick",
        "first_authoritative_visible_tick",
        "first_direct_reveal_tick",
        "first_member_action_tick",
        "first_death_tick",
        "fight_end_tick",
        "active_smoked_member_count",
        "active_smoked_player_ids",
        "pre_engagement_expected_count",
        "pre_engagement_positioned_count",
        "pre_engagement_completeness",
        "pre_engagement_centroid_x",
        "pre_engagement_centroid_y",
        "pre_engagement_rms_spread",
        "pre_engagement_max_pairwise_distance",
        "engagement_expected_count",
        "engagement_positioned_count",
        "engagement_completeness",
        "engagement_centroid_x",
        "engagement_centroid_y",
        "engagement_rms_spread",
        "engagement_max_pairwise_distance",
        "sampled_near_fight_spread_ticks",
        "near_fight_centroid_source",
        "fight_deaths",
        "fight_radiant_kills",
        "fight_dire_kills",
        "fight_winner",
        "follow_up_start_tick",
        "follow_up_end_tick",
        "follow_up_end_reasons",
        "evidence_gaps",
    ]
    member_columns = [
        "smoke_index",
        "fight_index",
        "status",
        "participant_index",
        "player_id",
        "hero_name",
        "resolved",
        "active_participant",
        "authoritative_visibility",
        "point_vision_status",
        "pre_engagement_x",
        "pre_engagement_y",
        "pre_engagement_sample_tick",
        "pre_engagement_sample_age_ticks",
        "engagement_x",
        "engagement_y",
        "engagement_sample_tick",
        "engagement_sample_age_ticks",
        "sampled_near_fight_tick",
        "sampled_near_fight_x",
        "sampled_near_fight_y",
        "sampled_near_fight_distance",
        "evidence_gaps",
    ]
    follow_up_columns = [
        "smoke_index",
        "fight_index",
        "kind",
        "source_index",
        "tick",
        "game_time_s",
        "tick_delta",
        "game_time_delta_s",
        "actor_name",
        "actor_player_id",
        "actor_team",
        "relation",
        "subject_name",
        "window_start_tick",
        "window_end_tick",
    ]

    smoke_fight_insight_rows: list[dict[str, Any]] = []
    smoke_fight_member_rows: list[dict[str, Any]] = []
    smoke_fight_follow_up_rows: list[dict[str, Any]] = []
    for insight in build_smoke_fight_insights(match):
        pre = insight.pre_engagement_formation
        engagement = insight.engagement_formation
        outcome = insight.outcome
        window = insight.follow_up_window
        smoke_fight_insight_rows.append(
            {
                "smoke_index": insight.smoke_index,
                "fight_index": insight.fight_index,
                "status": insight.status.value,
                "evidence_completeness": insight.evidence_completeness.value,
                "smoke_team": insight.smoke_team,
                "activator": insight.activator,
                "smoke_lifecycle_status": insight.smoke_lifecycle_status.value,
                "activation_tick": insight.activation.tick,
                "activation_game_time_s": insight.activation.game_time_s,
                "first_member_removal_tick": (
                    insight.first_member_removal.tick if insight.first_member_removal else None
                ),
                "first_authoritative_visible_tick": (
                    insight.first_authoritative_visible.tick
                    if insight.first_authoritative_visible
                    else None
                ),
                "first_direct_reveal_tick": (
                    insight.first_direct_reveal.tick if insight.first_direct_reveal else None
                ),
                "first_member_action_tick": (
                    insight.first_member_action.tick if insight.first_member_action else None
                ),
                "first_death_tick": insight.first_death.tick if insight.first_death else None,
                "fight_end_tick": insight.fight_end.tick if insight.fight_end else None,
                "active_smoked_member_count": len(insight.active_smoked_player_ids),
                "active_smoked_player_ids": ",".join(
                    str(player_id) for player_id in insight.active_smoked_player_ids
                ),
                "pre_engagement_expected_count": pre.expected_count if pre else None,
                "pre_engagement_positioned_count": pre.positioned_count if pre else None,
                "pre_engagement_completeness": pre.completeness.value if pre else None,
                "pre_engagement_centroid_x": pre.centroid_x if pre else None,
                "pre_engagement_centroid_y": pre.centroid_y if pre else None,
                "pre_engagement_rms_spread": pre.rms_spread if pre else None,
                "pre_engagement_max_pairwise_distance": (
                    pre.max_pairwise_distance if pre else None
                ),
                "engagement_expected_count": engagement.expected_count if engagement else None,
                "engagement_positioned_count": (
                    engagement.positioned_count if engagement else None
                ),
                "engagement_completeness": (engagement.completeness.value if engagement else None),
                "engagement_centroid_x": engagement.centroid_x if engagement else None,
                "engagement_centroid_y": engagement.centroid_y if engagement else None,
                "engagement_rms_spread": engagement.rms_spread if engagement else None,
                "engagement_max_pairwise_distance": (
                    engagement.max_pairwise_distance if engagement else None
                ),
                "sampled_near_fight_spread_ticks": insight.sampled_near_fight_spread_ticks,
                "near_fight_centroid_source": (
                    insight.near_fight_centroid_source.value
                    if insight.near_fight_centroid_source
                    else None
                ),
                "fight_deaths": outcome.deaths if outcome else None,
                "fight_radiant_kills": outcome.radiant_kills if outcome else None,
                "fight_dire_kills": outcome.dire_kills if outcome else None,
                "fight_winner": outcome.winner if outcome else None,
                "follow_up_start_tick": window.start_tick if window else None,
                "follow_up_end_tick": window.end_tick if window else None,
                "follow_up_end_reasons": (
                    ",".join(reason.value for reason in window.end_reasons) if window else ""
                ),
                "evidence_gaps": ";".join(insight.evidence_gaps),
            }
        )

        for member in insight.members:
            pre_position = member.pre_engagement_position
            engagement_position = member.engagement_position
            near = member.sampled_near_fight
            smoke_fight_member_rows.append(
                {
                    "smoke_index": insight.smoke_index,
                    "fight_index": insight.fight_index,
                    "status": insight.status.value,
                    "participant_index": member.participant_index,
                    "player_id": member.player_id,
                    "hero_name": member.hero_name,
                    "resolved": member.resolved,
                    "active_participant": member.active_participant,
                    "authoritative_visibility": member.authoritative_visibility.value,
                    "point_vision_status": (
                        member.point_vision.status.value if member.point_vision else None
                    ),
                    "pre_engagement_x": pre_position.x if pre_position else None,
                    "pre_engagement_y": pre_position.y if pre_position else None,
                    "pre_engagement_sample_tick": (
                        pre_position.sample_tick if pre_position else None
                    ),
                    "pre_engagement_sample_age_ticks": (
                        pre_position.sample_age_ticks if pre_position else None
                    ),
                    "engagement_x": engagement_position.x if engagement_position else None,
                    "engagement_y": engagement_position.y if engagement_position else None,
                    "engagement_sample_tick": (
                        engagement_position.sample_tick if engagement_position else None
                    ),
                    "engagement_sample_age_ticks": (
                        engagement_position.sample_age_ticks if engagement_position else None
                    ),
                    "sampled_near_fight_tick": near.tick if near else None,
                    "sampled_near_fight_x": near.x if near else None,
                    "sampled_near_fight_y": near.y if near else None,
                    "sampled_near_fight_distance": near.distance if near else None,
                    "evidence_gaps": ";".join(member.evidence_gaps),
                }
            )

        for follow_up in insight.follow_ups:
            smoke_fight_follow_up_rows.append(
                {
                    "smoke_index": insight.smoke_index,
                    "fight_index": insight.fight_index,
                    "kind": follow_up.kind.value,
                    "source_index": follow_up.source_index,
                    "tick": follow_up.tick,
                    "game_time_s": follow_up.game_time_s,
                    "tick_delta": follow_up.tick_delta,
                    "game_time_delta_s": follow_up.game_time_delta_s,
                    "actor_name": follow_up.actor_name,
                    "actor_player_id": follow_up.actor_player_id,
                    "actor_team": follow_up.actor_team,
                    "relation": follow_up.relation.value,
                    "subject_name": follow_up.subject_name,
                    "window_start_tick": window.start_tick if window else None,
                    "window_end_tick": window.end_tick if window else None,
                }
            )

    smoke_fight_insights_df = pd.DataFrame(
        smoke_fight_insight_rows,
        columns=insight_columns,
    )
    smoke_fight_members_df = pd.DataFrame(
        smoke_fight_member_rows,
        columns=member_columns,
    )
    smoke_fight_followups_df = pd.DataFrame(
        smoke_fight_follow_up_rows,
        columns=follow_up_columns,
    )

    return {
        "players": players_df,
        "players_minute": players_min_df,
        "positions": positions_df,
        "combat_log": combat_df,
        "wards": wards_df,
        "objectives": objectives_df,
        "opendota_objectives": opendota_objectives_df,
        "chat": chat_df,
        "match": match_df,
        "radiant_advantage": advantage_df,
        "draft": draft_df,
        "teamfights": teamfights_df,
        "teamfight_positioning": teamfight_positioning_df,
        "roshan_conversions": roshan_conversions_df,
        "roshan_conversion_fights": roshan_conversion_fights_df,
        "opendota_teamfights": opendota_teamfights_df,
        "smoke_events": smoke_df,
        "smoke_members": smoke_members_df,
        "smoke_fight_insights": smoke_fight_insights_df,
        "smoke_fight_members": smoke_fight_members_df,
        "smoke_fight_followups": smoke_fight_followups_df,
        "courier_snapshots": courier_df,
        "neutral_item_finds": neutral_item_finds_df,
        "hero_visibility_events": hero_visibility_df,
        "entity_visibility": entity_visibility_df,
        "vision_modifiers": vision_modifiers_df,
        "vision_modifier_pairing_issues": vision_modifier_pairing_issues_df,
        "player_kills_log": pd.DataFrame(player_kills_rows),
        "player_purchase_log": pd.DataFrame(player_purchase_rows),
        "player_runes_log": pd.DataFrame(player_runes_rows),
        "player_buyback_log": pd.DataFrame(player_buyback_rows),
    }

"""DataFrame conversion for :class:`ParsedMatch` output.

Converts the structured output of :func:`gem.parse` into pandas DataFrames
suitable for tabular analysis.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

    from gem.models import ParsedMatch


def build_dataframes(match: ParsedMatch) -> dict[str, pd.DataFrame]:
    """Convert a :class:`ParsedMatch` into a dict of pandas DataFrames.

    Args:
        match: Fully populated :class:`ParsedMatch`.

    Returns:
        Dictionary with keys:
        - ``"players"``: one row per player per sample tick (wide format).
        - ``"positions"``: one row per ``(player, tick)`` with x/y coordinates.
        - ``"combat_log"``: one row per combat log entry.
        - ``"wards"``: one row per ward placement.
        - ``"objectives"``: one row per tower/barracks/roshan kill.
        - ``"chat"``: one row per chat message.
    """
    from dataclasses import asdict

    import pandas as pd

    # --- players ---
    player_rows: list[dict] = []
    for pp in match.players:
        n = len(pp.times)
        for i in range(n):
            player_rows.append(
                {
                    "player_id": pp.player_id,
                    "hero_name": pp.hero_name,
                    "team": pp.team,
                    "tick": pp.times[i],
                    "gold": pp.gold_t[i] if i < len(pp.gold_t) else 0,
                    "lh": pp.lh_t[i] if i < len(pp.lh_t) else 0,
                    "dn": pp.dn_t[i] if i < len(pp.dn_t) else 0,
                    "xp": pp.xp_t[i] if i < len(pp.xp_t) else 0,
                    "damage_physical": pp.damage_by_type.get("physical", 0),
                    "damage_magical": pp.damage_by_type.get("magical", 0),
                    "damage_pure": pp.damage_by_type.get("pure", 0),
                    "damage_taken_physical": pp.damage_taken_by_type.get("physical", 0),
                    "damage_taken_magical": pp.damage_taken_by_type.get("magical", 0),
                    "damage_taken_pure": pp.damage_taken_by_type.get("pure", 0),
                }
            )
    players_df = pd.DataFrame(player_rows)

    # --- combat_log ---
    combat_df = pd.DataFrame([asdict(e) for e in match.combat_log])

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
            }
        )
    for r in match.roshans:
        obj_rows.append(
            {"type": "roshan", "tick": r.tick, "team": 0, "name": "roshan", "killer": r.killer}
        )
    objectives_df = pd.DataFrame(obj_rows)

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

    return {
        "players": players_df,
        "positions": positions_df,
        "combat_log": combat_df,
        "wards": wards_df,
        "objectives": objectives_df,
        "chat": chat_df,
    }

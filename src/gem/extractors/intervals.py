"""OpenDota-style interval snapshots for per-minute match curves.

The dense player extractor samples hero/controller state for general time
series use. OpenDota's ``gold_t``/``xp_t`` arrays, however, come from periodic
``interval`` entries built from ``CDOTA_PlayerResource`` plus
``CDOTA_DataRadiant``/``CDOTA_DataDire``. This extractor keeps that path
separate so match-level advantage curves can use the same authoritative fields
without overloading ``PlayerExtractor`` with another responsibility.

Reference:
    ``refs/parser/src/main/java/opendota/Parse.java`` interval block and
    ``refs/parser/src/main/java/opendota/CreateParsedDataBlob.java``
    ``handleInterval``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from gem.extractors._snapshots import _HERO_CLASS_PREFIX
from gem.state.entities import Entity, EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser

_TEAM_RADIANT = 2
_TEAM_DIRE = 3
_PLAYER_RESOURCE_SCAN_LIMIT = 30


@dataclass(frozen=True, slots=True)
class IntervalSnapshot:
    """One OpenDota-style interval sample for a player.

    ``gold`` and ``xp`` are cumulative earned totals from the team data entity,
    not current spendable gold or current-level XP. Those names mirror
    OpenDota's interval entry fields, which later become ``gold_t`` and
    ``xp_t`` arrays in parsed output.
    """

    tick: int
    time_s: int
    player_id: int
    player_slot: int
    team: int
    team_slot: int
    hero_name: str = ""
    gold: int = 0
    xp: int = 0
    lh: int = 0
    dn: int = 0
    net_worth: int = 0


@dataclass(slots=True)
class IntervalTimeSeries:
    """Parallel interval arrays for one player."""

    player_id: int
    ticks: list[int] = field(default_factory=list)
    times: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)


class IntervalExtractor:
    """Collect 60-second player intervals from authoritative team entities.

    The extractor is internal plumbing for OpenDota-parity output. It samples
    only when the parser's game clock lands on an exact interval boundary and
    falls silent otherwise; callers can fall back to existing player minute
    series when no complete interval data was observed for a replay.
    """

    snapshots: list[IntervalSnapshot]

    def __init__(self, interval_s: int = 60) -> None:
        """Initialise interval sampling.

        Args:
            interval_s: Game-time cadence in seconds. Defaults to 60 seconds,
                matching OpenDota's exported minute arrays.

        Raises:
            ValueError: If ``interval_s`` is not positive.
        """
        if interval_s <= 0:
            raise ValueError("interval_s must be positive")
        self._interval_s = interval_s
        self._parser: ReplayParser | None = None
        self._player_resource: Entity | None = None
        self._data_radiant: Entity | None = None
        self._data_dire: Entity | None = None
        self._player_index_by_id: dict[int, int] = {}
        self._player_team: dict[int, int] = {}
        self._player_team_slot: dict[int, int] = {}
        self._hero_names: dict[int, str] = {}
        self._next_interval_s: int | None = None
        self._last_emitted_time_s: int | None = None
        self._ended = False
        self.snapshots = []

    def attach(self, parser: ReplayParser) -> None:
        """Register parser callbacks."""
        self._parser = parser
        parser.on_entity(self._on_entity)
        parser.on_game_end(self._on_game_end)

    @property
    def all_snapshots(self) -> list[IntervalSnapshot]:
        """Return all collected interval snapshots."""
        return self.snapshots

    def series(self, player_id: int) -> IntervalTimeSeries:
        """Aggregate interval snapshots for one player.

        Args:
            player_id: OpenDota logical player slot, 0-9.

        Returns:
            Parallel arrays sorted by game time.
        """
        ts = IntervalTimeSeries(player_id=player_id)
        player_snaps = sorted(
            (snap for snap in self.snapshots if snap.player_id == player_id),
            key=lambda snap: (snap.time_s, snap.tick),
        )
        for snap in player_snaps:
            ts.ticks.append(snap.tick)
            ts.times.append(snap.time_s)
            ts.gold_t.append(snap.gold)
            ts.xp_t.append(snap.xp)
            ts.lh_t.append(snap.lh)
            ts.dn_t.append(snap.dn)
            ts.net_worth_t.append(snap.net_worth)
        return ts

    def _on_game_end(self, _tick: int) -> None:
        self._ended = True

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        cls = entity.get_class_name()

        if cls == "CDOTAGamerulesProxy":
            if not op.has(EntityOp.DELETED):
                self._maybe_emit()
            return

        if cls == "CDOTA_PlayerResource":
            if op.has(EntityOp.DELETED):
                self._player_resource = None
                self._player_index_by_id.clear()
                self._player_team.clear()
                self._player_team_slot.clear()
            else:
                self._player_resource = entity
                self._refresh_player_mappings()
                self._maybe_emit()
            return

        if cls in ("CDOTADataRadiant", "CDOTA_DataRadiant"):
            self._data_radiant = None if op.has(EntityOp.DELETED) else entity
            if not op.has(EntityOp.DELETED):
                self._maybe_emit()
            return

        if cls in ("CDOTADataDire", "CDOTA_DataDire"):
            self._data_dire = None if op.has(EntityOp.DELETED) else entity
            if not op.has(EntityOp.DELETED):
                self._maybe_emit()
            return

        if cls.startswith(_HERO_CLASS_PREFIX):
            player_id = _player_id_from_hero(entity)
            if player_id is None:
                return
            if op.has(EntityOp.DELETED):
                self._hero_names.pop(player_id, None)
            else:
                self._hero_names[player_id] = self._hero_name(entity)
                self._maybe_emit()

    def _refresh_player_mappings(self) -> None:
        """Build OpenDota logical slot mappings from ``CDOTA_PlayerResource``.

        OpenDota first scans PlayerResource for valid player indices, then uses
        the scan order as output slot ``0..9``. The resource index is not always
        the same as the logical output slot, so keep the indirection explicit.
        """
        pr = self._player_resource
        if pr is None:
            return

        player_index_by_id: dict[int, int] = {}
        player_team: dict[int, int] = {}
        player_team_slot: dict[int, int] = {}

        for resource_idx in range(_PLAYER_RESOURCE_SCAN_LIMIT):
            team = pr.get_int32(f"m_vecPlayerData.{resource_idx:04d}.m_iPlayerTeam")
            team_slot = pr.get_int32(f"m_vecPlayerTeamData.{resource_idx:04d}.m_iTeamSlot")
            if team not in (_TEAM_RADIANT, _TEAM_DIRE) or team_slot is None or team_slot < 0:
                continue
            player_id = len(player_index_by_id)
            if player_id >= 10:
                break
            player_index_by_id[player_id] = resource_idx
            player_team[player_id] = team
            player_team_slot[player_id] = team_slot

        self._player_index_by_id = player_index_by_id
        self._player_team = player_team
        self._player_team_slot = player_team_slot

    def _maybe_emit(self) -> None:
        if self._parser is None or self._ended:
            return
        if self._player_resource is None or not self._player_index_by_id:
            return
        teams = set(self._player_team.values())
        if _TEAM_RADIANT in teams and self._data_radiant is None:
            return
        if _TEAM_DIRE in teams and self._data_dire is None:
            return

        game_time_s = getattr(self._parser, "game_time_s", None)
        if game_time_s is None or game_time_s < 0:
            return
        if game_time_s % self._interval_s != 0:
            return
        if self._last_emitted_time_s == game_time_s:
            return
        if self._next_interval_s is not None and game_time_s < self._next_interval_s:
            return

        emitted = self._emit(game_time_s)
        if emitted:
            self._last_emitted_time_s = game_time_s
            self._next_interval_s = game_time_s + self._interval_s

    def _emit(self, game_time_s: int) -> bool:
        emitted = False
        tick = self._parser.tick if self._parser is not None else 0

        for player_id in sorted(self._player_index_by_id):
            team = self._player_team.get(player_id, 0)
            team_slot = self._player_team_slot.get(player_id)
            if team_slot is None:
                continue
            data_entity = self._data_radiant if team == _TEAM_RADIANT else self._data_dire
            if data_entity is None:
                continue

            prefix = f"m_vecDataTeam.{team_slot:04d}"
            player_slot = team_slot if team == _TEAM_RADIANT else 128 + team_slot
            self.snapshots.append(
                IntervalSnapshot(
                    tick=tick,
                    time_s=game_time_s,
                    player_id=player_id,
                    player_slot=player_slot,
                    team=team,
                    team_slot=team_slot,
                    hero_name=self._hero_names.get(player_id, ""),
                    gold=_int_or_zero(data_entity.get_int32(f"{prefix}.m_iTotalEarnedGold")),
                    xp=_int_or_zero(data_entity.get_int32(f"{prefix}.m_iTotalEarnedXP")),
                    lh=_int_or_zero(data_entity.get_int32(f"{prefix}.m_iLastHitCount")),
                    dn=_int_or_zero(data_entity.get_int32(f"{prefix}.m_iDenyCount")),
                    net_worth=_int_or_zero(data_entity.get_int32(f"{prefix}.m_iNetWorth")),
                )
            )
            emitted = True

        return emitted

    def _hero_name(self, entity: Entity) -> str:
        entity_names = (
            self._parser.string_tables.get_by_name("EntityNames")
            if self._parser is not None and self._parser.string_tables is not None
            else None
        )
        if entity_names is not None:
            name_idx = entity.get_int32("m_pEntity.m_nameStringableIndex")
            if name_idx is None:
                name_idx = entity.get_int32("m_pEntity.m_nameStringTableIndex")
            if name_idx is not None and name_idx >= 0:
                item = entity_names.items.get(name_idx)
                if item is not None:
                    return item[0] if isinstance(item, tuple) else str(item)

        ending = entity.get_class_name()[len(_HERO_CLASS_PREFIX) :].replace("_", "")
        return "npc_dota_hero" + re.sub(r"([A-Z])", r"_\1", ending).lower()


def _player_id_from_hero(entity: Entity) -> int | None:
    player_id = entity.get_int32("m_nPlayerID")
    if player_id is None:
        player_id = entity.get_int32("m_iPlayerID")
    if player_id is None or player_id < 0:
        return None
    return player_id // 2


def _int_or_zero(value: int | None) -> int:
    return value if value is not None else 0

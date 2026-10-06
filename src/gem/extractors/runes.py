"""Rune extractor: every rune that spawned, where, and how it ended.

Each power, bounty and water rune is a ``CDOTA_Item_Rune`` entity while it sits
on the map: its creation gives the spawn tick, type (``m_iRuneType``) and
position, and its deletion the tick it left. The rune chat events say who took
it and how: ``CHAT_MESSAGE_RUNE_PICKUP`` (taken), ``CHAT_MESSAGE_RUNE_BOTTLE``
(put in a Bottle) and ``CHAT_MESSAGE_RUNE_DENY`` (destroyed), with the player
slot in ``playerid_1`` and the rune type in ``value``. A rune removed with no
chat event was not taken (a power rune is replaced at the next spawn).

A Bottle's rune is used later with another ``CHAT_MESSAGE_RUNE_PICKUP`` that
removes no rune; it is matched to that player's last bottled rune of the type.
Wisdom runes are no entity, so they are not here (they are ``PICKUP_RUNE``
combat-log entries).

None of the pinned parsers reads rune entities, and only odota/parser handles a
rune chat event (``CHAT_MESSAGE_RUNE_PICKUP``, in ``Parse.java`` ``onChatEvent``
and ``CreateParsedDataBlob.java`` ``handleRunePickup``, keeping ``player1`` and
``value``); the bottle and deny events, and the matching to entities, are
gem-original, checked against the fixture replays. Chat-event type numbers:
``dota_usermessages.proto`` (pickup 22, bottle 23, deny 114).

Reference: odota/parser src/main/java/opendota/Parse.java (pinned revision in
CLAUDE.md).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from gem.extractors._snapshots import _pos
from gem.proto.dota_usermessages_pb2 import (
    CHAT_MESSAGE_RUNE_BOTTLE,
    CHAT_MESSAGE_RUNE_DENY,
    CHAT_MESSAGE_RUNE_PICKUP,
)
from gem.state.entities import EntityOp

if TYPE_CHECKING:
    from gem.parser import ReplayParser
    from gem.proto.dota_usermessages_pb2 import CDOTAUserMsg_ChatEvent
    from gem.state.entities import Entity

_RUNE_CLASS = "CDOTA_Item_Rune"
#: A chat event and its rune's removal share a tick in practice; allow this many either side.
_MATCH_TICKS = 2

RuneOutcome = Literal["picked_up", "bottled", "denied", "not_taken", "still_there"]

_CHAT_OUTCOMES: dict[int, RuneOutcome] = {
    CHAT_MESSAGE_RUNE_PICKUP: "picked_up",
    CHAT_MESSAGE_RUNE_BOTTLE: "bottled",
    CHAT_MESSAGE_RUNE_DENY: "denied",
}


@dataclass
class Rune:
    """One rune that spawned, and how it ended.

    Attributes:
        spawn_tick: Replay tick the rune appeared (its entity's creation).
        rune_type: The rune's type (``m_iRuneType``; the same numbers as
            ``CombatLogEntry.rune_type``: 5 bounty, 7 water, the others power
            runes).
        x: World x of the rune, or ``None`` if unavailable.
        y: World y of the rune, or ``None`` if unavailable.
        end_tick: Replay tick the rune left the map, or ``None`` if it was
            still there when the replay ended.
        outcome: ``picked_up``, ``bottled`` (put in a Bottle), ``denied``,
            ``not_taken`` (removed with no rune chat event) or ``still_there``.
        player_id: Player slot (0–9) that took, bottled or denied it, or ``None``.
        used_tick: For a bottled rune, the tick the Bottle was used (the later
            ``CHAT_MESSAGE_RUNE_PICKUP`` with no rune of its own), or ``None``.
    """

    spawn_tick: int
    rune_type: int
    x: float | None
    y: float | None
    end_tick: int | None = None
    outcome: RuneOutcome = "still_there"
    player_id: int | None = None
    used_tick: int | None = None


class RuneExtractor:
    """Collects every rune entity and the rune chat events, then matches them.

    Attach to a ``ReplayParser`` before calling ``parse()``, then call
    :meth:`finalize`:

    Example:
        >>> extractor = RuneExtractor()
        >>> extractor.attach(parser)
        >>> parser.parse()
        >>> runes = extractor.finalize()
    """

    def __init__(self) -> None:
        self._parser: ReplayParser | None = None
        self._runes: list[Rune] = []
        # Entity index → the rune on the map in that slot now.
        self._live: dict[int, Rune] = {}
        # (tick, outcome, player slot, rune type) for each rune chat event.
        self._chats: list[tuple[int, RuneOutcome, int, int]] = []

    def attach(self, parser: ReplayParser) -> None:
        """Register this extractor's callbacks with a parser.

        Args:
            parser: The ``ReplayParser`` instance to attach to.
        """
        self._parser = parser
        parser.on_chat_event(self._on_chat_event)
        parser._on_entity_filtered(self._on_entity, class_names=(_RUNE_CLASS,))

    def _on_entity(self, entity: Entity, op: EntityOp) -> None:
        tick = self._parser.tick if self._parser is not None else 0
        index = entity.get_index()
        if op & EntityOp.DELETED:
            rune = self._live.pop(index, None)
            if rune is not None:
                rune.end_tick = tick
            return
        # Any other op on a slot with no live rune is a new rune: a recycled slot
        # can come back as UPDATED (with ENTERED) instead of CREATED, as wards do.
        if index in self._live:
            return
        rune_type = entity.get_int32("m_iRuneType")
        pos = _pos(entity)
        rune = Rune(
            spawn_tick=tick,
            rune_type=rune_type if rune_type is not None else -1,
            x=pos[0] if pos else None,
            y=pos[1] if pos else None,
        )
        self._live[index] = rune
        self._runes.append(rune)

    def _on_chat_event(self, event: CDOTAUserMsg_ChatEvent, tick: int) -> None:
        outcome = _CHAT_OUTCOMES.get(event.type)
        if outcome is not None:
            self._chats.append((tick, outcome, event.playerid_1, event.value))

    def finalize(self) -> list[Rune]:
        """Match the chat events to the runes and return every rune, by spawn tick.

        Each type's chat events and removed runes are paired as a group (see
        :func:`_pair`): a chat event takes a rune of its type removed within
        ``_MATCH_TICKS`` of it. A pickup with no such rune is a Bottle being
        used: it sets ``used_tick`` on that player's latest bottled rune of the
        type not yet used. A removed rune no chat event took was not taken.

        Returns:
            Every rune, in spawn order.
        """
        chats = sorted(self._chats, key=lambda chat: chat[0])
        removed = sorted(
            (rune for rune in self._runes if rune.end_tick is not None),
            key=lambda rune: (rune.end_tick, rune.spawn_tick),
        )
        matched: set[int] = set()
        for rune_type in {chat[3] for chat in chats}:
            type_chats = [i for i, chat in enumerate(chats) if chat[3] == rune_type]
            type_runes = [rune for rune in removed if rune.rune_type == rune_type]
            ticks = [chats[i][0] for i in type_chats]
            for chat_at, rune in _pair(ticks, type_runes):
                index = type_chats[chat_at]
                rune.outcome, rune.player_id = chats[index][1], chats[index][2]
                matched.add(index)
        for index, (tick, outcome, slot, rune_type) in enumerate(chats):
            if index in matched or outcome != "picked_up":
                continue
            bottled = [
                rune
                for rune in self._runes
                if rune.outcome == "bottled"
                and rune.player_id == slot
                and rune.rune_type == rune_type
                and rune.used_tick is None
                and rune.end_tick is not None
                and rune.end_tick <= tick
            ]
            if bottled:
                max(bottled, key=lambda r: r.end_tick or 0).used_tick = tick
        for rune in self._runes:
            if rune.end_tick is not None and rune.player_id is None:
                rune.outcome = "not_taken"
        return sorted(self._runes, key=lambda rune: rune.spawn_tick)


def _pair(ticks: list[int], runes: list[Rune]) -> list[tuple[int, Rune]]:
    """Pair chat-event ticks with removed runes of one type, both in tick order.

    Takes as many pairs within ``_MATCH_TICKS`` as possible, then the smallest
    total tick gap, keeping both in order (crossed pairs are never needed). A
    nearest-first match can't do this: with runes removed at ticks 100 and 102
    and events at 102 and 104, the first event would take the rune at 102 and
    leave the second none. The events and runes are split where nothing lies
    within ``_MATCH_TICKS`` of the next, and each stretch is aligned on its own.

    Returns:
        ``(index into ticks, rune)`` for each pair.
    """
    items = sorted(
        [(tick, 0, i) for i, tick in enumerate(ticks)]
        + [(rune.end_tick or 0, 1, j) for j, rune in enumerate(runes)]
    )
    pairs: list[tuple[int, Rune]] = []
    start = 0
    for end in range(1, len(items) + 1):
        if end < len(items) and items[end][0] - items[end - 1][0] <= _MATCH_TICKS:
            continue
        stretch = items[start:end]
        start = end
        chat_ids = [i for _, kind, i in stretch if kind == 0]
        rune_ids = [j for _, kind, j in stretch if kind == 1]
        if chat_ids and rune_ids:
            pairs.extend(
                _align([ticks[i] for i in chat_ids], [runes[j] for j in rune_ids], chat_ids)
            )
    return pairs


def _align(ticks: list[int], runes: list[Rune], chat_ids: list[int]) -> list[tuple[int, Rune]]:
    n, m = len(ticks), len(runes)
    gap = [[abs(tick - (rune.end_tick or 0)) for rune in runes] for tick in ticks]
    # best[i][j]: (pairs, -total gap) for the first i events and first j runes.
    best = [[(0, 0)] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            score = max(best[i - 1][j], best[i][j - 1])
            if gap[i - 1][j - 1] <= _MATCH_TICKS:
                count, cost = best[i - 1][j - 1]
                score = max(score, (count + 1, cost - gap[i - 1][j - 1]))
            best[i][j] = score
    pairs: list[tuple[int, Rune]] = []
    i, j = n, m
    while i and j:
        count, cost = best[i - 1][j - 1]
        if gap[i - 1][j - 1] <= _MATCH_TICKS and best[i][j] == (
            count + 1,
            cost - gap[i - 1][j - 1],
        ):
            pairs.append((chat_ids[i - 1], runes[j - 1]))
            i, j = i - 1, j - 1
        elif best[i][j] == best[i - 1][j]:
            i -= 1
        else:
            j -= 1
    return pairs

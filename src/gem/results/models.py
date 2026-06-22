"""Output data models for gem replay parsing.

Defines ``ParsedPlayer`` and ``ParsedMatch`` dataclasses that aggregate all
extracted information into a structured, ML-friendly output.

Reference: refs/parser/src/main/java/opendota/CreateParsedDataBlob.java
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from gem.combat.log import CombatLogEntry
from gem.extractors.courier import CourierSnapshot
from gem.extractors.draft import DraftEvent
from gem.extractors.objectives import (
    AegisEvent,
    BarracksKill,
    RoshanKill,
    ShrineKill,
    TormentorKill,
    TowerKill,
)
from gem.extractors.teamfights import OpenDotaTeamfight, Teamfight
from gem.extractors.wards import WardEvent


@dataclass
class VisionModifierEvent:
    """A vision-granting modifier applied to a hero (Slardar ulti, BH Track, Dust, Gem, etc.).

    Tracks the time window during which an enemy hero is revealed by a
    vision-granting ability or item. Used by ``estimate_vision`` to extend the
    geometry-based approximation with special-ability reveals.

    Attributes:
        tick: Game tick when the modifier was applied.
        end_tick: Game tick when the modifier was removed, or ``None`` if still
            active at game end or removal was not observed.
        modifier_name: Internal modifier name, e.g. ``"modifier_slardar_amplify_damage"``.
        target_name: NPC name of the hero who received the modifier (the revealed hero).
        caster_name: NPC name of the hero who applied the modifier.
        caster_team: Team of the caster (2=Radiant, 3=Dire), or 0 if unknown.
    """

    tick: int
    end_tick: int | None
    modifier_name: str
    target_name: str
    caster_name: str
    caster_team: int


@dataclass
class SmokeEvent:
    """One Smoke of Deceit activation.

    Attributes:
        tick: Game tick when the smoke item was consumed.
        activator: NPC hero name of the player who used the smoke.
        team: Team number (2=Radiant, 3=Dire), or 0 if unknown.
        smoked: NPC hero names of all heroes that received the buff.
        x: World x coordinate of the activating hero at activation tick,
            or ``None`` if position data is unavailable.
        y: World y coordinate of the activating hero at activation tick,
            or ``None`` if position data is unavailable.
    """

    tick: int
    activator: str
    team: int
    smoked: list[str] = field(default_factory=list)
    x: float | None = None
    y: float | None = None


@dataclass
class ChatEntry:
    """A single chat message from the match.

    Attributes:
        tick: Game tick when the message was sent.
        player_slot: Source player slot (0–9).
        channel: ``"all"`` for all-chat, ``"team"`` for team-chat, or raw channel type string.
        text: Message text.
    """

    tick: int
    player_slot: int
    channel: str
    text: str


@dataclass
class NeutralItemFoundEvent:
    """A neutral item found event emitted by DOTA_UM_FoundNeutralItem.

    Attributes:
        tick: Game tick when the event was observed.
        player_id: Player slot that found the neutral item.
        item_ability_id: Numeric item ability ID for the neutral item.
        item_key: Internal item key resolved from ``item_ability_id``.
        item_tier: Neutral tier reported by the replay message.
        tier_item_count: Number of found items in this tier reported by the message.
        enhancement_ability_id: Numeric item ability ID for the neutral enhancement.
        enhancement_key: Internal item key resolved from ``enhancement_ability_id``.
        enhancement_level: Enhancement level reported by the replay message.
        trinket_level: Trinket level reported by the replay message.
    """

    tick: int
    player_id: int
    item_ability_id: int
    item_key: str = ""
    item_tier: int = 0
    tier_item_count: int = 0
    enhancement_ability_id: int = -1
    enhancement_key: str = ""
    enhancement_level: int = 0
    trinket_level: int = 0


# ---------------------------------------------------------------------------
# Per-player aggregated output
# ---------------------------------------------------------------------------


@dataclass
class ParsedPlayer:
    """Aggregated statistics for one player over a full match.

    Attributes:
        player_id: Player slot (0–9; 0–4 Radiant, 5–9 Dire).
        hero_name: NPC hero name, e.g. ``"npc_dota_hero_axe"``.
        player_name: Steam persona name (nickname), e.g. ``"Ame"``.
        steam_id: 64-bit Steam ID (e.g. ``76561197986172872``), or 0 if unavailable.
        account_id: 32-bit Steam account ID (e.g. ``25907144``), or 0 if unavailable.
            Derived as ``steam_id - 76561197960265728``.
        team: Team number (2=Radiant, 3=Dire).
        times: Sample tick values (parallel to gold_t / lh_t / …).
            Default sampling is every 30 ticks (1 game-second).
        gold_t: Current unspent gold at each sample tick.
        total_earned_gold_t: Cumulative total earned gold at each sample tick
            (``m_iTotalEarnedGold``).
        net_worth_t: Net worth (gold + item value) at each sample tick.
        lh_t: Last-hit count at each sample tick.
        dn_t: Deny count at each sample tick.
        xp_t: Cumulative XP at each sample tick.
        times_min: Tick values at each game-minute boundary (OpenDota-aligned).
        gold_t_min: OpenDota-compatible cumulative earned gold at each
            game-minute boundary when interval data is available; legacy
            current-unspent-gold fallback on replays without complete intervals.
        total_earned_gold_t_min: Cumulative total earned gold at each game-minute boundary
            (``m_iTotalEarnedGold``). Used for ``radiant_gold_adv`` computation.
        total_earned_xp_t_min: Cumulative total earned XP at each game-minute boundary
            (``m_iTotalEarnedXP``). Used for ``radiant_xp_adv`` computation.
        net_worth_t_min: Net worth at each game-minute boundary.
        lh_t_min: Last-hit count at each game-minute boundary.
        dn_t_min: Deny count at each game-minute boundary.
        xp_t_min: Cumulative XP at each game-minute boundary.
        total_hero_damage_t_min: Cumulative hero-vs-hero damage dealt at each game-minute boundary.
        total_hero_healing_t_min: Cumulative healing dealt to allied heroes at each game-minute boundary.
        total_deaths_t_min: Cumulative death count at each game-minute boundary.
        total_stuns_t_min: Cumulative stun duration dealt (seconds) at each game-minute boundary.
        obs_log: Observer ward placement events for this player.
        sen_log: Sentry ward placement events for this player.
        damage: Total damage dealt, keyed by target NPC name, credited to the
            damage *source* (``damage_source_name``) so summon / spell /
            projectile damage lands on the owning hero. Illusion targets are keyed
            ``illusion_<npc>`` (OpenDota's ``computeIllusionString``); damage logged
            against an ability/modifier name rather than a real unit is excluded.
            Mirrors OpenDota's per-target ``damage`` reconstruction; the small
            residual is its engine-internal illusion split, not reproducible
            offline (see issue #68).
        damage_taken: Total damage received (non-illusion hero targets only),
            keyed by the damage source NPC name (``damage_source_name``),
            mirroring OpenDota's ``damage_taken`` dict.
        damage_by_type: Total damage dealt, keyed by damage type label
            (``"physical"``, ``"magical"``, ``"pure"``).
        damage_taken_by_type: Total damage received, keyed by damage type label
            (``"physical"``, ``"magical"``, ``"pure"``).
        healing: Total healing dealt, credited to the heal *source*, keyed by
            target NPC name (illusion targets keyed ``illusion_<npc>``).
        ability_uses: Ability usage counts, keyed by ability name.
        ability_upgrades_arr: Ability upgrade IDs in learned order, matching
            OpenDota's ``ability_upgrades_arr``.
        item_uses: Item usage counts, keyed by item name.
        final_items: End-of-game inventory by slot index, keyed item name with
            the ``item_`` prefix (e.g. ``{0: "item_power_treads"}``). Slots 0-5
            are the main inventory, 6-8 the backpack, 9-16 the stash. Occupied
            slots only; empty slots are absent. Read from the hero entity at the
            game-end tick. Mirrors OpenDota's ``item_0``–``item_5`` /
            ``backpack_0``–``backpack_2`` / ``item_neutral`` (which use numeric
            item IDs rather than names).
        gold_reasons: Gold received per reason code.
        xp_reasons: XP received per reason code.
        kills_log: Combat log DEATH entries where this player was the attacker.
        purchase_log: PURCHASE combat log entries for this player.
        runes_log: ITEM combat log entries for rune pickups.
        buyback_log: BUYBACK combat log entries for this player.
        lane_pos: Dwell-tick counts keyed by ``"x_y"`` grid cell (64-unit resolution).
        position_log: Time-ordered ``(tick, x, y)`` tuples sampled at the
            extractor's interval. Useful for movement time-series and
            animated visualisations.
        stuns_dealt: Total stun duration dealt (seconds) accumulated from combat log.
        kills: Kill count from server scoreboard (``m_iKills``). Correctly accounts
            for reincarnation, summon kills, and all edge cases.
        deaths: Death count from server scoreboard (``m_iDeaths``).
        assists: Assist count from server scoreboard (``m_iAssists``).
        lane_role: Lane role inferred from the first-10-minute position heatmap.
            1=safe lane, 2=mid, 3=off lane, 4=jungle, 5=roaming, 0=unknown.
        lane_last_hits: Last-hit count at the 10-minute mark (``lh_t_min[10]``).
        lane_denies: Deny count at the 10-minute mark (``dn_t_min[10]``).
        lane_total_gold: Cumulative total earned gold at the 10-minute mark
            (``total_earned_gold_t_min[10]``).
        lane_total_xp: Cumulative total earned XP at the 10-minute mark
            (``total_earned_xp_t_min[10]``).
        lane_efficiency_pct: Tier-1 laning metric (OpenDota formula).
            ``floor(lane_total_gold / 4948 * 100)``. The denominator 4948 is the
            theoretical gold available from lane creeps + passive income + starting
            gold over 10 minutes. Values above 100 are normal for heroes with kills.
        lane_gold_adv: Tier-2 laning metric. Gold advantage at 10 minutes versus
            lane opponents on the opposing team (``lane_total_gold`` minus the sum
            of opponents' ``lane_total_gold``). Positive = ahead. ``None`` when no
            opponent with a matching lane role exists.
        lane_xp_adv: Tier-2 laning metric. XP advantage at 10 minutes versus
            lane opponents on the opposing team. Same pairing logic as
            ``lane_gold_adv``.
        net_worth: End-of-game net worth (gold + item value), the last dense
            sample (``net_worth_t[-1]``). Matches OpenDota's terminal
            ``net_worth`` scalar. Convenience accessor so callers need not index
            the series; ``0`` if no samples were collected.
        last_hits: End-of-game last-hit count, the last dense sample
            (``lh_t[-1]``). Matches OpenDota's terminal ``last_hits`` scalar.
        denies: End-of-game deny count, the last dense sample (``dn_t[-1]``).
            Matches OpenDota's terminal ``denies`` scalar.
        camps_stacked: Neutral camps stacked over the match (``m_iCampsStacked``).
            Matches OpenDota's ``camps_stacked``.
        creeps_stacked: Neutral creeps stacked over the match
            (``m_iCreepsStacked``). Matches OpenDota's ``creeps_stacked``.
        obs_placed: Observer wards placed (``m_iObserverWardsPlaced``). Matches
            OpenDota's ``obs_placed``.
        sen_placed: Sentry wards placed (``m_iSentryWardsPlaced``). Matches
            OpenDota's ``sen_placed``.
        rune_pickups: Runes picked up (``m_iRunePickups``). Matches OpenDota's
            ``rune_pickups``.
        tower_kills: Towers this player last-hit (``m_iTowerKills``). Matches
            OpenDota's per-player ``tower_kills``.
        killed: Kills per target unit name, derived from ``kills_log`` (summon
            kills credited to the owner). Mirrors OpenDota's ``killed`` map.
        ancient_kills: Ancient-neutral creeps killed (from ``killed``).
        neutral_kills: All neutral creeps killed, including ancients.
        lane_kills: Lane creeps killed (whole game, not just the laning phase).
        courier_kills: Couriers killed.
        observer_kills: Observer wards killed.
        sentry_kills: Sentry wards killed.
        roshan_kills: Roshans last-hit by this player. Derived from ``kills_log``
            (combat-log attributed), matching OpenDota's ``roshan_kills`` rather
            than the unreliable ``m_iRoshanKills`` entity counter.
        kda: OpenDota KDA ratio, ``round((kills + assists) / (deaths + 1), 2)``.
            Note the ``+1`` denominator (not ``max(deaths, 1)``) and 2-decimal
            rounding; matches OpenDota's ``kda`` exactly.
        buyback_count: Number of buybacks used (``len(buyback_log)``). Matches
            OpenDota's ``buyback_count``.
        is_radiant: True if the player is on Radiant (team 2). Matches OpenDota's
            ``isRadiant``.
        win: ``1`` if this player's team won, else ``0`` (also ``0`` when the
            match winner is unknown). Matches OpenDota's ``win``.
        kills_per_min: Kills divided by match duration in minutes
            (``kills / (ParsedMatch.duration / 60)``). Unrounded float matching
            OpenDota's ``kills_per_min``. ``0.0`` when duration is unknown.
        hero_damage: Damage dealt to enemy heroes, reconstructed from the combat
            log by crediting the damage source (``damage_source_name``) to
            non-illusion hero targets. Best-effort offline estimate (~90% vs
            OpenDota across fixtures). The residual is **not** a filter gap:
            OpenDota's headline ``hero_damage`` is a Game-Coordinator
            (``CMsgGameMatchSignOut``) value that accounts for in-engine
            mitigation the combat log cannot see, so it is unclosable offline.
            Overwritten with the exact API value by
            :func:`gem.replays.fetch.apply_api_rates`.
        tower_damage: Damage dealt to building structures (towers, barracks,
            fort/ancient), reconstructed from the combat log by damage source.
            Essentially exact offline (~99.97% vs OpenDota — the building sum
            equals the GC value); refreshed exactly via ``apply_api_rates``.
        hero_healing: Healing given to allied heroes (excluding self-heal),
            credited to the heal source, from the combat log. Best-effort offline
            estimate; OpenDota's headline value is GC-sourced (self-heal-excluded,
            mitigation-aware) and exact via ``apply_api_rates``.
        gold_per_min: Gold per minute. NOT derivable from the replay — sourced
            from the Steam GC / OpenDota match API. ``0`` until populated by
            :func:`gem.replays.fetch.enrich_with_api_rates`. See
            ``opendota-gpm-is-steam-api`` (the team-data earned-gold counter is a
            different quantity and does not match OpenDota's value).
        xp_per_min: XP per minute. Same API provenance as ``gold_per_min``;
            ``0`` until enriched.
        total_gold: Total gold, ``floor(gold_per_min * duration / 60)`` (OpenDota's
            own formula). ``0`` until ``gold_per_min`` is enriched.
        total_xp: Total XP, ``floor(xp_per_min * duration / 60)``. ``0`` until
            ``xp_per_min`` is enriched.
    """

    player_id: int
    hero_name: str = ""
    player_name: str = ""
    steam_id: int = 0
    account_id: int = 0
    team: int = 0
    times: list[int] = field(default_factory=list)
    gold_t: list[int] = field(default_factory=list)
    total_earned_gold_t: list[int] = field(default_factory=list)
    net_worth_t: list[int] = field(default_factory=list)
    lh_t: list[int] = field(default_factory=list)
    dn_t: list[int] = field(default_factory=list)
    xp_t: list[int] = field(default_factory=list)
    times_min: list[int] = field(default_factory=list)
    gold_t_min: list[int] = field(default_factory=list)
    total_earned_gold_t_min: list[int] = field(default_factory=list)
    total_earned_xp_t_min: list[int] = field(default_factory=list)
    net_worth_t_min: list[int] = field(default_factory=list)
    lh_t_min: list[int] = field(default_factory=list)
    dn_t_min: list[int] = field(default_factory=list)
    xp_t_min: list[int] = field(default_factory=list)
    total_hero_damage_t_min: list[int] = field(default_factory=list)
    total_hero_healing_t_min: list[int] = field(default_factory=list)
    total_deaths_t_min: list[int] = field(default_factory=list)
    total_stuns_t_min: list[float] = field(default_factory=list)
    obs_log: list[WardEvent] = field(default_factory=list)
    sen_log: list[WardEvent] = field(default_factory=list)
    damage: dict[str, int] = field(default_factory=dict)
    damage_taken: dict[str, int] = field(default_factory=dict)
    damage_by_type: dict[str, int] = field(default_factory=dict)
    damage_taken_by_type: dict[str, int] = field(default_factory=dict)
    healing: dict[str, int] = field(default_factory=dict)
    ability_uses: dict[str, int] = field(default_factory=dict)
    ability_upgrades_arr: list[int] = field(default_factory=list)
    item_uses: dict[str, int] = field(default_factory=dict)
    final_items: dict[int, str] = field(default_factory=dict)
    gold_reasons: dict[str, int] = field(default_factory=dict)
    xp_reasons: dict[str, int] = field(default_factory=dict)
    kills_log: list[CombatLogEntry] = field(default_factory=list)
    purchase_log: list[CombatLogEntry] = field(default_factory=list)
    runes_log: list[CombatLogEntry] = field(default_factory=list)
    buyback_log: list[CombatLogEntry] = field(default_factory=list)
    lane_pos: defaultdict[str, int] = field(default_factory=lambda: defaultdict(int))
    position_log: list[tuple[int, float, float]] = field(default_factory=list)
    stuns_dealt: float = 0.0
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    lane_role: int = 0
    lane_last_hits: int = 0
    lane_denies: int = 0
    lane_total_gold: int = 0
    lane_total_xp: int = 0
    lane_efficiency_pct: int = 0
    lane_gold_adv: int | None = None
    lane_xp_adv: int | None = None
    net_worth: int = 0
    last_hits: int = 0
    denies: int = 0
    camps_stacked: int = 0
    creeps_stacked: int = 0
    obs_placed: int = 0
    sen_placed: int = 0
    rune_pickups: int = 0
    tower_kills: int = 0
    kda: float = 0.0
    buyback_count: int = 0
    is_radiant: bool = False
    win: int = 0
    kills_per_min: float = 0.0
    hero_damage: int = 0
    tower_damage: int = 0
    hero_healing: int = 0
    gold_per_min: int = 0
    xp_per_min: int = 0
    total_gold: int = 0
    total_xp: int = 0
    # Derived kill aggregates (reshaped from kills_log; summon kills credited).
    killed: dict[str, int] = field(default_factory=dict)
    ancient_kills: int = 0
    neutral_kills: int = 0
    lane_kills: int = 0
    courier_kills: int = 0
    observer_kills: int = 0
    sentry_kills: int = 0
    roshan_kills: int = 0
    _ability_snapshots: list[tuple[int, dict[str, int]]] = field(default_factory=list)

    def __repr__(self) -> str:
        hero = self.hero_name.removeprefix("npc_dota_hero_") if self.hero_name else "unknown"
        team = "Radiant" if self.team == 2 else "Dire" if self.team == 3 else f"team={self.team}"
        return (
            f"ParsedPlayer(slot={self.player_id}, hero={hero}, team={team}, "
            f"kda={self.kills}/{self.deaths}/{self.assists}, net_worth={self.net_worth})"
        )


# ---------------------------------------------------------------------------
# Match-level aggregated output
# ---------------------------------------------------------------------------


@dataclass
class ParsedMatch:
    """Top-level parsed output for a single Dota 2 replay.

    Attributes:
        match_id: Dota 2 match ID, or 0 if unavailable.
        game_mode: Game mode integer (e.g. 22 = All Pick Ranked).
        leagueid: League ID, or 0 for non-league matches.
        radiant_win: True if Radiant won, False if Dire won, None if unknown.
        radiant_team_id: Radiant tournament team ID (e.g. ``8261500``), or 0 for pub games.
            Matches the OpenDota ``/teams/{id}`` URL.
        radiant_team_name: Radiant team name (e.g. ``"Xtreme Gaming"``), or empty string.
        radiant_team_tag: Radiant team tag (e.g. ``"XG"``), or empty string.
        dire_team_id: Dire tournament team ID, or 0 for pub games.
        dire_team_name: Dire team name (e.g. ``"Team Falcons"``), or empty string.
        dire_team_tag: Dire team tag (e.g. ``"FLCN"``), or empty string.
        players: One ``ParsedPlayer`` per player slot (index 0–9).
        towers: All tower kill events in chronological order.
        barracks: All barracks kill events in chronological order.
        roshans: All Roshan kill events in chronological order.
        aegis_events: All Aegis pickup / steal / denial events.
        tormentors: All Tormentor (miniboss) kill events in chronological order.
        shrines: All Shrine of Wisdom destruction events in chronological order.
        wards: All ward placement events with coordinates.
        radiant_gold_adv: Radiant gold advantage at each minute boundary.
        radiant_xp_adv: Radiant XP advantage at each minute boundary.
        combat_log: All raw combat log entries (unfiltered).
        chat: All chat messages in chronological order.
        courier_snapshots: Courier state snapshots at each sample interval.
        neutral_item_finds: Neutral item find events from ``DOTA_UM_FoundNeutralItem``.
        smoke_events: All Smoke of Deceit activations with grouped heroes and
            approximate activating-hero position.
        draft: Hero pick and ban events from the draft phase.
        teamfights: All detected teamfight windows with per-player breakdowns.
        opendota_teamfights: OpenDota-compatible temporal teamfight windows.
            These use OpenDota's 15-second death-window grouping and 3+ death
            filter, while ``teamfights`` keeps Gem's richer spatial detector.
        vision_modifiers: Vision-granting modifier events (Slardar Corrosive Haze,
            Bounty Hunter Track, Dust of Appearance, Gem of True Sight, etc.).
            Used by ``estimate_vision`` to detect reveals beyond geometry.
        game_start_tick: Absolute tick when the game clock started (creeps spawn).
            ``None`` if the transition was not observed.
        game_end_tick: Absolute tick of the final parser tick.
        duration: OpenDota-style match duration in seconds — the horn-anchored
            combat-log time at GAME_STATE==6 (ancient destroyed). Matches
            OpenDota's ``duration`` to within ~1s (sub-second rounding). ``0`` if
            the postGame transition was not observed. Distinct from the
            tick-derived ``duration_seconds`` property, which spans the raw parser
            ticks and includes pre/post-game time.
    """

    match_id: int = 0
    game_mode: int = 0
    leagueid: int = 0
    radiant_win: bool | None = None
    radiant_team_id: int = 0
    radiant_team_name: str = ""
    radiant_team_tag: str = ""
    dire_team_id: int = 0
    dire_team_name: str = ""
    dire_team_tag: str = ""
    game_start_tick: int | None = None
    game_end_tick: int = 0
    duration: int = 0
    players: list[ParsedPlayer] = field(
        default_factory=lambda: [ParsedPlayer(player_id=i) for i in range(10)]
    )
    towers: list[TowerKill] = field(default_factory=list)
    barracks: list[BarracksKill] = field(default_factory=list)
    roshans: list[RoshanKill] = field(default_factory=list)
    aegis_events: list[AegisEvent] = field(default_factory=list)
    tormentors: list[TormentorKill] = field(default_factory=list)
    shrines: list[ShrineKill] = field(default_factory=list)
    wards: list[WardEvent] = field(default_factory=list)
    radiant_gold_adv: list[int] = field(default_factory=list)
    radiant_xp_adv: list[int] = field(default_factory=list)
    combat_log: list[CombatLogEntry] = field(default_factory=list)
    chat: list[ChatEntry] = field(default_factory=list)
    courier_snapshots: list[CourierSnapshot] = field(default_factory=list)
    neutral_item_finds: list[NeutralItemFoundEvent] = field(default_factory=list)
    smoke_events: list[SmokeEvent] = field(default_factory=list)
    draft: list[DraftEvent] = field(default_factory=list)
    teamfights: list[Teamfight] = field(default_factory=list)
    opendota_teamfights: list[OpenDotaTeamfight] = field(default_factory=list)
    vision_modifiers: list[VisionModifierEvent] = field(default_factory=list)

    @property
    def duration_seconds(self) -> float:
        """Game duration in seconds, derived from ``game_start_tick`` and ``game_end_tick``."""
        start = self.game_start_tick or 0
        return max(self.game_end_tick - start, 0) / 30.0

    @property
    def duration_minutes(self) -> float:
        """Game duration in minutes, derived from ``game_start_tick`` and ``game_end_tick``."""
        return self.duration_seconds / 60.0

    def __repr__(self) -> str:
        winner = "Radiant" if self.radiant_win else "Dire" if self.radiant_win is False else "?"
        duration_min = (
            round(max(pp.times[-1] for pp in self.players if pp.times) / 30 / 60)
            if any(pp.times for pp in self.players)
            else 0
        )
        return (
            f"ParsedMatch(match_id={self.match_id}, winner={winner}, "
            f"duration=~{duration_min}min, players={len(self.players)})"
        )

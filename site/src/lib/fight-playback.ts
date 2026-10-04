/**
 * The data side of Figure 3's playback: hero state at a moment, what is active
 * then, the feed's rows and the damage strip. It reads `src/data/fight.json`
 * (written by scripts/export_site_home_data.py from gem.build_fight_timeline).
 *
 * Positions, HP and mana are sampled about once a second and interpolated
 * between samples, for display only. Every `t` is seconds since the fight
 * window started.
 */

/** A sample: t, map-square x and y, HP, max HP, mana, max mana. */
export type StateSample = [number, number, number, number, number, number, number];

export interface PlaybackHero {
  hero: string;
  icon: string;
  team: string;
  /** Sample runs in time order, each broken at a teleport or respawn. */
  runs: StateSample[][];
}

/** A hit: hero index, damage, damage type ("" when it only debuffed), stun seconds. */
export type Hit = [number, number, string, number];

export interface Cast {
  t: number;
  by: number;
  what: string;
  /** Item icon name, for an item. */
  item?: string;
  /** Hero index of the recorded target, when it is a hero. */
  target?: number;
  /** Name of the recorded target, when it is not a hero. */
  unit?: string;
  /** The cast affected (or targeted) the caster. */
  self?: boolean;
  hits: Hit[];
}

export interface Death {
  t: number;
  victim: number;
  killer: number | null;
  killer_name: string;
  aegis: boolean;
  gold_lost: number;
  gold: [number, number][];
  xp: [number, number][];
  /** The largest damage sources in the 10 s before: attacker, source, type, damage. */
  recent: [string, string, string, number][];
  /** All damage taken in those 10 s (every source, not only the rows). */
  recent_total: number;
  /**
   * The heroes that died on the same tick, when more than one did. Their shared
   * gold and XP are on the first of them only.
   */
  tick_victims?: number[];
}

export type ModifierKind = "disable" | "debuff" | "buff";
export type Modifier = [number, number, number, number | null, string, ModifierKind, string | null, number];

export interface FightData {
  start: string;
  /** The start in game seconds (``start`` is whole seconds). */
  start_s: number;
  duration: number;
  heroes: PlaybackHero[];
  casts: Cast[];
  /** t, attacker, target, damage, type, 1 when dealt by the hero itself, source ("Attack" for a right-click). */
  damage: [number, number, number, number, string, number, string][];
  /**
   * Modifiers on heroes: t, until (the removal, or the playback's end), target,
   * source hero or null, name, kind, the ring a buff is drawn with (or null), and
   * the duration it was applied with (a death or dispel can end it sooner).
   */
  modifiers: Modifier[];
  deaths: Death[];
  /** t, hero, cost. */
  buybacks: [number, number, number][];
  /**
   * Smokes on the heroes: team, when it was used (null before the playback), and
   * each member: hero, smoked from, smoke broke (null: still on at the end), and
   * when the enemy saw the hero as it broke (null: not within a second).
   */
  smokes: [string, number | null, [number, number, number | null, number | null][]][];
  /** hero, from, to: while the enemy team couldn't see the hero (replay visibility). */
  hidden: [number, number, number][];
}

/** The latest-started modifier of a kind on the hero at t (a disable, a ringed buff, …). */
export function activeModifier(
  data: FightData,
  hero: number,
  t: number,
  match: (m: Modifier) => boolean,
): Modifier | undefined {
  let found: Modifier | undefined;
  for (const m of data.modifiers) {
    if (m[2] === hero && m[0] <= t && t < m[1] && match(m) && (!found || m[0] >= found[0])) found = m;
  }
  return found;
}

/** Whether the hero was smoked at t. */
export function isSmoked(data: FightData, hero: number, t: number): boolean {
  return data.smokes.some(([, , members]) =>
    members.some(([h, from, broke]) => h === hero && from <= t && (broke === null || t < broke)),
  );
}

/** Whether the enemy team couldn't see the hero at t. */
export function isHidden(data: FightData, hero: number, t: number): boolean {
  return data.hidden.some(([h, from, to]) => h === hero && from <= t && t < to);
}

/** Items whose use the feed and map leave out: toggles and sips, not plays. */
export const QUIET_ITEMS = new Set(["power_treads", "phase_boots", "bottle", "magic_wand"]);

/** How long a hero stays at its last sample after a run ends (about one sample gap). */
export const HOLD_S = 1.5;

export interface HeroState {
  x: number;
  y: number;
  hp: number;
  maxHp: number;
  mana: number;
  maxMana: number;
}

/** When each hero died (Aegis deaths aside), by hero index. */
export function deathTimes(data: FightData): number[][] {
  const out = data.heroes.map(() => [] as number[]);
  for (const death of data.deaths) if (!death.aegis) out[death.victim].push(death.t);
  return out;
}

function lerp(a: number, b: number, k: number): number {
  return a + (b - a) * k;
}

/**
 * The hero's state at t, or null while it is dead or has no sample around t.
 * A hero is dead from its death until a new run (its respawn or buyback) starts.
 */
export function stateAt(hero: PlaybackHero, deaths: number[], t: number): HeroState | null {
  const died = deaths.filter((d) => d <= t).at(-1);
  if (died !== undefined && !hero.runs.some((run) => run[0][0] > died && run[0][0] <= t)) return null;
  const run = hero.runs.find((r) => r[0][0] <= t && t <= r[r.length - 1][0]);
  let sample: number[] | undefined;
  if (run) {
    const i = run.findIndex((s) => s[0] >= t);
    const b = run[i];
    const a = run[Math.max(0, i - 1)];
    const k = b[0] === a[0] ? 0 : (t - a[0]) / (b[0] - a[0]);
    sample = a.map((v, j) => lerp(v, b[j], k));
  } else {
    const ended = hero.runs.filter((r) => r[r.length - 1][0] < t && t - r[r.length - 1][0] <= HOLD_S).at(-1);
    sample = ended?.[ended.length - 1];
  }
  if (!sample) return null;
  return { x: sample[1], y: sample[2], hp: sample[3], maxHp: sample[4], mana: sample[5], maxMana: sample[6] };
}

/** The structured pieces of a cast's feed row, so the row and its text agree. */
export interface CastHit {
  hero: number;
  damage: number;
  type: string;
  stun: number;
}

export interface CastParts {
  /** Enemies the cast damaged or debuffed. */
  hits: CastHit[];
  /** Allies it reached (a buff, a save): "on" rather than "hit". */
  allies: CastHit[];
  /** A damage type shared by every damaging hit, shown once at the end. */
  sharedType: string | null;
  /** Total damage to enemies. */
  damage: number;
}

/** A cast's hits, split into enemies and allies of the caster (`teams` by hero index). */
export function castParts(cast: Cast, teams: string[]): CastParts {
  const all = cast.hits.map(([hero, damage, type, stun]) => ({ hero, damage, type, stun }));
  const hits = all.filter((h) => teams[h.hero] !== teams[cast.by]);
  const allies = all.filter((h) => teams[h.hero] === teams[cast.by]);
  const types = new Set(hits.filter((h) => h.damage > 0).map((h) => h.type));
  return {
    hits,
    allies,
    sharedType: types.size === 1 ? [...types][0] : null,
    damage: hits.reduce((sum, h) => sum + h.damage, 0),
  };
}

/** A cast as one line of text: "Avalanche hit Lion 312 · Pangolier 298 magical". */
export function castText(cast: Cast, names: string[], teams: string[]): string {
  const parts = castParts(cast, teams);
  let text = cast.what;
  if (cast.target !== undefined && !cast.hits.some(([hero]) => hero === cast.target)) {
    text += ` on ${names[cast.target]}`;
  } else if (cast.unit) {
    text += ` on ${cast.unit}`;
  } else if (cast.self && !cast.hits.length) {
    text += " on self";
  }
  if (parts.allies.length) text += ` on ${parts.allies.map((h) => names[h.hero]).join(", ")}`;
  if (parts.hits.length) {
    const hits = parts.hits.map((h) => {
      let hit = names[h.hero];
      if (h.damage) hit += ` ${h.damage}`;
      if (h.damage && !parts.sharedType && h.type) hit += ` ${h.type}`;
      return hit;
    });
    text += ` hit ${hits.join(" · ")}`;
    if (parts.sharedType && parts.sharedType !== "others") text += ` ${parts.sharedType}`;
  }
  return text;
}

/**
 * The buyback that followed a death: the hero's first buyback after it and before
 * its next death. None for an Aegis death, which needs no buyback.
 */
export function buybackAfter(data: FightData, death: Death): FightData["buybacks"][number] | undefined {
  if (death.aegis) return undefined;
  const next = data.deaths.find((d) => d.victim === death.victim && !d.aegis && d.t > death.t)?.t ?? Infinity;
  return data.buybacks.find(([t, hero]) => hero === death.victim && t >= death.t && t < next);
}

/** Damage dealt per whole second of the fight, by team: the strip under the map. */
export function damagePerSecond(data: FightData): { radiant: number[]; dire: number[] } {
  const n = Math.max(1, Math.ceil(data.duration));
  const out = { radiant: new Array<number>(n).fill(0), dire: new Array<number>(n).fill(0) };
  for (const [t, by, , damage] of data.damage) {
    const team = data.heroes[by]?.team;
    if (team === "radiant" || team === "dire") out[team][Math.min(n - 1, Math.max(0, Math.floor(t)))] += damage;
  }
  return out;
}

/** The feed's row kinds. */
export type RowKind = "death" | "buyback" | "spell" | "item" | "disable" | "debuff" | "buff" | "smoke" | "attack";

/** The feed's filter chips, and the row kinds each shows. */
export const FILTERS: { key: string; label: string; kinds: RowKind[]; on: boolean }[] = [
  { key: "deaths", label: "Deaths", kinds: ["death", "buyback"], on: true },
  { key: "spells", label: "Spells", kinds: ["spell"], on: true },
  { key: "items", label: "Items", kinds: ["item"], on: true },
  { key: "disables", label: "Disables", kinds: ["disable"], on: true },
  { key: "debuffs", label: "Debuffs", kinds: ["debuff"], on: true },
  { key: "buffs", label: "Buffs & smoke", kinds: ["buff", "smoke"], on: true },
  { key: "attacks", label: "Attacks", kinds: ["attack"], on: true },
];

export interface Row {
  t: number;
  kind: RowKind;
  /** Heroes the row involves, for following a hero. */
  heroes: number[];
  cast?: Cast;
  death?: Death;
  buyback?: FightData["buybacks"][number];
  /** A disable, debuff or buff from one source on one or more heroes. */
  effect?: { source: number | null; name: string; targets: { hero: number; seconds: number }[] };
  /** Right-click damage from one hero to another in one second. */
  attack?: { by: number; target: number; damage: number; type: string };
  /** A hero's smoke breaking, and whether the enemy saw it then. */
  smokeBreak?: { hero: number; seen: boolean };
}

/** Effects that start within this long of each other, from one source, share a row. */
const EFFECT_GROUP_S = 0.5;
/** A self-buff landing within this long after its cast (Shield Crash lands after the leap) says that cast. */
const SELF_BUFF_FOLD_S = 1.5;

/**
 * The feed's rows in time order. Disables, debuffs and buffs get rows of their
 * own: one per source and effect at a moment, listing every hero it reached; a
 * re-application while the same effect is still on (a slow refreshed by each
 * attack) extends it rather than adding a row. Right-click damage is summed per
 * attacker and target over each second.
 */
export function feedRows(data: FightData): Row[] {
  const rows: Row[] = [];
  const effectRows: Row[] = [];
  const on = new Map<string, number>(); // source|name|target -> until, for refreshes
  const open = new Map<string, Row>(); // source|name|kind -> the row being filled
  for (const [t, until, target, source, name, kind, , applied] of [...data.modifiers].sort((a, b) => a[0] - b[0])) {
    const effect = `${source}|${name}|${target}`;
    const still = on.get(effect);
    on.set(effect, Math.max(until, still ?? until));
    if (still !== undefined && t <= still + EFFECT_GROUP_S) continue;
    const key = `${source}|${name}|${kind}`;
    const row = open.get(key);
    const seconds = applied > 0 ? applied : Math.round((until - t) * 10) / 10;
    if (row && t - row.t <= EFFECT_GROUP_S) {
      if (!row.effect!.targets.some((x) => x.hero === target)) {
        row.effect!.targets.push({ hero: target, seconds });
        row.heroes.push(target);
      }
      continue;
    }
    const next: Row = {
      t,
      kind,
      heroes: source === null || source === target ? [target] : [source, target],
      effect: { source, name, targets: [{ hero: target, seconds }] },
    };
    open.set(key, next);
    effectRows.push(next);
  }
  rows.push(...effectRows);
  // A cast that only buffed its caster (Black King Bar, Feast of Souls) is said by
  // its buff row, which also has the duration.
  const saidByBuff = (cast: Cast) =>
    cast.self &&
    !cast.hits.length &&
    cast.target === undefined &&
    effectRows.some(
      (r) =>
        r.kind === "buff" &&
        r.effect!.source === cast.by &&
        r.effect!.name === cast.what &&
        r.effect!.targets.length === 1 &&
        r.effect!.targets[0].hero === cast.by &&
        r.t >= cast.t - EFFECT_GROUP_S &&
        r.t - cast.t <= SELF_BUFF_FOLD_S,
    );
  for (const cast of data.casts) {
    if ((cast.item && QUIET_ITEMS.has(cast.item)) || saidByBuff(cast)) continue;
    rows.push({ t: cast.t, kind: cast.item ? "item" : "spell", heroes: castHeroes(cast), cast });
  }
  for (const death of data.deaths) {
    rows.push({ t: death.t, kind: "death", heroes: [death.victim, ...(death.killer === null ? [] : [death.killer])], death });
  }
  for (const buyback of data.buybacks) rows.push({ t: buyback[0], kind: "buyback", heroes: [buyback[1]], buyback });
  for (const [, , members] of data.smokes) {
    for (const [hero, , broke, seen] of members) {
      if (broke !== null) rows.push({ t: broke, kind: "smoke", heroes: [hero], smokeBreak: { hero, seen: seen !== null } });
    }
  }
  const attacks = new Map<string, Row>();
  for (const [t, by, target, damage, type, direct, source] of data.damage) {
    if (source !== "Attack" || !direct) continue;
    const key = `${Math.floor(t)}:${by}:${target}`;
    const row = attacks.get(key);
    if (row) row.attack!.damage += damage;
    else attacks.set(key, { t, kind: "attack", heroes: [by, target], attack: { by, target, damage, type } });
  }
  rows.push(...attacks.values());
  return rows.sort((a, b) => a.t - b.t);
}

/** Whether a row shows: a filter that covers its kind is on, and it involves the followed hero (if any). */
export function rowShows(row: Row, on: Set<string>, follow: number | null): boolean {
  const filter = FILTERS.find((f) => f.kinds.includes(row.kind));
  return !!filter && on.has(filter.key) && (follow === null || row.heroes.includes(follow));
}

/** The heroes a cast involves: its caster, recorded target and hits. */
export function castHeroes(cast: Cast): number[] {
  return [cast.by, ...(cast.target !== undefined ? [cast.target] : []), ...cast.hits.map(([hero]) => hero)];
}

/** A start ("42:34", or game seconds) plus t seconds, as "mm:ss". */
export function clockAt(start: string | number, t: number): string {
  const base = typeof start === "number" ? start : start.split(":").reduce((m, s) => Number(m) * 60 + Number(s), 0);
  const total = Math.max(0, Math.floor(base + t + 1e-6));
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

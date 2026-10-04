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
  /** Damage taken in the 10 s before: attacker, source, type, damage. */
  recent: [string, string, string, number][];
}

export interface FightData {
  start: string;
  duration: number;
  heroes: PlaybackHero[];
  casts: Cast[];
  /** t, attacker, target, damage, type, 1 when dealt by the hero itself, source ("Attack" for a right-click). */
  damage: [number, number, number, number, string, number, string][];
  /** t, target, source hero or null, name, seconds. */
  disables: [number, number, number | null, string, number][];
  /** t, until, hero, kind. */
  buffs: [number, number, number, string][];
  deaths: Death[];
  /** t, hero, cost. */
  buybacks: [number, number, number][];
}

/** Items whose use the feed and map leave out: toggles and sips, not plays. */
export const QUIET_ITEMS = new Set(["power_treads", "phase_boots", "bottle", "magic_wand"]);

/** Stuns shorter than this (a ministun, or one tick of a repeating stun) aren't shown. */
export const MIN_STUN_S = 0.2;

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
      if (h.stun >= MIN_STUN_S) hit += ` (${h.stun}s stun)`;
      return hit;
    });
    text += ` hit ${hits.join(" · ")}`;
    if (parts.sharedType && parts.sharedType !== "others") text += ` ${parts.sharedType}`;
  }
  return text;
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
export type RowKind = "death" | "buyback" | "spell" | "item" | "disable" | "buff" | "attack";

/** The feed's filter chips, and the row kinds each shows. */
export const FILTERS: { key: string; label: string; kinds: RowKind[]; on: boolean }[] = [
  { key: "deaths", label: "Deaths", kinds: ["death", "buyback"], on: true },
  { key: "spells", label: "Spells", kinds: ["spell"], on: true },
  { key: "items", label: "Items", kinds: ["item"], on: true },
  { key: "disables", label: "Disables", kinds: ["disable"], on: true },
  { key: "buffs", label: "Buffs", kinds: ["buff"], on: true },
  { key: "attacks", label: "Attacks", kinds: ["attack"], on: false },
];

export interface Row {
  t: number;
  kind: RowKind;
  /** Heroes the row involves, for following a hero. */
  heroes: number[];
  cast?: Cast;
  /** How long the buff a cast gave its caster lasted, in seconds. */
  lasted?: number;
  death?: Death;
  buyback?: FightData["buybacks"][number];
  disable?: FightData["disables"][number];
  buff?: FightData["buffs"][number];
  /** Right-click damage from one hero to another in one second. */
  attack?: { by: number; target: number; damage: number; type: string };
}

/** The items that give each buff ring (export_site_home_data.BUFF_RINGS), so a buff folds into its own cast. */
export const BUFF_ITEMS: Record<string, string[]> = {
  bkb: ["black_king_bar", "minotaur_horn"],
  ghost: ["ghost"],
  blade_mail: ["blade_mail"],
  lotus: ["lotus_orb"],
  satanic: ["satanic"],
};

/** Seconds within which a disable or buff is the cast's own (it is folded into the cast's row). */
const CAST_WINDOW_S = 3;

/**
 * The feed's rows in time order. A disable a cast's hits already show, and a
 * buff a cast gave its caster, fold into the cast's row; right-click damage is
 * summed per attacker and target over each second.
 */
export function feedRows(data: FightData): Row[] {
  const rows: Row[] = [];
  const usedBuffs = new Set<number>();
  for (const cast of data.casts) {
    if (cast.item && QUIET_ITEMS.has(cast.item)) continue;
    const row: Row = { t: cast.t, kind: cast.item ? "item" : "spell", heroes: castHeroes(cast), cast };
    if (cast.self && cast.item) {
      const item = cast.item;
      const i = data.buffs.findIndex(
        ([t, , hero, kind], j) =>
          !usedBuffs.has(j) && hero === cast.by && BUFF_ITEMS[kind]?.includes(item) && Math.abs(t - cast.t) <= 0.5,
      );
      if (i >= 0) {
        usedBuffs.add(i);
        row.lasted = Math.round((data.buffs[i][1] - data.buffs[i][0]) * 10) / 10;
      }
    }
    rows.push(row);
  }
  data.buffs.forEach((buff, i) => {
    if (!usedBuffs.has(i)) rows.push({ t: buff[0], kind: "buff", heroes: [buff[2]], buff });
  });
  for (const disable of data.disables) {
    const [t, target, source] = disable;
    const shown = data.casts.some(
      (cast) =>
        cast.by === source &&
        cast.t <= t &&
        t - cast.t <= CAST_WINDOW_S &&
        cast.hits.some(([hero, , , stun]) => hero === target && stun > 0),
    );
    if (!shown) rows.push({ t, kind: "disable", heroes: source === null ? [target] : [target, source], disable });
  }
  for (const death of data.deaths) {
    rows.push({ t: death.t, kind: "death", heroes: [death.victim, ...(death.killer === null ? [] : [death.killer])], death });
  }
  for (const buyback of data.buybacks) rows.push({ t: buyback[0], kind: "buyback", heroes: [buyback[1]], buyback });
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

/** "42:34" plus t seconds, as "mm:ss". */
export function clockAt(start: string, t: number): string {
  const [m, s] = start.split(":").map(Number);
  const total = Math.max(0, Math.floor(m * 60 + s + t));
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

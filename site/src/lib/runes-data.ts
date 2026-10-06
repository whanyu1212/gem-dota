/**
 * The runes recipe's figure: each side's runes by kind in a stretch of the
 * match, where they were taken, the 0:00 bounties, and what happened while each
 * power rune lasted. No DOM here: the Markdown build renders the whole match
 * with it (src/figures/runes.ts) and the browser redraws a stage or a dragged
 * stretch with it (runes-figure.ts).
 *
 * The data is src/data/runes.json, from scripts/export_site_home_data.py (which
 * takes it from examples/cookbook/runes.py).
 */
import type { TimeRange } from "./range-picker";

export type Side = "r" | "d";
export type SpotName = "top_river" | "bot_river" | "radiant_jungle" | "dire_jungle";
export type Outcome = "picked_up" | "bottled" | "denied" | "not_taken" | "still_there";
export type Whose = "river" | "own" | "other";

/** [time_s (its spawn's for a rune still there), rune, spot, outcome, hero, side, a bounty's whose, a bottled rune's use]. */
export type RuneRow = [number, string, SpotName, Outcome, string | null, Side | "", Whose | null, number | null];
/** A 0:00 bounty: [spot, hero, side, whose, seconds after the horn, the enemy heroes near]. */
export type Opener = [SpotName, string, Side, Whose, number, string[]];
/** A hero death up to 1:30: [time_s, hero, side, killer]. */
export type Death = [number, string, Side | "", string];
/**
 * A power rune's window: [start_s, end_s, rune, hero, side, from a Bottle, the
 * taker died in it, who it killed, damage to Roshan, damage to buildings,
 * [objective, seconds after the start] for each its team took].
 */
export type RuneWindow = [number, number, string, string, Side, boolean, boolean, string[], number, number, [string, number][]];

export interface RunesData {
  start_s: number;
  end_s: number;
  /** [name, start_s, end_s or null for the end of the match]. */
  stages: [string, number, number | null][];
  /** World units: the enemies listed at a 0:00 bounty were this close. */
  near: number;
  /** The 0:00 bounties' deaths run up to this game second. */
  opening_s: number;
  /** Objectives this long after a window still count for it. */
  after_s: number;
  /** Each spot on the 1000-unit map square. */
  spots: Partial<Record<SpotName, [number, number]>>;
  runes: RuneRow[];
  openers: Opener[];
  deaths: Death[];
  windows: RuneWindow[];
}

export const TEAM = { r: "Radiant", d: "Dire" } as const;
export const SPOTS: [SpotName, string][] = [
  ["top_river", "Top river"],
  ["bot_river", "Bottom river"],
  ["radiant_jungle", "Radiant's jungle"],
  ["dire_jungle", "Dire's jungle"],
];
export const RUNE_LABEL: Record<string, string> = {
  double_damage: "Double Damage",
  haste: "Haste",
  illusion: "Illusion",
  invisibility: "Invisibility",
  regeneration: "Regeneration",
  arcane: "Arcane",
  shield: "Shield",
  bounty: "Bounty",
  water: "Water",
};
const POWER = new Set(["double_damage", "haste", "illusion", "invisibility", "regeneration", "arcane", "shield"]);
export const isPower = (rune: string) => POWER.has(rune);
const taken = (row: RuneRow) => row[3] === "picked_up" || row[3] === "bottled";

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
const sideClass = (side: Side | "") => (side === "r" ? "radiant" : side === "d" ? "dire" : "none");

/** In-game time: "7:13"; before the horn, "-0:29". */
export function clock(seconds: number): string {
  const s = Math.floor(Math.abs(seconds));
  return `${seconds < 0 ? "-" : ""}${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** A stage as a range of game seconds; the last one ends with the match. */
export function stageRange(data: RunesData, stage: [string, number, number | null]): TimeRange {
  return [stage[1], stage[2] ?? data.end_s];
}

const within = (t: number, range: TimeRange | null) => range === null || (t >= range[0] && t < range[1]);

/** The runes that left the map in the range (the whole match when there's none). */
export function runesIn(data: RunesData, range: TimeRange | null): RuneRow[] {
  return data.runes.filter((row) => within(row[0], range));
}

/** The power-rune windows that started in the range. */
export function windowsIn(data: RunesData, range: TimeRange | null): RuneWindow[] {
  return data.windows.filter((w) => within(w[0], range));
}

/** The figure's rows of counts: each kind of rune taken (or put in a Bottle), and denied. */
export const KINDS: [string, (row: RuneRow) => boolean][] = [
  ["Power runes", (row) => taken(row) && isPower(row[1])],
  ["Water runes", (row) => taken(row) && row[1] === "water"],
  ["Bounty, own jungle", (row) => taken(row) && row[6] === "own"],
  ["Bounty, other jungle", (row) => taken(row) && row[6] === "other"],
  ["Bounty, river", (row) => taken(row) && row[6] === "river"],
  ["Denied", (row) => row[3] === "denied"],
];

/** Each kind's count for each side: [label, Radiant's, Dire's]. */
export function counts(rows: RuneRow[]): [string, number, number][] {
  return KINDS.map(([label, test]) => [label, rows.filter((r) => test(r) && r[5] === "r").length, rows.filter((r) => test(r) && r[5] === "d").length]);
}

/** Bounties taken by one hero at once beyond the first: untaken bounties stay on the map and stack. */
export function stacked(rows: RuneRow[]): number {
  const seen = new Set<string>();
  let extra = 0;
  for (const row of rows) {
    if (row[1] !== "bounty" || !taken(row)) continue;
    const key = `${row[0]}|${row[4]}|${row[2]}`;
    if (seen.has(key)) extra += 1;
    seen.add(key);
  }
  return extra;
}

export function countsMarkup(rows: RuneRow[]): string {
  const values = counts(rows);
  const top = Math.max(1, ...values.flatMap(([, a, b]) => [a, b]));
  const bar = (v: number, team: string) => `<span class="lane-bar lane-bar--${team}"><i style="width: ${((v / top) * 100).toFixed(1)}%"></i></span>`;
  const lines = values
    .map(([label, a, b]) => `<li><span class="lane-v">${a}</span>${bar(a, "radiant")}<span class="lane-label">${label}</span>${bar(b, "dire")}<span class="lane-v lane-v--dire">${b}</span></li>`)
    .join("");
  const extra = stacked(rows);
  const total = rows.filter(taken).length;
  const note = `${total} runes taken${extra ? `, ${extra} of them a second or third bounty one hero took at once` : ""}.`;
  return (
    `<p class="runes-head"><span class="lane-heroes lane-heroes--radiant">Radiant</span><span></span><span class="lane-heroes lane-heroes--dire">Dire</span></p>` +
    `<ol class="lane-rows runes-counts">${lines}</ol><p class="runes-note">${note}</p>`
  );
}

/** The four spots on the map, with each side's runes taken there and the ones nobody took. */
export function mapMarkup(data: RunesData, rows: RuneRow[]): string {
  return SPOTS.filter(([spot]) => data.spots[spot])
    .map(([spot, label]) => {
      const [x, y] = data.spots[spot]!;
      const here = rows.filter((r) => r[2] === spot);
      const [a, b] = [here.filter((r) => taken(r) && r[5] === "r").length, here.filter((r) => taken(r) && r[5] === "d").length];
      const left = here.filter((r) => r[3] === "not_taken").length;
      const below = y > 700;
      const ly = below ? y + 46 : y - 30;
      return (
        `<g class="rune-spot" aria-label="${label}: Radiant took ${a}, Dire took ${b}${left ? `, ${left} not taken` : ""}">` +
        `<circle cx="${x}" cy="${y}" r="13"></circle>` +
        `<text class="rune-spot-label" x="${x}" y="${ly}" text-anchor="middle">${label}</text>` +
        `<text class="rune-spot-count rune-spot-count--radiant" x="${x - 20}" y="${y + 7}" text-anchor="end">${a}</text>` +
        `<text class="rune-spot-count rune-spot-count--dire" x="${x + 20}" y="${y + 7}">${b}</text>` +
        (left ? `<text class="rune-spot-left" x="${x}" y="${below ? ly + 24 : y + 40}" text-anchor="middle">${left} not taken</text>` : "") +
        `</g>`
      );
    })
    .join("");
}

/** Where a 0:00 bounty was taken: "in the top river", "in Dire's own jungle", "from Radiant's jungle". */
const WHOSE: Record<Whose, (side: Side, spot: SpotName) => string> = {
  river: (_, spot) => `in the ${spot === "top_river" ? "top" : "bottom"} river`,
  own: (side) => `in ${TEAM[side]}'s own jungle`,
  other: (side) => `from ${TEAM[side === "r" ? "d" : "r"]}'s jungle`,
};

/** The 0:00 bounties, in pickup order, and the deaths up to 1:30. */
export function openersMarkup(data: RunesData): string {
  const near = data.near.toLocaleString("en-US");
  const items = data.openers
    .map(([spot, hero, side, whose, after, enemies]) => {
      const who = enemies.length ? `${enemies.map(escape).join(", ")} within ${near}` : `no enemy within ${near}`;
      return (
        `<li><time>+${Math.round(after)} s</time>` +
        `<span><i class="lane-dot lane-dot--${sideClass(side)}" aria-hidden="true"></i>${escape(hero)} ${WHOSE[whose](side, spot)}</span>` +
        `<span class="runes-muted">${who}</span></li>`
      );
    })
    .join("");
  const deaths = data.deaths.length
    ? `Deaths up to ${clock(data.opening_s)}: ${data.deaths.map(([t, hero, , by]) => `${escape(hero)} at ${clock(t)}, by ${escape(by)}`).join("; ")}.`
    : `No hero died before ${clock(data.opening_s)}.`;
  return `<ol class="runes-list runes-openers">${items || `<li class="runes-muted">No bounties at 0:00.</li>`}</ol><p class="runes-note">${deaths}</p>`;
}

/** What followed a power rune, as phrases. */
export function windowFacts(w: RuneWindow, afterS: number): string[] {
  const [, , rune, , , , died, killed, roshan, buildings, took] = w;
  const facts: string[] = [];
  if (killed.length) facts.push(`killed ${killed.map(escape).join(", ")}`);
  if (roshan) facts.push(`${roshan.toLocaleString("en-US")} damage to Roshan`);
  if (buildings) facts.push(`${buildings.toLocaleString("en-US")} damage to buildings`);
  if (took.length) facts.push(`the team took ${took.map(([name, s]) => `${escape(name)} (+${s} s)`).join(", ")}`);
  // A buff ends when its hero dies; an illusion rune's illusions don't.
  if (died) facts.push(rune === "illusion" ? "the taker died" : "the taker died, which ended it");
  if (!facts.length) facts.push(`no kill, no damage to Roshan or buildings, no objective in the ${afterS} s after`);
  return facts;
}

export function windowsMarkup(windows: RuneWindow[], afterS: number): string {
  if (!windows.length) return `<ol class="runes-list"><li class="runes-muted">No power runes in this stretch.</li></ol>`;
  const items = windows
    .map((w) => {
      const [start, end, rune, hero, side, bottle] = w;
      const lasted = `${Math.round(end - start)} s${bottle ? ", from a Bottle" : ""}`;
      const objective = w[10].length ? " runes-window--objective" : "";
      return (
        `<li class="runes-window${objective}"><time>${clock(start)}</time>` +
        `<span><b>${RUNE_LABEL[rune] ?? rune}</b> <span class="runes-muted">${lasted}</span><br>` +
        `<i class="lane-dot lane-dot--${sideClass(side)}" aria-hidden="true"></i>${escape(hero)}</span>` +
        `<span>${windowFacts(w, afterS).join("; ")}</span></li>`
      );
    })
    .join("");
  return `<ol class="runes-list runes-windows">${items}</ol>`;
}

/** Who took the power runes in the stretch (or used them from a Bottle), most first. */
export function takers(rows: RuneRow[]): [string, Side, number][] {
  const by = new Map<string, [Side, number]>();
  for (const row of rows) {
    if (!taken(row) || !isPower(row[1]) || !row[4] || !row[5]) continue;
    const [side, n] = by.get(row[4]) ?? [row[5], 0];
    by.set(row[4], [side, n + 1]);
  }
  return [...by.entries()].map(([hero, [side, n]]) => [hero, side, n] as [string, Side, number]).sort((a, b) => b[2] - a[2] || a[0].localeCompare(b[0]));
}

export function takersMarkup(rows: RuneRow[]): string {
  const list = takers(rows);
  if (!list.length) return `<p class="runes-muted">No power runes taken in this stretch.</p>`;
  const top = list[0][2];
  return (
    `<ol class="runes-takers">` +
    list
      .map(
        ([hero, side, n]) =>
          `<li><span><i class="lane-dot lane-dot--${sideClass(side)}" aria-hidden="true"></i>${escape(hero)}</span>` +
          `<span class="runes-taker-bar runes-taker-bar--${sideClass(side)}"><i style="width: ${((n / top) * 100).toFixed(1)}%"></i></span><span class="lane-v">${n}</span></li>`,
      )
      .join("") +
    `</ol>`
  );
}

/** Everything in the figure that follows the stretch: counts, the map's spots, the power runes and their takers. */
export function stretchMarkup(data: RunesData, range: TimeRange | null): { counts: string; spots: string; windows: string; takers: string } {
  const rows = runesIn(data, range);
  return {
    counts: countsMarkup(rows),
    spots: mapMarkup(data, rows),
    windows: windowsMarkup(windowsIn(data, range), data.after_s),
    takers: takersMarkup(rows),
  };
}

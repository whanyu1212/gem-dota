/**
 * The objectives recipe's figure: which objectives fell in a stretch, how the
 * base stood at its end, each objective's card, and each team's edges and what
 * they led to. No DOM here: the Markdown build renders the figure's first frame
 * with it (src/figures/objectives.ts) and the browser redraws with it
 * (objectives-figure.ts).
 *
 * The data is src/data/objectives.json, from scripts/export_site_home_data.py
 * (which takes each row from examples/cookbook/objectives.py).
 */
import type { TimeRange } from "./range-picker";

export type Kind = "tower" | "barracks" | "roshan" | "tormentor";
export type Side = "r" | "d";

export interface Building {
  /** Its combat-log name: "goodguys_tower1_bot"; the two tier 4s keep _bot/_top. */
  key: string;
  kind: "tower" | "barracks" | "ancient";
  side: Side;
  at: [number, number];
}

export interface Objective {
  kind: Kind;
  name: string;
  /** The side it counted for: a building's for the side that didn't own it. */
  for: Side | "";
  time_s: number;
  time: string;
  at: [number, number] | null;
  last_hit: string;
  /** Damage to a building in the 90 s before it fell: [who, damage], most first. */
  damage: [string, number][];
  /** A tier 4: the combat log names both a side's tier 4s alike, so this is both's damage. */
  shared: boolean;
  /** The fight that ended in the 2 minutes before it: [number, seconds before]. */
  after: [number, number] | null;
}

export interface Edge {
  team: Side;
  edge: "fight" | "aegis";
  /** The fight's number, or Roshan's kill number. */
  number: number;
  time: string;
  /** c: converted, o: the other side took one first, n: nothing in the window. */
  outcome: "c" | "o" | "n";
  took: string[];
  after_s: number | null;
  kills?: [number, number];
  /** For "o": the side that took it. */
  by?: Side;
}

export interface ObjectivesData {
  start_s: number;
  end_s: number;
  buildings: Building[];
  tormentor_spawns: [number, number][];
  objectives: Objective[];
  edges: Edge[];
}

export const TEAM = { r: "Radiant", d: "Dire" } as const;
export const KINDS: [Kind, string][] = [
  ["tower", "Towers"],
  ["barracks", "Barracks"],
  ["roshan", "Roshan"],
  ["tormentor", "Tormentor"],
];

/** The objectives of the shown kinds that fell in the range (the whole match when there's none). */
export function objectivesIn(data: ObjectivesData, range: TimeRange | null, kinds: Set<Kind>): number[] {
  return data.objectives
    .map((o, i) => [o, i] as const)
    .filter(([o]) => kinds.has(o.kind) && (range === null || (o.time_s >= range[0] && o.time_s <= range[1])))
    .map(([, i]) => i);
}

/** The objective that is this building's fall, if it fell: matched by place. */
export function fallOf(data: ObjectivesData, building: Building): number | null {
  const i = data.objectives.findIndex(
    (o) => (o.kind === "tower" || o.kind === "barracks") && o.at !== null && o.at[0] === building.at[0] && o.at[1] === building.at[1],
  );
  return i < 0 ? null : i;
}

/** Each team's edges counted by outcome, per kind of edge: the figure's bars. */
export function tally(edges: Edge[], team: Side, edge: Edge["edge"]): { c: number; o: number; n: number; total: number } {
  const mine = edges.filter((e) => e.team === team && e.edge === edge);
  const count = (outcome: Edge["outcome"]) => mine.filter((e) => e.outcome === outcome).length;
  return { c: count("c"), o: count("o"), n: count("n"), total: mine.length };
}

/** What an edge led to, as a phrase. */
export function edgeText(edge: Edge): string {
  if (edge.edge === "aegis") {
    return edge.took.length ? `took ${edge.took.join(", ")}, the first ${edge.after_s} s after` : "no building fell to them in the next 5 minutes";
  }
  if (edge.outcome === "c") return `took the ${edge.took[0]} ${edge.after_s} s after`;
  if (edge.outcome === "o") return `${TEAM[edge.by ?? (edge.team === "r" ? "d" : "r")]} took the ${edge.took[0]} first, ${edge.after_s} s after`;
  return "nothing fell in the 2 minutes after";
}

/** An edge's own label: "Fight 9 · 16:42 · 0–3", "Roshan 4 · 58:11". */
export function edgeLabel(edge: Edge): string {
  return edge.edge === "fight" ? `Fight ${edge.number} · ${edge.time} · ${edge.kills![0]}–${edge.kills![1]}` : `Roshan ${edge.number} · ${edge.time}`;
}

/** The objective's card: what, when, for whom, who damaged it, and the fight before. */
export function objectiveCard(o: Objective): { title: string; line: string; after: string } {
  const who = o.for ? ` · for ${TEAM[o.for]}` : "";
  return {
    title: o.name,
    line: `${o.time}${who} · last hit: ${o.last_hit}`,
    after: o.after ? `After fight ${o.after[0]}, which ended ${o.after[1]} s earlier.` : "No fight ended in the 2 minutes before.",
  };
}

/** A side's class name; "unknown" when the replay didn't say whose it was. */
export const sideClass = (side: Side | "") => (side === "r" ? "radiant" : side === "d" ? "dire" : "unknown");

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

/**
 * The SVG for the map: every building as it stood at the end of the range
 * (fallen ones hollow and crossed, those that fell inside the range clickable),
 * and the Roshan and Tormentor kills inside the range at their places. The
 * selected objective is ringed.
 */
export function mapMarkup(data: ObjectivesData, range: TimeRange | null, shown: number[], selected: number | null): string {
  const end = range ? range[1] : data.end_s;
  const inShown = new Set(shown);
  const team = (side: Side) => (side === "r" ? "radiant" : "dire");
  const parts: string[] = [];
  for (const b of data.buildings) {
    const fall = fallOf(data, b);
    const fell = fall !== null && data.objectives[fall].time_s <= end;
    const active = fall !== null && inShown.has(fall);
    const size = b.kind === "ancient" ? 20 : b.kind === "barracks" ? 11 : 13;
    const [x, y] = b.at;
    const shape =
      b.kind === "tower"
        ? `<polygon points="${x},${y - size} ${x - size},${y + size * 0.8} ${x + size},${y + size * 0.8}"></polygon>`
        : `<rect x="${x - size}" y="${y - size}" width="${size * 2}" height="${size * 2}" rx="${b.kind === "ancient" ? 6 : 2}"></rect>`;
    const cross = fell ? `<path class="obj-cross" d="M${x - size * 0.7},${y - size * 0.7}L${x + size * 0.7},${y + size * 0.7}M${x + size * 0.7},${y - size * 0.7}L${x - size * 0.7},${y + size * 0.7}"></path>` : "";
    const ring = fall !== null && fall === selected ? `<circle class="obj-ring" cx="${x}" cy="${y}" r="${size + 12}"></circle>` : "";
    const attrs = active
      ? ` data-objective="${fall}" tabindex="0" role="button" aria-label="${escape(`${data.objectives[fall!].name}, ${data.objectives[fall!].time}`)}"`
      : "";
    parts.push(`<g class="obj obj--${team(b.side)}${fell ? " is-fallen" : ""}${active ? " is-active" : ""}"${attrs}>${shape}${cross}${ring}</g>`);
  }
  // Bosses: each kill in the range at its place, nudged apart when they share it.
  const seen = new Map<string, number>();
  for (const i of shown) {
    const o = data.objectives[i];
    if ((o.kind !== "roshan" && o.kind !== "tormentor") || !o.at) continue;
    const key = `${Math.round(o.at[0] / 40)},${Math.round(o.at[1] / 40)}`;
    const k = seen.get(key) ?? 0;
    seen.set(key, k + 1);
    const angle = k * 2.4;
    const [x, y] = [o.at[0] + (k ? 26 * Math.cos(angle) : 0), o.at[1] + (k ? 26 * Math.sin(angle) : 0)];
    const label = o.kind === "roshan" ? "R" : "T";
    const ring = i === selected ? `<circle class="obj-ring" cx="${x}" cy="${y}" r="26"></circle>` : "";
    parts.push(
      `<g class="obj-boss obj-boss--${sideClass(o.for)}" data-objective="${i}" tabindex="0" role="button" aria-label="${escape(`${o.name}, ${o.time}`)}">` +
        `<circle cx="${x}" cy="${y}" r="15"></circle><text x="${x}" y="${y + 6}" text-anchor="middle">${label}</text>${ring}</g>`,
    );
  }
  return parts.join("");
}

/**
 * The conversion bars: for each team, its fights won on kills and its Aegis
 * windows, each a bar split by outcome. A segment is a button that lists its
 * edges (`data-edges="r|fight|c"`); `picked` marks the one listed.
 */
export function tallyMarkup(edges: Edge[], picked: string | null = null): string {
  const bar = (team: Side, edge: Edge["edge"], title: string) => {
    const t = tally(edges, team, edge);
    const parts = (edge === "fight" ? (["c", "o", "n"] as const) : (["c", "n"] as const))
      .filter((outcome) => t[outcome] > 0)
      .map((outcome) => {
        const key = `${team}|${edge}|${outcome}`;
        const what = outcome === "c" ? (edge === "fight" ? "took the next objective" : "took a building") : outcome === "o" ? "the other side took one first" : "nothing";
        return `<button type="button" class="tally-seg tally-seg--${outcome} tally-seg--${team === "r" ? "radiant" : "dire"}" style="flex: ${t[outcome]}" data-edges="${key}" aria-pressed="${key === picked}" title="${what}: ${t[outcome]}">${t[outcome]}</button>`;
      })
      .join("");
    return (
      `<p class="tally-label"><span>${title}</span><span><b>${t.c} of ${t.total}</b> converted</span></p>` +
      `<div class="tally-bar">${parts || `<span class="tally-none">none</span>`}</div>`
    );
  };
  return (["r", "d"] as const)
    .map(
      (team) =>
        `<div class="tally-team"><p class="tally-name tally-name--${team === "r" ? "radiant" : "dire"}">${TEAM[team]}</p>` +
        bar(team, "fight", "Fights it won on kills") +
        bar(team, "aegis", "Aegis held (5 minutes)") +
        `</div>`,
    )
    .join("");
}

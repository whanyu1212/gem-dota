/**
 * The lanes recipe's figure: each lane's heroes, each side's numbers at a
 * reading (6:00 or 10:00), and what happened in the lane up to it. No DOM here:
 * the Markdown build renders the figure at 6:00 with it (src/figures/lanes.ts)
 * and the browser redraws it for the other reading (lanes-figure.ts).
 *
 * The data is src/data/lanes.json, from scripts/export_site_home_data.py (which
 * takes it from examples/cookbook/lanes.py).
 */

export type Side = "r" | "d";
export type LaneName = "top" | "mid" | "bot";

/** Net worth, XP, last hits, denies, then gold from lane creeps, hero kills, neutrals, the rest. */
export type Numbers = [number, number, number, number, number, number, number, number];

export interface LaneSide {
  /** [hero, the share of the laning stage it spent in this lane]. */
  heroes: [string, number][];
  /** The side's numbers at each reading, keyed by its game seconds. */
  at: Record<string, Numbers>;
}

export interface Lane {
  lane: LaneName;
  sides: Record<Side, LaneSide>;
}

/** [time_s, end_s (a visit's), kind, lane, hero, side, by (a death's killer), the hero's or killer's own lane]. */
export type LaneEvent = [number, number | null, "death" | "teleport" | "visit", string, string, Side | "", string | null, string | null];

export interface LanesData {
  /** The two readings, in game seconds: the laning stage's end, then 10:00. */
  readings: [number, number];
  lanes: Lane[];
  events: LaneEvent[];
  /** Heroes whose OpenDota lane (over 10 minutes) is another: [hero, OpenDota's, the recipe's]. */
  opendota: [string, string, string][];
}

export const LANE_LABEL: Record<string, string> = { top: "Top", mid: "Mid", bot: "Bottom", jungle: "jungle" };
const ROWS: [string, number][] = [
  ["Net worth", 0],
  ["XP", 1],
  ["Last hits", 2],
  ["Denies", 3],
];
const GOLD: [string, number][] = [
  ["Lane creeps", 4],
  ["Hero kills", 5],
  ["Neutrals", 6],
  ["The rest", 7],
];
/** Shares under this are shown next to the hero. */
const SHOW_SHARE = 0.8;

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

/** In-game time: "7:13". */
export function clock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** Gold or XP, without a sign: "950", "3.6k". */
export function amount(value: number): string {
  const a = Math.abs(value);
  return a >= 1000 ? `${(a / 1000).toFixed(1)}k` : String(Math.round(a));
}

/** The net-worth gap in a lane at a reading: "Dire +1.1k net worth at 6:00". */
export function gapText(lane: Lane, reading: number): string {
  const [r, d] = [lane.sides.r.at[reading]?.[0] ?? 0, lane.sides.d.at[reading]?.[0] ?? 0];
  if (r === d) return `Level on net worth at ${clock(reading)}`;
  return `${r > d ? "Radiant" : "Dire"} +${amount(r - d)} net worth at ${clock(reading)}`;
}

/** An event as a sentence, cut at the reading (a visit still under way says so). */
export function eventText(event: LaneEvent, reading: number): string {
  const [, end, kind, lane, hero, , by, from] = event;
  const elsewhere = from && from !== lane ? ` (from ${from === "bot" ? "bottom" : from})` : "";
  if (kind === "death") return `${hero} killed by ${by ?? "unknown"}${elsewhere}`;
  if (kind === "teleport") return `${hero} teleported to the lane${elsewhere}`;
  // The recipe ends a visit still under way at its last second, so one ending at the reading was still there.
  const until = end === null || end >= reading ? `, still there at ${clock(reading)}` : ` until ${clock(end)}`;
  return `${hero} in the lane${until}${elsewhere}`;
}

/** The events in a lane (or, with `lane` null, outside the three) up to a reading. */
export function eventsIn(data: LanesData, lane: LaneName | null, reading: number): LaneEvent[] {
  const lanes = new Set(["top", "mid", "bot"]);
  return data.events.filter(([t, , , where]) => t <= reading && (lane === null ? !lanes.has(where) : where === lane));
}

function heroesMarkup(side: LaneSide): string {
  return side.heroes
    .map(([hero, share]) => `${escape(hero)}${share < SHOW_SHARE ? ` <span class="lane-share" title="Share of 0:00–6:00 spent in this lane">${Math.round(share * 100)}%</span>` : ""}`)
    .join(", ");
}

function eventMarkup(event: LaneEvent, reading: number): string {
  const [t, , kind, , , side] = event;
  const label = kind === "death" ? "Death" : kind === "teleport" ? "Teleport" : "Visit";
  const team = side === "r" ? "radiant" : side === "d" ? "dire" : "even";
  return (
    `<li><time>${clock(t)}</time><span class="lane-ev-kind lane-ev-kind--${kind}">${label}</span>` +
    `<span><i class="lane-dot lane-dot--${team}" aria-hidden="true"></i>${escape(eventText(event, reading))}</span></li>`
  );
}

/** One lane's card at a reading: its heroes, numbers side against side, gold by source and events. */
export function laneMarkup(data: LanesData, lane: Lane, reading: number): string {
  const [r, d] = [lane.sides.r.at[reading], lane.sides.d.at[reading]];
  const row = ([label, i]: [string, number], bars: boolean) => {
    const [a, b] = [r?.[i] ?? 0, d?.[i] ?? 0];
    const top = Math.max(a, b) || 1;
    const show = (v: number) => (i <= 1 || i >= 4 ? amount(v) : String(v));
    const bar = (v: number, team: string) =>
      bars ? `<span class="lane-bar lane-bar--${team}"><i style="width: ${((v / top) * 100).toFixed(1)}%"></i></span>` : `<span></span>`;
    return `<li><span class="lane-v">${show(a)}</span>${bar(a, "radiant")}<span class="lane-label">${label}</span>${bar(b, "dire")}<span class="lane-v lane-v--dire">${show(b)}</span></li>`;
  };
  const events = eventsIn(data, lane.lane, reading);
  return (
    `<section class="lane-card" aria-label="${LANE_LABEL[lane.lane]} lane">` +
    `<header class="lane-head"><p class="lane-heroes lane-heroes--radiant">${heroesMarkup(lane.sides.r)}</p>` +
    `<p class="lane-name">${LANE_LABEL[lane.lane]}</p><p class="lane-heroes lane-heroes--dire">${heroesMarkup(lane.sides.d)}</p></header>` +
    `<ol class="lane-rows">${ROWS.map((x) => row(x, true)).join("")}</ol>` +
    `<p class="lane-gap">${gapText(lane, reading)}</p>` +
    `<p class="lane-sub">Earned gold by source</p>` +
    `<ol class="lane-rows lane-rows--gold" aria-label="Earned gold by source">${GOLD.map((x) => row(x, false)).join("")}</ol>` +
    `<ol class="lane-events">${events.length ? events.map((e) => eventMarkup(e, reading)).join("") : `<li class="lane-none">No deaths, teleports or visits.</li>`}</ol>` +
    `</section>`
  );
}

/** Everything in the figure below the reading switch, at a reading. */
export function figureMarkup(data: LanesData, reading: number): string {
  const elsewhere = eventsIn(data, null, reading);
  const outside = elsewhere.length
    ? `<p class="lane-elsewhere-head">Outside the lanes</p><ol class="lane-events">${elsewhere.map((e) => eventMarkup(e, reading)).join("")}</ol>`
    : "";
  const od = data.opendota.length
    ? `<p class="lane-note">${data.opendota.map(([hero, theirs, ours]) => `OpenDota puts ${escape(hero)} in ${theirs === "bot" ? "bottom" : theirs} (over 0:00–10:00); here it is in ${ours === "bot" ? "bottom" : ours}, where it spent the most of 0:00–6:00.`).join(" ")}</p>`
    : "";
  return `<div class="lane-cards">${data.lanes.map((lane) => laneMarkup(data, lane, reading)).join("")}</div>${outside}${od}`;
}

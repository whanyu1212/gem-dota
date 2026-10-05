/**
 * The fights recipe's figure: which fights are in a stretch, what a fight's card
 * says, and the SVG for the fights on the map. No DOM here: the Markdown build
 * renders the figure's first frame with it (src/figures/fights.ts) and the
 * browser redraws with it (fights-figure.ts).
 *
 * The data is src/data/fights/index.json, from scripts/export_site_home_data.py
 * (which takes each row from examples/cookbook/fights.py).
 */
import type { TimeRange } from "./range-picker";
import { clock, span } from "./wards-data";

export interface FightEntry {
  /** The fight's number in the match, in time order. */
  n: number;
  /** Its data file, from src/data: "fights/7.json", or "fight.json" for Figure 3's. */
  file: string;
  /** gem's clock at the fight's start, and its in-game seconds. */
  start: string;
  start_s: number;
  duration: number;
  deaths: number;
  /** Kills scored by Radiant and by Dire. */
  kills: [number, number];
  /** The side with more kills: r, d, or x for even. */
  more: "r" | "d" | "x";
  /** Map-square position of the centre of its deaths, or null when none had one. */
  at: [number, number] | null;
  /** Each side's net gold change near the fight (earned less lost on death). */
  gold: [number, number];
  /** The first building or Roshan within 2 minutes after: name, side (r/d), seconds after. */
  next: [string, "r" | "d" | "", number] | null;
  /** The map crop for a fight with a playback; absent for a breakdown only. */
  box?: [number, number, number];
}

export interface FightsData {
  start_s: number;
  end_s: number;
  fights: FightEntry[];
}

export const SIDE = { r: "Radiant", d: "Dire", x: "Even" } as const;

/** Whether the fight overlaps the range (the whole match when there's none). */
export function overlaps(fight: FightEntry, range: TimeRange | null): boolean {
  return range === null || (fight.start_s <= range[1] && fight.start_s + fight.duration >= range[0]);
}

/** The fights with at least `minDeaths` deaths that overlap the range, in time order. */
export function fightsIn(data: FightsData, range: TimeRange | null, minDeaths = 1): FightEntry[] {
  return data.fights.filter((f) => f.deaths >= minDeaths && overlaps(f, range));
}

/** The fight's kills as "4–6". */
export const score = (fight: FightEntry) => `${fight.kills[0]}–${fight.kills[1]}`;

/** What fell after the fight, as a sentence. */
export function nextText(fight: FightEntry): string {
  if (!fight.next) return "No building fell and Roshan wasn't killed in the 2 minutes after.";
  const [what, side, after] = fight.next;
  const who = side ? SIDE[side] : "Someone";
  return what === "Roshan" ? `${who} killed Roshan ${after} s after it ended.` : `${who} took the ${what} ${after} s after it ended.`;
}

/** The fight's card: time, kills, net gold and what fell next. */
export function card(fight: FightEntry): { title: string; kills: string; gold: string; next: string } {
  const gold = (n: number) => `${n >= 0 ? "+" : "−"}${Math.abs(n).toLocaleString("en-US")}`;
  return {
    title: `Fight ${fight.n} · ${fight.start}–${clock(fight.start_s + fight.duration)} · ${span(fight.duration)}`,
    kills:
      `${score(fight)} kills, Radiant–Dire` +
      (fight.more === "x" ? " · even" : ` · ${SIDE[fight.more]} had more`) +
      ` · ${fight.deaths} death${fight.deaths === 1 ? "" : "s"}`,
    gold: `Net gold near the fight: Radiant ${gold(fight.gold[0])}, Dire ${gold(fight.gold[1])}`,
    next: nextText(fight),
  };
}

/** A fight's dot radius on the map: grows with its deaths. */
export const dotRadius = (deaths: number) => 12 + 9 * Math.sqrt(deaths);

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

/**
 * The SVG for the fights shown: a dot per placed fight, sized by deaths and
 * coloured by the side with more kills, the biggest drawn first so small ones
 * stay clickable; the selected one is marked and drawn last.
 */
export function fightDots(fights: FightEntry[], selected: number | null = null): string {
  const side = { r: "radiant", d: "dire", x: "even" };
  const order = fights
    .filter((f) => f.at)
    .sort((a, b) => Number(a.n === selected) - Number(b.n === selected) || b.deaths - a.deaths);
  return order
    .map((f) => {
      const [x, y] = f.at!;
      const label = f.deaths > 1 ? `<text x="${x}" y="${y + 8}" text-anchor="middle">${f.deaths}</text>` : "";
      const c = card(f);
      return (
        `<g class="fight-dot fight-dot--${side[f.more]}${f.n === selected ? " is-selected" : ""}" data-fight="${f.n}" tabindex="0" role="button" aria-label="${escape(`${c.title}; ${c.kills}`)}">` +
        `<circle cx="${x}" cy="${y}" r="${dotRadius(f.deaths)}"></circle>${label}</g>`
      );
    })
    .join("");
}

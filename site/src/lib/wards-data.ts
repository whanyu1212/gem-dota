/**
 * The wards recipe's figure: which wards were up in a stretch of the match, the
 * counts and story the figure shows, and the SVG for the wards on the map. No
 * DOM here: the Markdown build renders the figure's first frame with it
 * (src/figures/wards.ts) and the browser redraws with it (wards-figure.ts).
 *
 * The data is src/data/wards.json, from scripts/export_site_home_data.py.
 */
import type { TimeRange } from "./range-picker";

/**
 * One ward: team (`r`/`d`), type (`o` observer, `s` sentry), map-square x and
 * y, the in-game seconds it went up and ended, how it ended (`k` killed, `e`
 * expired, `u` up when the recording ended), its placer, its killer, and gem's
 * clock for the two times. It is up from `placed_s` until `ended_s` (half open).
 */
export type Ward = [
  team: "r" | "d",
  type: "o" | "s",
  x: number,
  y: number,
  placedS: number,
  endedS: number,
  how: "k" | "e" | "u",
  placer: string,
  killer: string,
  placed: string,
  ended: string,
];

export interface WardsData {
  /** The timeline's first and last second (in-game seconds). */
  start_s: number;
  end_s: number;
  /** The vision model's observer radius, in map-square units. */
  radius: number;
  /** The stretch the figure opens on: around the home page's Figure 3 fight. */
  range: TimeRange | null;
  wards: Ward[];
}

export interface WardFilter {
  teams: Set<"r" | "d">;
  types: Set<"o" | "s">;
}

export const ALL: WardFilter = { teams: new Set(["r", "d"]), types: new Set(["o", "s"]) };
export const TEAM_NAMES = { r: "Radiant", d: "Dire" } as const;

/** Whether the ward was up at any moment in the range (the whole match when there's none). */
export function upIn(ward: Ward, range: TimeRange | null): boolean {
  return range === null || (ward[4] <= range[1] && ward[5] > range[0]);
}

/** The indices of the wards up in the range that pass the filter, in placement order. */
export function wardsIn(data: WardsData, range: TimeRange | null, filter: WardFilter = ALL): number[] {
  return data.wards
    .map((ward, i) => [ward, i] as const)
    .filter(([ward]) => filter.teams.has(ward[0]) && filter.types.has(ward[1]) && upIn(ward, range))
    .sort((a, b) => a[0][4] - b[0][4])
    .map(([, i]) => i);
}

/** For each whole minute of the timeline, the wards each team had up at some moment in it. */
export function perMinute(data: WardsData): { from: number; r: number; d: number }[] {
  const minutes = [];
  for (let from = Math.floor(data.start_s / 60) * 60; from < data.end_s; from += 60) {
    const counts = { from, r: 0, d: 0 };
    for (const ward of data.wards) if (upIn(ward, [from, from + 60])) counts[ward[0]]++;
    minutes.push(counts);
  }
  return minutes;
}

/** The figure's counts for the wards shown: observers and sentries up, and placed or killed in the range. */
export function counts(data: WardsData, shown: number[], range: TimeRange | null) {
  const wards = shown.map((i) => data.wards[i]);
  const within = (s: number) => range === null || (s >= range[0] && s <= range[1]);
  return {
    observers: wards.filter((w) => w[1] === "o").length,
    sentries: wards.filter((w) => w[1] === "s").length,
    placed: wards.filter((w) => within(w[4])).length,
    killed: wards.filter((w) => w[6] === "k" && within(w[5])).length,
  };
}

/** In-game seconds as gem shows them: "42:49", "-01:00" before the horn. */
export function clock(seconds: number): string {
  const whole = seconds < 0 ? Math.ceil(-seconds - 1e-6) : Math.floor(seconds + 1e-6);
  const text = `${String(Math.floor(whole / 60)).padStart(2, "0")}:${String(whole % 60).padStart(2, "0")}`;
  return seconds < 0 ? `-${text}` : text;
}

/** A duration as "m:ss". */
export function span(seconds: number): string {
  const whole = Math.round(seconds);
  return `${Math.floor(whole / 60)}:${String(whole % 60).padStart(2, "0")}`;
}

/** A ward's story: who placed it and when, how it ended, and how long it lasted. */
export function story(ward: Ward): string {
  const what = `${TEAM_NAMES[ward[0]]} ${ward[1] === "o" ? "observer" : "sentry"}`;
  const lasted = span(ward[5] - ward[4]);
  const end =
    ward[6] === "k"
      ? `killed by ${ward[8]} at ${ward[10]}, after ${lasted}`
      : ward[6] === "e"
        ? `expired at ${ward[10]}, after ${lasted}`
        : `still up when the recording ended (${ward[10]}), after ${lasted}`;
  return `${what} placed by ${ward[7]} at ${ward[9]}; ${end}.`;
}

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

/** Badge radius on the map, in map-square units. */
export const BADGE = 20;

/**
 * The SVG for the wards shown: observer vision circles first, then a badge
 * per ward (its icon in a ring of its team's colour). A ward killed inside the
 * range is drawn dashed; the selected one is marked. `assets` is the URL folder
 * holding ward_observer.png and ward_sentry.png.
 */
export function wardMarkup(
  data: WardsData,
  shown: number[],
  range: TimeRange | null,
  assets: string,
  selected: number | null = null,
): string {
  const team = (w: Ward) => (w[0] === "r" ? "radiant" : "dire");
  const killedIn = (w: Ward) => w[6] === "k" && (range === null || w[5] <= range[1]);
  const state = (w: Ward, i: number) => `${killedIn(w) ? " is-killed" : ""}${i === selected ? " is-selected" : ""}`;
  const vision = shown
    .filter((i) => data.wards[i][1] === "o")
    .map((i) => {
      const w = data.wards[i];
      return `<circle class="ward-vision ward-vision--${team(w)}${state(w, i)}" cx="${w[2]}" cy="${w[3]}" r="${data.radius}"></circle>`;
    });
  const width = (BADGE * 2 * 88) / 64;
  // The selected ward last, so it draws on top.
  const order = selected !== null && shown.includes(selected) ? [...shown.filter((i) => i !== selected), selected] : shown;
  const badges = order.map((i) => {
    const w = data.wards[i];
    const icon = `${assets}ward_${w[1] === "o" ? "observer" : "sentry"}.png`;
    return (
      `<g class="ward ward--${team(w)}${state(w, i)}" transform="translate(${w[2]} ${w[3]})" data-ward="${i}" tabindex="0" role="button" aria-label="${escape(story(w))}">` +
      `<circle class="ward-ring" r="${BADGE + 4}"></circle>` +
      `<image href="${icon}" x="${-width / 2}" y="${-BADGE}" width="${width}" height="${BADGE * 2}" clip-path="url(#wards-badge)"></image></g>`
    );
  });
  return [...vision, ...badges].join("");
}

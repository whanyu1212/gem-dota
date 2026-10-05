/**
 * The lead recipe's figure: the gold or XP lead over a match, and what moved it
 * between two readings, by source and by hero. No DOM here: the Markdown build
 * renders the figure's first frame with it (src/figures/lead.ts) and the
 * browser redraws with it (lead-figure.ts).
 *
 * The data is src/data/lead.json, from scripts/export_site_home_data.py (which
 * takes it from examples/cookbook/lead.py). Every series is a running total at
 * each reading (every game minute and the end of the game), Radiant minus Dire,
 * so a stretch's change is one reading minus another, and the sources add up
 * to the lead exactly.
 */

export type Kind = "gold" | "xp";
export type Side = "r" | "d";

export interface Split {
  lead: number[];
  /** Each source's share of the lead: [name, running total at each reading]. */
  sources: [string, number[]][];
}

export interface Hero {
  name: string;
  side: Side;
  /** Running gold: hero kills, lane and neutral creeps, everything else. */
  gold: [number[], number[], number[]];
  xp: number[];
}

export interface LeadData {
  /** Game seconds of each reading: every minute, then the end of the game. */
  times: number[];
  gold: Split;
  xp: Split;
  heroes: Hero[];
  /** [number, start_s, end_s, deaths, the side with more kills ("" when even)]. */
  fights: [number, number, number, number, Side | ""][];
  /** [kind, the side it counted for, game seconds]. */
  objectives: [string, Side | "", number][];
}

/** Each source's label, in the recipe's order. */
export const LABELS: Record<Kind, Record<string, string>> = {
  gold: {
    hero_kills: "Hero kills and assists",
    lane_creeps: "Lane creeps",
    neutral_creeps: "Neutral creeps",
    buildings: "Buildings",
    roshan: "Roshan",
    bounty_runes: "Bounty runes",
    passive_income: "Passive income",
    other: "Other",
    unlisted: "Not in the gold totals",
  },
  xp: {
    hero_kills: "Hero kills",
    lane_creeps: "Lane creeps",
    neutral_creeps: "Neutral creeps",
    other_units: "Summons and other units",
    unclear_creeps: "Creeps, kind unclear",
    roshan: "Roshan",
    wisdom_runes: "Wisdom runes",
    other: "Other",
    unlisted: "Not in the combat log",
  },
};
export const UNIT: Record<Kind, string> = { gold: "gold", xp: "XP" };
export const HERO_GROUPS = ["Hero kills and assists", "Lane and neutral creeps", "Everything else"];
const TEAM = { r: "Radiant", d: "Dire" } as const;

/** A reading's in-game time: "42:00", "92:56". */
export function clock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** An amount of gold or XP, without its sign: "950", "12.4k". */
export function amount(value: number): string {
  const a = Math.abs(value);
  return a >= 1000 ? `${(a / 1000).toFixed(1)}k` : String(Math.round(a));
}

/** The reading nearest a time (seconds). */
export function readingAt(data: LeadData, t: number): number {
  let best = 0;
  data.times.forEach((time, i) => {
    if (Math.abs(time - t) < Math.abs(data.times[best] - t)) best = i;
  });
  return best;
}

/** Who led, and by how much: "Dire led by 10.7k", "the teams were level". */
export function leadText(value: number): string {
  if (value === 0) return "the teams were level";
  return `${value > 0 ? "Radiant" : "Dire"} led by ${amount(value)}`;
}

export interface Row {
  key: string;
  label: string;
  /** Positive: toward Radiant. */
  value: number;
}

/**
 * How much each source moved the lead from reading `a` to reading `b`, then
 * the change in the lead (`key` "lead"). The sources add up to it. The
 * "unlisted" row is left out when it didn't move.
 */
export function moved(data: LeadData, kind: Kind, a: number, b: number): Row[] {
  const split = data[kind];
  const rows = split.sources
    .map(([key, series]) => ({ key, label: LABELS[kind][key] ?? key, value: series[b] - series[a] }))
    .filter((row) => row.key !== "unlisted" || row.value !== 0);
  return [...rows, { key: "lead", label: "Change in the lead", value: split.lead[b] - split.lead[a] }];
}

/** The sentence above the bars. */
export function summary(data: LeadData, kind: Kind, a: number, b: number): string {
  const lead = data[kind].lead;
  const unit = UNIT[kind];
  const at = (i: number) => clock(data.times[i]);
  const whole = a === 0 && b === data.times.length - 1;
  if (whole) return `At the end of the game, ${at(b)}, ${leadText(lead[b])} ${unit}.`;
  const change = lead[b] - lead[a];
  const toward = change === 0 ? "The lead didn't move" : `The lead moved ${amount(change)} ${unit} toward ${change > 0 ? "Radiant" : "Dire"}`;
  return `At ${at(a)} ${leadText(lead[a])}; at ${at(b)} ${leadText(lead[b])}. ${toward}.`;
}

export interface Flip {
  /** The reading where the lead was on the other side. */
  reading: number;
  ahead: Side;
  /** Fights that overlap the time since the reading before (a minute earlier, or the last minute). */
  fights: number[];
}

/**
 * The readings from `a` to `b` where the lead changed hands: on the other side
 * of 0 from the last reading that wasn't level (a level reading changes nothing).
 */
export function flips(data: LeadData, kind: Kind, a: number, b: number): Flip[] {
  const lead = data[kind].lead;
  const out: Flip[] = [];
  let side = 0;
  for (let i = 0; i <= b; i++) {
    const now = Math.sign(lead[i]);
    if (i > a && now && side && now !== side) {
      const [from, to] = [data.times[i - 1], data.times[i]];
      const fights = data.fights.filter(([, start, end]) => end > from && start <= to).map(([n]) => n);
      out.push({ reading: i, ahead: now > 0 ? "r" : "d", fights });
    }
    if (now) side = now;
  }
  return out;
}

export interface HeroRow {
  name: string;
  side: Side;
  /** What the hero earned from `a` to `b`: the gold groups, or one XP part. */
  parts: number[];
  total: number;
}

/** Each hero's gold (in its three groups) or XP from reading `a` to `b`. */
export function heroRows(data: LeadData, kind: Kind, a: number, b: number): HeroRow[] {
  return data.heroes.map((hero) => {
    const parts = kind === "gold" ? hero.gold.map((series) => series[b] - series[a]) : [hero.xp[b] - hero.xp[a]];
    return { name: hero.name, side: hero.side, parts, total: parts.reduce((s, v) => s + v, 0) };
  });
}

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

/** The y axis's step: at most three gridlines on the side with the larger lead. */
export function axisStep(top: number): number {
  for (const step of [500, 1000, 2000, 5000, 10000, 20000, 50000]) if (top / step <= 3) return step;
  return 100000;
}

/**
 * The chart's scale: the largest lead each way, padded. A side that never led
 * (or barely did) still gets a sixth of the chart, so 0 and its label show.
 */
export function scaleOf(data: LeadData, kind: Kind): { hi: number; lo: number } {
  const lead = data[kind].lead;
  const [hi, lo] = [Math.max(0, ...lead), Math.min(0, ...lead)];
  const floor = Math.max(1, hi - lo) / 6;
  return { hi: Math.max(hi, floor) * 1.06, lo: Math.min(lo, -floor) * 1.06 };
}

/** Where a lead sits on the chart, from 0 (its top) to 1 (its bottom). */
function depth(value: number, { hi, lo }: { hi: number; lo: number }): number {
  return (hi - value) / (hi - lo);
}

/** The gridline values: every step out from 0, inside the scale. */
function gridValues(scale: { hi: number; lo: number }): number[] {
  const step = axisStep(Math.max(scale.hi, -scale.lo));
  const values: number[] = [];
  for (let v = step; v < scale.hi; v += step) values.push(v);
  for (let v = -step; v > scale.lo; v -= step) values.push(v);
  return values;
}

/**
 * The curve as SVG, in a 1000×200 box with the time axis edge to edge:
 * gridlines, the lead's area (Radiant's above 0, Dire's below) and its line.
 */
export function curveMarkup(data: LeadData, kind: Kind): string {
  const scale = scaleOf(data, kind);
  const span = data.times[data.times.length - 1] - data.times[0] || 1;
  const x = (t: number) => (((t - data.times[0]) / span) * 1000).toFixed(1);
  const y = (v: number) => (depth(v, scale) * 200).toFixed(1);
  const zero = y(0);
  const grid = gridValues(scale).map((v) => `<line class="lead-grid" x1="0" x2="1000" y1="${y(v)}" y2="${y(v)}"></line>`);
  const points = data[kind].lead.map((v, i) => `${x(data.times[i])},${y(v)}`);
  const area = `M0,${zero} L${points.join(" L")} L1000,${zero} Z`;
  return (
    `<defs><clipPath id="lead-above"><rect width="1000" height="${zero}"></rect></clipPath>` +
    `<clipPath id="lead-below"><rect y="${zero}" width="1000" height="${(200 - Number(zero)).toFixed(1)}"></rect></clipPath></defs>` +
    grid.join("") +
    `<path class="lead-area lead-area--radiant" d="${area}" clip-path="url(#lead-above)"></path>` +
    `<path class="lead-area lead-area--dire" d="${area}" clip-path="url(#lead-below)"></path>` +
    `<line class="lead-zero" x1="0" x2="1000" y1="${zero}" y2="${zero}"></line>` +
    `<polyline class="lead-line" points="${points.join(" ")}"></polyline>`
  );
}

/** The y axis's labels (0 and each gridline), as HTML placed by percent beside the curve. */
export function axisMarkup(data: LeadData, kind: Kind): string {
  const scale = scaleOf(data, kind);
  return [0, ...gridValues(scale)]
    .map((v) => `<span style="top: ${(depth(v, scale) * 100).toFixed(2)}%">${v === 0 ? "0" : amount(v)}</span>`)
    .join("");
}

/**
 * The marks under the curve, as HTML placed by percent: each objective (a
 * square in the colour of the side it counted for) and each fight (a dot sized
 * by deaths, in the colour of the side with more kills). With `fightsUrl`, a
 * fight's dot links to it on the fights page, which opens `#fight-N` from its
 * script, so the links are the browser's to add.
 */
export function marksMarkup(data: LeadData, fightsUrl: string | null): string {
  const span = data.times[data.times.length - 1] - data.times[0] || 1;
  const left = (t: number) => `${(((t - data.times[0]) / span) * 100).toFixed(2)}%`;
  const side = (s: Side | "") => (s === "r" ? "radiant" : s === "d" ? "dire" : "even");
  const objectives = data.objectives
    .map(([kind, s, t]) => `<i class="lead-obj lead-obj--${side(s)}" style="left: ${left(t)}" title="${escape(`${kind} for ${s ? TEAM[s] : "neither side"}, ${clock(t)}`)}"></i>`)
    .join("");
  const fights = data.fights
    .map(([n, start, , deaths, more]) => {
      const size = Math.min(14, 6 + deaths);
      const label = `Fight ${n}, ${clock(start)}, ${deaths} ${deaths === 1 ? "death" : "deaths"}`;
      const style = `left: ${left(start)}; width: ${size}px; height: ${size}px`;
      return fightsUrl
        ? `<a class="lead-fight lead-fight--${side(more)}" href="${fightsUrl}#fight-${n}" style="${style}" aria-label="${label}" title="${label}"></a>`
        : `<i class="lead-fight lead-fight--${side(more)}" style="${style}" title="${label}"></i>`;
    })
    .join("");
  return `<div class="lead-marks-row lead-marks-row--objectives">${objectives}</div><div class="lead-marks-row lead-marks-row--fights">${fights}</div>`;
}

/** The time axis's labels every ten minutes. */
export function ticksMarkup(data: LeadData): string {
  const span = data.times[data.times.length - 1] - data.times[0] || 1;
  const out: string[] = [];
  for (let s = 0; s <= data.times[data.times.length - 1]; s += 600) {
    const at = ((s - data.times[0]) / span) * 100;
    const classes = [(s / 600) % 2 ? "ward-tick--minor" : "", at < 4 ? "ward-tick--edge" : ""].filter(Boolean).join(" ");
    out.push(`<span style="left: ${at.toFixed(2)}%"${classes ? ` class="${classes}"` : ""}>${clock(s)}</span>`);
  }
  return out.join("");
}

/** The diverging bars of `moved`: toward Dire to the left, toward Radiant to the right. */
export function movedMarkup(rows: Row[], kind: Kind): string {
  const top = Math.max(1, ...rows.map((r) => Math.abs(r.value)));
  const bar = (row: Row) => {
    const width = ((Math.abs(row.value) / top) * 50).toFixed(2);
    const where = row.value >= 0 ? `left: 50%; width: ${width}%` : `right: 50%; width: ${width}%`;
    const who = row.value > 0 ? "lead-bar--radiant" : row.value < 0 ? "lead-bar--dire" : "";
    const value = row.value === 0 ? "0" : `${row.value > 0 ? "Radiant" : "Dire"} +${amount(row.value)}`;
    return (
      `<li class="lead-row${row.key === "lead" ? " lead-row--total" : ""}">` +
      `<span class="lead-row-label">${escape(row.label)}</span>` +
      `<span class="lead-row-track"><i class="lead-bar ${who}" style="${where}"></i></span>` +
      `<span class="lead-row-value">${value}</span></li>`
    );
  };
  return (
    `<p class="lead-moved-head"><span>Toward Dire</span><span>${UNIT[kind] === "gold" ? "Gold" : "XP"}, by source</span><span>Toward Radiant</span></p>` +
    `<ol class="lead-rows">${rows.map(bar).join("")}</ol>`
  );
}

/** Each team's heroes, with what each earned in the stretch. */
export function heroesMarkup(rows: HeroRow[], kind: Kind): string {
  const top = Math.max(1, ...rows.map((r) => r.total));
  const team = (side: Side) => {
    const mine = rows.filter((r) => r.side === side);
    const total = mine.reduce((s, r) => s + r.total, 0);
    const heroes = mine
      .map(
        (r) =>
          `<li><span class="lead-hero-name">${escape(r.name)}</span>` +
          `<span class="lead-hero-bar">${r.parts.map((v, k) => `<i class="lead-part-${k}" style="width: ${((Math.max(0, v) / top) * 100).toFixed(2)}%"></i>`).join("")}</span>` +
          `<span class="lead-hero-value">${amount(r.total)}</span></li>`,
      )
      .join("");
    return `<div class="lead-team"><p class="lead-team-name lead-team-name--${side === "r" ? "radiant" : "dire"}">${TEAM[side]} · ${amount(total)} ${UNIT[kind]}</p><ol class="lead-heroes">${heroes}</ol></div>`;
  };
  const key =
    kind === "gold"
      ? HERO_GROUPS.map((label, k) => `<li class="legend-item"><i class="lead-part-${k}" aria-hidden="true"></i>${label}</li>`).join("")
      : `<li class="legend-item"><i class="lead-part-0" aria-hidden="true"></i>XP earned</li>`;
  return `<ul class="legend lead-hero-key" aria-label="Legend">${key}</ul><div class="lead-teams">${team("r")}${team("d")}</div>`;
}

/** Where the lead changed hands, as HTML; with `fightsUrl`, the fights in that minute are links. */
export function flipsMarkup(data: LeadData, list: Flip[], fightsUrl: string | null): string {
  if (!list.length) return "The lead didn't change hands in this stretch.";
  return list
    .map((flip) => {
      const fights = flip.fights.map((n) => (fightsUrl ? `<a href="${fightsUrl}#fight-${n}">fight ${n}</a>` : `fight ${n}`)).join(", ");
      const since = clock(data.times[flip.reading - 1]);
      return `<span>${clock(data.times[flip.reading])} ${TEAM[flip.ahead]} ahead${fights ? ` (${fights} since ${since})` : ""}</span>`;
    })
    .join(" · ");
}

/**
 * The stacks recipe's figure, rendered into the Markdown page at build time by
 * `::: figure stacks`: one row per player on the game clock, each stack a bar
 * split by who killed its creeps; the stacked camps on the map with the
 * most-stacked camp's stacks listed; and each player's numbers, then a caption
 * from the page. With JavaScript, src/lib/stacks-figure.ts adds the controls and
 * links the parts: picking a stack, a camp or a player shows its stacks in each.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import home from "../data/home.json";
import stacksJson from "../data/stacks.json";
import { campMarkup, campsMarkup, firstCamp, playersMarkup, rowsMarkup, segments, type Outcome, type StacksData } from "../lib/stacks-data";

const data = stacksJson as unknown as StacksData;
const points = (list: number[][]) => list.map(([x, y]) => `${x},${y}`).join(" ");
const CAMP_TYPES = ["small", "medium", "large", "ancient"];
const OUTCOMES: [Outcome, string][] = [
  ["self", "Killed by the stacker"],
  ["team", "by a teammate"],
  ["enemy", "by the enemy"],
  ["player", "by a player (no stacker credited)"],
  ["pulled", "pulled by lane creeps"],
  ["none", "by no player"],
];

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function stacksFigure(base: string): { open: string; close: string } {
  const assets = `${base.replace(/\/$/, "")}/figures/`;
  const first = firstCamp(data);
  const open = [
    `<figure class="fig recipe-fig stacks-fig" data-recipe-figure="stacks" data-pagefind-ignore>`,
    `<p class="stacks-sub">Each stack at its time, as tall as its creeps, split by who killed them</p>`,
    `<div class="stacks-controls" data-controls></div>`,
    `<div data-rows>${rowsMarkup(data, "stacker")}</div>`,
    `<p class="stacks-sub">The stacked camps</p>`,
    `<div class="stacks-fig-body">`,
    `<svg class="map stacks-map" viewBox="0 0 1000 1000" role="group" aria-label="The stacked camps on the map; pick one to list its stacks">`,
    `<image href="${assets}map.webp" width="1000" height="1000" preserveAspectRatio="xMidYMid slice"></image>`,
    `<rect class="map-dim" width="1000" height="1000"></rect>`,
    `<polyline class="map-half" points="${points(home.map.half_line)}"></polyline>`,
    `<g data-camps>${campsMarkup(data, first)}</g>`,
    `</svg>`,
    `<div class="stacks-camp-panel" data-camp-panel aria-live="polite">${campMarkup(data, first)}</div>`,
    `</div>`,
    `<p class="stacks-sub">Each player</p>`,
    playersMarkup(data),
    `<figcaption>`,
  ].join("");
  const shown = new Set(data.stacks.flatMap((stack) => segments(stack).map((s) => s.outcome)));
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    ...OUTCOMES.filter(([outcome]) => shown.has(outcome)).map(
      ([outcome, label]) => `<li class="legend-item"><i class="stacks-seg stacks-seg--${outcome}" aria-hidden="true"></i>${label}</li>`,
    ),
    ...CAMP_TYPES.map((type) => `<li class="legend-item" style="--camp: var(--camp-${type})"><i aria-hidden="true"></i>${type}</li>`),
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

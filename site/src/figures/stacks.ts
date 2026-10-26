/**
 * The stacks recipe's figure, rendered into the Markdown page at build time by
 * `::: figure stacks`: who stacked for whom, the stacked camps on the map with
 * the most-stacked camp's stacks listed, when each stack was made, and each
 * player's numbers, then a caption from the page. With JavaScript,
 * src/lib/stacks-figure.ts lists the stacks of the camp picked on the map.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import home from "../data/home.json";
import stacksJson from "../data/stacks.json";
import { campMarkup, campsMarkup, firstCamp, flowsMarkup, playersMarkup, timelineMarkup, type StacksData } from "../lib/stacks-data";

const data = stacksJson as unknown as StacksData;
const points = (list: number[][]) => list.map(([x, y]) => `${x},${y}`).join(" ");
const CAMP_TYPES = ["small", "medium", "large", "ancient"];

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function stacksFigure(base: string): { open: string; close: string } {
  const assets = `${base.replace(/\/$/, "")}/figures/`;
  const first = firstCamp(data);
  const open = [
    `<figure class="fig recipe-fig stacks-fig" data-recipe-figure="stacks" data-pagefind-ignore>`,
    `<p class="stacks-sub">Who stacked for whom: stacked creeps, by stacker and by who killed them</p>`,
    flowsMarkup(data),
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
    `<p class="stacks-sub">When each camp was stacked</p>`,
    timelineMarkup(data),
    `<p class="stacks-sub">Each player</p>`,
    playersMarkup(data),
    `<figcaption>`,
  ].join("");
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    ...CAMP_TYPES.map((type) => `<li class="legend-item" style="--camp: var(--camp-${type})"><i aria-hidden="true"></i>${type}</li>`),
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire</li>`,
    `<li class="legend-item stacks-legend-enemy"><i aria-hidden="true"></i>Killed by the enemy</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

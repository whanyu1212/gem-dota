/**
 * The lanes recipe's figure, rendered into the Markdown page at build time by
 * `::: figure lanes`: each lane's heroes, each side's numbers at 6:00 and what
 * happened in the lane up to then, then a caption from the page. With
 * JavaScript, src/lib/lanes-figure.ts adds the switch to the 10:00 reading.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import lanesJson from "../data/lanes.json";
import { figureMarkup, type LanesData } from "../lib/lanes-data";

const data = lanesJson as unknown as LanesData;

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML. */
export function lanesFigure(): { open: string; close: string } {
  const open = [
    `<figure class="fig recipe-fig lanes-fig" data-recipe-figure="lanes" data-pagefind-ignore>`,
    `<div class="lanes-fig-controls" data-controls hidden></div>`,
    `<div data-lanes>${figureMarkup(data, data.readings[0])}</div>`,
    `<figcaption>`,
  ].join("");
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

/**
 * The runes recipe's figure, rendered into the Markdown page at build time by
 * `::: figure runes`: each side's runes by kind over the whole match, the four
 * rune spots on the map with each side's runes taken there, the 0:00 bounties,
 * every power rune with what happened while it lasted, and who took them, then
 * a caption from the page. With JavaScript, src/lib/runes-figure.ts adds the
 * stage chips and a timeline to pick a stretch on.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import home from "../data/home.json";
import runesJson from "../data/runes.json";
import { openersMarkup, stretchMarkup, type RunesData } from "../lib/runes-data";

const data = runesJson as unknown as RunesData;
const points = (list: number[][]) => list.map(([x, y]) => `${x},${y}`).join(" ");
/** The map crop around the four spots: the middle of the map square. */
const VIEW = "143 202 660 660";

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function runesFigure(base: string): { open: string; close: string } {
  const assets = `${base.replace(/\/$/, "")}/figures/`;
  const shown = stretchMarkup(data, null);
  const open = [
    `<figure class="fig recipe-fig runes-fig" data-recipe-figure="runes" data-pagefind-ignore>`,
    `<div class="runes-fig-controls" data-controls hidden></div>`,
    `<div class="runes-fig-strip" data-timeline hidden></div>`,
    `<div class="runes-fig-body">`,
    `<div data-counts>${shown.counts}</div>`,
    `<svg class="map runes-map" viewBox="${VIEW}" role="img" aria-label="The rune spots, with each side's runes taken there">`,
    `<image href="${assets}map.webp" width="1000" height="1000" preserveAspectRatio="xMidYMid slice"></image>`,
    `<rect class="map-dim" width="1000" height="1000"></rect>`,
    `<polyline class="map-half" points="${points(home.map.half_line)}"></polyline>`,
    `<g data-spots>${shown.spots}</g>`,
    `</svg>`,
    `</div>`,
    `<p class="runes-sub">The 0:00 bounties</p>`,
    openersMarkup(data),
    `<p class="runes-sub">Power runes, and what happened while each lasted</p>`,
    `<div data-windows>${shown.windows}</div>`,
    `<p class="runes-sub">Who took the power runes</p>`,
    `<div data-takers>${shown.takers}</div>`,
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

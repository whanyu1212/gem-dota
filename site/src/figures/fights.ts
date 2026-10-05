/**
 * The fights recipe's figure, rendered into the Markdown page at build time by
 * `::: figure fights`: the map with every fight, sized by deaths and coloured by
 * the side with more kills, and a caption from the page. With JavaScript,
 * src/lib/fights-figure.ts adds the size filter, the timeline, the list, each
 * fight's card, and its breakdown (with a playback for the bigger fights) in
 * Figure 3's player.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import home from "../data/home.json";
import index from "../data/fights/index.json";
import { fightDots, type FightsData } from "../lib/fights-data";

const data = index as unknown as FightsData;
const points = (list: number[][]) => list.map(([x, y]) => `${x},${y}`).join(" ");

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function fightsFigure(base: string): { open: string; close: string } {
  const assets = `${base.replace(/\/$/, "")}/figures/`;
  const open = [
    `<figure class="fig recipe-fig fights-fig" data-recipe-figure="fights" data-assets="${assets}" data-pagefind-ignore>`,
    `<div class="fights-fig-controls" data-controls hidden></div>`,
    `<div class="fights-fig-body">`,
    `<svg class="map" viewBox="0 0 1000 1000" role="img" aria-label="The fights on the map">`,
    `<image href="${assets}map.webp" width="1000" height="1000" preserveAspectRatio="xMidYMid slice"></image>`,
    `<rect class="map-dim" width="1000" height="1000"></rect>`,
    `<polyline class="map-half" points="${points(home.map.half_line)}"></polyline>`,
    `<g data-fights>${fightDots(data.fights)}</g>`,
    `</svg>`,
    `<div class="fights-fig-side" data-side hidden></div>`,
    `</div>`,
    `<div class="fights-fig-strip" data-timeline hidden></div>`,
    `<div class="fights-fig-list" data-list hidden></div>`,
    `<div class="fights-fig-panel" data-panel hidden></div>`,
    `<figcaption>`,
  ].join("");
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant had more kills</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire had more kills</li>`,
    `<li class="legend-item team-even"><i aria-hidden="true"></i>Even</li>`,
    `<li class="legend-item"><i class="swatch-size" aria-hidden="true"></i>Size: deaths in the fight</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

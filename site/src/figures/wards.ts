/**
 * The wards recipe's figure, rendered into the Markdown page at build time by
 * the `::: figure wards` directive (src/markdown/preprocess.ts): the map with
 * the wards up in the stretch it opens on, and a caption from the page. With
 * JavaScript, src/lib/wards-figure.ts takes over and adds the filters, the
 * timeline to pick a stretch on, the counts and the list.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to wards.json alone would not reach it: `npm run build` passes --force.
 */
import home from "../data/home.json";
import wardsJson from "../data/wards.json";
import { BADGE, wardMarkup, wardsIn, type WardsData } from "../lib/wards-data";

const data = wardsJson as unknown as WardsData;

const points = (list: number[][]) => list.map(([x, y]) => `${x},${y}`).join(" ");

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function wardsFigure(base: string): { open: string; close: string } {
  const assets = `${base.replace(/\/$/, "")}/figures/`;
  const shown = wardsIn(data, data.range);
  const open = [
    `<figure class="fig recipe-fig ward-fig" data-recipe-figure="wards" data-assets="${assets}" data-pagefind-ignore>`,
    `<div class="ward-fig-controls" data-controls hidden></div>`,
    `<div class="ward-fig-body">`,
    `<svg class="map" viewBox="0 0 1000 1000" role="img" aria-label="The wards on the map">`,
    `<defs><clipPath id="wards-badge" clipPathUnits="userSpaceOnUse"><circle r="${BADGE}"></circle></clipPath></defs>`,
    `<image href="${assets}map.webp" width="1000" height="1000" preserveAspectRatio="xMidYMid slice"></image>`,
    `<rect class="map-dim" width="1000" height="1000"></rect>`,
    `<polyline class="map-half" points="${points(home.map.half_line)}"></polyline>`,
    `<g data-wards>${wardMarkup(data, shown, data.range, assets)}</g>`,
    `</svg>`,
    `<div class="ward-fig-side" data-side hidden></div>`,
    `</div>`,
    `<div class="ward-fig-list" data-list hidden></div>`,
    `<div class="ward-fig-strip" data-strip hidden></div>`,
    `<figcaption>`,
  ].join("");
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    `<li class="legend-item"><img src="${assets}ward_observer.png" alt="" width="18" height="18">Observer</li>`,
    `<li class="legend-item"><img src="${assets}ward_sentry.png" alt="" width="18" height="18">Sentry</li>`,
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire</li>`,
    `<li class="legend-item"><i class="swatch-vision" aria-hidden="true"></i>Observer vision (the model's circle)</li>`,
    `<li class="legend-item"><i class="swatch-killed" aria-hidden="true"></i>Killed in the stretch</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

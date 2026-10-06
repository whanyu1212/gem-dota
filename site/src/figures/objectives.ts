/**
 * The objectives recipe's figure, rendered into the Markdown page at build time
 * by `::: figure objectives`: the map with every building as it stood at the
 * end of the match (the fallen crossed out), the Roshan and Tormentor kills and
 * the wisdom runes taken at each shrine, each team's conversion bars, and who
 * took each shrine's wisdom runes, then a caption from the page. With
 * JavaScript, src/lib/objectives-figure.ts adds the kind filter, the timeline,
 * the list, each objective's card, and the edges behind each bar.
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import home from "../data/home.json";
import objectivesJson from "../data/objectives.json";
import { KINDS, mapMarkup, objectivesIn, tallyMarkup, wisdomMarkup, type ObjectivesData } from "../lib/objectives-data";

const data = objectivesJson as unknown as ObjectivesData;
const points = (list: number[][]) => list.map(([x, y]) => `${x},${y}`).join(" ");

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function objectivesFigure(base: string): { open: string; close: string } {
  const assets = `${base.replace(/\/$/, "")}/figures/`;
  const shown = objectivesIn(data, null, new Set(KINDS.map(([kind]) => kind)));
  const open = [
    `<figure class="fig recipe-fig objectives-fig" data-recipe-figure="objectives" data-fights="${base.replace(/\/$/, "")}/cookbook/fights" data-pagefind-ignore>`,
    `<div class="objectives-fig-controls" data-controls hidden></div>`,
    `<div class="objectives-fig-body">`,
    `<svg class="map" viewBox="0 0 1000 1000" role="img" aria-label="The objectives on the map">`,
    `<image href="${assets}map.webp" width="1000" height="1000" preserveAspectRatio="xMidYMid slice"></image>`,
    `<rect class="map-dim" width="1000" height="1000"></rect>`,
    `<polyline class="map-half" points="${points(home.map.half_line)}"></polyline>`,
    `<g data-objectives>${mapMarkup(data, null, shown, null)}</g>`,
    `</svg>`,
    `<div class="objectives-fig-side" data-side hidden></div>`,
    `</div>`,
    `<div class="objectives-fig-strip" data-timeline hidden></div>`,
    `<div class="objectives-fig-list" data-list hidden></div>`,
    `<div class="objectives-fig-tally">`,
    `<p class="tally-head">Did each team convert its edges?</p>`,
    `<div class="tally-teams" data-tally>${tallyMarkup(data.edges)}</div>`,
    `<p class="tally-hint" data-tally-hint hidden>Click a bar segment to list its edges.</p>`,
    `<ol class="tally-list" data-tally-list hidden></ol>`,
    `</div>`,
    `<div class="objectives-fig-tally">`,
    `<p class="tally-head">Who took each wisdom rune?</p>`,
    `<div class="tally-teams">${wisdomMarkup(data.wisdom)}</div>`,
    `<p class="tally-hint"><i class="wisdom-key tally-seg--o" aria-hidden="true"></i>Not taken before the next spawn <i class="wisdom-key tally-seg--n" aria-hidden="true"></i>Not taken before the game ended</p>`,
    `</div>`,
    `<figcaption>`,
  ].join("");
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    `<li class="legend-item"><i class="swatch-tower" aria-hidden="true"></i>Tower</li>`,
    `<li class="legend-item"><i class="swatch-barracks" aria-hidden="true"></i>Barracks</li>`,
    `<li class="legend-item"><i class="swatch-boss" aria-hidden="true">R</i>Roshan, <i class="swatch-boss" aria-hidden="true">T</i>Tormentor (in the colour of the side that killed it)</li>`,
    `<li class="legend-item"><i class="swatch-boss" aria-hidden="true">W</i>Wisdom-rune shrine, <i class="swatch-rune" aria-hidden="true"></i>a rune taken there (in the colour of the side that took it)</li>`,
    `<li class="legend-item"><i class="swatch-fallen" aria-hidden="true"></i>Fallen</li>`,
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

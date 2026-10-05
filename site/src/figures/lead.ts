/**
 * The lead recipe's figure, rendered into the Markdown page at build time by
 * `::: figure lead`: the gold lead over the whole match with the fights and
 * objectives under it, what moved it by source, each hero's gold, and where it
 * changed hands, then a caption from the page. With JavaScript,
 * src/lib/lead-figure.ts adds the gold/XP switch, picking a stretch, and the
 * links to the fights page (which opens a linked fight from its own script).
 *
 * Astro caches a page's rendered Markdown by the page's own text, so a change
 * to the data alone would not reach it: `npm run build` passes --force.
 */
import leadJson from "../data/lead.json";
import {
  axisMarkup,
  curveMarkup,
  flips,
  flipsMarkup,
  heroesMarkup,
  heroRows,
  marksMarkup,
  moved,
  movedMarkup,
  summary,
  ticksMarkup,
  type LeadData,
} from "../lib/lead-data";

const data = leadJson as unknown as LeadData;

/** The figure's opening HTML (through `<figcaption>`) and its closing HTML, for a site at `base`. */
export function leadFigure(base: string): { open: string; close: string } {
  const fights = `${base.replace(/\/$/, "")}/cookbook/fights`;
  const [a, b] = [0, data.times.length - 1];
  const open = [
    `<figure class="fig recipe-fig lead-fig" data-recipe-figure="lead" data-fights="${fights}" data-pagefind-ignore>`,
    `<div class="lead-fig-controls" data-controls hidden></div>`,
    `<div class="lead-chart">`,
    `<div class="lead-axis" data-axis aria-hidden="true">${axisMarkup(data, "gold")}</div>`,
    `<div class="lead-plot">`,
    `<div class="lead-curve-box">`,
    `<svg class="lead-curve" viewBox="0 0 1000 200" preserveAspectRatio="none" role="img" aria-label="Radiant's gold lead over the match" data-curve>${curveMarkup(data, "gold")}</svg>`,
    `<span class="lead-side lead-side--radiant" aria-hidden="true">Radiant ahead</span>`,
    `<span class="lead-side lead-side--dire" aria-hidden="true">Dire ahead</span>`,
    `</div>`,
    `<div class="lead-marks" data-marks>${marksMarkup(data, null)}</div>`,
    `<div class="ward-ticks" aria-hidden="true">${ticksMarkup(data)}</div>`,
    `</div>`,
    `</div>`,
    `<p class="lead-summary" data-summary>${summary(data, "gold", a, b)}</p>`,
    `<div class="lead-moved" data-moved>${movedMarkup(moved(data, "gold", a, b), "gold")}</div>`,
    `<p class="lead-head">Who earned it</p>`,
    `<div data-heroes>${heroesMarkup(heroRows(data, "gold", a, b), "gold")}</div>`,
    `<p class="lead-head">Where the lead changed hands</p>`,
    `<p class="lead-flips" data-flips>${flipsMarkup(data, flips(data, "gold", a, b), null)}</p>`,
    `<figcaption>`,
  ].join("");
  const legend = [
    `<ul class="legend" aria-label="Legend">`,
    `<li class="legend-item team-radiant"><i aria-hidden="true"></i>Radiant</li>`,
    `<li class="legend-item team-dire"><i aria-hidden="true"></i>Dire</li>`,
    `<li class="legend-item"><i class="swatch-lead-fight" aria-hidden="true"></i>A fight, sized by deaths, in the colour of the side with more kills (grey: even)</li>`,
    `<li class="legend-item"><i class="swatch-lead-obj" aria-hidden="true"></i>An objective, in the colour of the side it counted for</li>`,
    `</ul>`,
  ].join("");
  return { open, close: `${legend}</figcaption></figure>` };
}

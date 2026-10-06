/**
 * The runes recipe's figure in the browser. The page already shows the whole
 * match (src/figures/runes.ts); this adds the stage chips and a timeline of the
 * runes to drag a stretch on. A chip and a drag set the same stretch: the
 * counts, the spots, the power runes and their takers follow it. The 0:00
 * bounties stay.
 */
import { attachRangePicker, placeRange, type TimeRange } from "./range-picker";
import { clock, isPower, stageRange, stretchMarkup, type RunesData } from "./runes-data";

const SVG = "http://www.w3.org/2000/svg";
/** A drag on the timeline shorter than this is a click. */
const MIN_RANGE_S = 20;

function el<K extends keyof HTMLElementTagNameMap>(tag: K, attrs: Record<string, string> = {}, ...children: (Node | string)[]) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  node.append(...children);
  return node;
}
function svgEl(tag: string, attrs: Record<string, string | number>, parent: Element) {
  const node = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  parent.append(node);
  return node;
}

export function mountRunesFigure(figure: HTMLElement, data: RunesData): void {
  const $ = <T extends Element>(selector: string) => figure.querySelector<T>(selector)!;
  let range: TimeRange | null = null;

  // --- Stage chips: each sets the stretch to its stage; the pill shows a dragged one ---
  const controls = $<HTMLElement>("[data-controls]");
  const presets: [string, TimeRange | null][] = [["Whole match", null], ...data.stages.map((stage) => [stage[0].replace("-", "–"), stageRange(data, stage)] as [string, TimeRange])];
  const chips = presets.map(([label, preset]) => {
    const button = el("button", { type: "button", class: "chip" }, label);
    button.addEventListener("click", () => {
      range = preset;
      render();
    });
    return { button, preset };
  });
  const pill = el("button", { type: "button", class: "chip range-pill", "aria-pressed": "true", hidden: "" });
  pill.addEventListener("click", () => {
    range = null;
    render();
  });
  controls.append(el("span", { class: "chip-label" }, "Stage"), ...chips.map((c) => c.button), pill);

  // --- The timeline: Radiant's runes above the line, Dire's below; power runes tall ---
  const strip = $<HTMLElement>("[data-timeline]");
  const timeline = document.createElementNS(SVG, "svg") as SVGSVGElement;
  timeline.setAttribute("viewBox", "0 0 1000 72");
  timeline.setAttribute("preserveAspectRatio", "none");
  timeline.setAttribute("aria-hidden", "true");
  const rangeRect = svgEl("rect", { class: "strip-range", y: 0, height: 72, visibility: "hidden" }, timeline) as SVGRectElement;
  svgEl("line", { class: "strip-axis", x1: 0, x2: 1000, y1: 36, y2: 36 }, timeline);
  const x = (s: number) => ((s - data.start_s) / (data.end_s - data.start_s)) * 1000;
  const marks = data.runes
    .filter((row) => row[5] && (row[3] === "picked_up" || row[3] === "bottled"))
    .map((row) => {
      const power = isPower(row[1]);
      const above = row[5] === "r";
      const height = power ? 26 : 12;
      const y = above ? 36 - height - 2 : 38;
      const mark = svgEl("rect", { class: `runes-mark runes-mark--${above ? "radiant" : "dire"}${power ? " runes-mark--power" : ""}`, x: x(row[0]) - 1.5, y, width: 3, height }, timeline);
      return { mark, t: row[0] };
    });
  const ticks = el("div", { class: "ward-ticks", "aria-hidden": "true" });
  for (let s = 0; s <= data.end_s; s += 600) {
    const classes = [(s / 600) % 2 ? "ward-tick--minor" : "", x(s) < 40 ? "ward-tick--edge" : ""].filter(Boolean);
    ticks.append(el("span", { style: `left: ${x(s) / 10}%`, class: classes.join(" ") }, clock(s)));
  }
  strip.append(
    el(
      "p",
      { class: "strip-label" },
      "Runes taken over the match",
      el("span", {}, "Radiant's above, Dire's below; power runes tall"),
      el("span", { class: "strip-hint" }, "Drag to pick a stretch; click for the whole match"),
    ),
    timeline,
    ticks,
  );
  attachRangePicker(timeline, {
    min: data.start_s,
    max: data.end_s,
    minSpan: MIN_RANGE_S,
    onRange(r) {
      range = r;
      render();
    },
    onClick() {
      range = null;
      render();
    },
  });

  const parts = {
    counts: $<HTMLElement>("[data-counts]"),
    spots: $<SVGGElement>("[data-spots]"),
    windows: $<HTMLElement>("[data-windows]"),
    takers: $<HTMLElement>("[data-takers]"),
  };
  const same = (a: TimeRange | null, b: TimeRange | null) => (a === null ? b === null : b !== null && a[0] === b[0] && a[1] === b[1]);

  function render() {
    const shown = stretchMarkup(data, range);
    parts.counts.innerHTML = shown.counts;
    parts.spots.innerHTML = shown.spots;
    parts.windows.innerHTML = shown.windows;
    parts.takers.innerHTML = shown.takers;
    placeRange(rangeRect, range, data.start_s, data.end_s);
    const preset = chips.find((c) => same(c.preset, range));
    for (const c of chips) c.button.setAttribute("aria-pressed", String(c === preset));
    pill.hidden = preset !== undefined;
    if (!preset && range) {
      const label = `${clock(range[0])}–${clock(range[1])}`;
      pill.textContent = `${label} ✕`;
      pill.setAttribute("aria-label", `Show the whole match instead of ${label}`);
    }
    for (const { mark, t } of marks) mark.classList.toggle("is-out", range !== null && (t < range[0] || t >= range[1]));
  }

  controls.hidden = false;
  strip.hidden = false;
  render();
}

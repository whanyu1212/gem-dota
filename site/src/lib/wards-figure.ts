/**
 * The wards recipe's figure in the browser. The page already shows the map with
 * the wards up in the stretch it opens on (src/figures/wards.ts); this adds the
 * team and type filters, a timeline of wards up each minute to pick another
 * stretch on (drag; a click goes back to the whole match), the counts for the
 * stretch, and a list of its wards. Clicking a ward, on the map or in the list,
 * tells its story.
 */
import { attachRangePicker, placeRange, type TimeRange } from "./range-picker";
import {
  ALL,
  clock,
  counts,
  perMinute,
  story,
  TEAM_NAMES,
  wardMarkup,
  wardsIn,
  type WardFilter,
  type WardsData,
} from "./wards-data";

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

export function mountWardsFigure(figure: HTMLElement, data: WardsData): void {
  const assets = figure.dataset.assets ?? "";
  const $ = <T extends Element>(selector: string) => figure.querySelector<T>(selector)!;
  const filter: WardFilter = { teams: new Set(ALL.teams), types: new Set(ALL.types) };
  let range: TimeRange | null = data.range;
  let selected: number | null = null;

  // --- Filters and the range pill ---
  const controls = $<HTMLElement>("[data-controls]");
  const chip = (label: string, toggle: () => boolean) => {
    const button = el("button", { type: "button", class: "chip", "aria-pressed": "true" }, label);
    button.addEventListener("click", () => {
      button.setAttribute("aria-pressed", String(toggle()));
      render();
    });
    return button;
  };
  const flip = <T>(set: Set<T>, value: T) => () => (set.has(value) ? (set.delete(value), false) : (set.add(value), true));
  const pill = el("button", { type: "button", class: "chip range-pill", "aria-pressed": "true" });
  pill.addEventListener("click", () => {
    range = null;
    render();
  });
  controls.append(
    chip("Radiant", flip(filter.teams, "r")),
    chip("Dire", flip(filter.teams, "d")),
    el("span", { class: "chip-gap", "aria-hidden": "true" }),
    chip("Observers", flip(filter.types, "o")),
    chip("Sentries", flip(filter.types, "s")),
    pill,
  );

  // --- Counts, story and list beside the map ---
  const side = $<HTMLElement>("[data-side]");
  const stats = el("div", { class: "ward-stats" });
  const storyEl = el("p", { class: "ward-story", "aria-live": "polite" });
  const list = el("ol", { class: "ward-list", "aria-label": "Wards in the stretch" });
  side.append(stats, storyEl);
  const listBox = $<HTMLElement>("[data-list]");
  listBox.append(list);

  // --- Selecting a ward, on the map or in the list ---
  const wardsLayer = $<SVGGElement>("[data-wards]");
  const select = (i: number) => {
    selected = selected === i ? null : i;
    render();
    list.querySelector(`[data-ward="${selected}"]`)?.scrollIntoView({ block: "nearest" });
  };
  wardsLayer.addEventListener("click", (event) => {
    const ward = (event.target as Element).closest("[data-ward]");
    if (ward) select(Number(ward.getAttribute("data-ward")));
  });
  wardsLayer.addEventListener("keydown", (event) => {
    const ward = (event.target as Element).closest("[data-ward]");
    if (ward && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      select(Number(ward.getAttribute("data-ward")));
    }
  });
  list.addEventListener("click", (event) => {
    const row = (event.target as Element).closest("[data-ward]");
    if (row) select(Number(row.getAttribute("data-ward")));
  });

  // --- The timeline: wards up each minute, Radiant above and Dire below ---
  const strip = $<HTMLElement>("[data-strip]");
  const label = el(
    "p",
    { class: "strip-label" },
    "Wards up each minute",
    el("span", {}, el("i", { class: "strip-key strip-key--radiant", "aria-hidden": "true" }), "Radiant above"),
    el("span", {}, el("i", { class: "strip-key strip-key--dire", "aria-hidden": "true" }), "Dire below"),
    el("span", { class: "strip-hint" }, "Drag to pick a stretch; click for the whole match"),
  );
  const timeline = document.createElementNS(SVG, "svg") as SVGSVGElement;
  timeline.setAttribute("viewBox", "0 0 1000 64");
  timeline.setAttribute("preserveAspectRatio", "none");
  timeline.setAttribute("aria-hidden", "true");
  const rangeRect = svgEl("rect", { class: "strip-range", y: 0, height: 64, visibility: "hidden" }, timeline) as SVGRectElement;
  const minutes = perMinute(data);
  const peak = Math.max(1, ...minutes.map((m) => Math.max(m.r, m.d)));
  const x = (s: number) => ((s - data.start_s) / (data.end_s - data.start_s)) * 1000;
  for (const minute of minutes) {
    const left = x(Math.max(minute.from, data.start_s));
    const width = Math.max(0.5, x(Math.min(minute.from + 60, data.end_s)) - left - 1);
    svgEl("rect", { class: "strip-radiant", x: left, y: 32 - (minute.r / peak) * 28, width, height: (minute.r / peak) * 28 }, timeline);
    svgEl("rect", { class: "strip-dire", x: left, y: 32, width, height: (minute.d / peak) * 28 }, timeline);
  }
  svgEl("line", { class: "strip-axis", x1: 0, x2: 1000, y1: 32, y2: 32 }, timeline);
  const ticks = el("div", { class: "ward-ticks", "aria-hidden": "true" });
  for (let s = 0; s <= data.end_s; s += 600) {
    // A label near the left edge starts at its tick instead of centring on it.
    const classes = [(s / 600) % 2 ? "ward-tick--minor" : "", x(s) < 40 ? "ward-tick--edge" : ""].filter(Boolean);
    ticks.append(el("span", { style: `left: ${x(s) / 10}%`, class: classes.join(" ") }, clock(s)));
  }
  strip.append(label, timeline, ticks);
  attachRangePicker(timeline, {
    min: data.start_s,
    max: data.end_s,
    minSpan: MIN_RANGE_S,
    onRange(picked) {
      range = picked;
      render();
    },
    onClick() {
      range = null;
      render();
    },
  });

  function render() {
    const shown = wardsIn(data, range, filter);
    if (selected !== null && !shown.includes(selected)) selected = null;
    // Redrawing replaces the badges: keep the keyboard on the ward it was on.
    const focused = (document.activeElement as Element | null)?.closest?.("[data-wards] [data-ward]")?.getAttribute("data-ward");
    wardsLayer.innerHTML = wardMarkup(data, shown, range, assets, selected);
    if (focused) wardsLayer.querySelector<SVGGElement>(`[data-ward="${focused}"]`)?.focus();
    placeRange(rangeRect, range, data.start_s, data.end_s);
    const label = range ? `${clock(range[0])}–${clock(range[1])}` : "Whole match";
    pill.textContent = range ? `${label} ✕` : label;
    pill.setAttribute("aria-pressed", String(range !== null));
    pill.setAttribute("aria-label", range ? `Show the whole match instead of ${label}` : "Showing the whole match");

    const c = counts(data, shown, range);
    const stat = (n: number, what: string) => el("div", { class: "ward-stat" }, el("b", {}, String(n)), el("span", {}, what));
    stats.replaceChildren(
      stat(c.observers, "observers up"),
      stat(c.sentries, "sentries up"),
      stat(c.placed, range ? "placed in the stretch" : "placed"),
      stat(c.killed, range ? "killed in the stretch" : "killed"),
    );
    storyEl.textContent = selected !== null ? story(data.wards[selected]) : "Click a ward, on the map or below, for its story.";

    list.replaceChildren(
      ...shown.map((i) => {
        const w = data.wards[i];
        const team = w[0] === "r" ? "radiant" : "dire";
        const end = w[6] === "k" ? `killed by ${w[8]} ${w[10]}` : w[6] === "e" ? `expired ${w[10]}` : "up at the end";
        return el(
          "li",
          {},
          el(
            "button",
            { type: "button", "data-ward": String(i), "aria-pressed": String(i === selected), title: story(w) },
            el("time", {}, w[9]),
            el("span", { class: `ward-mark ward-mark--${team}`, "aria-label": `${TEAM_NAMES[w[0]]} ${w[1] === "o" ? "observer" : "sentry"}` }, w[1] === "o" ? "●" : "◆"),
            el("span", {}, `${w[7]} · ${end}`),
          ),
        );
      }),
    );
  }

  for (const part of [controls, side, listBox, strip]) part.hidden = false;
  render();
}

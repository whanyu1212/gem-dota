/**
 * The objectives recipe's figure in the browser. The page already shows the map
 * and each team's conversion bars (src/figures/objectives.ts); this adds a kind
 * filter, a timeline of objectives to pick a stretch on (drag; a click goes
 * back to the whole match), a list, each objective's card (who damaged it, and
 * a link to the fight before it on the fights page), and the edges behind each
 * bar segment.
 */
import {
  edgeLabel,
  edgeText,
  KINDS,
  mapMarkup,
  objectiveCard,
  objectivesIn,
  sideClass,
  tallyMarkup,
  TEAM,
  type Kind,
  type ObjectivesData,
} from "./objectives-data";
import { attachRangePicker, placeRange, type TimeRange } from "./range-picker";
import { clock } from "./wards-data";

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

export function mountObjectivesFigure(figure: HTMLElement, data: ObjectivesData): void {
  const fightsUrl = figure.dataset.fights ?? "";
  const $ = <T extends Element>(selector: string) => figure.querySelector<T>(selector)!;
  const kinds = new Set<Kind>(KINDS.map(([kind]) => kind));
  let range: TimeRange | null = null;
  let selected: number | null = null;
  let picked: string | null = null;

  // --- Kind filter and the range pill ---
  const controls = $<HTMLElement>("[data-controls]");
  const pill = el("button", { type: "button", class: "chip range-pill", "aria-pressed": "true", hidden: "" });
  pill.addEventListener("click", () => {
    range = null;
    render();
  });
  controls.append(
    el("span", { class: "chip-label" }, "Show"),
    ...KINDS.map(([kind, label]) => {
      const button = el("button", { type: "button", class: "chip", "aria-pressed": "true" }, label);
      button.addEventListener("click", () => {
        if (kinds.has(kind)) kinds.delete(kind);
        else kinds.add(kind);
        button.setAttribute("aria-pressed", String(kinds.has(kind)));
        render();
      });
      return button;
    }),
    pill,
  );

  // --- Picking an objective: on the map, the timeline or in the list ---
  const layer = $<SVGGElement>("[data-objectives]");
  const pickFrom = (event: Event) => {
    const target = (event.target as Element).closest("[data-objective]");
    if (!target) return;
    const i = Number(target.getAttribute("data-objective"));
    selected = selected === i ? null : i;
    render();
  };
  for (const host of [layer]) {
    host.addEventListener("click", pickFrom);
    host.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        pickFrom(event);
      }
    });
  }

  // --- The timeline: Radiant's losses above, Dire's below, bosses on the line ---
  const strip = $<HTMLElement>("[data-timeline]");
  const timeline = document.createElementNS(SVG, "svg") as SVGSVGElement;
  timeline.setAttribute("viewBox", "0 0 1000 72");
  timeline.setAttribute("preserveAspectRatio", "none");
  timeline.setAttribute("aria-hidden", "true");
  const rangeRect = svgEl("rect", { class: "strip-range", y: 0, height: 72, visibility: "hidden" }, timeline) as SVGRectElement;
  svgEl("line", { class: "strip-axis", x1: 0, x2: 1000, y1: 36, y2: 36 }, timeline);
  const x = (s: number) => ((s - data.start_s) / (data.end_s - data.start_s)) * 1000;
  const marks = data.objectives.map((o, i) => {
    const lost = o.for === "r" ? "d" : "r"; // a building is lost by the side it didn't count for
    const boss = o.kind === "roshan" || o.kind === "tormentor";
    const y = boss ? 36 : lost === "r" ? 14 : 58;
    const g = svgEl("g", { class: `obj-mark obj-mark--${sideClass(o.for)} obj-mark--${o.kind}`, "data-objective": i }, timeline);
    const cx = x(o.time_s);
    if (o.kind === "tower") svgEl("polygon", { points: `${cx},${y - 8} ${cx - 5},${y + 6} ${cx + 5},${y + 6}` }, g);
    else if (o.kind === "barracks") svgEl("rect", { x: cx - 4, y: y - 6, width: 8, height: 12 }, g);
    else svgEl("rect", { x: cx - 3, y: y - 9, width: 6, height: 18, rx: 3 }, g);
    return { i, g };
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
      "Objectives over the match",
      el("span", {}, "Radiant's losses above, Dire's below; Roshan and Tormentor on the line"),
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
    onClick(at) {
      // A click on an objective's mark picks it; anywhere else, the whole match.
      const near = data.objectives
        .map((o, i) => [Math.abs(o.time_s - at), i] as const)
        .filter(([gap, i]) => gap < (data.end_s - data.start_s) / 200 && kinds.has(data.objectives[i].kind))
        .sort((a, b) => a[0] - b[0])[0];
      if (near) selected = near[1];
      else range = null;
      render();
    },
  });

  // --- Card beside the map, and the list ---
  const side = $<HTMLElement>("[data-side]");
  const listBox = $<HTMLElement>("[data-list]");
  const list = el("ol", { class: "obj-list", "aria-label": "Objectives" });
  listBox.append(list);
  list.addEventListener("click", pickFrom);

  // --- The conversion bars and the edges behind a segment ---
  const tallyEl = $<HTMLElement>("[data-tally]");
  const hint = $<HTMLElement>("[data-tally-hint]");
  const edgeList = $<HTMLOListElement>("[data-tally-list]");
  tallyEl.addEventListener("click", (event) => {
    const segment = (event.target as Element).closest("[data-edges]");
    if (!segment) return;
    const key = segment.getAttribute("data-edges");
    picked = picked === key ? null : key;
    renderTally();
  });
  function renderTally() {
    tallyEl.innerHTML = tallyMarkup(data.edges, picked);
    const [team, edge, outcome] = (picked ?? "||").split("|");
    const rows = picked ? data.edges.filter((e) => e.team === team && e.edge === edge && e.outcome === outcome) : [];
    hint.textContent = picked ? `${rows.length} edges. Click the segment again to close.` : "Click a bar segment to list its edges.";
    edgeList.hidden = !picked;
    edgeList.replaceChildren(
      ...rows.map((e) =>
        el(
          "li",
          {},
          el(
            "span",
            { class: `tally-edge tally-edge--${e.team === "r" ? "radiant" : "dire"}` },
            `${TEAM[e.team]} · `,
            // A fight opens on the fights page; an Aegis is just its label.
            e.edge === "fight" ? el("a", { href: `${fightsUrl}#fight-${e.number}` }, edgeLabel(e)) : edgeLabel(e),
          ),
          el("span", { class: `tally-outcome tally-outcome--${e.outcome}` }, e.outcome === "c" ? "converted" : e.outcome === "o" ? "other side first" : "nothing"),
          el("span", {}, edgeText(e)),
        ),
      ),
    );
  }

  function render() {
    const shown = objectivesIn(data, range, kinds);
    if (selected !== null && !shown.includes(selected)) selected = null;
    layer.innerHTML = mapMarkup(data, range, shown, selected);
    placeRange(rangeRect, range, data.start_s, data.end_s);
    pill.hidden = range === null;
    if (range) {
      const label = `${clock(range[0])}–${clock(range[1])}`;
      pill.textContent = `${label} ✕`;
      pill.setAttribute("aria-label", `Show the whole match instead of ${label}`);
    }
    for (const { i, g } of marks) {
      g.classList.toggle("is-out", !shown.includes(i));
      g.classList.toggle("is-selected", i === selected);
    }

    side.replaceChildren();
    const o = selected !== null ? data.objectives[selected] : null;
    if (o) {
      const c = objectiveCard(o);
      side.append(el("p", { class: "obj-card-title" }, c.title), el("p", { class: "obj-card-line" }, c.line));
      if (o.damage.length) {
        const total = o.damage.reduce((sum, [, d]) => sum + d, 0);
        const bar = el("div", { class: "obj-damage" });
        const key = el("p", { class: "obj-damage-key" });
        o.damage.forEach(([who, d], k) => {
          bar.append(el("i", { class: `obj-damage-${k % 6}`, style: `flex: ${d}`, title: `${who}: ${d}` }));
          key.append(el("span", {}, el("i", { class: `obj-damage-${k % 6}`, "aria-hidden": "true" }), `${who} ${Math.round((100 * d) / total)}%`));
        });
        side.append(el("p", { class: "obj-card-line" }, "Damage to it in the 90 s before it fell"), bar, key);
        if (o.shared) side.append(el("p", { class: "obj-card-note" }, "Both tier 4s share a name in the combat log, so this is the damage to both."));
      }
      const after = el("p", { class: "obj-card-line" }, c.after);
      if (o.after) after.append(" ", el("a", { href: `${fightsUrl}#fight-${o.after[0]}` }, `Open fight ${o.after[0]} →`));
      side.append(after);
    } else {
      side.append(el("p", { class: "obj-card-line" }, "Pick an objective on the map, the timeline or the list for who took it and what came before."));
    }

    list.replaceChildren(
      el("li", { class: "obj-list-head" }, `${shown.length} objectives · ${shown.filter((i) => data.objectives[i].after).length} came within 2 minutes after a fight`),
      ...shown.map((i) => {
        const obj = data.objectives[i];
        return el(
          "li",
          {},
          el(
            "button",
            { type: "button", "data-objective": String(i), "aria-pressed": String(i === selected) },
            el("time", {}, obj.time),
            el("span", { class: `obj-list-side obj-list-side--${sideClass(obj.for)}` }, obj.for ? TEAM[obj.for] : "unknown"),
            el("span", {}, `${obj.name} · ${obj.last_hit}${obj.after ? ` · after fight ${obj.after[0]}` : ""}`),
          ),
        );
      }),
    );
  }

  for (const part of [controls, side, strip, listBox, hint]) part.hidden = false;
  render();
  renderTally();
}

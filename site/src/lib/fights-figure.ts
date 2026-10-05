/**
 * The fights recipe's figure in the browser. The page already shows every
 * fight on the map (src/figures/fights.ts); this adds a size filter, a timeline
 * of each fight's kills to pick a stretch on (drag; a click goes back to the
 * whole match), a list, and each fight's card. Picking a fight loads its data
 * and opens it in Figure 3's player below: the feed, the death recaps and the
 * damage timeline for every fight, and the map playback for the bigger ones.
 */
import { createPlayer, type View } from "./fight-player";
import { damageStrip, fightLegend, playbackControls } from "./fight-markup";
import type { FightData } from "./fight-playback";
import { card, fightDots, fightsIn, pickShown, score, type FightEntry, type FightsData } from "./fights-data";
import { attachRangePicker, placeRange, type TimeRange } from "./range-picker";
import { clock } from "./wards-data";

const SVG = "http://www.w3.org/2000/svg";
/** A drag on the timeline shorter than this is a click. */
const MIN_RANGE_S = 20;
const SIZES: [number, string][] = [
  [1, "All fights"],
  [2, "2+ deaths"],
  [3, "3+"],
  [5, "5+"],
];

// Each fight's data, loaded when it's picked. Figure 3's fight is fight.json.
const FILES = {
  ...import.meta.glob<{ default: FightData }>("../data/fights/[0-9]*.json"),
  "../data/fight.json": () => import("../data/fight.json") as unknown as Promise<{ default: FightData }>,
};
// Hero and item icons, as Figure 3 uses them.
const iconUrls = (found: Record<string, string>) =>
  Object.fromEntries(Object.entries(found).map(([path, url]) => [path.split("/").at(-1)!.replace(".png", ""), url]));
const ICONS = {
  heroes: iconUrls(import.meta.glob<string>("../assets/icons/heroes/*.png", { eager: true, query: "?url", import: "default" })),
  items: iconUrls(import.meta.glob<string>("../assets/icons/items/*.png", { eager: true, query: "?url", import: "default" })),
};

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

export function mountFightsFigure(figure: HTMLElement, data: FightsData): void {
  const assets = figure.dataset.assets ?? "";
  const $ = <T extends Element>(selector: string) => figure.querySelector<T>(selector)!;
  let minDeaths = 1;
  let range: TimeRange | null = null;
  // Open on the biggest fight: Figure 3's, on the home page.
  let selected: number | null = [...data.fights].sort((a, b) => b.deaths - a.deaths)[0]?.n ?? null;
  let player: ReturnType<typeof createPlayer> | undefined;
  let loading = 0;

  // --- Size filter and the range pill ---
  const controls = $<HTMLElement>("[data-controls]");
  const sizeButtons = SIZES.map(([n, label]) => {
    const button = el("button", { type: "button", class: "chip", "aria-pressed": String(n === minDeaths) }, label);
    button.addEventListener("click", () => {
      minDeaths = n;
      for (const [k, b] of sizeButtons.entries()) b.setAttribute("aria-pressed", String(SIZES[k][0] === n));
      render();
    });
    return button;
  });
  const pill = el("button", { type: "button", class: "chip range-pill", "aria-pressed": "true", hidden: "" });
  pill.addEventListener("click", () => {
    range = null;
    render();
  });
  controls.append(el("span", { class: "chip-label" }, "Show"), ...sizeButtons, pill);

  // --- The card beside the map ---
  const side = $<HTMLElement>("[data-side]");

  // --- Picking a fight: on the map, in the list, or on the timeline ---
  const dots = $<SVGGElement>("[data-fights]");
  const pick = (n: number) => {
    if (n === selected) return;
    selected = n;
    render();
    openPanel();
  };
  const pickFrom = (event: Event) => {
    const target = (event.target as Element).closest("[data-fight]");
    if (target) pick(Number(target.getAttribute("data-fight")));
  };
  dots.addEventListener("click", pickFrom);
  dots.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      pickFrom(event);
    }
  });

  // --- The timeline: each fight's kills, Radiant above and Dire below ---
  const strip = $<HTMLElement>("[data-timeline]");
  const timeline = document.createElementNS(SVG, "svg") as SVGSVGElement;
  timeline.setAttribute("viewBox", "0 0 1000 64");
  timeline.setAttribute("preserveAspectRatio", "none");
  timeline.setAttribute("aria-hidden", "true");
  const rangeRect = svgEl("rect", { class: "strip-range", y: 0, height: 64, visibility: "hidden" }, timeline) as SVGRectElement;
  const x = (s: number) => ((s - data.start_s) / (data.end_s - data.start_s)) * 1000;
  const peak = Math.max(1, ...data.fights.map((f) => Math.max(...f.kills)));
  const bars = data.fights.map((f) => {
    const g = svgEl("g", { class: "fight-bar" }, timeline);
    const left = x(f.start_s);
    const width = Math.max(4, x(f.start_s + f.duration) - left);
    svgEl("rect", { class: "strip-radiant", x: left, y: 32 - (f.kills[0] / peak) * 28, width, height: (f.kills[0] / peak) * 28 }, g);
    svgEl("rect", { class: "strip-dire", x: left, y: 32, width, height: (f.kills[1] / peak) * 28 }, g);
    return { f, g };
  });
  svgEl("line", { class: "strip-axis", x1: 0, x2: 1000, y1: 32, y2: 32 }, timeline);
  const ticks = el("div", { class: "ward-ticks", "aria-hidden": "true" });
  for (let s = 0; s <= data.end_s; s += 600) {
    const classes = [(s / 600) % 2 ? "ward-tick--minor" : "", x(s) < 40 ? "ward-tick--edge" : ""].filter(Boolean);
    ticks.append(el("span", { style: `left: ${x(s) / 10}%`, class: classes.join(" ") }, clock(s)));
  }
  strip.append(
    el(
      "p",
      { class: "strip-label" },
      "Kills in each fight",
      el("span", {}, el("i", { class: "strip-key strip-key--radiant", "aria-hidden": "true" }), "Radiant above"),
      el("span", {}, el("i", { class: "strip-key strip-key--dire", "aria-hidden": "true" }), "Dire below"),
      el("span", { class: "strip-hint" }, "Drag to pick a stretch; click for the whole match"),
    ),
    timeline,
    ticks,
  );
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

  // --- The list ---
  const listBox = $<HTMLElement>("[data-list]");
  const list = el("ol", { class: "fight-list", "aria-label": "Fights" });
  listBox.append(list);
  list.addEventListener("click", pickFrom);

  // --- The panel: the picked fight in Figure 3's player ---
  const panel = $<HTMLElement>("[data-panel]");
  async function openPanel() {
    const fight = data.fights.find((f) => f.n === selected);
    player?.destroy();
    player = undefined;
    panel.replaceChildren();
    if (!fight) return;
    const ticket = ++loading;
    const fightData = (await FILES[`../data/${fight.file}` as keyof typeof FILES]()).default;
    if (ticket !== loading) return; // another fight was picked meanwhile
    const box = fight.box ?? [0, 0, 1000];
    const [bx, by, size] = box;
    const view: View = { box: box as [number, number, number], px: size / 480, icons: ICONS };
    panel.innerHTML =
      `<p class="fights-panel-head">${fight.box ? "Its playback" : "Its breakdown"}: ${card(fight).title}</p>` +
      `<div class="fights-panel">` +
      `<div class="fights-panel-map">` +
      `<div class="fight-layers" data-layers hidden></div>` +
      `<svg class="map" viewBox="${bx} ${by} ${size} ${size}" data-map>` +
      `<defs><clipPath id="hero-badge" clipPathUnits="userSpaceOnUse"><circle r="${11 * view.px}"></circle></clipPath></defs>` +
      (fight.box ? `<image href="${assets}fights/${fight.n}.webp" x="${bx}" y="${by}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid slice"></image>` : "") +
      `<rect class="map-dim map-dim--fight" x="${bx}" y="${by}" width="${size}" height="${size}"></rect>` +
      `</svg>` +
      playbackControls(clock(fightData.start_s + fightData.duration)) +
      damageStrip() +
      fightLegend() +
      `</div>` +
      `<div class="fights-panel-feed">` +
      `<div class="fight-status" data-status hidden></div>` +
      `<div class="feed-filters" data-filters hidden></div>` +
      `<ol class="feed" data-feed hidden></ol>` +
      `</div></div>`;
    player = createPlayer(panel, view, fightData);
  }

  function render() {
    const shown = fightsIn(data, range, minDeaths);
    // A picked fight the filters leave out gives way to the biggest one left, or
    // to none (and an empty panel) when no fight is left.
    const next = pickShown(selected, shown);
    if (next !== selected) {
      selected = next;
      openPanel();
    }
    dots.innerHTML = fightDots(shown, selected);
    placeRange(rangeRect, range, data.start_s, data.end_s);
    pill.hidden = range === null;
    if (range) {
      const label = `${clock(range[0])}–${clock(range[1])}`;
      pill.textContent = `${label} ✕`;
      pill.setAttribute("aria-label", `Show the whole match instead of ${label}`);
    }
    for (const { f, g } of bars) {
      g.classList.toggle("is-out", f.deaths < minDeaths);
      g.classList.toggle("is-selected", f.n === selected);
    }

    const fight = data.fights.find((f) => f.n === selected);
    side.replaceChildren();
    if (fight) {
      const c = card(fight);
      side.append(
        el("p", { class: "fights-card-title" }, c.title),
        el("p", { class: `fights-card-kills fights-card-kills--${fight.more}` }, c.kills),
        el("p", { class: "fights-card-line" }, c.gold),
        el("p", { class: "fights-card-line" }, c.next),
        el("p", { class: "fights-card-line" }, fight.box ? "Below: its playback and breakdown." : "Below: its breakdown."),
      );
    } else {
      side.append(el("p", { class: "fights-card-line" }, "No fights here. Pick another stretch, or a smaller size."));
    }
    const counts = { r: 0, d: 0, x: 0 };
    for (const f of shown) counts[f.more]++;
    list.replaceChildren(
      el("li", { class: "fight-list-head" }, `${shown.length} fights · Radiant had more kills in ${counts.r}, Dire in ${counts.d}, even in ${counts.x}`),
      ...shown.map((f) =>
        el(
          "li",
          {},
          el(
            "button",
            { type: "button", "data-fight": String(f.n), "aria-pressed": String(f.n === selected) },
            el("time", {}, f.start),
            el("span", { class: `fight-score fight-score--${f.more}` }, score(f)),
            el("span", {}, `${f.deaths} death${f.deaths === 1 ? "" : "s"}${f.box ? " · playback" : ""}${f.next ? ` · then ${f.next[0]}` : ""}`),
          ),
        ),
      ),
    );
  }

  for (const part of [controls, side, strip, listBox, panel]) part.hidden = false;
  render();
  openPanel();
}

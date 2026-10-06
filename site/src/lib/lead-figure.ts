/**
 * The lead recipe's figure in the browser. The page already shows the gold
 * lead over the whole match and what moved it (src/figures/lead.ts); this adds
 * the gold/XP switch and picking a stretch: drag on the curve (snapped to the
 * readings, one a minute and the end of the game) and every part redraws for
 * it; a click goes back to the whole match. It also links each fight to the
 * fights page.
 */
import {
  axisMarkup,
  clock,
  curveMarkup,
  flips,
  flipsMarkup,
  heroesMarkup,
  heroRows,
  marksMarkup,
  moved,
  movedMarkup,
  readingAt,
  summary,
  type Kind,
  type LeadData,
} from "./lead-data";
import { attachRangePicker, placeRange } from "./range-picker";

/** A drag shorter than this (seconds) is a click. */
const MIN_RANGE_S = 30;

function el<K extends keyof HTMLElementTagNameMap>(tag: K, attrs: Record<string, string> = {}, ...children: (Node | string)[]) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  node.append(...children);
  return node;
}

export function mountLeadFigure(figure: HTMLElement, data: LeadData): void {
  const fightsUrl = figure.dataset.fights ?? "";
  const $ = <T extends Element>(selector: string) => figure.querySelector<T>(selector)!;
  const last = data.times.length - 1;
  let kind: Kind = "gold";
  let [a, b] = [0, last];

  // --- Gold or XP, and the range pill ---
  const controls = $<HTMLElement>("[data-controls]");
  const pill = el("button", { type: "button", class: "chip range-pill", "aria-pressed": "true", hidden: "" });
  pill.addEventListener("click", () => {
    [a, b] = [0, last];
    render();
  });
  const kinds: [Kind, string][] = [
    ["gold", "Gold lead"],
    ["xp", "XP lead"],
  ];
  const buttons = kinds.map(([k, label]) => {
    const button = el("button", { type: "button", class: "chip", "aria-pressed": String(k === kind) }, label);
    button.addEventListener("click", () => {
      kind = k;
      for (const [other, b2] of buttons) b2.setAttribute("aria-pressed", String(other === kind));
      render();
    });
    return [k, button] as const;
  });
  controls.append(el("span", { class: "chip-label" }, "Show"), ...buttons.map(([, button]) => button), pill);

  // --- Picking a stretch on the curve ---
  const curve = $<SVGSVGElement>("[data-curve]");
  const pick = (from: number, to: number) => {
    const [i, j] = [readingAt(data, from), readingAt(data, to)];
    if (i === j) return false;
    [a, b] = [Math.min(i, j), Math.max(i, j)];
    return true;
  };
  attachRangePicker(curve, {
    min: data.times[0],
    max: data.times[last],
    minSpan: MIN_RANGE_S,
    onRange([from, to]) {
      if (pick(from, to)) render();
    },
    onClick() {
      [a, b] = [0, last];
      render();
    },
  });

  function render() {
    const whole = a === 0 && b === last;
    curve.innerHTML = curveMarkup(data, kind) + `<rect class="strip-range" y="0" height="200" visibility="hidden"></rect>`;
    curve.setAttribute("aria-label", `Radiant's ${kind === "gold" ? "gold" : "XP"} lead over the match`);
    placeRange(curve.querySelector<SVGRectElement>(".strip-range")!, whole ? null : [data.times[a], data.times[b]], data.times[0], data.times[last]);
    $<HTMLElement>("[data-axis]").innerHTML = axisMarkup(data, kind);
    pill.hidden = whole;
    if (!whole) {
      const label = `${clock(data.times[a])}–${clock(data.times[b])}`;
      pill.textContent = `${label} ✕`;
      pill.setAttribute("aria-label", `Show the whole match instead of ${label}`);
    }
    $<HTMLElement>("[data-summary]").textContent = summary(data, kind, a, b);
    $<HTMLElement>("[data-moved]").innerHTML = movedMarkup(moved(data, kind, a, b), kind);
    $<HTMLElement>("[data-heroes]").innerHTML = heroesMarkup(heroRows(data, kind, a, b), kind);
    $<HTMLElement>("[data-flips]").innerHTML = flipsMarkup(data, flips(data, kind, a, b), fightsUrl);
  }

  $<HTMLElement>("[data-marks]").innerHTML = marksMarkup(data, fightsUrl);
  controls.hidden = false;
  render();
}

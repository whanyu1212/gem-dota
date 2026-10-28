/**
 * The stacks recipe's figure in the browser. The page already shows the rows by
 * stacker over the whole match and the most-stacked camp's stacks
 * (src/figures/stacks.ts); this adds chips to show the rows by killer or only
 * the first 30:00, and links the rows, the map and the table: hovering a stack,
 * a camp or a player shows its stacks in each, and a click keeps that and lists
 * them in the card. A second click, Escape or "Show all" lets go.
 */
import { axisEnd, campMarkup, firstCamp, isPicked, pickMarkup, playersIn, rowsMarkup, type Pick, type RowsBy, type StacksData } from "./stacks-data";

/** The stretch the rows open on: most stacks come early, and a whole match crowds them. */
const EARLY_S = 30 * 60;

const samePick = (a: Pick | null, b: Pick | null) => JSON.stringify(a) === JSON.stringify(b);

export function mountStacksFigure(figure: HTMLElement, data: StacksData): void {
  const controls = figure.querySelector<HTMLElement>("[data-controls]");
  const rowsHost = figure.querySelector<HTMLElement>("[data-rows]");
  const panel = figure.querySelector<HTMLElement>("[data-camp-panel]");
  const camps = [...figure.querySelectorAll<SVGGElement>("[data-camp]")];
  if (!controls || !rowsHost || !panel) return;
  const end = axisEnd(data);
  const resting = firstCamp(data);
  let by: RowsBy = "stacker";
  let shownTo = end > EARLY_S ? EARLY_S : end;
  let pinned: Pick | null = null;

  // --- Chips: rows by stacker or by killer; the first 30:00 or the whole match ---
  const chip = (label: string, onClick: () => void) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "chip";
    button.textContent = label;
    button.addEventListener("click", onClick);
    return button;
  };
  const label = (text: string) => {
    const span = document.createElement("span");
    span.className = "chip-label";
    span.textContent = text;
    return span;
  };
  const byChips: [RowsBy, HTMLButtonElement][] = [
    ["stacker", chip("By stacker", () => setBy("stacker"))],
    ["killer", chip("By killer", () => setBy("killer"))],
  ];
  const rangeChips: [number, HTMLButtonElement][] =
    end > EARLY_S ? [[EARLY_S, chip("First 30:00", () => setRange(EARLY_S))], [end, chip("Whole match", () => setRange(end))]] : [];
  const group = (text: string, chips: HTMLButtonElement[]) => {
    const span = document.createElement("span");
    span.className = "stacks-chips";
    span.append(label(text), ...chips);
    return span;
  };
  controls.append(group("Rows", byChips.map(([, c]) => c)));
  if (rangeChips.length) controls.append(group("Time", rangeChips.map(([, c]) => c)));
  const clear = chip("Show all stacks", () => pin(null));
  clear.classList.add("stacks-clear");

  // --- Linking: a pick lights its stacks, their camps and their players, and dims the rest ---
  const show = (pick: Pick | null) => {
    const picked = pick ? new Set(data.stacks.flatMap((s, i) => (isPicked(s, i, pick) ? [i] : []))) : null;
    const players = picked ? playersIn(data.stacks.filter((_, i) => picked.has(i))) : null;
    for (const bar of figure.querySelectorAll<HTMLElement>("[data-stack]")) {
      bar.classList.toggle("is-off", !!picked && !picked.has(Number(bar.dataset.stack)));
    }
    for (const row of figure.querySelectorAll<HTMLElement>("[data-row]")) {
      row.classList.toggle("is-off", !!players && !players.has(row.dataset.row ?? ""));
    }
    for (const camp of camps) {
      const id = Number(camp.dataset.camp);
      camp.classList.toggle("is-off", !!picked && !data.stacks.some((s, i) => picked.has(i) && s[1] === id));
    }
  };
  const markCamp = (id: number | null) => {
    for (const camp of camps) {
      const on = Number(camp.dataset.camp) === id;
      camp.classList.toggle("is-selected", on);
      camp.setAttribute("aria-pressed", String(on));
    }
  };
  const pin = (pick: Pick | null) => {
    pinned = pick && !samePick(pick, pinned) ? pick : null;
    show(pinned);
    markCamp(pinned ? (pinned.kind === "camp" ? pinned.id : null) : resting);
    panel.innerHTML = pinned ? pickMarkup(data, pinned) : campMarkup(data, resting);
    if (pinned) panel.append(clear);
  };
  // Hovering only previews: redrawing the card would move what is under the pointer.
  const preview = (pick: Pick | null) => show(pick ?? pinned);

  const pickOf = (target: EventTarget | null): Pick | null => {
    if (!(target instanceof Element)) return null;
    const bar = target.closest<HTMLElement>("[data-stack]");
    if (bar) return { kind: "stack", index: Number(bar.dataset.stack) };
    const hero = target.closest<HTMLElement>("[data-hero]");
    if (hero?.dataset.hero) return { kind: "hero", hero: hero.dataset.hero };
    const camp = target.closest<SVGGElement>("[data-camp]");
    if (camp) return { kind: "camp", id: Number(camp.dataset.camp) };
    return null;
  };
  figure.addEventListener("click", (event) => {
    const pick = pickOf(event.target);
    if (pick) pin(pick);
  });
  figure.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && pinned) return pin(null);
    // The camps are SVG groups, not buttons, so they take Enter and Space here.
    const camp = event.target instanceof Element ? event.target.closest("[data-camp]") : null;
    if (!camp || (event.key !== "Enter" && event.key !== " ")) return;
    event.preventDefault();
    pin(pickOf(camp));
  });
  figure.addEventListener("mouseover", (event) => preview(pickOf(event.target)));
  figure.addEventListener("mouseleave", () => preview(null));
  figure.addEventListener("focusin", (event) => preview(pickOf(event.target)));
  figure.addEventListener("focusout", (event) => {
    if (!(event.relatedTarget instanceof Node && figure.contains(event.relatedTarget))) preview(null);
  });

  // --- Rows: redrawn for a new grouping; a shorter stretch only moves the axis end ---
  const drawRows = () => {
    rowsHost.innerHTML = rowsMarkup(data, by);
    const rows = rowsHost.querySelector<HTMLElement>(".stacks-rows");
    rows?.style.setProperty("--end", String(shownTo));
    rows?.classList.toggle("is-early", shownTo < end);
    for (const node of rowsHost.querySelectorAll<HTMLElement>("[data-t]")) node.hidden = Number(node.dataset.t) > shownTo;
    for (const [value, button] of byChips) button.setAttribute("aria-pressed", String(value === by));
    for (const [value, button] of rangeChips) button.setAttribute("aria-pressed", String(value === shownTo));
    show(pinned);
  };
  const setBy = (value: RowsBy) => {
    by = value;
    drawRows();
  };
  const setRange = (value: number) => {
    shownTo = value;
    drawRows();
  };
  drawRows();
}

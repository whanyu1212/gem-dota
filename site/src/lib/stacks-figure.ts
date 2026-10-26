/**
 * The stacks recipe's figure in the browser. The page already shows the
 * most-stacked camp's stacks (src/figures/stacks.ts); this lists the stacks of
 * any camp picked on the map, by click or keyboard.
 */
import { campMarkup, type StacksData } from "./stacks-data";

export function mountStacksFigure(figure: HTMLElement, data: StacksData): void {
  const panel = figure.querySelector<HTMLElement>("[data-camp-panel]");
  const camps = [...figure.querySelectorAll<SVGGElement>("[data-camp]")];
  if (!panel) return;
  const pick = (picked: SVGGElement) => {
    for (const camp of camps) {
      const on = camp === picked;
      camp.classList.toggle("is-selected", on);
      camp.setAttribute("aria-pressed", String(on));
    }
    panel.innerHTML = campMarkup(data, Number(picked.dataset.camp));
  };
  for (const camp of camps) {
    camp.addEventListener("click", () => pick(camp));
    camp.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      pick(camp);
    });
  }
}

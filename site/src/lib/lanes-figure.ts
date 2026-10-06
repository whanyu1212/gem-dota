/**
 * The lanes recipe's figure in the browser. The page already shows the lanes at
 * the end of the laning stage (src/figures/lanes.ts); this adds the switch to
 * the second reading, 10:00, and back.
 */
import { clock, figureMarkup, type LanesData } from "./lanes-data";

export function mountLanesFigure(figure: HTMLElement, data: LanesData): void {
  const controls = figure.querySelector<HTMLElement>("[data-controls]")!;
  const body = figure.querySelector<HTMLElement>("[data-lanes]")!;
  const label = document.createElement("span");
  label.className = "chip-label";
  label.textContent = "Reading at";
  const [first, second] = data.readings;
  const names: [number, string][] = [
    [first, `${clock(first)}, the laning stage`],
    [second, clock(second)],
  ];
  const buttons = names.map(([reading, text]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "chip";
    button.textContent = text;
    button.setAttribute("aria-pressed", String(reading === first));
    button.addEventListener("click", () => {
      for (const b of buttons) b.setAttribute("aria-pressed", String(b === button));
      body.innerHTML = figureMarkup(data, reading);
    });
    return button;
  });
  controls.append(label, ...buttons);
  controls.hidden = false;
}

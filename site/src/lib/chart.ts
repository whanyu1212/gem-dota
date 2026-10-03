/** Layout for the home page's gold-advantage chart, computed at build time. */

export interface ChartBox {
  width: number;
  height: number;
  left: number;
  right: number;
  top: number;
  bottom: number;
}

/** Evenly spaced round values covering [min, max], e.g. -50000, -40000, …, 10000. */
export function ticks(min: number, max: number, count = 6): number[] {
  const span = Math.max(max - min, 1);
  const raw = span / count;
  const magnitude = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * magnitude).find((s) => s >= raw)!;
  const first = Math.floor(min / step) * step;
  const last = Math.ceil(max / step) * step;
  const values: number[] = [];
  for (let v = first; v <= last + step / 2; v += step) values.push(Math.round(v));
  return values;
}

/** "+10k", "−20k", "0": gold values for axis labels (with a real minus sign). */
export function formatGold(value: number): string {
  if (value === 0) return "0";
  const sign = value > 0 ? "+" : "−";
  const k = Math.abs(value) / 1000;
  return `${sign}${Number.isInteger(k) ? k : k.toFixed(1)}k`;
}

/** Scales and SVG paths for a per-minute series in a box. */
export function lineChart(values: number[], box: ChartBox) {
  const yTicks = ticks(Math.min(0, ...values), Math.max(0, ...values));
  const yMin = yTicks[0];
  const yMax = yTicks.at(-1)!;
  const minutes = values.length - 1;
  const x = (minute: number) => box.left + (minute / Math.max(minutes, 1)) * (box.width - box.left - box.right);
  const y = (value: number) => box.top + ((yMax - value) / (yMax - yMin)) * (box.height - box.top - box.bottom);
  const points = values.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`);
  const line = `M${points.join("L")}`;
  const zero = y(0);
  const area = `${line}L${x(minutes).toFixed(1)},${zero.toFixed(1)}L${x(0).toFixed(1)},${zero.toFixed(1)}Z`;
  const xStep = minutes > 60 ? 15 : minutes > 30 ? 10 : 5;
  const xTicks = Array.from({ length: Math.floor(minutes / xStep) + 1 }, (_, i) => i * xStep);
  return { x, y, line, area, zero, yTicks, xTicks };
}

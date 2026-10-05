/**
 * Picking a stretch of time on a timeline strip: Figure 3's damage strip and the
 * wards recipe's timeline. Drag across the strip to pick a range; a click
 * without a drag is a click at a time. The strip is an SVG drawn 1000 units
 * wide, with `min` at its left edge and `max` at its right.
 */

/** A stretch of time, [from, to], in the strip's own units (seconds). */
export type TimeRange = [number, number];

/** The time at a fraction (0 at the left edge, 1 at the right) of a strip from `min` to `max`, kept on the strip. */
export function timeAtFraction(fraction: number, min: number, max: number): number {
  return min + Math.min(1, Math.max(0, fraction)) * (max - min);
}

/** The range between two times, earlier first, or `null` when they're closer than `minSpan` (a click). */
export function rangeBetween(a: number, b: number, minSpan: number): TimeRange | null {
  return Math.abs(b - a) >= minSpan ? [Math.min(a, b), Math.max(a, b)] : null;
}

export interface RangePickerOptions {
  /** Time at the strip's left and right edges. */
  min: number;
  max: number;
  /** A drag shorter than this is a click. */
  minSpan: number;
  /** A drag picking a range: while it moves (`done` false), and where it ends. */
  onRange(range: TimeRange, done: boolean): void;
  /** A click without a drag, at a time. */
  onClick(t: number): void;
  /** The browser took the pointer away mid-drag. */
  onCancel?(): void;
}

/** Make `strip` pick ranges. Vertical swipes still scroll the page (`touch-action: pan-y` in CSS). */
export function attachRangePicker(strip: SVGSVGElement, options: RangePickerOptions): void {
  const timeAt = (clientX: number) => {
    const box = strip.getBoundingClientRect();
    return timeAtFraction((clientX - box.left) / (box.width || 1), options.min, options.max);
  };
  let from: number | null = null;
  strip.addEventListener("pointerdown", (event) => {
    from = timeAt(event.clientX);
    strip.setPointerCapture(event.pointerId);
  });
  strip.addEventListener("pointermove", (event) => {
    if (from === null) return;
    const range = rangeBetween(from, timeAt(event.clientX), options.minSpan);
    if (range) options.onRange(range, false);
  });
  strip.addEventListener("pointerup", (event) => {
    if (from === null) return;
    const to = timeAt(event.clientX);
    const range = rangeBetween(from, to, options.minSpan);
    from = null;
    if (range) options.onRange(range, true);
    else options.onClick(to);
  });
  strip.addEventListener("pointercancel", () => {
    from = null;
    options.onCancel?.();
  });
}

/** Place a strip's range rectangle over `range` (hidden when there is none). */
export function placeRange(rect: SVGRectElement, range: TimeRange | null, min: number, max: number): void {
  rect.setAttribute("visibility", range ? "visible" : "hidden");
  if (!range) return;
  const x = (t: number) => ((t - min) / (max - min || 1)) * 1000;
  rect.setAttribute("x", String(x(range[0])));
  rect.setAttribute("width", String(x(range[1]) - x(range[0])));
}

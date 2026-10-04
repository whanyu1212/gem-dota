/**
 * Hero paths for the home page's fight figure: smooth curves through the
 * sampled positions, cut into pieces that fade from the fight's start (faint)
 * to its last death (solid), so the trails read like comet tails.
 */

/** A sampled position: map-square x, y, and seconds since the fight window started. */
export type Sample = [number, number, number];

export interface PathPiece {
  /** SVG path data. */
  d: string;
  /** Fade level, 0 (oldest, faintest) to levels - 1 (newest). */
  level: number;
}

const f = (n: number) => n.toFixed(1);

/**
 * Cubic Bézier control points for the segment p1 -> p2 of a Catmull-Rom spline
 * through p0, p1, p2, p3. The curve passes through every sample.
 */
export function catmullRom(p0: number[], p1: number[], p2: number[], p3: number[]): [number[], number[]] {
  return [
    [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6],
    [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6],
  ];
}

/** The path as smooth pieces, one per run of segments that share a fade level. */
export function fadedPieces(samples: Sample[], duration: number, levels = 6): PathPiece[] {
  const pieces: PathPiece[] = [];
  const levelOf = (t: number) => Math.min(levels - 1, Math.max(0, Math.floor((t / Math.max(duration, 1)) * levels)));
  for (let i = 0; i + 1 < samples.length; i++) {
    const p0 = samples[Math.max(0, i - 1)];
    const [p1, p2] = [samples[i], samples[i + 1]];
    const p3 = samples[Math.min(samples.length - 1, i + 2)];
    const [c1, c2] = catmullRom(p0, p1, p2, p3);
    const level = levelOf((p1[2] + p2[2]) / 2);
    const curve = `C${f(c1[0])},${f(c1[1])} ${f(c2[0])},${f(c2[1])} ${f(p2[0])},${f(p2[1])}`;
    const last = pieces.at(-1);
    if (last && last.level === level) last.d += curve;
    else pieces.push({ d: `M${f(p1[0])},${f(p1[1])}${curve}`, level });
  }
  return pieces;
}

/** Stroke opacity for a fade level: faint for the oldest, solid for the newest. */
export function fadeOpacity(level: number, levels = 6): number {
  return Number((0.12 + 0.88 * ((level + 1) / levels) ** 1.6).toFixed(2));
}

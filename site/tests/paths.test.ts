import { describe, expect, it } from "vitest";
import { catmullRom, fadeOpacity, fadedPieces, type Sample } from "../src/lib/paths";

describe("fight paths", () => {
  it("keeps a straight line straight", () => {
    const [c1, c2] = catmullRom([0, 0], [10, 0], [20, 0], [30, 0]);
    expect(c1[1]).toBe(0);
    expect(c2[1]).toBe(0);
    expect(c1[0]).toBeCloseTo(10 + 20 / 6);
  });

  it("passes through every sample, starting each piece at one", () => {
    const samples: Sample[] = [[0, 0, 0], [10, 5, 10], [20, 0, 20], [30, 5, 30]];
    const pieces = fadedPieces(samples, 30, 3);
    expect(pieces.map((p) => p.level)).toEqual([0, 1, 2]);
    expect(pieces[0].d.startsWith("M0.0,0.0C")).toBe(true);
    expect(pieces[1].d.startsWith("M10.0,5.0C")).toBe(true);
    expect(pieces[2].d.endsWith(" 30.0,5.0")).toBe(true);
  });

  it("joins consecutive segments of one fade level into one piece", () => {
    const samples: Sample[] = [[0, 0, 0], [1, 0, 1], [2, 0, 2], [3, 0, 3]];
    expect(fadedPieces(samples, 100, 6)).toHaveLength(1);
    expect(fadedPieces([[0, 0, 0]], 10)).toEqual([]);
  });

  it("fades from faint to solid", () => {
    expect(fadeOpacity(0)).toBeLessThan(0.2);
    expect(fadeOpacity(5)).toBe(1);
    expect(fadeOpacity(2)).toBeGreaterThan(fadeOpacity(1));
  });
});

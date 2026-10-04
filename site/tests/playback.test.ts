import { describe, expect, it } from "vitest";
import { clockAt, headAt, isDead, runUntil, tracks } from "../src/lib/playback";

const paths = [
  { hero: "Lion", icon: "lion", team: "radiant", points: [[0, 0, 0], [10, 0, 1], [20, 0, 2], [30, 0, 3]] },
  // Respawned (or bought back) far away, then walked back into the frame.
  { hero: "Lion", team: "radiant", points: [[100, 100, 8], [110, 100, 9]] },
  { hero: "Tiny", team: "radiant", points: [[50, 50, 0], [50, 60, 1]] },
];
const [lion, tiny] = tracks(paths, [{ hero: "Lion", t: 3 }]);

describe("fight playback", () => {
  it("groups runs and deaths by hero, in time order", () => {
    expect(lion.runs).toHaveLength(2);
    expect(lion.icon).toBe("lion");
    expect(lion.deaths).toEqual([3]);
    expect(tiny.runs).toHaveLength(1);
  });

  it("interpolates between samples, for display", () => {
    expect(headAt(lion, 1.5)).toEqual([15, 0, 1.5]);
    expect(runUntil(lion.runs[0], 1.5).map((p) => p[0])).toEqual([0, 10, 15]);
  });

  it("hides a hero while dead, until its next path segment starts", () => {
    expect(isDead(lion, 2.9)).toBe(false);
    expect(isDead(lion, 3)).toBe(true);
    expect(headAt(lion, 5)).toBeNull();
    expect(isDead(lion, 8.5)).toBe(false);
    expect(headAt(lion, 8.5)).toEqual([105, 100, 8.5]);
  });

  it("holds a hero at its last sample for about one sample gap, then hides it", () => {
    expect(headAt(tiny, 2)).toEqual([50, 60, 1]);
    expect(headAt(tiny, 4)).toBeNull();
    // A dead hero is not held.
    expect(headAt(lion, 3.5)).toBeNull();
  });

  it("formats the in-game clock", () => {
    expect(clockAt("42:34", 15)).toBe("42:49");
    expect(clockAt("42:34", 57.2)).toBe("43:31");
  });
});

import { describe, expect, it } from "vitest";
import { rangeBetween, timeAtFraction } from "../src/lib/range-picker";

describe("range picker", () => {
  it("maps a point on the strip to a time, kept on the strip", () => {
    expect(timeAtFraction(0.5, 0, 74)).toBe(37);
    expect(timeAtFraction(0.25, -90, 5510)).toBe(1310);
    expect(timeAtFraction(-0.2, -90, 5510)).toBe(-90);
    expect(timeAtFraction(1.4, 0, 74)).toBe(74);
  });

  it("makes a range from a drag, earlier first, and a click from a short one", () => {
    expect(rangeBetween(30, 26, 0.2)).toEqual([26, 30]);
    expect(rangeBetween(26, 26.1, 0.2)).toBeNull();
    expect(rangeBetween(2400, 2420, 20)).toEqual([2400, 2420]);
  });
});

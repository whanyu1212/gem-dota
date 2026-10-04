import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import home from "../src/data/home.json";
import { RECIPE_CARDS } from "../src/data/recipes";
import { formatGold, lineChart, ticks } from "../src/lib/chart";

const docs = new URL("../src/content/docs/", import.meta.url);

describe("recipe cards", () => {
  it.each(RECIPE_CARDS.map((card) => [card.link, card]))("%s quotes its recipe page", (_, card) => {
    const page = readFileSync(new URL(card.file, docs), "utf8").replace(/\s+/g, " ");
    expect(page).toContain(card.source);
    expect(card.answer).toContain(card.figure);
    expect(`/${card.file.replace(/\.md$/, "")}`).toBe(card.link);
  });
});

describe("home snapshot", () => {
  const { match, map } = home;

  it("has the match the figures need", () => {
    expect(match.players).toHaveLength(10);
    expect(match.radiant_gold_adv.length).toBeGreaterThan(1);
    expect(typeof match.radiant_win).toBe("boolean");
  });

  it("lists Radiant then Dire, as the example's players[:5] / [5:] assumes", () => {
    expect(match.players.slice(0, 5).every((p) => p.team === "radiant")).toBe(true);
    expect(match.players.slice(5).every((p) => p.team === "dire")).toBe(true);
  });

  it("has every camp and both lotus pools inside the map square", () => {
    expect(map.camps).toHaveLength(28);
    expect(map.lotus_pools).toHaveLength(2);
    // The half line runs past the edges on purpose, so the two halves cover the square.
    for (const [x, y] of [...map.camps.map((c) => c.at), ...map.lotus_pools, ...map.river]) {
      expect(x).toBeGreaterThanOrEqual(0);
      expect(x).toBeLessThanOrEqual(map.size);
      expect(y).toBeGreaterThanOrEqual(0);
      expect(y).toBeLessThanOrEqual(map.size);
    }
  });
});

describe("gold chart", () => {
  it("picks round ticks that cover the data and zero", () => {
    expect(ticks(-47262, 152)).toEqual([-50000, -40000, -30000, -20000, -10000, 0, 10000]);
    expect(ticks(0, 16887)).toEqual([0, 5000, 10000, 15000, 20000]);
  });

  it("labels gold with a sign and a real minus", () => {
    expect(formatGold(10000)).toBe("+10k");
    expect(formatGold(-2500)).toBe("−2.5k");
    expect(formatGold(0)).toBe("0");
  });

  it("maps the first and last minute to the plot edges", () => {
    const box = { width: 560, height: 560, left: 52, right: 14, top: 18, bottom: 40 };
    const { x, xTicks } = lineChart([0, 100, -100], box);
    expect(x(0)).toBe(52);
    expect(x(2)).toBe(546);
    expect(xTicks).toEqual([0]);
  });
});

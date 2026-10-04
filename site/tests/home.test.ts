import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import home from "../src/data/home.json";
import { RECIPE_CARDS } from "../src/data/recipes";

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

  it("has the match Table 1 needs", () => {
    expect(match.players).toHaveLength(10);
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

describe("wards and the fight", () => {
  const { wards, fight, map } = home;
  const inSquare = ([x, y]: number[]) => x >= 0 && x <= map.size && y >= 0 && y <= map.size;

  it("has the whole-match ward totals and the wards up at the fight", () => {
    expect(wards.totals.observer).toBeGreaterThan(0);
    expect(wards.totals.sentry).toBeGreaterThan(0);
    expect(wards.up.length).toBeGreaterThan(0);
    for (const ward of wards.up) {
      expect(["observer", "sentry"]).toContain(ward.type);
      expect(inSquare(ward.at)).toBe(true);
      // Only observers give map vision.
      expect("vision_radius" in ward).toBe(ward.type === "observer");
    }
  });

  it("frames the fight inside the map, and narrates it in time order", () => {
    expect(fight).not.toBeNull();
    const [x, y, size] = fight!.box;
    expect(x).toBeGreaterThanOrEqual(0);
    expect(y).toBeGreaterThanOrEqual(0);
    expect(x + size).toBeLessThanOrEqual(map.size);
    expect(y + size).toBeLessThanOrEqual(map.size);
    const times = fight!.events.map((e) => e.time.split(":").reduce((m, s) => Number(m) * 60 + Number(s), 0));
    expect(times).toEqual([...times].sort((a, b) => a - b));
    // The playback's clock (seconds since the window started) agrees with the shown times.
    const offsets = fight!.events.map((e) => e.t);
    expect(offsets).toEqual([...offsets].sort((a, b) => a - b));
    for (const [i, event] of fight!.events.entries()) {
      expect(Math.abs(times[i] - times[0] - (event.t - fight!.events[0].t))).toBeLessThanOrEqual(1);
    }
    for (const death of fight!.deaths_at) expect(death.t).toBeGreaterThanOrEqual(0);
    expect(fight!.events.filter((e) => e.text.includes(" killed "))).toHaveLength(fight!.deaths);
    expect(fight!.radiant_kills + fight!.dire_kills).toBe(fight!.deaths);
  });

  it("puts every death spot inside the fight's frame", () => {
    const [x, y, size] = fight!.box;
    for (const death of fight!.deaths_at) {
      expect(death.at[0]).toBeGreaterThanOrEqual(x);
      expect(death.at[0]).toBeLessThanOrEqual(x + size);
      expect(death.at[1]).toBeGreaterThanOrEqual(y);
      expect(death.at[1]).toBeLessThanOrEqual(y + size);
    }
  });
});

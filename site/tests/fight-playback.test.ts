import { readdirSync, statSync } from "node:fs";
import { describe, expect, it } from "vitest";
import fight from "../src/data/fight.json";
import home from "../src/data/home.json";
import {
  buybackAfter,
  isHidden,
  isSmoked,
  castText,
  clockAt,
  damagePerSecond,
  deathTimes,
  FILTERS,
  feedRows,
  rowShows,
  stateAt,
  type Cast,
  type FightData,
} from "../src/lib/fight-playback";

const names = ["Lion", "Tiny", "Ember Spirit", "Pangolier"];
const teams = ["radiant", "radiant", "dire", "dire"];
const hero = (team: string, runs: number[][][]) => ({ hero: "", icon: "", team, runs: runs as never });

const data: FightData = {
  start: "42:34",
  start_s: 2554,
  duration: 10,
  heroes: [
    // Lion walks right, dies at 3 s, buys back at the fountain at 6 s.
    hero("radiant", [
      [[0, 0, 0, 600, 600, 300, 300], [1, 10, 0, 400, 600, 200, 300], [2, 20, 0, 100, 600, 200, 300]],
      [[6, 900, 900, 600, 600, 300, 300], [7, 900, 900, 600, 600, 300, 300]],
    ]),
    hero("radiant", [[[0, 50, 50, 900, 900, 100, 100], [1, 50, 60, 900, 900, 100, 100]]]),
    hero("dire", []),
    hero("dire", []),
  ],
  casts: [
    { t: 1, by: 1, what: "Avalanche", hits: [[2, 312, "magical", 1.2], [3, 298, "magical", 1.2]] },
    // Blink at the same moment gives no buff: Black King Bar's must not fold into it.
    { t: 2, by: 1, what: "Swift Blink", item: "swift_blink", self: true, hits: [] },
    { t: 2, by: 1, what: "Black King Bar", item: "black_king_bar", self: true, hits: [] },
    { t: 2.5, by: 1, what: "Power Treads", item: "power_treads", hits: [] },
    { t: 4, by: 0, what: "Hex", target: 2, hits: [[2, 0, "", 3.2]] },
  ],
  damage: [
    [1, 1, 2, 312, "magical", 1, "Avalanche"],
    [1.2, 1, 3, 298, "magical", 1, "Avalanche"],
    [2.1, 2, 0, 100, "physical", 1, "Attack"],
    [2.6, 2, 0, 80, "physical", 1, "Attack"],
    [2.7, 3, 0, 50, "physical", 0, "Attack"],
  ],
  disables: [
    [1, 2, 1, "Avalanche", 1.2],
    [2.9, 0, 3, "Bash", 0.8],
  ],
  buffs: [
    [2, 9, 1, "bkb"],
    [5, 8, 3, "blade_mail"],
  ],
  deaths: [
    { t: 3, victim: 0, killer: 2, killer_name: "Ember Spirit", aegis: false, gold_lost: 210, gold: [[2, 326]], xp: [[2, 468]], recent: [], recent_total: 0 },
    { t: 5, victim: 2, killer: 1, killer_name: "Tiny", aegis: true, gold_lost: 0, gold: [], xp: [], recent: [], recent_total: 0 },
  ],
  buybacks: [[6, 0, 831]],
  // Radiant smoked Lion and Tiny; Lion's broke at 2 s and Dire saw him, Tiny's at 4 s unseen.
  smokes: [["radiant", 0, [[0, 0, 2, 2], [1, 0, 4, null]]]],
  hidden: [
    [0, 0, 2],
    [1, 0, 1.5],
    [1, 5, 6],
  ],
};

describe("hero state", () => {
  const deaths = deathTimes(data);

  it("ignores Aegis deaths", () => {
    expect(deaths).toEqual([[3], [], [], []]);
  });

  it("interpolates position, HP and mana between samples, for display", () => {
    expect(stateAt(data.heroes[0], deaths[0], 0.5)).toEqual({ x: 5, y: 0, hp: 500, maxHp: 600, mana: 250, maxMana: 300 });
  });

  it("hides a dead hero until its next run starts, and holds one about a sample gap after its run", () => {
    expect(stateAt(data.heroes[0], deaths[0], 3.5)).toBeNull();
    expect(stateAt(data.heroes[0], deaths[0], 6.5)?.x).toBe(900);
    expect(stateAt(data.heroes[1], deaths[1], 2)?.y).toBe(60);
    expect(stateAt(data.heroes[1], deaths[1], 3)).toBeNull();
  });
});

describe("cast text", () => {
  it("puts each hit's damage beside the hero, with a shared type once", () => {
    expect(castText(data.casts[0], names, teams)).toBe(
      "Avalanche hit Ember Spirit 312 (1.2s stun) · Pangolier 298 (1.2s stun) magical",
    );
  });

  it("leaves out ministuns", () => {
    const cast: Cast = { t: 0, by: 1, what: "Avalanche", hits: [[2, 118, "magical", 0.1]] };
    expect(castText(cast, names, teams)).toBe("Avalanche hit Ember Spirit 118 magical");
  });

  it("names the type per hit when the types differ", () => {
    const cast: Cast = { t: 0, by: 1, what: "Toss", hits: [[2, 200, "magical", 0], [3, 50, "physical", 0]] };
    expect(castText(cast, names, teams)).toBe("Toss hit Ember Spirit 200 magical · Pangolier 50 physical");
  });

  it("says 'on' for allies the cast reached, and 'hit' for enemies", () => {
    const crest: Cast = { t: 0, by: 0, what: "Solar Crest", hits: [[1, 0, "", 0]] };
    expect(castText(crest, names, teams)).toBe("Solar Crest on Tiny");
    const shiva: Cast = { t: 0, by: 1, what: "Shiva's Guard", hits: [[0, 0, "", 0], [2, 169, "magical", 0]] };
    expect(castText(shiva, names, teams)).toBe("Shiva's Guard on Lion hit Ember Spirit 169 magical");
  });

  it("shows a debuff-only hit, a self-cast, and a target that is not a hero", () => {
    expect(castText(data.casts[4], names, teams)).toBe("Hex hit Ember Spirit (3.2s stun)");
    expect(castText(data.casts[2], names, teams)).toBe("Black King Bar on self");
    expect(castText({ t: 0, by: 1, what: "Toss", unit: "Creep dire melee", hits: [] }, names, teams)).toBe(
      "Toss on Creep dire melee",
    );
    expect(castText({ t: 0, by: 0, what: "Hex", target: 3, hits: [] }, names, teams)).toBe("Hex on Pangolier");
  });
});

describe("feed rows", () => {
  const rows = feedRows(data);
  const kinds = rows.map((r) => r.kind);

  it("leaves out quiet items, and folds a cast's buff and its hits' disables into its row", () => {
    expect(rows.some((r) => r.cast?.item === "power_treads")).toBe(false);
    expect(rows.find((r) => r.cast?.item === "black_king_bar")?.lasted).toBe(7);
    expect(rows.find((r) => r.cast?.item === "swift_blink")?.lasted).toBeUndefined();
    // Avalanche's stun is in its row; the Bash no cast shows gets a row of its own.
    expect(rows.filter((r) => r.kind === "disable").map((r) => r.disable![3])).toEqual(["Bash"]);
    // Blade Mail came from no cast in the data: a row of its own.
    expect(rows.filter((r) => r.kind === "buff").map((r) => r.buff![3])).toEqual(["blade_mail"]);
  });

  it("sums a hero's right-clicks on one target per second, and leaves out summons", () => {
    const attacks = rows.filter((r) => r.kind === "attack").map((r) => r.attack);
    expect(attacks).toEqual([{ by: 2, target: 0, damage: 180, type: "physical" }]);
  });

  it("is in time order, with deaths and buybacks", () => {
    expect(rows.map((r) => r.t)).toEqual([...rows.map((r) => r.t)].sort((a, b) => a - b));
    expect(kinds.filter((k) => k === "death")).toHaveLength(2);
    expect(kinds).toContain("buyback");
  });

  it("shows rows whose filter is on and that involve the followed hero", () => {
    const on = new Set(FILTERS.filter((f) => f.on).map((f) => f.key));
    // Every filter is on by default, attacks included.
    expect(FILTERS.every((f) => f.on)).toBe(true);
    const attack = rows.find((r) => r.kind === "attack")!;
    expect(rowShows(attack, on, null)).toBe(true);
    expect(rowShows(attack, new Set([...on].filter((k) => k !== "attacks")), null)).toBe(false);
    const avalanche = rows.find((r) => r.cast?.what === "Avalanche")!;
    expect(rowShows(avalanche, on, null)).toBe(true);
    expect(rowShows(avalanche, on, 3)).toBe(true);
    expect(rowShows(avalanche, on, 0)).toBe(false);
  });
});

describe("smoke and visibility", () => {
  it("knows who was smoked and who the enemy couldn't see", () => {
    expect(isSmoked(data, 0, 1.9)).toBe(true);
    expect(isSmoked(data, 0, 2)).toBe(false);
    expect(isSmoked(data, 2, 1)).toBe(false);
    // Tiny stayed smoked to 4 s but Dire saw him from 1.5 s to 5 s: two separate facts.
    expect(isSmoked(data, 1, 3)).toBe(true);
    expect(isHidden(data, 1, 3)).toBe(false);
    expect(isHidden(data, 1, 5.5)).toBe(true);
  });

  it("adds a feed row as each smoke breaks, saying whether the enemy saw the hero", () => {
    const breaks = feedRows(data).filter((r) => r.kind === "smoke");
    expect(breaks.map((r) => [r.t, r.smokeBreak])).toEqual([
      [2, { hero: 0, seen: true }],
      [4, { hero: 1, seen: false }],
    ]);
    const on = new Set(FILTERS.filter((f) => f.on).map((f) => f.key));
    expect(breaks.every((r) => rowShows(r, on, null))).toBe(true);
  });
});

describe("buybacks", () => {
  const death = (t: number, aegis = false) => ({ t, victim: 0, killer: 2, killer_name: "", aegis, gold_lost: 0, gold: [], xp: [], recent: [], recent_total: 0 });

  it("binds a buyback to the death just before it, not an earlier one", () => {
    const deaths = [death(1, true), death(3), death(8)];
    const fight: FightData = { ...data, deaths, buybacks: [[4, 0, 900], [9, 0, 1200]] };
    expect(buybackAfter(fight, deaths[0])).toBeUndefined(); // Aegis
    expect(buybackAfter(fight, deaths[1])?.[2]).toBe(900);
    expect(buybackAfter(fight, deaths[2])?.[2]).toBe(1200);
    const noBuyback: FightData = { ...fight, buybacks: [[9, 0, 1200]] };
    expect(buybackAfter(noBuyback, deaths[1])).toBeUndefined();
  });
});

describe("damage strip", () => {
  it("sums each team's damage per second", () => {
    const strip = damagePerSecond(data);
    expect(strip.radiant.slice(0, 2)).toEqual([0, 610]);
    expect(strip.dire[2]).toBe(230);
    expect(strip.radiant).toHaveLength(10);
  });

  it("formats the in-game clock", () => {
    expect(clockAt("42:34", 15)).toBe("42:49");
  });
});

describe("the committed fight playback", () => {
  const playback = fight as unknown as FightData;
  const valid = (i: number | null) => i === null || (Number.isInteger(i) && i >= 0 && i < playback.heroes.length);
  const inWindow = (t: number) => t >= 0 && t <= playback.duration;

  it("is the home page's fight, on the same clock", () => {
    const seconds = (clock: string) => clock.split(":").reduce((m, s) => Number(m) * 60 + Number(s), 0);
    // It may start earlier than the fight window, at the smoke that led into it.
    expect(seconds(playback.start)).toBeLessThanOrEqual(seconds(home.fight!.start));
    expect(playback.heroes).toHaveLength(10);
    const kills = playback.deaths.filter((d) => !d.aegis);
    expect(kills).toHaveLength(home.fight!.deaths);
    // Each kill falls at the narration's time for it.
    const told = home.fight!.events.filter((e) => e.text.includes(" killed ")).map((e) => e.time);
    expect(kills.map((d) => clockAt(playback.start_s, d.t))).toEqual(told);
  });

  it("starts at Radiant's smoke, and every smoked hero becomes visible to Dire as it breaks", () => {
    expect(playback.start).toBe("42:19");
    const [[team, used, members]] = playback.smokes;
    expect([team, used, members.length]).toEqual(["radiant", 0, 5]);
    for (const [hero, , broke, seen] of members) {
      expect(broke).not.toBeNull();
      expect(seen! - broke!).toBeGreaterThanOrEqual(0);
      expect(seen! - broke!).toBeLessThanOrEqual(1);
      expect(isHidden(playback, hero, broke! - 0.5)).toBe(true);
    }
  });

  it("refers to heroes by valid index, and times every record inside the window", () => {
    for (const cast of playback.casts) {
      expect(inWindow(cast.t)).toBe(true);
      expect([cast.by, cast.target ?? null, ...cast.hits.map(([h]) => h)].every(valid)).toBe(true);
    }
    for (const [t, by, target] of playback.damage) expect(inWindow(t) && valid(by) && valid(target)).toBe(true);
    for (const [t, target, source] of playback.disables) expect(inWindow(t) && valid(target) && valid(source)).toBe(true);
    for (const death of playback.deaths) expect(inWindow(death.t) && valid(death.victim) && valid(death.killer)).toBe(true);
    for (const hero of playback.heroes) {
      for (const run of hero.runs) for (const [t, , , hp, maxHp] of run) expect(inWindow(t) && hp <= maxHp).toBe(true);
    }
  });

  it("has every icon it names, from the same export", () => {
    const icons = (folder: string) =>
      new Set(readdirSync(new URL(`../src/assets/icons/${folder}/`, import.meta.url)).map((f) => f.replace(".png", "")));
    expect(new Set(playback.heroes.map((h) => h.icon))).toEqual(icons("heroes"));
    const items = icons("items");
    // An item without a downloaded icon is skipped by the export and shown by name.
    for (const item of items) expect(playback.casts.some((c) => c.item === item)).toBe(true);
  });

  it("stays small, since the browser loads it", () => {
    expect(statSync(new URL("../src/data/fight.json", import.meta.url)).size).toBeLessThan(200_000);
  });
});

import { describe, expect, it } from "vitest";
import committed from "../src/data/runes.json";
import {
  clock,
  counts,
  mapMarkup,
  openersMarkup,
  runesIn,
  stacked,
  stageRange,
  stretchMarkup,
  takers,
  windowFacts,
  windowsIn,
  type RuneRow,
  type RunesData,
  type RuneWindow,
} from "../src/lib/runes-data";

const runes: RuneRow[] = [
  [0, "bounty", "dire_jungle", "picked_up", "Shadow Fiend", "d", "own", null],
  [1, "bounty", "bot_river", "picked_up", "Lion", "r", "river", null],
  [144, "water", "bot_river", "bottled", "Ember Spirit", "d", null, 188],
  [154, "water", "top_river", "denied", "Lion", "r", null, null],
  [400, "arcane", "top_river", "picked_up", "Timbersaw", "r", null, null],
  [1929, "double_damage", "bot_river", "bottled", "Ember Spirit", "d", null, 1929],
  // Two bounties Treant took at once, from Dire's own jungle.
  [5085, "bounty", "dire_jungle", "picked_up", "Treant Protector", "d", "own", null],
  [5085, "bounty", "dire_jungle", "picked_up", "Treant Protector", "d", "own", null],
  [5200, "haste", "top_river", "not_taken", null, "", null, null],
];
const windows: RuneWindow[] = [
  [844, 894, "arcane", "Timbersaw", "r", false, false, [], 0, 0, []],
  [1929, 1974, "double_damage", "Ember Spirit", "d", true, false, ["Lion", "Sniper"], 0, 1200, [["Radiant tier 2 top tower", 31]]],
  [3813, 3820, "illusion", "Ember Spirit", "d", false, true, [], 900, 0, []],
];
const data: RunesData = {
  start_s: 0,
  end_s: 5576,
  stages: [
    ["0:00-6:00", 0, 360],
    ["6:00-20:00", 360, 1200],
    ["20:00-end", 1200, null],
  ],
  near: 1200,
  opening_s: 90,
  after_s: 30,
  spots: { top_river: [396, 465], bot_river: [550, 592], radiant_jungle: [518, 780], dire_jungle: [431, 284] },
  runes,
  openers: [
    ["dire_jungle", "Shadow Fiend", "d", "own", 0, []],
    ["bot_river", "Lion", "r", "river", 1, ["Pudge"]],
  ],
  deaths: [],
  windows,
};

describe("runes", () => {
  it("formats times, before the horn too", () => {
    expect(clock(433)).toBe("7:13");
    expect(clock(-29)).toBe("-0:29");
  });

  it("ends the last stage with the match", () => {
    expect(stageRange(data, data.stages[2])).toEqual([1200, 5576]);
  });

  it("keeps the runes and windows of a stretch", () => {
    expect(runesIn(data, [0, 360]).map((r) => r[0])).toEqual([0, 1, 144, 154]);
    expect(windowsIn(data, [1200, 5576]).map((w) => w[0])).toEqual([1929, 3813]);
  });

  it("counts each side's runes by kind, a bottled rune as taken", () => {
    expect(counts(runes)).toEqual([
      ["Power runes", 1, 1],
      ["Water runes", 0, 1],
      ["Bounty, own jungle", 0, 3],
      ["Bounty, other jungle", 0, 0],
      ["Bounty, river", 1, 0],
      ["Denied", 1, 0],
    ]);
    expect(stacked(runes)).toBe(1);
  });

  it("puts each side's runes on the spot they were taken at", () => {
    const markup = mapMarkup(data, runes);
    expect(markup).toContain('aria-label="Dire\'s jungle: Radiant took 0, Dire took 3"');
    expect(markup).toContain('aria-label="Top river: Radiant took 1, Dire took 0, 1 not taken"');
  });

  it("says what followed a power rune, and when nothing did", () => {
    expect(windowFacts(windows[1], 30)).toEqual(["killed Lion, Sniper", "1,200 damage to buildings", "the team took Radiant tier 2 top tower (+31 s)"]);
    // An illusion rune's illusions outlive their hero.
    expect(windowFacts(windows[2], 30)).toEqual(["900 damage to Roshan", "the taker died"]);
    expect(windowFacts(windows[0], 30)).toEqual(["no kill, no damage to Roshan or buildings, no objective in the 30 s after"]);
  });

  it("lists the power runes' takers, most first", () => {
    expect(takers(runes)).toEqual([
      ["Ember Spirit", "d", 1],
      ["Timbersaw", "r", 1],
    ]);
  });

  it("lists the 0:00 bounties with whose they were and who was near", () => {
    const markup = openersMarkup(data);
    expect(markup).toContain("Shadow Fiend in Dire's own jungle");
    expect(markup).toContain("Pudge within 1,200");
    expect(markup).toContain("No hero died before 1:30.");
  });

  it("draws the committed match", () => {
    const match = committed as unknown as RunesData;
    const shown = stretchMarkup(match, null);
    expect(match.runes.length).toBeGreaterThan(0);
    expect(match.openers).toHaveLength(4);
    expect(Object.keys(match.spots).sort()).toEqual(["bot_river", "dire_jungle", "radiant_jungle", "top_river"]);
    expect(shown.windows.match(/<li class="runes-window/g)).toHaveLength(match.windows.length);
  });
});

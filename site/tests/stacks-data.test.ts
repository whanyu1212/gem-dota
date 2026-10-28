import { describe, expect, it } from "vitest";
import committed from "../src/data/stacks.json";
import {
  campMarkup,
  campsMarkup,
  clock,
  firstCamp,
  isPicked,
  pickMarkup,
  playerRows,
  playersMarkup,
  rowsMarkup,
  segments,
  type Pick,
  type StacksData,
} from "../src/lib/stacks-data";

const data: StacksData = {
  end_s: 1800,
  camps: [
    { id: 3, type: "ancient", xy: [500, 400] },
    { id: 6, type: "flooded_medium", xy: [300, 600] },
  ],
  stacks: [
    [240, 3, "Lion", "r", "s", true, 2, 5, 0, 210, [["Timbersaw", "r", 2], ["Lion", "r", 1], ["Shadow Fiend", "d", 1]]],
    [300, 3, "Lion", "r", "s", true, 3, 1, 1, 0, []],
    [300, 6, "Shadow Fiend", "d", "c", false, 2, 2, 0, 60, [["Rubick", "d", 2]]],
  ],
  players: [
    ["Lion", "r", "s", 2, 2, 1, 40, 75],
    ["Timbersaw", "r", "c", 0, 0, 2, 100, 300],
  ],
};

describe("stacks", () => {
  it("opens on the camp stacked most often", () => {
    expect(firstCamp(data)).toBe(3);
    expect(firstCamp({ ...data, camps: [], stacks: [] })).toBeNull();
  });

  it("splits a stack's creeps by who killed them", () => {
    const run = (o: string, creeps: number) => ({ outcome: o, creeps });
    expect(segments(data.stacks[0])).toEqual([run("self", 1), run("team", 2), run("enemy", 1), run("none", 1)]);
    expect(segments(data.stacks[1])).toEqual([run("pulled", 1)]);
    expect(segments([600, 3, null, "", "", false, 2, 2, 0, 50, [["Tiny", "r", 2]]])).toEqual([run("player", 2)]);
  });

  it("puts one row per stacker or per killer, Radiant's first", () => {
    const rows = (by: "stacker" | "killer") => playerRows(data, by).map((r) => [r.hero, r.bars.length, r.others]);
    expect(rows("stacker")).toEqual([
      ["Lion", 2, [["Timbersaw", 2], ["Lion", 1], ["Shadow Fiend", 1]]],
      ["Shadow Fiend", 1, [["Rubick", 2]]],
    ]);
    expect(rows("killer")).toEqual([
      ["Timbersaw", 1, [["Lion", 2]]],
      ["Lion", 1, [["Lion", 1]]],
      ["Shadow Fiend", 1, [["Lion", 1]]],
      ["Rubick", 1, [["Shadow Fiend", 2]]],
    ]);
  });

  it("draws each stack as a bar at its time on an axis to the match's end", () => {
    const html = rowsMarkup(data, "stacker");
    expect(html).toContain('style="--end: 1800; --most: 5"');
    expect(html.match(/class="stacks-bar"/g)).toHaveLength(3);
    expect(html).toContain('data-stack="1" data-t="300" style="--t: 300; --dodge: 0"');
    expect(html).toContain("2 stacks → Timbersaw 2, Lion 1, Shadow Fiend 1");
    expect(html).toContain('<span class="stacks-tick stacks-tick--10" data-t="600" style="--t: 600">10:00</span>');
    expect(rowsMarkup(data, "killer")).toContain("1 creep ← Lion 1");
  });

  it("picks a player's stacks: those they made and those they cleared", () => {
    const pick: Pick = { kind: "hero", hero: "Shadow Fiend" };
    expect(data.stacks.map((s, i) => isPicked(s, i, pick))).toEqual([true, false, true]);
    const card = pickMarkup(data, pick);
    expect(card).toContain("1 stack made, 1 stacked creep killed");
    expect(card).toContain("Camp 3: 5 creeps in 2 waves");
    expect(pickMarkup(data, { kind: "stack", index: 2 })).toContain("Camp 6 at 5:00");
  });

  it("rings each camp by the sides that stacked it and marks the one picked", () => {
    const camps = campsMarkup(data, 6);
    expect(camps).toContain('data-camp="6" tabindex="0" role="button" aria-label="flooded medium camp, stacked 1 time" aria-pressed="true"');
    expect(camps).toContain("var(--camp-flooded-medium)");
    expect(camps.match(/stacks-ring--radiant/g)).toHaveLength(1);
    expect(camps.match(/stacks-ring--dire/g)).toHaveLength(1);
  });

  it("lists a camp's stacks with the enemy's kills marked", () => {
    const list = campMarkup(data, 3);
    expect(list).toContain("Camp 3, stacked 2 times");
    expect(list).toContain('<span class="stacks-enemy">Shadow Fiend 1</span>');
    expect(list).toContain("killed by nobody, 1 pulled");
    expect(campMarkup(data, 99)).toContain("No camp was stacked");
  });

  it("shows each player's share of their neutral gold", () => {
    const table = playersMarkup(data);
    expect(table).toContain("<td>53%</td>");
    expect(table).toContain("<td>33%</td>");
    expect(table).toContain('<button type="button" class="stacks-pick" data-hero="Timbersaw">');
    expect(clock(5460)).toBe("91:00");
  });

  it("reads the committed snapshot", () => {
    const snapshot = committed as unknown as StacksData;
    expect(snapshot.stacks.length).toBeGreaterThan(0);
    expect(snapshot.players).toHaveLength(10);
    const camps = new Set(snapshot.camps.map((c) => c.id));
    expect(snapshot.stacks.every((s) => s[1] === null || camps.has(s[1]))).toBe(true);
  });
});

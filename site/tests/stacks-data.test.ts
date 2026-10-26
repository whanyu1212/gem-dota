import { describe, expect, it } from "vitest";
import committed from "../src/data/stacks.json";
import {
  campMarkup,
  campsMarkup,
  clock,
  firstCamp,
  flowMarkup,
  playersMarkup,
  sideFlows,
  takenByEnemy,
  timelineMarkup,
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
  flows: [
    ["Lion", "r", "s", "Timbersaw", "r", "c", 2, 100],
    ["Shadow Fiend", "d", "c", "Rubick", "d", "s", 2, 60],
    ["Lion", "r", "s", "Lion", "r", "s", 1, 40],
    ["Lion", "r", "s", "Shadow Fiend", "d", "c", 1, 70],
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

  it("splits each side's flows and counts what went to the enemy", () => {
    expect(sideFlows(data, "r").creeps).toBe(4);
    expect(takenByEnemy(data, "r")).toEqual([1, 70]);
    expect(takenByEnemy(data, "d")).toEqual([0, 0]);
  });

  it("draws one ribbon per flow, amber for the enemy's", () => {
    const svg = flowMarkup(data, "r");
    expect(svg.match(/class="stacks-ribbon /g)).toHaveLength(3);
    expect(svg.match(/stacks-ribbon--enemy/g)).toHaveLength(1);
    expect(svg).toContain("Lion <b>S</b> · 4");
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

  it("puts one dot per stack on the timeline, Radiant above and Dire below", () => {
    const svg = timelineMarkup(data);
    expect(svg.match(/stacks-tick--radiant/g)).toHaveLength(2);
    expect(svg.match(/stacks-tick--dire/g)).toHaveLength(1);
    expect(svg).toContain('<span class="stacks-minor" style="left: 100.00%">30:00</span>');
  });

  it("shows each player's share of their neutral gold", () => {
    const table = playersMarkup(data);
    expect(table).toContain("<td>53%</td>");
    expect(table).toContain("<td>33%</td>");
    expect(clock(5460)).toBe("91:00");
  });

  it("reads the committed snapshot", () => {
    const snapshot = committed as unknown as StacksData;
    expect(snapshot.stacks.length).toBeGreaterThan(0);
    expect(snapshot.players).toHaveLength(10);
    const camps = new Set(snapshot.camps.map((c) => c.id));
    expect(snapshot.stacks.every((s) => camps.has(s[1]))).toBe(true);
  });
});

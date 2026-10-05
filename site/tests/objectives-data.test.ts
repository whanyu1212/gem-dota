import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import committed from "../src/data/objectives.json";
import {
  edgeLabel,
  edgeText,
  fallOf,
  mapMarkup,
  objectiveCard,
  objectivesIn,
  tally,
  tallyMarkup,
  type Edge,
  type Kind,
  type Objective,
  type ObjectivesData,
} from "../src/lib/objectives-data";

const objective = (kind: Kind, time_s: number, at: [number, number] | null, extra: Partial<Objective> = {}): Objective => ({
  kind,
  name: kind === "tower" ? "Radiant tier 1 middle tower" : "Roshan",
  for: "d",
  time_s,
  time: "00:00",
  at,
  last_hit: "Lina",
  damage: [],
  shared: false,
  after: null,
  ...extra,
});
const data: ObjectivesData = {
  start_s: -90,
  end_s: 1000,
  buildings: [
    { key: "goodguys_tower1_mid", kind: "tower", side: "r", at: [400, 600] },
    { key: "goodguys_tower2_mid", kind: "tower", side: "r", at: [300, 680] },
  ],
  tormentor_spawns: [],
  objectives: [objective("tower", 300, [400, 600], { after: [2, 30] }), objective("roshan", 500, [640, 675]), objective("roshan", 700, [641, 676])],
  edges: [
    { team: "d", edge: "fight", number: 2, time: "04:00", outcome: "c", took: ["Radiant tier 1 middle tower"], after_s: 30, kills: [0, 2] },
    { team: "r", edge: "fight", number: 3, time: "06:00", outcome: "o", took: ["Roshan"], after_s: 12, kills: [1, 0], by: "d" },
    { team: "d", edge: "aegis", number: 1, time: "08:20", outcome: "n", took: [], after_s: null },
  ],
};
const all = new Set<Kind>(["tower", "barracks", "roshan", "tormentor"]);

describe("objectives in a stretch", () => {
  it("lists the shown kinds that fell in the stretch", () => {
    expect(objectivesIn(data, null, all)).toEqual([0, 1, 2]);
    expect(objectivesIn(data, [400, 1000], all)).toEqual([1, 2]);
    expect(objectivesIn(data, null, new Set<Kind>(["tower"]))).toEqual([0]);
  });

  it("matches a building to its fall by place, and draws the base as it stood", () => {
    expect(fallOf(data, data.buildings[0])).toBe(0);
    expect(fallOf(data, data.buildings[1])).toBeNull();
    const before = mapMarkup(data, [0, 200], [], null); // the tower hadn't fallen yet
    expect(before).not.toContain("is-fallen");
    const after = mapMarkup(data, null, [0, 1, 2], 0);
    expect(after).toContain('class="obj obj--radiant is-fallen is-active" data-objective="0"');
    expect(after.match(/obj-boss /g)).toHaveLength(2); // both Roshans, nudged apart
    expect(after).toContain('class="obj-ring"');
  });

  it("tallies each team's edges and says what each led to", () => {
    expect(tally(data.edges, "d", "fight")).toEqual({ c: 1, o: 0, n: 0, total: 1 });
    expect(edgeText(data.edges[0])).toBe("took the Radiant tier 1 middle tower 30 s after");
    expect(edgeText(data.edges[1])).toBe("Dire took the Roshan first, 12 s after");
    expect(edgeText(data.edges[2])).toBe("no building fell to them in the next 5 minutes");
    expect(edgeLabel(data.edges[0])).toBe("Fight 2 · 04:00 · 0–2");
    expect(tallyMarkup(data.edges)).toContain('data-edges="r|fight|o"');
    expect(objectiveCard(data.objectives[0]).after).toBe("After fight 2, which ended 30 s earlier.");
  });
});

describe("the committed objectives", () => {
  const objectives = committed as unknown as ObjectivesData;
  const page = readFileSync(new URL("../src/content/docs/cookbook/objectives.md", import.meta.url), "utf8").replace(/\s+/g, " ");

  it("places every objective, and every fallen building matches one standing building", () => {
    expect(objectives.objectives).toHaveLength(34);
    expect(objectives.objectives.every((o) => o.at)).toBe(true);
    const fallen = objectives.buildings.filter((b) => fallOf(objectives, b) !== null);
    expect(fallen).toHaveLength(objectives.objectives.filter((o) => o.kind === "tower" || o.kind === "barracks").length);
  });

  it("states the page's numbers", () => {
    expect(page).toContain(`All ${objectives.objectives.length} objectives in match 8856501050`);
    const d = tally(objectives.edges, "d", "fight");
    const r = tally(objectives.edges, "r", "fight");
    expect(page).toContain(`Dire won ${d.total} fights on kills and took the next objective after ${d.c} of them`);
    expect(page).toContain(`Radiant took it after ${r.c} of its ${r.total}`);
  });
});

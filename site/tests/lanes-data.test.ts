import { describe, expect, it } from "vitest";
import committed from "../src/data/lanes.json";
import { amount, clock, eventsIn, eventText, figureMarkup, gapText, laneMarkup, type Lane, type LaneEvent, type LanesData } from "../src/lib/lanes-data";

const numbers = (nw: number, lh: number): [number, number, number, number, number, number, number, number] => [nw, 1000, lh, 2, 900, 100, 0, 600];
const top: Lane = {
  lane: "top",
  sides: {
    r: { heroes: [["Timbersaw", 0.94], ["Lion", 0.6]], at: { "360": numbers(3556, 29), "600": numbers(5998, 65) } },
    d: { heroes: [["Shadow Fiend", 0.95]], at: { "360": numbers(4695, 52), "600": numbers(5998, 96) } },
  },
};
const events: LaneEvent[] = [
  [103, null, "death", "jungle", "Lion", "r", "Shadow Fiend", "top"],
  [420, null, "teleport", "top", "Sniper", "r", null, "mid"],
  [424, 448, "visit", "top", "Sniper", "r", null, "mid"],
  [433, null, "death", "top", "Shadow Fiend", "d", "Timbersaw", "top"],
  [539, 600, "visit", "top", "Rubick", "d", null, "bot"],
];
const data: LanesData = { readings: [360, 600], lanes: [top], events, opendota: [["Lion", "mid", "top"]] };

describe("lanes", () => {
  it("formats times and amounts", () => {
    expect(clock(433)).toBe("7:13");
    expect(amount(4695)).toBe("4.7k");
  });

  it("says which side was ahead on net worth", () => {
    expect(gapText(top, 360)).toBe("Dire +1.1k net worth at 6:00");
    expect(gapText(top, 600)).toBe("Level on net worth at 10:00");
  });

  it("keeps a lane's events up to the reading, and the rest apart", () => {
    expect(eventsIn(data, "top", 360)).toEqual([]);
    expect(eventsIn(data, "top", 600).map((e) => e[0])).toEqual([420, 424, 433, 539]);
    expect(eventsIn(data, null, 600).map((e) => e[3])).toEqual(["jungle"]);
  });

  it("names the killer's or visitor's lane only when it is another", () => {
    expect(eventText(events[3], 600)).toBe("Shadow Fiend killed by Timbersaw");
    expect(eventText(events[1], 600)).toBe("Sniper teleported to the lane (from mid)");
    expect(eventText(events[2], 600)).toBe("Sniper in the lane until 7:28 (from mid)");
    expect(eventText(events[4], 600)).toBe("Rubick in the lane, still there at 10:00 (from bottom)");
  });

  it("draws both sides' bars and shows shares under 80%", () => {
    const html = laneMarkup(data, top, 360);
    expect(html).toContain('Lion <span class="lane-share"');
    expect(html).not.toContain("Timbersaw <span");
    expect(html).toContain('<span class="lane-v">3.6k</span><span class="lane-bar lane-bar--radiant"><i style="width: 75.7%">');
    expect(html).toContain("<span>29</span>".replace("<span>", '<span class="lane-v">'));
    expect(html).toContain("No deaths, teleports or visits.");
  });

  it("lists the deaths outside the lanes and where OpenDota differs", () => {
    const html = figureMarkup(data, 600);
    expect(html).toContain("Outside the lanes");
    expect(html).toContain("Lion killed by Shadow Fiend (from top)");
    expect(html).toContain("OpenDota puts Lion in mid (over 0:00–10:00); here it is in top");
  });
});

describe("the committed data", () => {
  const real = committed as unknown as LanesData;
  it("has three lanes, each side with heroes and both readings", () => {
    expect(real.lanes.map((l) => l.lane)).toEqual(["top", "mid", "bot"]);
    const heroes = real.lanes.flatMap((l) => [...l.sides.r.heroes, ...l.sides.d.heroes]);
    expect(heroes).toHaveLength(10);
    for (const lane of real.lanes) for (const side of [lane.sides.r, lane.sides.d]) expect(Object.keys(side.at)).toEqual(["360", "600"]);
  });

  it("matches the page: Dire 1.1k ahead in top at 6:00", () => {
    expect(gapText(real.lanes[0], 360)).toBe("Dire +1.1k net worth at 6:00");
  });
});

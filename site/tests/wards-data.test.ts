import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import committed from "../src/data/wards.json";
import {
  clock,
  counts,
  perMinute,
  span,
  story,
  upIn,
  wardMarkup,
  wardsIn,
  type Ward,
  type WardsData,
} from "../src/lib/wards-data";

const ward = (team: "r" | "d", type: "o" | "s", placed: number, ended: number, how: "k" | "e" | "u", killer = ""): Ward => [
  team, type, 100, 200, placed, ended, how, "Lion", killer, clock(placed), clock(ended),
];
const data: WardsData = {
  start_s: -90,
  end_s: 300,
  radius: 87.3,
  range: [60, 120],
  wards: [
    ward("r", "o", 100, 460, "e"), // placed in the range
    ward("d", "s", -60, 70, "k", "Sniper"), // killed in the range
    ward("r", "s", 0, 60, "e"), // gone as the range starts: not up in it
    ward("d", "o", 130, 300, "u"), // after the range
  ],
};

describe("wards in a stretch", () => {
  it("counts a ward as up from its placement until it ended, half open", () => {
    expect(data.wards.map((w) => upIn(w, [60, 120]))).toEqual([true, true, false, false]);
    expect(data.wards.every((w) => upIn(w, null))).toBe(true);
  });

  it("lists the stretch's wards in placement order, through the filters", () => {
    expect(wardsIn(data, [60, 120])).toEqual([1, 0]);
    expect(wardsIn(data, null)).toEqual([1, 2, 0, 3]);
    expect(wardsIn(data, null, { teams: new Set(["r"]), types: new Set(["o", "s"]) })).toEqual([2, 0]);
    expect(wardsIn(data, null, { teams: new Set(["r", "d"]), types: new Set(["o"]) })).toEqual([0, 3]);
  });

  it("counts what's up, placed and killed in the stretch", () => {
    expect(counts(data, wardsIn(data, [60, 120]), [60, 120])).toEqual({ observers: 1, sentries: 1, placed: 1, killed: 1 });
  });

  it("counts each team's wards up in each minute", () => {
    const minutes = perMinute(data);
    expect(minutes[0]).toEqual({ from: -120, r: 0, d: 1 });
    expect(minutes.find((m) => m.from === 60)).toEqual({ from: 60, r: 1, d: 1 });
    expect(minutes.at(-1)!.from).toBe(240);
  });

  it("writes times as gem does, and tells a ward's story", () => {
    expect([clock(2569.9), clock(17), clock(-59.4), clock(-0.5)]).toEqual(["42:49", "00:17", "-01:00", "-00:01"]);
    expect(span(338.5)).toBe("5:39");
    expect(story(data.wards[1])).toBe("Dire sentry placed by Lion at -01:00; killed by Sniper at 01:10, after 2:10.");
    expect(story(data.wards[3])).toContain("still up when the recording ended");
  });

  it("draws observer circles under the badges, dashes the killed and puts the selected on top", () => {
    const svg = wardMarkup(data, [1, 0], [60, 120], "/f/", 1);
    expect(svg.indexOf("<circle class=\"ward-vision")).toBeLessThan(svg.indexOf("<g class=\"ward"));
    expect(svg.match(/<circle class="ward-vision /g)).toHaveLength(1); // the sentry has no circle
    expect(svg).toContain('class="ward ward--dire is-killed is-selected"');
    expect(svg.lastIndexOf('data-ward="1"')).toBeGreaterThan(svg.indexOf('data-ward="0"'));
    expect(svg).toContain('href="/f/ward_sentry.png"');
  });
});

describe("the committed wards", () => {
  const wards = committed as unknown as WardsData;

  it("is every ward of the home page's match, each ending after it went up", () => {
    expect(wards.wards).toHaveLength(221);
    expect(wards.wards.every((w) => w[5] > w[4])).toBe(true);
    expect(wards.wards.filter((w) => w[1] === "o")).toHaveLength(82);
  });

  it("opens on the stretch the recipe page's caption names", () => {
    const page = readFileSync(new URL("../src/content/docs/cookbook/wards.md", import.meta.url), "utf8");
    const [from, to] = wards.range!;
    expect(page).toContain(`The wards up from ${clock(from)} to ${clock(to)}`);
  });
});

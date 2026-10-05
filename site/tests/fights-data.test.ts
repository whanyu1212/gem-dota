import { readdirSync, readFileSync } from "node:fs";
import { gzipSync } from "node:zlib";
import { describe, expect, it } from "vitest";
import committed from "../src/data/fights/index.json";
import { card, fightDots, fightsIn, nextText, overlaps, type FightEntry, type FightsData } from "../src/lib/fights-data";

const fight = (n: number, start_s: number, deaths: number, kills: [number, number], extra: Partial<FightEntry> = {}): FightEntry => ({
  n,
  file: `fights/${n}.json`,
  start: "00:00",
  start_s,
  duration: 30,
  deaths,
  kills,
  more: kills[0] > kills[1] ? "r" : kills[1] > kills[0] ? "d" : "x",
  at: [100 * n, 100],
  gold: [100, -20],
  next: null,
  ...extra,
});
const data: FightsData = {
  start_s: -90,
  end_s: 600,
  fights: [fight(1, 60, 1, [0, 1]), fight(2, 200, 4, [3, 1], { next: ["Dire tier 1 middle tower", "r", 30] }), fight(3, 400, 2, [1, 1])],
};

describe("fights in a stretch", () => {
  it("keeps the fights that overlap the stretch, of at least a size", () => {
    expect(overlaps(data.fights[0], [80, 100])).toBe(true); // 60–90 overlaps
    expect(overlaps(data.fights[0], [91, 100])).toBe(false);
    expect(fightsIn(data, null).map((f) => f.n)).toEqual([1, 2, 3]);
    expect(fightsIn(data, null, 2).map((f) => f.n)).toEqual([2, 3]);
    expect(fightsIn(data, [150, 420], 1).map((f) => f.n)).toEqual([2, 3]);
  });

  it("says what a fight's card says", () => {
    const c = card({ ...data.fights[1], start: "03:20" });
    expect(c.title).toBe("Fight 2 · 03:20–03:50 · 0:30");
    expect(c.kills).toBe("3–1 kills, Radiant–Dire · Radiant had more · 4 deaths");
    expect(c.gold).toBe("Net gold near the fight: Radiant +100, Dire −20");
    expect(nextText(data.fights[1])).toBe("Radiant took the Dire tier 1 middle tower 30 s after it ended.");
    expect(nextText({ ...data.fights[1], next: ["Roshan", "d", 14] })).toBe("Dire killed Roshan 14 s after it ended.");
    expect(nextText(data.fights[0])).toContain("No building fell");
    expect(card(data.fights[2]).kills).toContain("even");
  });

  it("draws the biggest first, labels the bigger fights, and the selected last", () => {
    const svg = fightDots(data.fights, 1);
    expect(svg.indexOf('data-fight="2"')).toBeLessThan(svg.indexOf('data-fight="3"'));
    expect(svg.lastIndexOf('data-fight="1"')).toBeGreaterThan(svg.indexOf('data-fight="3"'));
    expect(svg).toContain('class="fight-dot fight-dot--dire is-selected"');
    expect(svg).toContain(">4</text>");
    expect(svg).not.toContain(">1</text>");
    expect(fightDots([{ ...data.fights[0], at: null }])).toBe(""); // can't be placed
  });
});

describe("the committed fights", () => {
  const fights = committed as unknown as FightsData;
  const dir = new URL("../src/data/", import.meta.url);

  it("is every fight of the home page's match, each with its file", () => {
    expect(fights.fights).toHaveLength(36);
    for (const f of fights.fights) expect(() => readFileSync(new URL(f.file, dir))).not.toThrow();
    // Figure 3's fight reuses fight.json; the rest have their own.
    expect(fights.fights.filter((f) => f.file === "fight.json")).toHaveLength(1);
    expect(readdirSync(new URL("fights/", dir)).filter((f) => /^\d+\.json$/.test(f))).toHaveLength(35);
  });

  it("gives a playback (a map crop) to exactly the fights with 3 or more deaths", () => {
    expect(fights.fights.filter((f) => f.box).map((f) => f.n)).toEqual(fights.fights.filter((f) => f.deaths >= 3).map((f) => f.n));
  });

  it("keeps each fight's file small: a breakdown tiny, a playback within budget", () => {
    for (const f of fights.fights.filter((f) => f.file !== "fight.json")) {
      const raw = readFileSync(new URL(f.file, dir));
      const heroStates = (JSON.parse(raw.toString()) as { heroes: { runs: unknown[] }[] }).heroes.some((h) => h.runs.length);
      expect(heroStates).toBe(Boolean(f.box));
      expect(gzipSync(raw).length).toBeLessThan(f.box ? 100_000 : 10_000);
    }
  });

  it("matches the recipe page's caption", () => {
    const page = readFileSync(new URL("../src/content/docs/cookbook/fights.md", import.meta.url), "utf8").replace(/\s+/g, " ");
    const biggest = [...fights.fights].sort((a, b) => b.deaths - a.deaths)[0];
    expect(page).toContain(`All ${fights.fights.length} fights in match 8856501050`);
    expect(page).toContain(`It opens on the biggest fight, ${biggest.start}.`);
  });
});

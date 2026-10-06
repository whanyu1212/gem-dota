import { describe, expect, it } from "vitest";
import committed from "../src/data/lead.json";
import {
  amount,
  axisMarkup,
  axisStep,
  clock,
  curveMarkup,
  flips,
  flipsMarkup,
  heroesMarkup,
  heroRows,
  marksMarkup,
  moved,
  movedMarkup,
  readingAt,
  scaleOf,
  summary,
  type LeadData,
} from "../src/lib/lead-data";

// Readings at 0:00, 1:00, 2:00, 3:00 and the end, 3:20.
const data: LeadData = {
  times: [0, 60, 120, 180, 200],
  gold: {
    lead: [0, 300, -200, 0, 1500],
    sources: [
      ["hero_kills", [0, 300, 100, 100, 1600]],
      ["neutral_creeps", [0, 0, -300, -100, -100]],
      ["unlisted", [0, 0, 0, 0, 0]],
    ],
  },
  xp: {
    lead: [0, 100, 100, 100, 100],
    sources: [["hero_kills", [0, 100, 100, 100, 100]]],
  },
  heroes: [
    { name: "Axe", side: "r", gold: [[0, 300, 300, 300, 1600], [0, 0, 50, 100, 100], [0, 90, 180, 270, 300]], xp: [0, 100, 100, 100, 100] },
    { name: "Lina", side: "d", gold: [[0, 0, 200, 200, 0], [0, 0, 300, 300, 300], [0, 90, 180, 270, 300]], xp: [0, 0, 0, 0, 0] },
  ],
  fights: [
    [1, 70, 100, 2, "d"],
    [2, 185, 199, 3, "r"],
  ],
  objectives: [["tower", "r", 195]],
};
const real = committed as unknown as LeadData;

describe("readings", () => {
  it("formats the in-game clock and amounts", () => {
    expect(clock(5576.4)).toBe("92:56");
    expect(clock(60)).toBe("1:00");
    expect(amount(-10730)).toBe("10.7k");
    expect(amount(950)).toBe("950");
  });

  it("snaps a time to the nearest reading", () => {
    expect(readingAt(data, 0)).toBe(0);
    expect(readingAt(data, 95)).toBe(2);
    expect(readingAt(data, 199)).toBe(4);
  });
});

describe("what moved the lead", () => {
  it("splits a stretch's change by source, adding up to the change in the lead", () => {
    const rows = moved(data, "gold", 1, 4);
    // The unlisted row didn't move, so it's left out.
    expect(rows.map((r) => [r.key, r.value])).toEqual([
      ["hero_kills", 1300],
      ["neutral_creeps", -100],
      ["lead", 1200],
    ]);
    expect(rows.at(-1)!.label).toBe("Change in the lead");
  });

  it("keeps the unlisted row when it moved", () => {
    const withGap: LeadData = { ...data, gold: { ...data.gold, sources: [...data.gold.sources.slice(0, 2), ["unlisted", [0, 0, 0, 0, 40]]] } };
    expect(moved(withGap, "gold", 0, 4).map((r) => r.label)).toContain("Not in the gold totals");
  });

  it("says who led at each end of the stretch", () => {
    expect(summary(data, "gold", 0, 4)).toBe("At the end of the game, 3:20, Radiant led by 1.5k gold.");
    expect(summary(data, "gold", 1, 2)).toBe("At 1:00 Radiant led by 300; at 2:00 Dire led by 200. The lead moved 500 gold toward Dire.");
    expect(summary(data, "xp", 2, 3)).toBe("At 2:00 Radiant led by 100; at 3:00 Radiant led by 100. The lead didn't move.");
  });

  it("draws Radiant's bars to the right and Dire's to the left", () => {
    const html = movedMarkup(moved(data, "gold", 1, 4), "gold");
    expect(html).toContain('class="lead-bar lead-bar--radiant" style="left: 50%; width: 50.00%"');
    expect(html).toContain('class="lead-bar lead-bar--dire" style="right: 50%; width: 3.85%"');
    expect(html).toContain("Radiant +1.2k");
    expect(html).toContain('class="lead-row lead-row--total"');
  });
});

describe("where the lead changed hands", () => {
  it("counts a flip only across zero, with the fights since the reading before", () => {
    expect(flips(data, "gold", 0, 4)).toEqual([
      { reading: 2, ahead: "d", fights: [1] },
      { reading: 4, ahead: "r", fights: [2] },
    ]);
  });

  it("keeps to the stretch, but remembers who led before it", () => {
    expect(flips(data, "gold", 3, 4)).toEqual([{ reading: 4, ahead: "r", fights: [2] }]);
    expect(flips(data, "gold", 0, 1)).toEqual([]);
  });

  it("links each fight to the fights page", () => {
    const html = flipsMarkup(data, flips(data, "gold", 0, 4), "/cookbook/fights");
    expect(html).toContain('2:00 Dire ahead (<a href="/cookbook/fights#fight-1">fight 1</a> since 1:00)');
    expect(flipsMarkup(data, [], "/x")).toBe("The lead didn't change hands in this stretch.");
    // Without the URL (the build's HTML), the fights are plain text.
    expect(flipsMarkup(data, flips(data, "gold", 0, 4), null)).toContain("(fight 1 since 1:00)");
  });
});

describe("heroes", () => {
  it("gives each hero's gold in three groups, or one XP part", () => {
    expect(heroRows(data, "gold", 1, 4)[0]).toEqual({ name: "Axe", side: "r", parts: [1300, 100, 210], total: 1610 });
    expect(heroRows(data, "xp", 0, 4)[1].parts).toEqual([0]);
  });

  it("draws a bar per hero under each team's total", () => {
    const html = heroesMarkup(heroRows(data, "gold", 0, 4), "gold");
    expect(html).toContain("Radiant · 2.0k gold");
    expect(html).toContain("Hero kills and assists");
    expect(heroesMarkup(heroRows(data, "xp", 0, 4), "xp")).toContain("XP earned");
  });
});

describe("the chart", () => {
  it("steps the axis to at most three gridlines a side", () => {
    expect(axisStep(1620)).toBe(1000);
    expect(axisStep(48000)).toBe(20000);
  });

  it("fits the scale to the lead, with a band for the side that barely led", () => {
    // Leads from -200 to 1500: Dire's side is a sixth of the span, not 200.
    const { hi, lo } = scaleOf(data, "gold");
    expect(hi).toBeCloseTo(1590);
    expect(lo).toBeCloseTo((-1700 / 6) * 1.06);
  });

  it("draws the readings edge to edge, with the area split at 0", () => {
    const svg = curveMarkup(data, "gold");
    const zero = ((1590 / (1590 + (1700 / 6) * 1.06)) * 200).toFixed(1);
    expect(svg).toContain(`points="0.0,${zero} 300.0,`);
    expect(svg).toContain(" 1000.0,");
    expect(svg).toContain(`class="lead-zero" x1="0" x2="1000" y1="${zero}" y2="${zero}"`);
    expect(svg).toContain(`<clipPath id="lead-above"><rect width="1000" height="${zero}">`);
  });

  it("labels 0 and each gridline", () => {
    const labels = [...axisMarkup(data, "gold").matchAll(/>([^<]+)</g)].map((m) => m[1]);
    expect(labels).toEqual(["0", "1.0k"]);
  });

  it("links each fight's dot to the fights page and sizes it by deaths", () => {
    const html = marksMarkup(data, "/cookbook/fights");
    expect(html).toContain('href="/cookbook/fights#fight-2" style="left: 92.50%; width: 9px; height: 9px" aria-label="Fight 2, 3:05, 3 deaths"');
    expect(html).toContain('class="lead-obj lead-obj--radiant" style="left: 97.50%"');
    expect(marksMarkup(data, null)).not.toContain("href");
  });
});

describe("the committed data", () => {
  it("adds every reading's sources up to its lead", () => {
    for (const kind of ["gold", "xp"] as const) {
      const split = real[kind];
      split.lead.forEach((lead, i) => expect(split.sources.reduce((s, [, series]) => s + series[i], 0)).toBe(lead));
    }
  });

  it("has every series at every reading, ending at the end of the game", () => {
    const n = real.times.length;
    expect(real.heroes).toHaveLength(10);
    for (const hero of real.heroes) {
      expect(hero.xp).toHaveLength(n);
      for (const series of hero.gold) expect(series).toHaveLength(n);
    }
    expect(clock(real.times[n - 1])).toBe("92:56");
  });
});

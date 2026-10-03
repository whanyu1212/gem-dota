import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { SECTIONS, activeLink, groupOf, prevNext, sectionOf } from "../src/nav";

const pages = readFileSync(new URL("../url-manifest.txt", import.meta.url), "utf8").split("\n").filter(Boolean);
const guide = SECTIONS.find((s) => s.key === "guide")!;
const internals = SECTIONS.find((s) => s.key === "internals")!;

describe("sections", () => {
  it("put every page except the home page in exactly one section", () => {
    for (const page of pages.filter((p) => p !== "/")) {
      const owners = SECTIONS.filter((section) => section.contains(page)).map((s) => s.key);
      expect(owners, page).toHaveLength(1);
    }
  });

  it("only link to pages that exist", () => {
    const links = SECTIONS.flatMap((s) => [s.link, ...s.groups.flatMap((g) => g.items.map((i) => i.link))]);
    expect(links.filter((link) => !pages.includes(link))).toEqual([]);
  });

  it("keep recipes out of Internals although they live in cookbook/", () => {
    expect(sectionOf("/cookbook/core-farm")?.key).toBe("recipes");
    expect(sectionOf("/cookbook/proto-files")?.key).toBe("internals");
    expect(sectionOf("/cookbook/proto-fields/demo")?.key).toBe("internals");
  });
});

describe("sidebar state", () => {
  it("highlights the page, or the nearest listed folder for an unlisted page", () => {
    expect(activeLink("/guides/09_cli", guide.groups)).toBe("/guides/09_cli");
    expect(activeLink("/cookbook/proto-fields/demo", internals.groups)).toBe("/cookbook/proto-fields/");
    expect(groupOf("/cookbook/proto-fields/demo", internals.groups)?.text).toBe("Protobuf");
  });

  it("steps through pages in sidebar order, across groups", () => {
    const { prev, next } = prevNext("/architecture", guide.groups);
    expect(prev?.link).toBe("/guides/01_quickstart");
    expect(next?.link).toBe("/guides/");
    expect(prevNext("/guides/01_quickstart", guide.groups).prev).toBeUndefined();
    expect(prevNext("/cookbook/proto-fields/demo", internals.groups)).toEqual({});
  });
});

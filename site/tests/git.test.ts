import { describe, expect, it } from "vitest";
import { lastEdits } from "../src/lib/git";

// `git log --format=@%cI --name-status -M`, newest commit first.
const log = [
  "@2026-10-04T10:00:00+08:00",
  "R100\tdocs/guides/a.md\tsite/src/content/docs/guides/a.md",
  "R088\tdocs/guides/b.md\tsite/src/content/docs/guides/b.md",
  "D\tdocs/old.md",
  "@2026-10-03T10:00:00+08:00",
  "M\tdocs/guides/a.md",
  "M\tdocs/guides/b.md",
  "A\tsite/src/new.ts",
  "@2026-09-01T10:00:00+08:00",
  "M\tdocs/guides/a.md",
  "A\tdocs/old.md",
].join("\n");

describe("lastEdits", () => {
  const dates = lastEdits(log);

  it("keeps a moved file's last edit, not the move", () => {
    expect(dates.get("site/src/content/docs/guides/a.md")).toBe("2026-10-03T10:00:00+08:00");
  });

  it("counts a rename with edits as a change", () => {
    expect(dates.get("site/src/content/docs/guides/b.md")).toBe("2026-10-04T10:00:00+08:00");
  });

  it("uses the newest commit for files that were never moved", () => {
    expect(dates.get("site/src/new.ts")).toBe("2026-10-03T10:00:00+08:00");
  });
});

import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { relative, resolve } from "node:path";
import { getCollection, type CollectionEntry } from "astro:content";
import { SECTIONS, type NavGroup, type Section } from "../nav";

export type DocEntry = CollectionEntry<"docs">;

// Astro runs from site/ (its project root), and entry.filePath is relative to it.
// import.meta.url would point into the bundled build output, not src/.
const siteRoot = process.cwd();
const repoRoot = resolve(siteRoot, "..");
export const REPO_URL = "https://github.com/whanyu1212/gem-dota";

/** Whether the entry is a folder's index page (docs/x/index.md or docs/index.md). */
export function isIndexPage(entry: DocEntry): boolean {
  return entry.id === "index" || entry.id.endsWith("/index");
}

/** The folder an index page stands for: "" for the home page, "x" for docs/x/index.md. */
export function indexFolder(entry: DocEntry): string {
  return entry.id === "index" ? "" : entry.id.slice(0, -"/index".length);
}

/** The page's path without the base, e.g. "/guides/01_quickstart" or "/reference/". */
export function pagePath(entry: DocEntry): string {
  if (entry.id === "index") return "/";
  return isIndexPage(entry) ? `/${indexFolder(entry)}/` : `/${entry.id}`;
}

/** The title: frontmatter `title`, else the first `# heading`, without Markdown code marks. */
export function pageTitle(entry: DocEntry): string {
  const heading = /^#\s+(.+?)\s*#*\s*$/m.exec(entry.body ?? "")?.[1];
  return (entry.data.title ?? heading ?? entry.id).replace(/`/g, "");
}

export async function getDocs(): Promise<DocEntry[]> {
  return getCollection("docs");
}

/** The file's path from the repository root, e.g. "docs/guides/01_quickstart.md". */
export function repoPath(entry: DocEntry): string {
  return relative(repoRoot, resolve(siteRoot, entry.filePath!));
}

let lastCommits: Map<string, string> | undefined;

/** When the page's file was last committed (ISO date), from one `git log` over the repo. */
export function lastUpdated(entry: DocEntry): string | undefined {
  if (!lastCommits) {
    lastCommits = new Map();
    try {
      const log = execFileSync("git", ["log", "--format=@%cI", "--name-only", "--", "."], {
        cwd: repoRoot,
        encoding: "utf8",
        maxBuffer: 256 * 1024 * 1024,
      });
      let date = "";
      for (const line of log.split("\n")) {
        if (line.startsWith("@")) date = line.slice(1);
        else if (line && !lastCommits.has(line)) lastCommits.set(line, date);
      }
    } catch {
      // Not a git checkout: pages show no date.
    }
  }
  return lastCommits.get(repoPath(entry));
}

/** The package version from pyproject.toml. */
export const VERSION =
  /^version\s*=\s*"([^"]+)"/m.exec(readFileSync(resolve(repoRoot, "pyproject.toml"), "utf8"))?.[1] ?? "";

/** The Reference sidebar, built from the reference pages. */
export function referenceGroups(docs: DocEntry[]): NavGroup[] {
  const pages = docs.filter((entry) => entry.id.startsWith("reference/") && !isIndexPage(entry));
  const item = (entry: DocEntry) => ({ text: pageTitle(entry), link: pagePath(entry) });
  const byTitle = (a: { text: string }, b: { text: string }) => a.text.localeCompare(b.text);
  return [
    { text: "Reference", items: [{ text: "Overview", link: "/reference/" }] },
    {
      text: "Modules",
      items: pages.filter((entry) => !entry.id.startsWith("reference/extractors/")).map(item).sort(byTitle),
    },
    {
      text: "Extractors",
      items: [
        { text: "Overview", link: "/reference/extractors/" },
        ...pages.filter((entry) => entry.id.startsWith("reference/extractors/")).map(item).sort(byTitle),
      ],
    },
  ];
}

/** The page's section, with the Reference sidebar filled in. */
export function sectionFor(path: string, docs: DocEntry[]): Section | undefined {
  const section = SECTIONS.find((s) => s.contains(path));
  if (section?.key === "reference") return { ...section, groups: referenceGroups(docs) };
  return section;
}

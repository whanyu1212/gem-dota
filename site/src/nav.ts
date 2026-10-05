/**
 * The site's navigation: five sections shown as tabs in the top bar, each with
 * its own sidebar. Links are page paths without the base ("/guides/01_quickstart",
 * "/reference/"), the same form as url-manifest.txt.
 *
 * The Reference sidebar is filled from the reference pages themselves (see
 * pages.ts), since those pages are generated from the docstrings.
 */

export interface NavItem {
  text: string;
  link: string;
}

export interface NavGroup {
  text: string;
  items: NavItem[];
}

export interface Section {
  key: "guide" | "recipes" | "reference" | "internals" | "changelog";
  text: string;
  /** Where the tab goes. */
  link: string;
  groups: NavGroup[];
  /** Whether a page belongs to this section, including pages not in its sidebar. */
  contains: (path: string) => boolean;
}

const RECIPES = [
  "/cookbook/questions",
  "/cookbook/roshan-next-fight",
  "/cookbook/core-farm",
  "/cookbook/smoke-to-kill",
  "/cookbook/fights",
  "/cookbook/wards",
];

const startsWithAny = (path: string, prefixes: string[]) => prefixes.some((p) => path.startsWith(p));

export const SECTIONS: Section[] = [
  {
    key: "guide",
    text: "Guide",
    link: "/guides/01_quickstart",
    contains: (path) => startsWithAny(path, ["/guides/", "/architecture", "/reports/", "/experimental/"]),
    groups: [
      {
        text: "Getting started",
        items: [
          { text: "Quickstart", link: "/guides/01_quickstart" },
          { text: "Architecture", link: "/architecture" },
        ],
      },
      {
        text: "Guides",
        items: [
          { text: "Overview", link: "/guides/" },
          { text: "Entity State", link: "/guides/02_entity_state" },
          { text: "Combat Log", link: "/guides/03_combat_log" },
          { text: "Full Match Data", link: "/guides/04_match_data" },
          { text: "Time Series and DataFrames", link: "/guides/05_timeseries" },
          { text: "Fight Detection", link: "/guides/06_fights" },
          { text: "Custom Extractors", link: "/guides/07_custom_extractors" },
          { text: "Laning Analysis", link: "/guides/08_laning" },
          { text: "CLI Reference", link: "/guides/09_cli" },
          { text: "JSON Output Shape", link: "/guides/10_json_output" },
          { text: "Map Regions and Camps", link: "/experimental/map-annotations" },
        ],
      },
      {
        text: "Reports",
        items: [{ text: "Match Reports", link: "/reports/" }],
      },
      {
        text: "Experimental",
        items: [
          { text: "Overview", link: "/experimental/" },
          { text: "Farming Patterns", link: "/experimental/farming-patterns" },
          { text: "Farming Route Calibration", link: "/experimental/farming-patterns-calibration" },
          { text: "Roshan Conversion", link: "/experimental/rosh-conversion" },
          { text: "Roshan Conversion Calibration", link: "/experimental/rosh-conversion-calibration" },
          { text: "Smoke Analysis", link: "/experimental/smoke-analysis" },
          { text: "Fight Positioning", link: "/experimental/fight-positioning" },
          { text: "Fight Timeline", link: "/experimental/fight-timeline" },
          { text: "Point-Vision Evidence", link: "/experimental/estimate-vision" },
          { text: "Vision Modifiers", link: "/experimental/vision-modifiers" },
        ],
      },
    ],
  },
  {
    key: "recipes",
    text: "Recipes",
    link: "/cookbook/questions",
    contains: (path) => RECIPES.includes(path),
    groups: [
      {
        text: "Recipes",
        items: [
          { text: "Answering Questions from the Facts", link: "/cookbook/questions" },
          { text: "Roshan and the Next Fight", link: "/cookbook/roshan-next-fight" },
          { text: "Core Farm, 10 to 20 Minutes", link: "/cookbook/core-farm" },
          { text: "Smokes and Kills", link: "/cookbook/smoke-to-kill" },
          { text: "Wards and Vision", link: "/cookbook/wards" },
          { text: "Fights and Kills", link: "/cookbook/fights" },
        ],
      },
    ],
  },
  {
    key: "reference",
    text: "Reference",
    link: "/reference/",
    contains: (path) => path.startsWith("/reference/"),
    groups: [],
  },
  {
    key: "internals",
    text: "Internals",
    link: "/deep-dives/",
    contains: (path) =>
      !RECIPES.includes(path) && startsWithAny(path, ["/deep-dives/", "/cookbook/", "/benchmarks/"]),
    groups: [
      {
        text: "Parser internals",
        items: [
          { text: "Overview", link: "/deep-dives/" },
          { text: "Entity Decoding 1: The Schema", link: "/deep-dives/entity-schema" },
          { text: "Entity Decoding 2: Field Paths", link: "/deep-dives/entity-field-paths" },
          { text: "Entity Decoding 3: Field Decoders", link: "/deep-dives/entity-field-decoders" },
          { text: "Entity Decoding 4: Field State", link: "/deep-dives/entity-field-state" },
          { text: "Entity Decoding 5: Entity Lifecycle", link: "/deep-dives/entity-lifecycle" },
          { text: "String Tables", link: "/deep-dives/string-tables" },
          { text: "Replay Edge Cases", link: "/deep-dives/replay-edge-cases" },
        ],
      },
      {
        text: "Protobuf",
        items: [
          { text: "Overview", link: "/cookbook/" },
          { text: "Bits and Bytes Primer", link: "/cookbook/bits-and-bytes-primer" },
          { text: "How Proto Parsing Works", link: "/cookbook/proto-parsing-pipeline" },
          { text: "The Proto Files gem Uses", link: "/cookbook/proto-files" },
          { text: "Proto Field Atlas", link: "/cookbook/proto-fields/" },
        ],
      },
      {
        text: "Performance",
        items: [
          { text: "Parser Performance", link: "/deep-dives/parser-performance" },
          { text: "Parser Profile, 2026-09", link: "/deep-dives/parser-profile-2026-09" },
          { text: "Profile Measurements", link: "/benchmarks/2026-09-08-parser/" },
          { text: "Rust Kernel Plan", link: "/deep-dives/rust-kernel-plan" },
        ],
      },
    ],
  },
  {
    key: "changelog",
    text: "Changelog",
    link: "/changelog",
    contains: (path) => path === "/changelog",
    groups: [],
  },
];

export function sectionOf(path: string): Section | undefined {
  return SECTIONS.find((section) => section.contains(path));
}

/**
 * The sidebar item to highlight: the page itself, or for a page that isn't
 * listed (a proto-field page) the closest listed folder above it.
 */
export function activeLink(path: string, groups: NavGroup[]): string | undefined {
  const links = groups.flatMap((group) => group.items.map((item) => item.link));
  if (links.includes(path)) return path;
  return links
    .filter((link) => link.endsWith("/") && path.startsWith(link))
    .sort((a, b) => b.length - a.length)[0];
}

/** The previous and next pages in sidebar order, for a page listed in the sidebar. */
export function prevNext(path: string, groups: NavGroup[]): { prev?: NavItem; next?: NavItem } {
  const items = groups.flatMap((group) => group.items);
  const index = items.findIndex((item) => item.link === path);
  if (index === -1) return {};
  return { prev: items[index - 1], next: items[index + 1] };
}

/** The sidebar group a page sits in, for the breadcrumb. */
export function groupOf(path: string, groups: NavGroup[]): NavGroup | undefined {
  const link = activeLink(path, groups);
  return groups.find((group) => group.items.some((item) => item.link === link));
}

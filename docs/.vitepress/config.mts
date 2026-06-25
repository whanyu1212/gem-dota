import { defineConfig } from "vitepress";
import { withMermaid } from "vitepress-plugin-mermaid";

export default withMermaid(
  defineConfig({
  title: "gem-dota",
  description: "A Python Dota 2 replay parser.",
  base: "/gem-dota/",
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "Docs", link: "/" },
      { text: "API Reference", link: "/reference/" },
      { text: "Changelog", link: "/changelog" },
    ],
    sidebar: [
      {
        text: "Getting Started",
        items: [
          { text: "Home", link: "/" },
          { text: "Architecture", link: "/architecture" },
          { text: "Quickstart", link: "/guides/01_quickstart" },
          { text: "Bits & Bytes Primer", link: "/cookbook/bits-and-bytes-primer" },
        ],
      },
      {
        text: "Proto Cookbook",
        items: [
          { text: "Overview", link: "/cookbook/" },
          { text: "How Proto Parsing Works", link: "/cookbook/proto-parsing-pipeline" },
          { text: "Full Proto Dota2 Catalog", link: "/cookbook/proto-dota2-catalog" },
          { text: "Proto Field Atlas", link: "/cookbook/proto-fields/" },
        ],
      },
      {
        text: "Internals",
        items: [
          { text: "Parser Internals", link: "/deep-dives/" },
          { text: "Replay Edge Cases", link: "/deep-dives/replay-edge-cases" },
        ],
      },
      {
        text: "Guides",
        items: [
          { text: "Overview", link: "/guides/" },
          { text: "Entity State", link: "/guides/02_entity_state" },
          { text: "Combat Log", link: "/guides/03_combat_log" },
          { text: "Full Match Data", link: "/guides/04_match_data" },
          { text: "Time-Series and DataFrames", link: "/guides/05_timeseries" },
          { text: "Teamfight Detection", link: "/guides/06_teamfights" },
          { text: "Custom Extractors", link: "/guides/07_custom_extractors" },
          { text: "Laning Analysis", link: "/guides/08_laning" },
          { text: "CLI Reference", link: "/guides/09_cli" },
          { text: "JSON Output Shape", link: "/guides/10_json_output" },
        ],
      },
      {
        text: "Reports",
        items: [{ text: "Match Reports", link: "/reports/" }],
      },
      {
        text: "Experimental Features",
        items: [
          { text: "Overview", link: "/experimental/" },
          { text: "Farming Patterns", link: "/experimental/farming-patterns" },
          { text: "Roshan Conversion", link: "/experimental/rosh-conversion" },
          { text: "Estimate Vision", link: "/experimental/estimate-vision" },
          { text: "Vision Modifiers", link: "/experimental/vision-modifiers" },
        ],
      },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/whanyu1212/gem-dota" }],
    search: {
      provider: "local",
    },
  },
  // Mermaid runtime options — themed to follow VitePress light/dark.
  mermaid: {
    theme: "default",
  },
  }),
);

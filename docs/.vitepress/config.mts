import { defineConfig } from "vitepress";

export default defineConfig({
  title: "gem-dota",
  description: "A Python Dota 2 replay parser.",
  base: "/gem-dota/",
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "Getting Started", link: "/" },
      { text: "Proto Cookbook", link: "/cookbook/" },
      { text: "Deep Dives", link: "/deep-dives/" },
      { text: "Guides", link: "/guides/" },
      { text: "Reports", link: "/reports/" },
      { text: "Experimental Features", link: "/experimental/" },
      { text: "Changelog", link: "/changelog" },
      // { text: "Replay Parser", link: "/replay-parser" },
      { text: "API Reference", link: "/reference/" },
    ],
    sidebar: [
      {
        text: "Getting Started",
        items: [
          { text: "Home", link: "/" },
          { text: "Changelog", link: "/changelog" },
          { text: "Quickstart", link: "/guides/01_quickstart" },
          { text: "Troubleshooting", link: "/guides/troubleshooting" },
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
        text: "Deep Dives",
        items: [
          { text: "Overview", link: "/deep-dives/" },
          { text: "Stream Layer", link: "/deep-dives/stream-layer" },
          { text: "Parser Layer", link: "/deep-dives/parser-layer" },
          { text: "SendTable Layer", link: "/deep-dives/sendtable-layer" },
          {
            text: "State Reconstruction Layer",
            link: "/deep-dives/state-layer",
          },
          {
            text: "Event Normalization Layer",
            link: "/deep-dives/event-layer",
          },
          {
            text: "Extractors Layer",
            link: "/deep-dives/extractors-layer",
          },
          {
            text: "Match Assembly Layer",
            link: "/deep-dives/match-assembly-layer",
          },
          {
            text: "Replay Edge Cases",
            link: "/deep-dives/replay-edge-cases",
          },
        ],
      },
      {
        text: "Guides",
        items: [
          { text: "Entity State", link: "/guides/02_entity_state" },
          { text: "Combat Log", link: "/guides/03_combat_log" },
          { text: "Full Match Data", link: "/guides/04_match_data" },
          { text: "Time-Series and DataFrames", link: "/guides/05_timeseries" },
          { text: "Teamfight Detection", link: "/guides/06_teamfights" },
          { text: "Custom Extractors", link: "/guides/07_custom_extractors" },
          { text: "Laning Analysis", link: "/guides/08_laning" },
          { text: "CLI Reference", link: "/guides/09_cli" },
          { text: "Annotated JSON Output", link: "/guides/10_json_output" },
        ],
      },
      {
        text: "Interactive",
        items: [
          // { text: "Replay Parser", link: "/replay-parser" },
          // { text: "Replay API Contract", link: "/guides/replay-api" },
          // { text: "Architecture", link: "/architecture" },
          { text: "Reports", link: "/reports/" },
        ],
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
      {
        text: "Changelog",
        items: [{ text: "Changelog", link: "/changelog" }],
      },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/whanyu1212/gem-dota" }],
    search: {
      provider: "local",
    },
  },
});

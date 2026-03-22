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
      { text: "Guides", link: "/guides/index" },
      { text: "Understanding", link: "/understanding/index" },
      { text: "Replay Parser", link: "/replay-parser" },
      { text: "API Reference", link: "/reference/index" },
      { text: "Reports", link: "/reports/" },
    ],
    sidebar: [
      {
        text: "Getting Started",
        items: [
          { text: "Home", link: "/" },
          { text: "Guides Overview", link: "/guides/index" },
          { text: "Quickstart", link: "/guides/01_quickstart" },
          { text: "Troubleshooting", link: "/guides/troubleshooting" },
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
        text: "Understanding",
        items: [
          { text: "Overview", link: "/understanding/index" },
          { text: "Protocol Buffers", link: "/understanding/01_protobuf" },
          { text: "The .dem Format", link: "/understanding/02_dem_format" },
          { text: "Snappy Compression", link: "/understanding/03_snappy" },
          { text: "Send Tables and Schema", link: "/understanding/04_send_tables" },
          { text: "Field Paths and Huffman", link: "/understanding/05_field_paths" },
          { text: "Field Decoders", link: "/understanding/06_field_decoders" },
          { text: "String Tables", link: "/understanding/07_string_tables" },
          { text: "Entity System", link: "/understanding/08_entity_system" },
          { text: "Combat Log", link: "/understanding/09_combat_log" },
          { text: "Game Events", link: "/understanding/10_game_events" },
        ],
      },
      {
        text: "Interactive",
        items: [
          { text: "Replay Parser", link: "/replay-parser" },
          { text: "Replay API Contract", link: "/guides/replay-api" },
          { text: "Architecture", link: "/architecture" },
          { text: "Reports", link: "/reports/" },
        ],
      },
    ],
    socialLinks: [{ icon: "github", link: "https://github.com/whanyu1212/gem-dota" }],
    search: {
      provider: "local",
    },
  },
});

// The gem docs site. Until HY-118 moves the content here, pages are read from
// ../docs, and URLs must match the VitePress build (see url-manifest.txt).
import { fileURLToPath } from "node:url";
import { defineConfig } from "astro/config";
import { docsMarkdown } from "./src/markdown/index.ts";

const base = "/gem-dota";
const path = (relative) => fileURLToPath(new URL(relative, import.meta.url));

export default defineConfig({
  site: "https://whanyu1212.github.io",
  base,
  trailingSlash: "ignore",
  publicDir: "../docs/public",
  // "preserve" writes x/index.md as x/index.html and x/y.md as x/y.html, the
  // same files VitePress writes with cleanUrls.
  build: { format: "preserve" },
  markdown: {
    shikiConfig: { theme: "github-dark" },
    processor: docsMarkdown({
      base,
      contentRoot: path("../docs"),
      publicDir: path("../docs/public"),
      repoRoot: path(".."),
      repoBlobUrl: "https://github.com/whanyu1212/gem-dota/blob/main",
    }),
  },
});

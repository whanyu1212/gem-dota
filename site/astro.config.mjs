// The gem docs site. Pages are Markdown in src/content/docs; their URLs must
// keep matching the old VitePress site's (see url-manifest.txt).
import { fileURLToPath } from "node:url";
import { defineConfig } from "astro/config";
import { docsMarkdown } from "./src/markdown/index.ts";
import { gemCodeTheme } from "./src/markdown/shiki-theme.ts";

const base = "/gem-dota";
const path = (relative) => fileURLToPath(new URL(relative, import.meta.url));

export default defineConfig({
  site: "https://whanyu1212.github.io",
  base,
  trailingSlash: "ignore",
  // "preserve" writes x/index.md as x/index.html and x/y.md as x/y.html, the
  // same files VitePress writes with cleanUrls.
  build: { format: "preserve" },
  markdown: {
    shikiConfig: { theme: gemCodeTheme },
    processor: docsMarkdown({
      base,
      contentRoot: path("src/content/docs"),
      publicDir: path("public"),
      repoRoot: path(".."),
      repoBlobUrl: "https://github.com/whanyu1212/gem-dota/blob/main",
    }),
  },
});

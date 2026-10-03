// The gem docs site. Until HY-118 moves the content here, pages are read from
// ../docs, and URLs must match the VitePress build (see url-manifest.txt).
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://whanyu1212.github.io",
  base: "/gem-dota",
  trailingSlash: "ignore",
  publicDir: "../docs/public",
  // "preserve" writes x/index.md as x/index.html and x/y.md as x/y.html, the
  // same files VitePress writes with cleanUrls.
  build: { format: "preserve" },
  markdown: { shikiConfig: { theme: "github-dark" } },
});

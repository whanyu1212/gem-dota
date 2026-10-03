// Check that the built site still serves every URL in url-manifest.txt.
//
//   node scripts/check-urls.mjs                 compare dist/ with the manifest
//   node scripts/check-urls.mjs --write <dir>   rewrite the manifest from a built site
//
// The manifest was written from the VitePress build (docs/.vitepress/dist), so
// moving to Astro keeps every published URL. A missing URL fails; a new page is
// only listed.
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const siteDir = fileURLToPath(new URL("..", import.meta.url));
const manifestPath = join(siteDir, "url-manifest.txt");

function htmlFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((item) => {
    const path = join(dir, item.name);
    if (item.isDirectory()) return htmlFiles(path);
    return item.name.endsWith(".html") ? [path] : [];
  });
}

/** The URL GitHub Pages serves a file at: x/index.html -> /x/, x/y.html -> /x/y. */
function urlOf(root, file) {
  const path = relative(root, file).split(sep).join("/");
  if (path === "index.html") return "/";
  if (path.endsWith("/index.html")) return `/${path.slice(0, -"index.html".length)}`;
  return `/${path.slice(0, -".html".length)}`;
}

function urls(root) {
  return htmlFiles(root)
    .map((file) => urlOf(root, file))
    .filter((url) => url !== "/404")
    .sort();
}

const args = process.argv.slice(2);
if (args[0] === "--write") {
  if (!args[1]) throw new Error("usage: check-urls.mjs --write <built site dir>");
  const list = urls(args[1]);
  writeFileSync(manifestPath, `${list.join("\n")}\n`);
  console.log(`Wrote ${list.length} URLs to url-manifest.txt`);
} else {
  const expected = readFileSync(manifestPath, "utf8").split("\n").filter(Boolean);
  const built = new Set(urls(join(siteDir, "dist")));
  const missing = expected.filter((url) => !built.has(url));
  const added = [...built].filter((url) => !expected.includes(url));
  for (const url of added) console.log(`new page: ${url}`);
  if (missing.length) {
    for (const url of missing) console.error(`missing: ${url}`);
    console.error(`${missing.length} of ${expected.length} URLs are missing from dist/`);
    process.exit(1);
  }
  console.log(`All ${expected.length} URLs in url-manifest.txt are built.`);
}

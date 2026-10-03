// Check every internal link and image in the built site (dist/): the page or
// file must exist, and a #fragment must match an id on the target page.
//
//   node scripts/check-links.mjs
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { join, relative } from "node:path";
import { fileURLToPath } from "node:url";

const BASE = "/gem-dota";
const dist = fileURLToPath(new URL("../dist", import.meta.url));

function htmlFiles(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((item) => {
    const path = join(dir, item.name);
    if (item.isDirectory()) return htmlFiles(path);
    return item.name.endsWith(".html") ? [path] : [];
  });
}

/** The file GitHub Pages serves for a URL path under the base, if any. */
function servedFile(urlPath) {
  const rest = urlPath.slice(BASE.length) || "/";
  const candidates = rest.endsWith("/")
    ? [join(dist, rest, "index.html")]
    : [join(dist, rest), join(dist, `${rest}.html`), join(dist, rest, "index.html")];
  return candidates.find((path) => existsSync(path) && statSync(path).isFile());
}

/** The URL a page is served at, used to resolve its relative links. */
function pageUrl(file) {
  const path = relative(dist, file).split("\\").join("/");
  if (path.endsWith("index.html")) return `${BASE}/${path.slice(0, -"index.html".length)}`;
  return `${BASE}/${path.slice(0, -".html".length)}`;
}

const ids = new Map();
function idsOf(file) {
  if (!ids.has(file)) {
    const html = readFileSync(file, "utf8");
    ids.set(file, new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1])));
  }
  return ids.get(file);
}

const decode = (text) => text.replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#x27;|&#39;/g, "'");

const broken = [];
let checked = 0;
for (const file of htmlFiles(dist)) {
  const html = readFileSync(file, "utf8");
  const page = new URL(pageUrl(file), "http://site");
  for (const [, attribute, raw] of html.matchAll(/\s(href|src)="([^"]*)"/g)) {
    const value = decode(raw);
    if (/^([a-z][a-z\d+.-]*:|\/\/)/i.test(value) || value === "") continue;
    checked++;
    const url = new URL(value, page);
    const path = decodeURIComponent(url.pathname);
    const target = path === page.pathname ? file : servedFile(path);
    const where = `${relative(dist, file)}: ${attribute}="${value}"`;
    if (!path.startsWith(BASE) || !target) {
      broken.push(`${where} (no such page or file)`);
    } else if (url.hash && target.endsWith(".html") && !idsOf(target).has(decodeURIComponent(url.hash.slice(1)))) {
      broken.push(`${where} (no #${decodeURIComponent(url.hash.slice(1))} on ${relative(dist, target)})`);
    }
  }
}

for (const line of broken) console.error(line);
if (broken.length) {
  console.error(`${broken.length} of ${checked} internal links are broken`);
  process.exit(1);
}
console.log(`All ${checked} internal links resolve.`);

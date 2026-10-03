/**
 * Rewrites internal links the way VitePress does, so Markdown written for
 * VitePress keeps working:
 *
 * - `guides/04_match_data.md#anchor` (relative to the page's file) becomes
 *   `/gem-dota/guides/04_match_data#anchor`, and `x/index.md` becomes `/gem-dota/x/`.
 * - Absolute site paths (`/map-annotations.jpg`, `/guides/09_cli`) get the base.
 * - A link to a file in the repository that the site doesn't serve (a benchmark
 *   JSON next to its page, an example script) points at the file on GitHub.
 *
 * Other relative links (`guides/01_quickstart`, `../reference/`) are already
 * page URLs, and the browser resolves them the same way it did under VitePress.
 */
import { existsSync, statSync } from "node:fs";
import { dirname, relative, resolve, sep } from "node:path";
import type { Element, Root } from "hast";
import { visit } from "unist-util-visit";
import type { VFile } from "vfile";

export interface LinkOptions {
  /** The site's base path, e.g. "/gem-dota". */
  base: string;
  /** Absolute path of the folder the pages are read from (src/content/docs). */
  contentRoot: string;
  /** Absolute path of the folder served at the site root (public assets). */
  publicDir: string;
  /** Absolute path of the repository root, for GitHub links. */
  repoRoot: string;
  /** Prefix for GitHub links to repository files, e.g. ".../blob/main". */
  repoBlobUrl: string;
}

const EXTERNAL = /^([a-z][a-z\d+.-]*:|\/\/|#)/i;

const isFile = (path: string) => existsSync(path) && statSync(path).isFile();
const toPosix = (path: string) => path.split(sep).join("/");

/** The page URL path (without base) for a Markdown file under the content root. */
function pageUrl(contentPath: string): string {
  const page = toPosix(contentPath).replace(/\.md$/, "");
  if (page === "index") return "/";
  if (page.endsWith("/index")) return `/${page.slice(0, -"index".length)}`;
  return `/${page}`;
}

export function rewriteUrl(url: string, filePath: string | undefined, options: LinkOptions): string {
  if (!url || EXTERNAL.test(url)) return url;
  const match = /^([^?#]*)(.*)$/.exec(url)!;
  const path = decodeURI(match[1]);
  const suffix = match[2];
  if (!path) return url;

  if (path.startsWith("/")) {
    if (path === options.base || path.startsWith(`${options.base}/`)) return url;
    const target = path.endsWith(".md") ? pageUrl(path.slice(1)) : path;
    return `${options.base}${target}${suffix}`;
  }

  if (!filePath) return url;
  const target = resolve(dirname(filePath), path);
  const inContent = !relative(options.contentRoot, target).startsWith("..");

  if (path.endsWith(".md") && inContent) {
    return `${options.base}${pageUrl(relative(options.contentRoot, target))}${suffix}`;
  }
  if (isFile(target) && !target.startsWith(options.publicDir)) {
    // A repository file the site doesn't publish, e.g. ../../CHANGELOG.md or data.json.
    return `${options.repoBlobUrl}/${toPosix(relative(options.repoRoot, target))}${suffix}`;
  }
  return url;
}

export default function rehypeLinks(options: LinkOptions) {
  return (tree: Root, file: VFile) => {
    visit(tree, "element", (node: Element) => {
      const attribute = node.tagName === "a" ? "href" : node.tagName === "img" ? "src" : undefined;
      if (!attribute) return;
      const value = node.properties[attribute];
      if (typeof value !== "string") return;
      // Relative images are Astro's (it bundles them); only absolute ones need the base.
      if (attribute === "src" && !value.startsWith("/")) return;
      node.properties[attribute] = rewriteUrl(value, file.path, options);
    });
  };
}

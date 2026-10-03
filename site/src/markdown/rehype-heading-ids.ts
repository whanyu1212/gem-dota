/**
 * Heading IDs that match VitePress's, so `#anchor` links into the docs keep
 * working after the move. Astro's own heading-ID step (github-slugger) only
 * fills in headings that have no ID yet, so it keeps these, and its heading list
 * (the "On this page" outline) uses them too.
 *
 * Reference: VitePress 1.6 `slugify` (from @mdit-vue/shared) and markdown-it-anchor's
 * unique-slug rule (`x`, `x-1`, `x-2`, …).
 */
import type { Element, ElementContent, Root } from "hast";
import { visit } from "unist-util-visit";

const CONTROL = /[\u0000-\u001f]/g;
const SPECIAL = /[\s~`!@#$%^&*()\-_+=[\]{}|\\;:"'“”‘’<>,.?/]+/g;
const COMBINING = /[̀-ͯ]/g;

export function vitepressSlug(text: string): string {
  return text
    .normalize("NFKD")
    .replace(COMBINING, "")
    .replace(CONTROL, "")
    .replace(SPECIAL, "-")
    .replace(/-{2,}/g, "-")
    .replace(/^-+|-+$/g, "")
    .replace(/^(\d)/, "_$1")
    .toLowerCase();
}

/** The heading's text as markdown-it sees it: text and inline code, not image alt text. */
function headingText(nodes: ElementContent[]): string {
  return nodes
    .map((node) => {
      if (node.type === "text") return node.value;
      if (node.type === "element") return headingText(node.children);
      return "";
    })
    .join("");
}

export default function rehypeHeadingIds() {
  return (tree: Root) => {
    const used = new Set<string>();
    visit(tree, "element", (node: Element) => {
      if (!/^h[1-6]$/.test(node.tagName)) return;
      if (typeof node.properties.id === "string") {
        used.add(node.properties.id);
        return;
      }
      const base = vitepressSlug(headingText(node.children));
      let slug = base;
      for (let i = 1; used.has(slug); i++) slug = `${base}-${i}`;
      used.add(slug);
      node.properties.id = slug;
    });
  };
}

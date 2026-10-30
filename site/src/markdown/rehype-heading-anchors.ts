/**
 * A link to each section, so a reader can copy it: every h2–h4 at the top level
 * of a page gets `<a class="heading-anchor" href="#id">` after its text, shown on
 * hover and keyboard focus (prose.css).
 *
 * The link holds no text. Its "#" is drawn by CSS, so Astro's heading list (the
 * "On this page" outline) and Pagefind read the heading as they did before.
 * Headings inside callouts, figures and code groups get none, nor do headings
 * that already hold a link (a link can't sit inside another).
 *
 * Runs after rehype-heading-ids.ts, which gives every heading its ID.
 */
import type { Element, ElementContent, Root } from "hast";

const SECTION = /^h[2-4]$/;

function text(nodes: ElementContent[]): string {
  return nodes
    .map((node) => {
      if (node.type === "text") return node.value;
      if (node.type === "element") return text(node.children);
      return "";
    })
    .join("");
}

function holdsLink(node: Element): boolean {
  return node.children.some((child) => child.type === "element" && (child.tagName === "a" || holdsLink(child)));
}

export default function rehypeHeadingAnchors() {
  return (tree: Root) => {
    for (const node of tree.children) {
      if (node.type !== "element" || !SECTION.test(node.tagName)) continue;
      const id = node.properties.id;
      if (typeof id !== "string" || holdsLink(node)) continue;
      node.children.push({
        type: "element",
        tagName: "a",
        properties: {
          className: ["heading-anchor"],
          href: `#${id}`,
          ariaLabel: `Link to section “${text(node.children).trim()}”`,
          dataPagefindIgnore: "",
        },
        children: [],
      });
    }
  };
}

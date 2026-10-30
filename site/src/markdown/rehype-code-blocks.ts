/**
 * Wraps every code block in `<div class="code-block">` at build time and labels
 * it: with the file's path for a `<<< @/…` import (preprocess.ts writes that
 * wrapper itself, with `data-file`), otherwise with the block's language. Plain
 * text blocks get no label, nor do blocks in a code group, whose tabs name them.
 *
 * The label sits before the `<pre>`, so it isn't part of what the copy button
 * copies, and Pagefind skips it. The copy button and the fade shown while a
 * block scrolls further right are added in the browser (src/lib/code-blocks.ts).
 *
 * Runs after rehype-raw (so the import wrappers are elements) and after Astro's
 * Shiki step, which sets `data-language` on each `<pre>`. Without highlighting
 * (the tests), the language comes from the `language-*` class on the `<code>`.
 */
import type { Element, ElementContent, Parents, Root } from "hast";

/** Fence languages shown under another name. */
const ALIASES: Record<string, string> = { py: "python", sh: "bash", shell: "bash", zsh: "bash" };
/** Fence languages that get no label: output and plain text. */
const UNLABELLED = new Set(["", "plaintext", "text", "txt"]);

function classes(node: Element): string[] {
  const value = node.properties.className;
  return Array.isArray(value) ? value.map(String) : [];
}

function languageOf(pre: Element): string {
  if (typeof pre.properties.dataLanguage === "string") return pre.properties.dataLanguage;
  const code = pre.children.find((child): child is Element => child.type === "element" && child.tagName === "code");
  const match = code && classes(code).map((name) => /^language-(.+)$/.exec(name)).find(Boolean);
  return match ? match[1] : "";
}

function label(text: string, file: boolean): Element {
  return {
    type: "element",
    tagName: "span",
    properties: { className: file ? ["code-label", "code-label--file"] : ["code-label"], dataPagefindIgnore: "" },
    children: [{ type: "text", value: text }],
  };
}

function wrap(parent: Parents, inCodeGroup: boolean) {
  const children = parent.children as ElementContent[];
  for (let index = 0; index < children.length; index++) {
    const node = children[index];
    if (node.type !== "element") continue;

    if (node.tagName === "pre") {
      const outer = parent.type === "element" && classes(parent).includes("code-block") ? parent : undefined;
      const file = outer && typeof outer.properties.dataFile === "string" ? outer.properties.dataFile : undefined;
      const language = languageOf(node).toLowerCase();
      const text = file ?? (inCodeGroup || UNLABELLED.has(language) ? undefined : (ALIASES[language] ?? language));
      const block: Element = outer ?? {
        type: "element",
        tagName: "div",
        properties: { className: ["code-block"] },
        children: [node],
      };
      if (file) block.properties.className = [...classes(block), "code-block--file"];
      if (text) block.children.splice(block.children.indexOf(node), 0, label(text, Boolean(file)));
      if (!outer) children[index] = block;
      if (outer) break; // the import wrapper holds this one block and its label
      continue;
    }

    wrap(node, inCodeGroup || classes(node).includes("code-group-panels"));
  }
}

export default function rehypeCodeBlocks() {
  return (tree: Root) => wrap(tree, false);
}

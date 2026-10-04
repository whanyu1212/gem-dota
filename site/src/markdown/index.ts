/**
 * The Markdown processor for the docs: Astro's unified (remark/rehype) pipeline
 * plus the plugins that make VitePress-flavoured Markdown render the same way.
 */
import { unified } from "@astrojs/markdown-remark";
import rehypeRaw from "rehype-raw";
import type { Processor } from "unified";
import type { VFile } from "vfile";
import { preprocess } from "./preprocess";
import rehypeHeadingIds from "./rehype-heading-ids";
import rehypeLinks, { type LinkOptions } from "./rehype-links";

export type DocsMarkdownOptions = LinkOptions;

/**
 * Runs {@link preprocess} on the source before remark parses it. Callouts and
 * code groups span several Markdown blocks, so they are rewritten as text, the
 * way VitePress's markdown-it containers read them, rather than in the tree.
 */
function remarkPreprocess(this: Processor, options: { importRoot: string }) {
  const parse = this.parser!;
  this.parser = (document: string, file: VFile) => parse(preprocess(document, options), file);
}

export function docsMarkdown(options: DocsMarkdownOptions) {
  return unified({
    // VitePress doesn't curl quotes or turn -- into dashes; keep prose as written.
    smartypants: false,
    remarkPlugins: [[remarkPreprocess, { importRoot: options.repoRoot }]],
    rehypePlugins: [
      // Astro parses raw HTML last; do it first so links and headings written as
      // HTML are rewritten too.
      rehypeRaw,
      rehypeHeadingIds,
      [rehypeLinks, options],
    ],
  });
}

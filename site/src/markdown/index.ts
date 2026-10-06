/**
 * The Markdown processor for the docs: Astro's unified (remark/rehype) pipeline
 * plus the plugins that make VitePress-flavoured Markdown render the same way.
 */
import { unified } from "@astrojs/markdown-remark";
import rehypeRaw from "rehype-raw";
import type { Processor } from "unified";
import type { VFile } from "vfile";
import { fightsFigure } from "../figures/fights";
import { lanesFigure } from "../figures/lanes";
import { leadFigure } from "../figures/lead";
import { objectivesFigure } from "../figures/objectives";
import { runesFigure } from "../figures/runes";
import { wardsFigure } from "../figures/wards";
import { preprocess, type PreprocessOptions } from "./preprocess";
import rehypeHeadingIds from "./rehype-heading-ids";
import rehypeLinks, { type LinkOptions } from "./rehype-links";

export type DocsMarkdownOptions = LinkOptions;

/**
 * Runs {@link preprocess} on the source before remark parses it. Callouts and
 * code groups span several Markdown blocks, so they are rewritten as text, the
 * way VitePress's markdown-it containers read them, rather than in the tree.
 */
function remarkPreprocess(this: Processor, options: PreprocessOptions) {
  const parse = this.parser!;
  this.parser = (document: string, file: VFile) => parse(preprocess(document, options), file);
}

export function docsMarkdown(options: DocsMarkdownOptions) {
  return unified({
    // VitePress doesn't curl quotes or turn -- into dashes; keep prose as written.
    smartypants: false,
    remarkPlugins: [
      [
        remarkPreprocess,
        {
          importRoot: options.repoRoot,
          figures: {
            wards: () => wardsFigure(options.base),
            fights: () => fightsFigure(options.base),
            objectives: () => objectivesFigure(options.base),
            lead: () => leadFigure(options.base),
            lanes: () => lanesFigure(),
            runes: () => runesFigure(options.base),
          },
        },
      ],
    ],
    rehypePlugins: [
      // Astro parses raw HTML last; do it first so links and headings written as
      // HTML are rewritten too.
      rehypeRaw,
      rehypeHeadingIds,
      [rehypeLinks, options],
    ],
  });
}

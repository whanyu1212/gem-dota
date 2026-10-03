import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const docs = defineCollection({
  loader: glob({
    base: "../docs",
    pattern: ["**/*.md", "!**/node_modules/**", "!public/**"],
    // Keep the file path as the ID (the default slugifies it), so the URL of
    // docs/guides/01_quickstart.md stays /guides/01_quickstart.
    generateId: ({ entry }) => entry.replace(/\.md$/, ""),
  }),
  schema: z.looseObject({ title: z.string().optional() }),
});

export const collections = { docs };

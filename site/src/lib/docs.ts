import { getCollection, type CollectionEntry } from "astro:content";

export type DocEntry = CollectionEntry<"docs">;

/** Whether the entry is a folder's index page (docs/x/index.md or docs/index.md). */
export function isIndexPage(entry: DocEntry): boolean {
  return entry.id === "index" || entry.id.endsWith("/index");
}

/** The folder an index page stands for: "" for the home page, "x" for docs/x/index.md. */
export function indexFolder(entry: DocEntry): string {
  return entry.id === "index" ? "" : entry.id.slice(0, -"/index".length);
}

export async function getDocs(): Promise<DocEntry[]> {
  return getCollection("docs");
}

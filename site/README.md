# gem docs site (Astro)

The new docs site, replacing the VitePress site in `docs/` (HY-110). Until the
switch-over (HY-118) the pages are read from `../docs`, and the live site is
still the VitePress build.

Needs Node 22.12 or newer (Astro 7; see `engines` in `package.json` and `.nvmrc`).

```bash
cd site
npm install
npm run dev          # http://localhost:4321/gem-dota/
npm run build        # -> site/dist
npm run check-urls   # every URL in url-manifest.txt must be built
npm run check-links  # every internal link and #anchor in dist/ must resolve
npm run check        # type-check the Astro code
npm test             # Markdown plugin tests (vitest)
```

`url-manifest.txt` lists the URLs the VitePress site publishes (written from
`docs/.vitepress/dist` with `node scripts/check-urls.mjs --write <dir>`). The
Astro build must keep all of them, so links to the docs keep working after the
move.

## Markdown

Pages are rendered with Astro's unified (remark/rehype) processor, configured
in `src/markdown/`, so Markdown written for VitePress renders the same way:

- `preprocess.ts` rewrites `::: info|tip|warning|danger|important|details`
  callouts, `::: code-group` tabs and `<<< @/path{lang}` file imports before
  parsing (`@` is the content root);
- `rehype-heading-ids.ts` gives headings VitePress's IDs, so `#anchor` links keep
  working;
- `rehype-links.ts` turns `.md` links into page URLs, adds the `/gem-dota` base
  to absolute paths, and points links to unpublished repository files at GitHub.

SmartyPants is off: VitePress doesn't curl quotes or turn `--` into dashes.

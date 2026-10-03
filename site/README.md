# gem docs site (Astro)

The new docs site, replacing the VitePress site in `docs/` (HY-110). Until the
switch-over (HY-118) the pages are read from `../docs`, and the live site is
still the VitePress build.

```bash
cd site
npm install
npm run dev          # http://localhost:4321/gem-dota/
npm run build        # -> site/dist
npm run check-urls   # every URL in url-manifest.txt must be built
npm run check        # type-check the Astro code
```

`url-manifest.txt` lists the URLs the VitePress site publishes (written from
`docs/.vitepress/dist` with `node scripts/check-urls.mjs --write <dir>`). The
Astro build must keep all of them, so links to the docs keep working after the
move.

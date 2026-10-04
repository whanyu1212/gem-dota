# gem docs site (Astro)

The docs site, deployed to <https://whanyu1212.github.io/gem-dota/> by
`.github/workflows/docs.yml` (pull requests build and check it without
deploying). The pages are Markdown in `src/content/docs/`; public assets (logo,
favicon, README banner, map figure) are in `public/`.

Needs Node 22.12 or newer (Astro 7; see `engines` in `package.json` and `.nvmrc`).

```bash
cd site
npm install
npm run dev          # http://localhost:4321/gem-dota/ (regenerates the API reference first)
npm run build        # API reference, then site/dist, then the Pagefind index in dist/pagefind
npm run gen          # regenerate the API reference pages only
npm run gen-all      # also the proto-field pages (needs scripts/download_protos.sh first)
npm run check-urls   # every URL in url-manifest.txt must be built
npm run check-links  # every internal link and #anchor in dist/ must resolve
npm run check        # type-check the Astro code
npm test             # navigation, Markdown plugin and colour-contrast tests (vitest)
```

`url-manifest.txt` lists the URLs the old VitePress site published (written from
its build with `node scripts/check-urls.mjs --write <dir>`). The
Astro build must keep all of them, so links to the docs keep working after the
move.

## Markdown

Pages are rendered with Astro's unified (remark/rehype) processor, configured
in `src/markdown/`, so the Markdown (first written for VitePress) renders the same way:

- `preprocess.ts` rewrites `::: info|tip|warning|danger|important|details`
  callouts, GitHub `> [!NOTE]`-style alerts, `::: code-group` tabs and
  `<<< @/path{lang}` file imports before parsing (`@` is the repository root);
- `rehype-heading-ids.ts` gives headings VitePress's IDs, so `#anchor` links keep
  working;
- `rehype-links.ts` turns `.md` links into page URLs, adds the `/gem-dota` base
  to absolute paths, and points links to unpublished repository files at GitHub.

SmartyPants is off: VitePress doesn't curl quotes or turn `--` into dashes.

## Layout and theme

- `src/nav.ts` defines the five sections (Guide, Recipes, Reference, Internals,
  Changelog), their sidebars, and which pages belong to each. The Reference
  sidebar is built from the reference pages (`src/lib/docs.ts`).
- `src/styles/tokens.css` holds every colour: the light theme and Night paper
  (dark). Dark follows the system setting until the reader picks one with the
  toggle; the choice is kept in `localStorage` (`gem-theme`).
- Fonts are self-hosted from Fontsource packages: Source Serif 4 (headings),
  Inter (text), JetBrains Mono (code).
- `src/markdown/shiki-theme.ts` is the code theme. Code blocks are dark in both
  themes.
- Generated pages (`reference/`, `cookbook/proto-fields/`) use a wider column and
  sans-serif headings.

## Home page

`src/pages/index.astro` is the home page. Its figures come from a committed
snapshot, so the build never parses a replay:

```bash
uv run python scripts/export_site_home_data.py [replay.dem]
```

writes `src/data/home.json` and two map images in `src/assets/`. The default
replay is the TI2026 fixture 8856501050, the match the committed snapshot comes
from. The snapshot holds:

- the match and its players (Table 1);
- gem's map overlay: half line, river, lotus pools and camps (Figure 1);
- the wards up at the first death of the match's biggest fight, with observer
  vision, and whole-match ward counts by region (Figure 2);
- that fight's hero paths, death spots and events: smoke, kills, buybacks and
  team totals (Figure 3 and its narration), with `home-fight.jpg`, a sharp crop
  of the map around it. Every sample, death and event carries its seconds since
  the fight window started, for the playback.

Figure 3 plays the fight back (`src/lib/playback.ts`): each hero's minimap icon,
ringed in its team's colour, moves along its sampled path at 4×, on a loop,
while the figure is on screen, and the narration follows the clock. Positions
between samples are interpolated for display. Paused, with reduced motion
(until play is pressed) or without JavaScript, it shows where everyone was at
the last death.

The export also copies the observer, sentry and fight heroes' icons into
`src/assets/icons/` from the icons that `scripts/fetch_item_icons.py` and
`scripts/fetch_hero_icons.py` download (run those first).

Ward positions are exact; hero paths and death spots are sampled positions.
Every paired diagram sits on one
two-column grid (`.pair`, `.figures`, `.fight` in `src/styles/home.css`), so
their edges line up. The recipe cards quote their recipe pages
(`src/data/recipes.ts`), and `tests/home.test.ts` fails if a quoted sentence is
no longer on its page.

## Search

`npm run build` runs [Pagefind](https://pagefind.app) after Astro (`pagefind.yml`).
It indexes each page's `<article data-pagefind-body>` only, tagged with its
section; pages with `search: false` in their frontmatter are left out, and the
generated proto-field pages are weighted down. `src/components/Search.astro` is
the dialog (⌘K, Ctrl+K or `/`): results are grouped by section, best match
first. Search needs the built index, so it works in `npm run preview`, not
`npm run dev`, and the button stays hidden without JavaScript.

## Generated pages

Two scripts write Markdown into the content folder; both take the folder as an
argument (the defaults are below):

- `scripts/generate_api_reference.py [--reference-dir src/content/docs/reference]` keeps
  each reference page's text above `## Generated API` and regenerates the rest
  from the docstrings. `npm run build` and `npm run dev` run it.
- `scripts/generate_proto_field_docs.py [--out-dir src/content/docs/cookbook/proto-fields]`
  rewrites the proto-field pages from `proto_definitions/` (gitignored; fetch it
  with `scripts/download_protos.sh`). Run it by hand after a proto refresh.

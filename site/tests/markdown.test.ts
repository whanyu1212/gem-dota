import { fileURLToPath, pathToFileURL } from "node:url";
import { describe, expect, it } from "vitest";
import { docsMarkdown } from "../src/markdown";
import { preprocess } from "../src/markdown/preprocess";
import { vitepressSlug } from "../src/markdown/rehype-heading-ids";
import { rewriteUrl } from "../src/markdown/rehype-links";

const repo = fileURLToPath(new URL("./fixtures/repo/", import.meta.url));
const options = {
  base: "/gem-dota",
  contentRoot: `${repo}docs`,
  publicDir: `${repo}docs/public`,
  repoRoot: repo.replace(/\/$/, ""),
  repoBlobUrl: "https://github.com/o/r/blob/main",
};
const page = `${repo}docs/guides/01_start.md`;
const pre = { importRoot: options.repoRoot };

async function render(markdown: string) {
  const renderer = await docsMarkdown(options).createRenderer({ syntaxHighlight: false } as never);
  const { code, metadata } = await renderer.render(markdown, { fileURL: pathToFileURL(page) } as never);
  return { html: code, headings: metadata.headings };
}

describe("callouts", () => {
  it("renders a titled callout with Markdown inside", async () => {
    const { html } = await render("::: info Parquet dependency\nNeeds `pyarrow`:\n```bash\npip install pyarrow\n```\n:::\n");
    expect(html).toMatchInlineSnapshot(`
      "<aside class="callout callout--info"><p class="callout-title">Parquet dependency</p>
      <p>Needs <code>pyarrow</code>:</p>
      <pre><code class="language-bash">pip install pyarrow
      </code></pre>
      </aside>"
    `);
  });

  it("uses the default title, and supports important and details", async () => {
    const { html } = await render("::: tip\nA\n:::\n\n::: important\nB\n:::\n\n::: details More\nC\n:::\n");
    expect(html).toContain('<aside class="callout callout--tip"><p class="callout-title">TIP</p>');
    expect(html).toContain('<aside class="callout callout--important"><p class="callout-title">IMPORTANT</p>');
    expect(html).toContain('<details class="callout callout--details"><summary>More</summary>');
  });

  it("escapes HTML in the title", () => {
    expect(preprocess("::: warning <b>x</b>\nA\n:::", pre)).toContain(
      '<p class="callout-title">&lt;b&gt;x&lt;/b&gt;</p>',
    );
  });

  it("leaves ::: inside fenced code alone", () => {
    const source = "```md\n::: info\nnot a callout\n:::\n```";
    expect(preprocess(source, pre)).toBe(source);
  });

  it("leaves unknown containers as text, like VitePress", () => {
    expect(preprocess("::: v-pre\n:::", pre)).toBe("::: v-pre\n:::");
  });

  it("fails on an unclosed callout", () => {
    expect(() => preprocess("::: info\nA", pre)).toThrow("Unclosed ::: info");
  });
});

describe("figures", () => {
  const figures = { demo: () => ({ open: '<figure class="demo"><figcaption>', close: "</figcaption></figure>" }) };

  it("renders a figure around its caption, which stays Markdown", () => {
    const out = preprocess("::: figure demo\n**Figure 1.** A *map*.\n:::", { ...pre, figures });
    expect(out).toBe('\n<figure class="demo"><figcaption>\n\n**Figure 1.** A *map*.\n\n</figcaption></figure>\n');
  });

  it("refuses a figure it doesn't know", () => {
    expect(() => preprocess("::: figure nope\n:::", { ...pre, figures })).toThrow("Unknown figure: ::: figure nope");
  });
});

describe("GitHub alerts", () => {
  it("renders > [!IMPORTANT] as a callout, with Markdown inside", async () => {
    const { html } = await render("> [!IMPORTANT]\n> Experimental does **not** mean random.\n>\n> - a\n> - b\n\nAfter.\n");
    expect(html).toContain('<aside class="callout callout--important"><p class="callout-title">IMPORTANT</p>');
    expect(html).toContain("<strong>not</strong>");
    expect(html).toContain("<li>a</li>");
    expect(html).not.toContain("[!IMPORTANT]");
    expect(html).toContain("<p>After.</p>");
  });

  it("maps NOTE to info and CAUTION to danger, and leaves plain quotes alone", () => {
    expect(preprocess("> [!NOTE]\n> x", pre)).toContain("callout--info");
    expect(preprocess("> [!CAUTION]\n> x", pre)).toContain("callout--danger");
    expect(preprocess("> just a quote", pre)).toBe("> just a quote");
  });
});

describe("code groups", () => {
  it("renders labelled code blocks as radio tabs", async () => {
    const { html } = await render("::: code-group\n\n```bash [pip]\npip install gem-dota\n```\n\n```bash [uv]\nuv add gem-dota\n```\n\n:::\n");
    expect(html).toMatchInlineSnapshot(`
      "<div class="code-group">
      <input type="radio" name="code-group-0" id="code-group-0-0" checked><label for="code-group-0-0">pip</label>
      <input type="radio" name="code-group-0" id="code-group-0-1"><label for="code-group-0-1">uv</label>
      <div class="code-group-panels">
      <pre><code class="language-bash">pip install gem-dota
      </code></pre>
      <pre><code class="language-bash">uv add gem-dota
      </code></pre>
      </div>
      </div>"
    `);
  });
});

describe("file imports", () => {
  it("inlines the file with the language from the braces", () => {
    expect(preprocess("<<< @/examples/demo.py{python}", pre)).toBe(
      '````python\ndef main() -> str:\n    return "```"\n````',
    );
  });

  it("takes the language from the extension when the braces have none", () => {
    expect(preprocess("<<< @/examples/demo.py{1,2}", pre)).toMatch(/^````python\n/);
  });

  it("fails the build when the file is missing", () => {
    expect(() => preprocess("<<< @/examples/missing.py{python}", pre)).toThrow("<<< import not found");
  });
});

describe("heading ids", () => {
  it.each([
    ["Quickstart", "quickstart"],
    ["Parse a replay", "parse-a-replay"],
    ["`gem.parse()` and `ParsedMatch`", "gem-parse-and-parsedmatch"],
    ["0.4.1 parity", "_0-4-1-parity"],
    ["Gold / XP field sources — critical", "gold-xp-field-sources-—-critical"],
    ["snake_case names", "snake-case-names"],
  ])("slugs %j like VitePress", (text, slug) => {
    expect(vitepressSlug(text)).toBe(slug);
  });

  it("numbers repeated headings and feeds the outline", async () => {
    const { html, headings } = await render("## Notes\n\n## Notes\n\n### `code` *em*\n");
    expect(html).toContain('<h2 id="notes">');
    expect(html).toContain('<h2 id="notes-1">');
    expect(headings.map((h) => [h.depth, h.slug])).toEqual([
      [2, "notes"],
      [2, "notes-1"],
      [3, "code-em"],
    ]);
  });
});

describe("links", () => {
  const rewrite = (url: string) => rewriteUrl(url, page, options);

  it.each([
    ["01_start.md", "/gem-dota/guides/01_start"],
    ["./01_start.md#install", "/gem-dota/guides/01_start#install"],
    ["index.md", "/gem-dota/guides/"],
    ["../guides/index.md", "/gem-dota/guides/"],
    ["/guides/01_start", "/gem-dota/guides/01_start"],
    ["/map.png", "/gem-dota/map.png"],
    ["/gem-dota/guides/", "/gem-dota/guides/"],
    ["data.json", "https://github.com/o/r/blob/main/docs/guides/data.json"],
    ["../../examples/demo.py", "https://github.com/o/r/blob/main/examples/demo.py"],
    ["01_start", "01_start"],
    ["https://example.com/x.md", "https://example.com/x.md"],
    ["#anchor", "#anchor"],
  ])("rewrites %j to %j", (from, to) => {
    expect(rewrite(from)).toBe(to);
  });

  it("rewrites links written as raw HTML too", async () => {
    const { html } = await render('<a class="button" href="01_start.md">Start</a>\n\n![map](/map.png)\n');
    expect(html).toContain('href="/gem-dota/guides/01_start"');
    expect(html).toContain('src="/gem-dota/map.png"');
  });
});

it("keeps quotes and dashes as written", async () => {
  const { html } = await render('Run "gem" with --help.\n');
  expect(html).toBe('<p>Run "gem" with --help.</p>');
});

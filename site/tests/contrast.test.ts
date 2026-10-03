import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { gemCodeTheme } from "../src/markdown/shiki-theme";

// WCAG contrast of the theme's text colours against the surfaces they sit on,
// in both themes: at least 4.5:1 (AA for body text).

const css = readFileSync(new URL("../src/styles/tokens.css", import.meta.url), "utf8");
const block = (selector: string) => css.slice(css.indexOf(selector)).split("}")[0];
const tokens = (text: string) =>
  Object.fromEntries([...text.matchAll(/--([\w-]+):\s*(#[0-9a-f]{6})\b/gi)].map(([, k, v]) => [k, v]));
const light = tokens(block(":root {"));
const dark = { ...light, ...tokens(block(':root[data-theme="dark"]')) };
const systemDark = { ...light, ...tokens(block(':root:not([data-theme="light"])')) };

const channel = (c: number) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
const luminance = (hex: string) => {
  const [r, g, b] = [1, 3, 5].map((i) => channel(parseInt(hex.slice(i, i + 2), 16) / 255));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a: string, b: string) => {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
};

const TEXT_ON_SURFACE = [
  ["ink", "bg"], ["body", "bg"], ["muted", "bg"], ["accent", "bg"],
  ["body", "paper"], ["muted", "paper"], ["accent", "paper"],
  ["ink", "inline-code-bg"],
  ["note", "bg"], ["tip", "bg"], ["warning", "bg"], ["danger", "bg"], ["important", "bg"],
  ["code-fg", "code-bg"], ["code-muted", "code-bg"],
];
const CODE_COLOURS = [...new Set(gemCodeTheme.tokenColors.map((t) => t.settings.foreground))];

describe.each([
  ["light", light],
  ["Night paper", dark],
])("%s theme", (_, theme) => {
  it.each(TEXT_ON_SURFACE)("%s on %s meets AA", (fg, bg) => {
    expect(ratio(theme[fg], theme[bg])).toBeGreaterThanOrEqual(4.5);
  });

  it.each(CODE_COLOURS)("code colour %s meets AA on the code background", (fg) => {
    expect(ratio(fg, theme["code-bg"])).toBeGreaterThanOrEqual(4.5);
  });
});

it("uses the same Night paper values for the system preference", () => {
  expect(systemDark).toEqual(dark);
});

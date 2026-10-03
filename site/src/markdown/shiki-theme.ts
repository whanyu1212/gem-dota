/**
 * The code theme. Code blocks are dark in both site themes, so one Shiki theme
 * covers both; the block background comes from the --code-bg token.
 * Colours follow the Editorial mockups: warm keywords, green functions, blue strings.
 */
export const gemCodeTheme = {
  name: "gem-editorial",
  type: "dark",
  colors: {
    "editor.background": "#15191d",
    "editor.foreground": "#e8e6df",
  },
  tokenColors: [
    { settings: { foreground: "#e8e6df" } },
    {
      scope: ["comment", "punctuation.definition.comment"],
      settings: { foreground: "#9aa3ab", fontStyle: "italic" },
    },
    {
      // Docstrings can run to a dozen lines; keep them upright.
      scope: ["string.quoted.docstring", "string.quoted.docstring punctuation.definition.string"],
      settings: { foreground: "#a9b4a0" },
    },
    {
      scope: ["keyword", "storage", "storage.type", "storage.modifier", "keyword.operator.logical.python"],
      settings: { foreground: "#e9a36a" },
    },
    {
      scope: ["string", "punctuation.definition.string", "string.quoted"],
      settings: { foreground: "#b9d4f2" },
    },
    {
      scope: ["entity.name.function", "support.function", "meta.function-call.generic", "variable.function"],
      settings: { foreground: "#8fd8b4" },
    },
    {
      scope: ["constant.numeric", "constant.language", "support.constant", "variable.language", "constant.other"],
      settings: { foreground: "#e6c07b" },
    },
    {
      scope: ["entity.name.type", "entity.name.class", "support.type", "support.class", "entity.other.inherited-class"],
      settings: { foreground: "#f0d39a" },
    },
    {
      scope: ["entity.name.tag", "meta.decorator", "entity.name.function.decorator", "punctuation.definition.decorator"],
      settings: { foreground: "#d7a8e0" },
    },
    {
      scope: ["support.type.property-name", "entity.other.attribute-name", "variable.other.object.property"],
      settings: { foreground: "#c9d6a3" },
    },
    {
      scope: ["markup.heading", "markup.bold"],
      settings: { foreground: "#e9a36a", fontStyle: "bold" },
    },
    {
      scope: ["markup.inserted"],
      settings: { foreground: "#8fd8b4" },
    },
    {
      scope: ["markup.deleted"],
      settings: { foreground: "#f0a39a" },
    },
  ],
};

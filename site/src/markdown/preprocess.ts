/**
 * Rewrites the VitePress-only block syntax in the docs into plain Markdown and
 * HTML before the Markdown is parsed:
 *
 * - `::: info [title]` … `:::` callouts (also tip, warning, danger, important,
 *   details) become `<aside class="callout callout--info">` blocks.
 * - GitHub alerts (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`,
 *   `> [!CAUTION]` followed by `>` lines) become the same callouts.
 * - `::: code-group` around code blocks labelled ```` ```bash [pip] ```` becomes
 *   radio-button tabs that work without JavaScript.
 * - `<<< @/path/to/file.py{python}` is replaced by the file's contents in a code
 *   block. `@` is the repository root, e.g. `<<< @/examples/cookbook/x.py{python}`.
 * - `::: figure name` … `:::` renders a recipe figure (src/figures/) around the
 *   block's Markdown, which becomes the figure's caption.
 *
 * Fenced code is left alone, so a `:::` or `<<<` line inside a code block stays
 * as written. Blank lines around the inserted HTML make CommonMark parse the
 * content between the tags as Markdown again.
 */
import { readFileSync } from "node:fs";
import { extname, resolve } from "node:path";

/** A recipe figure's HTML: everything before its caption, and after it. */
export type FigureRenderer = () => { open: string; close: string };

export interface PreprocessOptions {
  /** Absolute path that `@` stands for in `<<< @/…` imports: the repository root. */
  importRoot: string;
  /** The figures `::: figure name` can render, by name. */
  figures?: Record<string, FigureRenderer>;
}

const FENCE_OPEN = /^ {0,3}(`{3,}|~{3,})(.*)$/;
const CONTAINER_OPEN = /^ {0,3}:::\s*([\w-]+)\s*(.*?)\s*$/;
const CONTAINER_CLOSE = /^ {0,3}:::\s*$/;
const IMPORT = /^ {0,3}<<<\s+(\S+?)(?:\{([^}]*)\})?\s*$/;
const LABELLED_FENCE = /^( {0,3})(`{3,}|~{3,})(\S*)(.*?)\s*\[([^\]]+)\]\s*$/;
const ALERT_OPEN = /^ {0,3}>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$/i;
const QUOTE_LINE = /^ {0,3}>(.*)$/;

/** GitHub alert kinds as callout kinds, with VitePress's titles. */
const ALERTS: Record<string, { kind: string; title: string }> = {
  NOTE: { kind: "info", title: "NOTE" },
  TIP: { kind: "tip", title: "TIP" },
  IMPORTANT: { kind: "important", title: "IMPORTANT" },
  WARNING: { kind: "warning", title: "WARNING" },
  CAUTION: { kind: "danger", title: "CAUTION" },
};

const CALLOUT_KINDS = new Set(["info", "tip", "warning", "danger", "important", "details"]);
const DEFAULT_TITLES: Record<string, string> = {
  info: "INFO",
  tip: "TIP",
  warning: "WARNING",
  danger: "DANGER",
  important: "IMPORTANT",
  details: "Details",
};

const LANGUAGES_BY_EXTENSION: Record<string, string> = {
  ".py": "python",
  ".ts": "ts",
  ".js": "js",
  ".mjs": "js",
  ".json": "json",
  ".sh": "bash",
  ".toml": "toml",
  ".yml": "yaml",
  ".yaml": "yaml",
};

export function escapeHtml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

interface Frame {
  kind: string;
  /** For a figure: the HTML that closes it. */
  close?: string;
  /** For a code group: where its tab bar goes, and the tabs found so far. */
  tabsAt?: number;
  labels?: string[];
}

export function preprocess(source: string, options: PreprocessOptions): string {
  const out: string[] = [];
  const stack: Frame[] = [];
  let fence: { char: string; length: number } | undefined;
  let codeGroups = 0;

  const lines = source.split("\n");
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    if (fence) {
      out.push(line);
      const close = new RegExp(`^ {0,3}${fence.char === "`" ? "`" : "~"}{${fence.length},}\\s*$`);
      if (close.test(line)) fence = undefined;
      continue;
    }

    const group = stack.at(-1)?.labels ? stack.at(-1) : undefined;
    const labelled = group ? LABELLED_FENCE.exec(line) : null;
    if (group && labelled) {
      const [, indent, marks, lang, rest, label] = labelled;
      group.labels!.push(label.trim());
      out.push(`${indent}${marks}${lang}${rest}`);
      fence = { char: marks[0], length: marks.length };
      continue;
    }

    const opened = FENCE_OPEN.exec(line);
    if (opened) {
      fence = { char: opened[1][0], length: opened[1].length };
      out.push(line);
      continue;
    }

    const alert = ALERT_OPEN.exec(line);
    if (alert) {
      const { kind, title } = ALERTS[alert[1].toUpperCase()];
      const body: string[] = [];
      while (index + 1 < lines.length && QUOTE_LINE.test(lines[index + 1])) {
        body.push(QUOTE_LINE.exec(lines[++index])![1].replace(/^ /, ""));
      }
      out.push("", `<aside class="callout callout--${kind}"><p class="callout-title">${title}</p>`, "");
      out.push(...preprocess(body.join("\n"), options).split("\n"));
      out.push("", "</aside>", "");
      continue;
    }

    const imported = IMPORT.exec(line);
    if (imported) {
      out.push(...importFile(imported[1], imported[2], options));
      continue;
    }

    if (stack.length && CONTAINER_CLOSE.test(line)) {
      const frame = stack.pop()!;
      if (frame.labels) {
        out.splice(frame.tabsAt!, 0, ...codeGroupTabs(codeGroups++, frame.labels));
        out.push("", "</div>", "</div>", "");
      } else if (frame.close !== undefined) {
        out.push("", frame.close, "");
      } else {
        out.push("", frame.kind === "details" ? "</details>" : "</aside>", "");
      }
      continue;
    }

    const container = CONTAINER_OPEN.exec(line);
    if (container?.[1] === "figure") {
      const render = options.figures?.[container[2]];
      if (!render) throw new Error(`Unknown figure: ::: figure ${container[2]}`);
      const { open, close } = render();
      out.push("", open, "");
      stack.push({ kind: "figure", close });
      continue;
    }
    if (container && (container[1] === "code-group" || CALLOUT_KINDS.has(container[1]))) {
      const [, kind, title] = container;
      if (kind === "code-group") {
        out.push("", '<div class="code-group">');
        stack.push({ kind, tabsAt: out.length, labels: [] });
        out.push('<div class="code-group-panels">', "");
      } else {
        const heading = escapeHtml(title || DEFAULT_TITLES[kind]);
        out.push(
          "",
          kind === "details"
            ? `<details class="callout callout--details"><summary>${heading}</summary>`
            : `<aside class="callout callout--${kind}"><p class="callout-title">${heading}</p>`,
          "",
        );
        stack.push({ kind });
      }
      continue;
    }

    out.push(line);
  }

  if (stack.length) {
    throw new Error(`Unclosed ::: ${stack.at(-1)!.kind} block`);
  }
  return out.join("\n");
}

function codeGroupTabs(index: number, labels: string[]): string[] {
  const name = `code-group-${index}`;
  return labels.map((label, i) => {
    const id = `${name}-${i}`;
    const checked = i === 0 ? " checked" : "";
    return `<input type="radio" name="${name}" id="${id}"${checked}><label for="${id}">${escapeHtml(label)}</label>`;
  });
}

function importFile(path: string, braces: string | undefined, options: PreprocessOptions): string[] {
  if (!path.startsWith("@/")) {
    throw new Error(`<<< imports must start with @/ (the repository root): ${path}`);
  }
  const file = resolve(options.importRoot, path.slice(2));
  let code: string;
  try {
    code = readFileSync(file, "utf8").replace(/\n$/, "");
  } catch {
    throw new Error(`<<< import not found: ${path} (looked for ${file})`);
  }
  // VitePress puts line highlights and the language in the braces, e.g.
  // {python} or {1,3-4 python}. Only the language is kept.
  const lang =
    braces?.split(/\s+/).find((token) => /^[a-z][\w+-]*$/i.test(token)) ??
    LANGUAGES_BY_EXTENSION[extname(file)] ??
    "";
  const longestRun = Math.max(2, ...[...code.matchAll(/`+/g)].map((m) => m[0].length));
  const marks = "`".repeat(longestRun + 1);
  return [`${marks}${lang}`, code, marks];
}

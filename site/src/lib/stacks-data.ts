/**
 * The stacks recipe's figure: one row per player on the game clock (each stack a
 * bar at its time, split by who killed its creeps), the stacked camps on the map,
 * a card for what the reader picked, and each player's numbers. No DOM here: the
 * Markdown build renders the figure with it (src/figures/stacks.ts) and the
 * browser redraws the rows and the card as the reader picks (stacks-figure.ts).
 *
 * The data is src/data/stacks.json, from scripts/export_site_home_data.py (which
 * takes it from examples/cookbook/stacks.py).
 */

export type Side = "r" | "d";
export type Role = "s" | "c";

export interface Camp {
  id: number;
  /** The camp's type in camp_zones.json: small, medium, large, ancient, flooded_small, flooded_medium. */
  type: string;
  /** On the 1000-unit map square. */
  xy: [number, number];
}

/** [hero, side, stacked creeps killed]. */
export type Clearer = [string, Side, number];

/** [time_s, camp (null: off the camp catalog, so not on the map), hero, side, role, exact, waves, creeps, pulled, gold, cleared]. */
export type Stack = [number, number | null, string | null, Side | "", Role | "", boolean, number, number, number, number, Clearer[]];

/** [hero, side, role, stacks, exact, killed, gold, neutral_gold]. */
export type Player = [string, Side | "", Role | "", number, number, number, number, number];

export interface StacksData {
  /** The game second the replay ends, for the time axis. */
  end_s: number;
  camps: Camp[];
  stacks: Stack[];
  players: Player[];
}

/**
 * Who killed some of a stack's creeps: the stacker, a teammate, the enemy, a
 * player when the game credited nobody with the stack, a lane creep (a pull), or
 * no player.
 */
export type Outcome = "self" | "team" | "enemy" | "player" | "pulled" | "none";

/** Some of a stack's creeps, and who killed them. */
export interface Segment {
  outcome: Outcome;
  creeps: number;
}

/** Each row lists one side's players: those who stacked, or those who killed stacked creeps. */
export type RowsBy = "stacker" | "killer";

/** What the reader picked: one stack (its index in `stacks`), a camp, or a player. */
export type Pick = { kind: "stack"; index: number } | { kind: "camp"; id: number } | { kind: "hero"; hero: string };

const TEAM: Record<Side, string> = { r: "radiant", d: "dire" };
const SIDE_NAME: Record<Side, string> = { r: "Radiant", d: "Dire" };
const ROLE: Record<Role, string> = { s: "support", c: "core" };
const KILLED_FIRST: Outcome[] = ["self", "team", "enemy", "player"];

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
const plural = (n: number, word: string) => `${n} ${word}${n === 1 ? "" : "s"}`;
const team = (side: Side | "") => (side ? TEAM[side] : "none");

/** In-game time: "7:13". */
export function clock(seconds: number): string {
  const s = Math.max(0, Math.floor(seconds));
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
}

/** A camp type for a reader: "flooded_medium" -> "flooded medium". */
export const campType = (type: string) => type.replace("_", " ");

/** Each camp's stacks, in time order. */
export function stacksAt(data: StacksData, camp: number): Stack[] {
  return data.stacks.filter((s) => s[1] === camp);
}

/** The camp stacked most often (the earliest of a tie): the one the figure opens on. */
export function firstCamp(data: StacksData): number | null {
  let best: number | null = null;
  let most = 0;
  for (const camp of data.camps) {
    const n = stacksAt(data, camp.id).length;
    if (n > most) [best, most] = [camp.id, n];
  }
  return best;
}

/** Who a player who killed some of a stack's creeps was to its stacker. */
function outcomeOf(stack: Stack, [killer, side]: Clearer): Outcome {
  if (!stack[3]) return "player";
  if (killer === stack[2]) return "self";
  return side === stack[3] ? "team" : "enemy";
}

/** A stack's creeps by who killed them: the stacker, teammates, the enemy, then the pulled and the rest. */
export function segments(stack: Stack): Segment[] {
  const [, , , , , , , creeps, pulled, , cleared] = stack;
  const killed = cleared
    .map((c) => ({ outcome: outcomeOf(stack, c), creeps: c[2] }))
    .sort((a, b) => KILLED_FIRST.indexOf(a.outcome) - KILLED_FIRST.indexOf(b.outcome));
  const rest = creeps - pulled - cleared.reduce((n, c) => n + c[2], 0);
  const runs: Segment[] = [...killed];
  if (pulled) runs.push({ outcome: "pulled", creeps: pulled });
  if (rest > 0) runs.push({ outcome: "none", creeps: rest });
  return runs;
}

/** Whether a stack is one the pick names: that stack, a stack of that camp, or one the player stacked or cleared. */
export function isPicked(stack: Stack, index: number, pick: Pick): boolean {
  switch (pick.kind) {
    case "stack":
      return index === pick.index;
    case "camp":
      return stack[1] === pick.id;
    case "hero":
      return stack[2] === pick.hero || stack[10].some(([hero]) => hero === pick.hero);
    default: {
      const never: never = pick;
      return never;
    }
  }
}

/** The players in a set of stacks: who stacked them and who killed their creeps. */
export function playersIn(stacks: Stack[]): Set<string> {
  return new Set(stacks.flatMap((s) => [...(s[2] ? [s[2]] : []), ...s[10].map(([hero]) => hero)]));
}

/** One stack in a sentence: when, which camp, who stacked it, and where its creeps went. */
function stackSentence(data: StacksData, stack: Stack): string {
  const [t, campId, hero, , , , waves, creeps, pulled, gold, cleared] = stack;
  const camp = data.camps.find((c) => c.id === campId);
  const where = camp ? `camp ${camp.id} (${campType(camp.type)})` : "a camp off the catalog";
  const by = cleared.length
    ? cleared.map((c) => `${c[0]} ${c[2]}${outcomeOf(stack, c) === "enemy" ? " (the enemy)" : ""}`).join(", ")
    : "nobody";
  return (
    `${clock(t)}: ${hero ?? "no player credited"} stacked ${where}, ${creeps} creeps in ${waves} waves; ` +
    `killed by ${by}${pulled ? `, ${pulled} pulled` : ""}. ${gold} gold to the killers.`
  );
}

interface Bar {
  stack: number;
  segments: Segment[];
}

interface Row {
  hero: string | null;
  side: Side | "";
  bars: Bar[];
  /** The players at the other end, with their creeps, most first. */
  others: [string, number][];
}

/**
 * One row per player, Radiant's then Dire's, each in the order of its first
 * bar. By stacker, a bar is a stack the player made, split by who killed its
 * creeps; by killer, it is the creeps the player killed from one stack.
 */
export function playerRows(data: StacksData, by: RowsBy): Row[] {
  const rows = new Map<string, { row: Row; others: Map<string, number> }>();
  const add = (hero: string | null, side: Side | "", bar: Bar, others: [string, number][]) => {
    const key = hero ?? "";
    const entry = rows.get(key) ?? { row: { hero, side, bars: [], others: [] }, others: new Map<string, number>() };
    entry.row.bars.push(bar);
    for (const [other, n] of others) entry.others.set(other, (entry.others.get(other) ?? 0) + n);
    rows.set(key, entry);
  };
  data.stacks.forEach((stack, index) => {
    const [, , hero, side, , , , , , , cleared] = stack;
    if (by === "stacker") {
      add(hero, side, { stack: index, segments: segments(stack) }, cleared.map(([h, , n]) => [h, n]));
      return;
    }
    for (const clearer of cleared) {
      const segment = { outcome: outcomeOf(stack, clearer), creeps: clearer[2] };
      add(clearer[0], clearer[1], { stack: index, segments: [segment] }, [[hero ?? "no player credited", clearer[2]]]);
    }
  });
  const rank = (side: Side | "") => (side === "r" ? 0 : side === "d" ? 1 : 2);
  return [...rows.values()]
    .map(({ row, others }) => ({ ...row, others: [...others.entries()].sort((a, b) => b[1] - a[1]) }))
    .sort((a, b) => rank(a.side) - rank(b.side));
}

/** The game second the time axis ends at: the replay's end, or a later stack. */
export function axisEnd(data: StacksData): number {
  return Math.max(data.end_s, ...data.stacks.map((s) => s[0]), 60);
}

/** A row's summary: "6 stacks → Timbersaw 12, Sniper 7", or "48 creeps ← Timbersaw 35, Lion 12". */
function rowSummary(row: Row, by: RowsBy): string {
  const others = row.others.map(([hero, n]) => `${hero} ${n}`).join(", ");
  if (by === "stacker") return `${plural(row.bars.length, "stack")} → ${others || "no player"}`;
  const creeps = row.bars.reduce((n, bar) => n + bar.segments[0].creeps, 0);
  return `${plural(creeps, "creep")} ← ${others}`;
}

/** A player's name as a button that picks them, or plain text for a stack nobody was credited with. */
function heroButton(hero: string | null, side: Side | ""): string {
  if (!hero) return `<span class="stacks-hero stacks-hero--none">No player credited</span>`;
  return `<button type="button" class="stacks-pick" data-hero="${escape(hero)}"><span class="stacks-hero stacks-hero--${team(side)}">${escape(hero)}</span></button>`;
}

/**
 * The rows, with a time axis under them. Positions are fractions of `--end`
 * (game seconds), so the browser can show a shorter stretch by setting it; a
 * bar's height is its creeps times `--creep`.
 */
export function rowsMarkup(data: StacksData, by: RowsBy): string {
  const rows = playerRows(data, by);
  if (!rows.length) return `<p class="stacks-none">No stacks.</p>`;
  const end = axisEnd(data);
  const most = Math.max(...rows.flatMap((row) => row.bars.map((bar) => bar.segments.reduce((n, s) => n + s.creeps, 0))));
  const head = (side: Side | "") =>
    side ? `${SIDE_NAME[side]} ${by === "stacker" ? "stacked" : "killed stacked creeps"}` : "Nobody credited";
  const html: string[] = [];
  rows.forEach((row, i) => {
    if (i === 0 || row.side !== rows[i - 1].side) html.push(`<p class="stacks-rows-side">${head(row.side)}</p>`);
    const dodge: Record<number, number> = {};
    const bars = row.bars.map(({ stack, segments: segs }) => {
      const t = data.stacks[stack][0];
      dodge[t] = (dodge[t] ?? -1) + 1;
      const text = escape(stackSentence(data, data.stacks[stack]));
      const runs = segs.map((s) => `<i class="stacks-seg stacks-seg--${s.outcome}" style="--n: ${s.creeps}"></i>`).join("");
      return `<button type="button" class="stacks-bar" data-stack="${stack}" data-t="${t}" style="--t: ${t}; --dodge: ${dodge[t]}" title="${text}" aria-label="${text}">${runs}</button>`;
    });
    html.push(
      `<div class="stacks-row">` +
        `<p class="stacks-row-label" data-row="${escape(row.hero ?? "")}">${heroButton(row.hero, row.side)} <span class="stacks-muted">${escape(rowSummary(row, by))}</span></p>` +
        `<div class="stacks-track">${bars.join("")}</div></div>`,
    );
  });
  const ticks: string[] = [];
  for (let m = 0; m * 60 <= end; m += 5) {
    const every = m % 20 === 0 ? 20 : m % 10 === 0 ? 10 : 5;
    ticks.push(`<span class="stacks-tick stacks-tick--${every}" data-t="${m * 60}" style="--t: ${m * 60}">${m}:00</span>`);
  }
  html.push(`<div class="stacks-row stacks-axis" aria-hidden="true"><span></span><div class="stacks-track">${ticks.join("")}</div></div>`);
  return `<div class="stacks-rows" style="--end: ${end}; --most: ${most}">${html.join("")}</div>`;
}

/** The stacked camps on the map: sized by how often each was stacked, ringed by the side that stacked it. */
export function campsMarkup(data: StacksData, selected: number | null): string {
  const groups = data.camps.map((camp) => {
    const stacks = stacksAt(data, camp.id);
    const n = stacks.length;
    const r = 15 + 6 * n;
    const [x, y] = camp.xy;
    const radiant = stacks.filter((s) => s[3] === "r").length;
    const circ = 2 * Math.PI * r;
    const arc = (from: number, frac: number, team: string) =>
      frac > 0
        ? `<circle class="stacks-ring stacks-ring--${team}" cx="${x}" cy="${y}" r="${r}" stroke-dasharray="${(frac * circ).toFixed(1)} ${circ.toFixed(1)}" stroke-dashoffset="${(-from * circ).toFixed(1)}" transform="rotate(-90 ${x} ${y})"></circle>`
        : "";
    const label = `${campType(camp.type)} camp, stacked ${n} time${n === 1 ? "" : "s"}`;
    return (
      `<g class="stacks-camp${camp.id === selected ? " is-selected" : ""}" data-camp="${camp.id}" tabindex="0" role="button" aria-label="${escape(label)}" aria-pressed="${camp.id === selected}" style="--camp: var(--camp-${camp.type.replace("_", "-")})">` +
      `<circle class="stacks-halo" cx="${x}" cy="${y}" r="${r + 7}"></circle>` +
      `<circle class="stacks-dot" cx="${x}" cy="${y}" r="${r - 3}"></circle>` +
      arc(0, radiant / n, "radiant") +
      arc(radiant / n, (n - radiant) / n, "dire") +
      `<text class="stacks-count" x="${x}" y="${y + 7}" text-anchor="middle">${n}</text>` +
      `</g>`
    );
  });
  return groups.join("");
}

/** A stack in the card's list: when, who stacked it, and who killed its creeps; with its camp when the list mixes camps. */
function stackItem(stack: Stack, withCamp: boolean): string {
  const [t, campId, hero, side, role, exact, waves, creeps, pulled, gold, cleared] = stack;
  const who = hero
    ? `<span class="stacks-hero stacks-hero--${team(side)}">${escape(hero)}</span> <span class="stacks-muted">${role ? ROLE[role] : ""}${exact ? "" : ", matched by position"}</span>`
    : `<span class="stacks-muted">Not placed</span>`;
  const by = cleared.length
    ? cleared.map(([h, s, n]) => `<span class="${side && s !== side ? "stacks-enemy" : ""}">${escape(h)} ${n}</span>`).join(", ")
    : "nobody";
  const camp = withCamp ? (campId === null ? "Off the catalog: " : `Camp ${campId}: `) : "";
  return (
    `<li><time>${clock(t)}</time><div>${who}` +
    `<p>${camp}${creeps} creeps in ${waves} waves; killed by ${by}${pulled ? `, ${pulled} pulled` : ""}</p>` +
    `<p class="stacks-muted">${gold} gold to the killers</p></div></li>`
  );
}

const campChip = (camp: Camp) =>
  `<span class="stacks-chip" style="--camp: var(--camp-${camp.type.replace("_", "-")})">${campType(camp.type)}</span>`;

/** One camp's stacks: when, who stacked it, and who killed its creeps. */
export function campMarkup(data: StacksData, campId: number | null): string {
  const camp = data.camps.find((c) => c.id === campId);
  if (!camp) return `<p class="stacks-none">No camp was stacked.</p>`;
  const stacks = stacksAt(data, camp.id);
  return (
    `<p class="stacks-camp-head">${campChip(camp)}Camp ${camp.id}, stacked ${plural(stacks.length, "time")}</p>` +
    `<ol class="stacks-list">${stacks.map((s) => stackItem(s, false)).join("")}</ol>`
  );
}

/** The card for a pick: the stack, the camp's stacks, or the stacks a player made or cleared. */
export function pickMarkup(data: StacksData, pick: Pick): string {
  switch (pick.kind) {
    case "camp":
      return campMarkup(data, pick.id);
    case "stack": {
      const stack = data.stacks[pick.index];
      const camp = data.camps.find((c) => c.id === stack[1]);
      const head = camp ? `${campChip(camp)}Camp ${camp.id} at ${clock(stack[0])}` : `Off the camp catalog at ${clock(stack[0])}`;
      return `<p class="stacks-camp-head">${head}</p><ol class="stacks-list">${stackItem(stack, false)}</ol>`;
    }
    case "hero": {
      const stacks = data.stacks.filter((s, i) => isPicked(s, i, pick));
      const made = stacks.filter((s) => s[2] === pick.hero).length;
      const killed = stacks.reduce((n, s) => n + s[10].filter(([h]) => h === pick.hero).reduce((m, c) => m + c[2], 0), 0);
      const side = data.players.find((p) => p[0] === pick.hero)?.[1] ?? "";
      const counts = [made ? `${plural(made, "stack")} made` : "", killed ? `${plural(killed, "stacked creep")} killed` : ""];
      return (
        `<p class="stacks-camp-head"><span class="stacks-hero stacks-hero--${team(side)}">${escape(pick.hero)}</span>` +
        `${counts.filter(Boolean).join(", ")}</p>` +
        `<ol class="stacks-list">${stacks.map((s) => stackItem(s, true)).join("")}</ol>`
      );
    }
    default: {
      const never: never = pick;
      return never;
    }
  }
}

/** Each player's stacks, and the stacked creeps they killed and their gold. */
export function playersMarkup(data: StacksData): string {
  const top = Math.max(1, ...data.players.map((p) => p[6]));
  const rows = data.players.map(([hero, side, role, stacks, exact, killed, gold, neutral]) => {
    const share = neutral ? `${Math.round((gold / neutral) * 100)}%` : "–";
    return (
      `<tr data-row="${escape(hero)}"><td>${heroButton(hero, side)}</td><td>${role ? ROLE[role] : ""}</td>` +
      `<td>${stacks}${stacks ? ` <span class="stacks-muted">(${exact})</span>` : ""}</td><td>${killed}</td>` +
      `<td><span class="stacks-gold">${gold.toLocaleString("en-US")}<i style="width: ${((gold / top) * 40).toFixed(1)}px"></i></span></td>` +
      `<td>${share}</td></tr>`
    );
  });
  return (
    `<div class="stacks-table"><table><thead><tr><th>Hero</th><th>Role</th><th>Stacks (exact)</th>` +
    `<th>Creeps killed</th><th>Gold</th><th title="Of the player's neutral gold">Share</th></tr></thead>` +
    `<tbody>${rows.join("")}</tbody></table></div>`
  );
}

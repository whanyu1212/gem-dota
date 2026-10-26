/**
 * The stacks recipe's figure: who stacked for whom (each side's stackers and the
 * players who killed their stacked creeps), the stacked camps on the map with one
 * camp's stacks listed, when each stack was made, and each player's numbers. No
 * DOM here: the Markdown build renders the figure with it (src/figures/stacks.ts)
 * and the browser redraws the camp list for the camp picked (stacks-figure.ts).
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

/** [stacker, side, role, killer, side, role, creeps, gold]. */
export type Flow = [string, Side, Role, string, Side, Role, number, number];

/** [hero, side, role, stacks, exact, killed, gold, neutral_gold]. */
export type Player = [string, Side | "", Role | "", number, number, number, number, number];

export interface StacksData {
  /** The game second the replay ends, for the timeline. */
  end_s: number;
  camps: Camp[];
  stacks: Stack[];
  flows: Flow[];
  players: Player[];
}

const TEAM: Record<Side, string> = { r: "radiant", d: "dire" };
const SIDE_NAME: Record<Side, string> = { r: "Radiant", d: "Dire" };
const ROLE: Record<Role, string> = { s: "support", c: "core" };

const escape = (text: string) => text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

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

/** The flows out of one side's stacks, and their stacked creeps in all. */
export function sideFlows(data: StacksData, side: Side): { flows: Flow[]; creeps: number } {
  const flows = data.flows.filter((f) => f[1] === side);
  return { flows, creeps: flows.reduce((sum, f) => sum + f[6], 0) };
}

/** A side's stacked creeps the other side killed: [creeps, gold]. */
export function takenByEnemy(data: StacksData, side: Side): [number, number] {
  return sideFlows(data, side)
    .flows.filter((f) => f[4] !== side)
    .reduce(([n, g], f) => [n + f[6], g + f[7]], [0, 0]);
}

/** Ribbon pixels per stacked creep, so both sides draw to one scale. */
const PER_CREEP = 2.6;
/** Each node takes at least this many pixels, so its label never meets the next. */
const MIN_SLOT = 18;
const GAP = 6;

interface Node {
  y: number;
  h: number;
  used: number;
  role: Role;
  side: Side;
  total: number;
}

/**
 * One side's stackers (left) joined to the players who killed their stacked
 * creeps (right). The labels are HTML at the page's own size; the ribbons are an
 * SVG between them that stretches only sideways, so a node's pixel height is its
 * creeps at any width.
 */
export function flowMarkup(data: StacksData, side: Side): string {
  const { flows, creeps } = sideFlows(data, side);
  if (!flows.length) return `<p class="stacks-none">${SIDE_NAME[side]} made no stacks a player cleared.</p>`;
  const place = (end: (f: Flow) => [string, Side, Role]): Map<string, Node> => {
    const nodes = new Map<string, Node>();
    for (const f of flows) {
      const [hero, s, role] = end(f);
      const node = nodes.get(hero) ?? { y: 0, h: 0, used: 0, role, side: s, total: 0 };
      node.total += f[6];
      nodes.set(hero, node);
    }
    let y = 0;
    for (const node of nodes.values()) {
      node.y = y;
      node.h = node.total * PER_CREEP;
      y += Math.max(node.h, MIN_SLOT) + GAP;
    }
    return nodes;
  };
  const stackers = place((f) => [f[0], f[1], f[2]]);
  const killers = place((f) => [f[3], f[4], f[5]]);
  const height = Math.max(...[...stackers.values(), ...killers.values()].map((n) => n.y + Math.max(n.h, MIN_SLOT)));
  const ribbons = flows.map((f) => {
    const [a, b] = [stackers.get(f[0]), killers.get(f[3])];
    if (!a || !b) return "";
    const w = f[6] * PER_CREEP;
    const [ya, yb] = [a.y + a.used + w / 2, b.y + b.used + w / 2];
    a.used += w;
    b.used += w;
    const enemy = f[4] !== side;
    const title = `${f[0]} → ${f[3]}: ${f[6]} stacked creeps, ${f[7]} gold${enemy ? " (the enemy)" : ""}`;
    return (
      `<path class="stacks-ribbon stacks-ribbon--${enemy ? "enemy" : TEAM[side]}" d="M0,${ya.toFixed(1)} C50,${ya.toFixed(1)} 50,${yb.toFixed(1)} 100,${yb.toFixed(1)}" stroke-width="${Math.max(w, 1.5).toFixed(1)}">` +
      `<title>${escape(title)}</title></path>`
    );
  });
  // Each column also lists its labels unpositioned and unseen, so it is as wide as its longest.
  const labels = (map: Map<string, Node>) => {
    const text = (hero: string, n: Node) => `${escape(hero)} <b>${n.role === "s" ? "S" : "C"}</b> · ${n.total}`;
    const placed = [...map.entries()].map(
      ([hero, n]) =>
        `<li class="stacks-node stacks-node--${TEAM[n.side]}" style="top: ${n.y.toFixed(1)}px; height: ${Math.max(n.h, 2).toFixed(1)}px"><span>${text(hero, n)}</span></li>`,
    );
    const sizer = [...map.entries()].map(([hero, n]) => `<li class="stacks-node stacks-node--sizer"><span>${text(hero, n)}</span></li>`);
    return placed.join("") + sizer.join("");
  };
  return (
    `<div class="stacks-flow" role="img" aria-label="${SIDE_NAME[side]}'s ${creeps} stacked creeps, by stacker and by who killed them">` +
    `<p class="stacks-flow-head"><span>${SIDE_NAME[side]} stacked</span><span>Killed by</span></p>` +
    `<div class="stacks-flow-body" style="height: ${height.toFixed(0)}px">` +
    `<ol class="stacks-nodes stacks-nodes--left">${labels(stackers)}</ol>` +
    `<svg class="stacks-ribbons" viewBox="0 0 100 ${height.toFixed(0)}" preserveAspectRatio="none" aria-hidden="true">${ribbons.join("")}</svg>` +
    `<ol class="stacks-nodes stacks-nodes--right">${labels(killers)}</ol>` +
    `</div></div>`
  );
}

/** Both sides' flows, with each side's stacked creeps the enemy killed. */
export function flowsMarkup(data: StacksData): string {
  const side = (s: Side) => {
    const [n, gold] = takenByEnemy(data, s);
    const note = n ? `<p class="stacks-enemy-note">${n} of ${SIDE_NAME[s]}'s stacked creeps (${gold} gold) went to the enemy.</p>` : "";
    return `<div class="stacks-flow-side">${flowMarkup(data, s)}${note}</div>`;
  };
  return `<div class="stacks-flows">${side("r")}${side("d")}</div>`;
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

/** One camp's stacks: when, who stacked it, and who killed its creeps. */
export function campMarkup(data: StacksData, campId: number | null): string {
  const camp = data.camps.find((c) => c.id === campId);
  if (!camp) return `<p class="stacks-none">No camp was stacked.</p>`;
  const stacks = stacksAt(data, camp.id);
  const rows = stacks.map(([t, , hero, side, role, exact, waves, creeps, pulled, gold, cleared]) => {
    const who = hero ? `<span class="stacks-hero stacks-hero--${side ? TEAM[side] : "none"}">${escape(hero)}</span> <span class="stacks-muted">${role ? ROLE[role] : ""}${exact ? "" : ", matched by position"}</span>` : `<span class="stacks-muted">Not placed</span>`;
    const by = cleared.length
      ? cleared.map(([h, s, n]) => `<span class="${side && s !== side ? "stacks-enemy" : ""}">${escape(h)} ${n}</span>`).join(", ")
      : "nobody";
    const extra = pulled ? `, ${pulled} pulled` : "";
    return (
      `<li><time>${clock(t)}</time><div>${who}` +
      `<p>${creeps} creeps in ${waves} waves; killed by ${by}${extra}</p>` +
      `<p class="stacks-muted">${gold} gold to the killers</p></div></li>`
    );
  });
  return (
    `<p class="stacks-camp-head"><span class="stacks-chip" style="--camp: var(--camp-${camp.type.replace("_", "-")})">${campType(camp.type)}</span>` +
    `Camp ${camp.id}, stacked ${stacks.length} time${stacks.length === 1 ? "" : "s"}</p>` +
    `<ol class="stacks-list">${rows.join("")}</ol>`
  );
}

/** When each stack was made: Radiant's above the line, Dire's below, one dot a stack, by minute. */
export function timelineMarkup(data: StacksData): string {
  const end = Math.max(data.end_s, ...data.stacks.map((s) => s[0]), 60);
  const left = (t: number) => `${((t / end) * 100).toFixed(2)}%`;
  const count: Record<string, number> = {};
  const dots = data.stacks.map(([t, , hero, side]) => {
    const minute = Math.floor(t / 60);
    const key = `${minute}${side}`;
    count[key] = (count[key] ?? 0) + 1;
    const team = side ? TEAM[side] : "none";
    return `<i class="stacks-tick stacks-tick--${team}" style="left: ${left(minute * 60)}; --row: ${count[key]}" title="${clock(t)} ${escape(hero ?? "")}"></i>`;
  });
  const labels: string[] = [];
  for (let m = 0; m * 60 <= end; m += 10) {
    const minor = m % 20 ? ' class="stacks-minor"' : "";
    labels.push(`<span${minor} style="left: ${left(m * 60)}">${m}:00</span>`);
  }
  return (
    `<div class="stacks-timeline" role="img" aria-label="When each stack was made: ${data.stacks.length} stacks">` +
    `<div class="stacks-timeline-track">${dots.join("")}</div>` +
    `<div class="stacks-timeline-labels" aria-hidden="true">${labels.join("")}</div></div>`
  );
}

/** Each player's stacks, and the stacked creeps they killed and their gold. */
export function playersMarkup(data: StacksData): string {
  const top = Math.max(1, ...data.players.map((p) => p[6]));
  const rows = data.players.map(([hero, side, role, stacks, exact, killed, gold, neutral]) => {
    const share = neutral ? `${Math.round((gold / neutral) * 100)}%` : "–";
    return (
      `<tr><td><span class="stacks-hero stacks-hero--${side ? TEAM[side] : "none"}">${escape(hero)}</span></td><td>${role ? ROLE[role] : ""}</td>` +
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

/**
 * Figure 3's playback in the browser. FightFigure.astro renders the final frame
 * and a narration; when the figure comes into view this loads the playback
 * data (src/data/fight.json) and takes over: the map layers, each hero's
 * status, the feed, the damage strip and following a hero.
 *
 * Plays like a GIF while on screen (2×, looping), unless the reader paused it
 * or prefers reduced motion; then it waits on the final frame for play.
 */
import {
  buybackAfter,
  castParts,
  castText,
  clockAt,
  damagePerSecond,
  deathTimes,
  FILTERS,
  feedRows,
  activeModifier,
  isHidden,
  isSmoked,
  QUIET_ITEMS,
  rowShows,
  stateAt,
  type Cast,
  type FightData,
  type HeroState,
  type Row,
} from "./fight-playback";

interface View {
  box: [number, number, number];
  /** Map units per screen pixel the server assumed (used until the map is measured). */
  px: number;
  icons: { heroes: Record<string, string>; items: Record<string, string> };
}

const SPEEDS = [0.5, 1, 2, 4];
const DEFAULT_SPEED = 2;
const HOLD_MS = 1800; // pause on the last frame before looping
const CAST_POP_S = 1.4; // how long a cast's label and lines stay up
const DAMAGE_LINE_S = 0.6;
const GOLD_POP_S = 2.2;
const SMOKE_PUFF_S = 0.9;
const LAYERS = [
  { key: "hp", label: "HP & mana" },
  { key: "casts", label: "Casts" },
  { key: "damage", label: "Damage" },
  { key: "status", label: "Disables & buffs" },
  { key: "gold", label: "Gold" },
] as const;
type Layer = (typeof LAYERS)[number]["key"];
const BUFF_LABELS: Record<string, string> = {
  bkb: "Spell immune",
  ghost: "Ghost form",
  blade_mail: "Blade Mail",
  lotus: "Lotus Orb",
  satanic: "Satanic",
  aeon_disk: "Aeon Disk",
};

const SVG = "http://www.w3.org/2000/svg";
function svg<K extends keyof SVGElementTagNameMap>(
  tag: K,
  attrs: Record<string, string | number> = {},
  parent?: Element,
): SVGElementTagNameMap[K] {
  const el = document.createElementNS(SVG, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, String(v));
  parent?.appendChild(el);
  return el;
}
function html<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string> = {},
  ...children: (Node | string)[]
): HTMLElementTagNameMap[K] {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  el.append(...children);
  return el;
}
const number = (n: number) => Math.round(n).toLocaleString("en-US");

export function mountFightPlayer(root: HTMLElement): void {
  const viewEl = root.querySelector<HTMLScriptElement>("[data-fight-view]");
  if (!viewEl) return;
  const view = JSON.parse(viewEl.textContent ?? "{}") as View;
  let player: ReturnType<typeof createPlayer> | undefined;
  let visible = false;
  // Load the playback a little before the figure scrolls into view.
  new IntersectionObserver(
    ([entry]) => {
      if (!entry.isIntersecting || player) return;
      import("../data/fight.json").then(({ default: data }) => {
        player = createPlayer(root, view, data as unknown as FightData);
        player.setVisible(visible);
      });
    },
    { rootMargin: "300px" },
  ).observe(root);
  new IntersectionObserver(
    ([entry]) => {
      visible = entry.isIntersecting;
      player?.setVisible(visible);
    },
    { threshold: 0.35 },
  ).observe(root);
}

function createPlayer(root: HTMLElement, view: View, data: FightData) {
  // Size marks in screen pixels for the map as drawn (wider on a desktop than a phone).
  const drawn = root.querySelector<SVGSVGElement>("[data-map]")!.getBoundingClientRect().width;
  const px = drawn > 0 ? view.box[2] / drawn : view.px;
  const badge = 11 * px;
  root.querySelector("#hero-badge circle")?.setAttribute("r", String(badge));
  const heroes = data.heroes;
  const names = heroes.map((h) => h.hero);
  const teams = heroes.map((h) => h.team);
  const deaths = deathTimes(data);
  const rows = feedRows(data);
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const layers = new Set<Layer>(LAYERS.map((l) => l.key));
  const filters = new Set(FILTERS.filter((f) => f.on).map((f) => f.key));
  let follow: number | null = null;
  let speed = DEFAULT_SPEED;
  let t = data.duration;
  let playing = false;
  let pausedByReader = reducedMotion;
  let last = 0;
  let holdUntil = 0;
  let lastCurrent: HTMLLIElement | undefined;

  // --- Reveal the live figure; the static frame and narration step aside. ---
  const $ = <T extends Element>(selector: string) => root.querySelector<T>(selector)!;
  $<SVGGElement>("[data-static]").remove();
  $<HTMLOListElement>("[data-events]").hidden = true;
  $<HTMLElement>("[data-caption-static]").hidden = true;
  for (const selector of ["[data-layers]", "[data-playback]", "[data-strip]", "[data-legend]", "[data-status]", "[data-filters]", "[data-feed]", "[data-caption-live]"]) {
    $<HTMLElement>(selector).hidden = false;
  }

  const heroIcon = (i: number) => view.icons.heroes[heroes[i].icon] ?? "";
  const iconImg = (i: number) =>
    html("img", { class: `hero-icon hero-icon--${heroes[i].team}`, src: heroIcon(i), alt: names[i], title: names[i], width: "18", height: "18" });

  // --- Map layers ---
  const map = $<SVGSVGElement>("[data-map]");
  const gDeaths = svg("g", {}, map);
  const gDamage = svg("g", {}, map);
  const gLinks = svg("g", {}, map);
  const gHeroes = svg("g", {}, map);
  const gPops = svg("g", {}, map);
  // A soft blur for the smoke cloud behind a smoked hero.
  const blur = svg("filter", { id: "smoke-blur", x: "-50%", y: "-50%", width: "200%", height: "200%" }, map.querySelector("defs")!);
  svg("feGaussianBlur", { stdDeviation: 3 * px }, blur);

  const spotBefore = (hero: number, at: number): HeroState | null => stateAt(heroes[hero], [], at - 0.05);
  const deathMarks = data.deaths.map((death) => {
    const spot = spotBefore(death.victim, death.t);
    const g = svg("g", { class: `fight-death fight-death--${death.aegis ? "aegis" : heroes[death.victim].team}` }, gDeaths);
    if (spot) g.setAttribute("transform", `translate(${spot.x} ${spot.y}) scale(${px})`);
    svg("path", { class: "halo", d: "M-5,-5 L5,5 M5,-5 L-5,5" }, g);
    svg("path", { d: "M-5,-5 L5,5 M5,-5 L-5,5" }, g);
    return { death, spot, g };
  });

  const circumference = 2 * Math.PI * 15.5 * px;
  const heroEls = heroes.map((hero, i) => {
    const g = svg("g", { class: `fight-hero fight-hero--${hero.team}` }, gHeroes);
    g.addEventListener("click", () => setFollow(i));
    svg("title", {}, g).textContent = hero.hero;
    svg("circle", { class: "smoke-cloud", r: badge * 1.9, filter: "url(#smoke-blur)" }, g);
    svg("circle", { class: "hidden-ring", r: badge + 4 * px, "stroke-width": 1.4 * px, "stroke-dasharray": `${3 * px} ${2.5 * px}` }, g);
    const buff = svg("circle", { class: "buff-ring", r: 17 * px, "stroke-width": 2.4 * px }, g);
    // Disabled: a solid arc that drains as the disable runs out, on a dark track.
    const disable = svg("circle", { class: "disable-track", r: 15.5 * px, "stroke-width": 3 * px }, g);
    const disableArc = svg("circle", { class: "disable-arc", r: 15.5 * px, "stroke-width": 3 * px, transform: "rotate(-90)" }, g);
    const flash = svg("circle", { class: "hit-flash", r: badge + 2.5 * px }, g);
    svg("circle", { class: "hero-ring", r: badge + 2 * px, "stroke-width": 1.2 * px }, g);
    svg("image", { class: "hero-badge", href: heroIcon(i), x: -badge, y: -badge, width: badge * 2, height: badge * 2, "clip-path": "url(#hero-badge)" }, g);
    const bars = svg("g", { class: "hero-bars" }, g);
    svg("rect", { class: "bar-bg", x: -14 * px, y: 15 * px, width: 28 * px, height: 6.4 * px, rx: 1 * px }, bars);
    const hp = svg("rect", { class: "bar-hp", x: -13.4 * px, y: 15.6 * px, height: 3 * px }, bars);
    const mana = svg("rect", { class: "bar-mana", x: -13.4 * px, y: 19.2 * px, height: 1.6 * px }, bars);
    const chips = svg("g", {}, g);
    return { g, buff, disable, disableArc, flash, bars, hp, mana, chips };
  });

  // --- Controls: layers, speed, play, strip ---
  const chip = (label: string, on: boolean, onClick: (button: HTMLButtonElement) => void) => {
    const button = html("button", { type: "button", class: "chip", "aria-pressed": String(on) }, label);
    button.addEventListener("click", () => onClick(button));
    return button;
  };
  const layersEl = $<HTMLElement>("[data-layers]");
  layersEl.append(
    html("span", { class: "chip-label" }, "On the map"),
    ...LAYERS.map((layer) =>
      chip(layer.label, true, (button) => {
        if (layers.has(layer.key)) layers.delete(layer.key);
        else layers.add(layer.key);
        button.setAttribute("aria-pressed", String(layers.has(layer.key)));
        render();
      }),
    ),
  );
  const speedsEl = $<HTMLElement>("[data-speeds]");
  const speedButtons = SPEEDS.map((s) =>
    chip(`${s}×`, s === speed, () => {
      speed = s;
      for (const [k, b] of speedButtons.entries()) b.setAttribute("aria-pressed", String(SPEEDS[k] === speed));
    }),
  );
  speedsEl.append(...speedButtons);
  const button = $<HTMLButtonElement>("[data-play]");
  const clock = $<HTMLOutputElement>("[data-clock]");
  const scrub = $<HTMLInputElement>("[data-scrub]");
  scrub.max = String(data.duration);

  const strip = $<SVGSVGElement>("[data-strip] svg");
  const perSecond = damagePerSecond(data);
  const peak = Math.max(1, ...perSecond.radiant, ...perSecond.dire);
  const width = 1000 / perSecond.radiant.length;
  perSecond.radiant.forEach((v, i) => {
    svg("rect", { class: "strip-radiant", x: i * width + 0.5, y: 32 - (v / peak) * 28, width: width - 1, height: (v / peak) * 28 }, strip);
    svg("rect", { class: "strip-dire", x: i * width + 0.5, y: 32, width: width - 1, height: (perSecond.dire[i] / peak) * 28 }, strip);
  });
  svg("line", { class: "strip-axis", x1: 0, x2: 1000, y1: 32, y2: 32 }, strip);
  // Deaths and buybacks as marks beside the strip: Radiant's above it, Dire's
  // below, each in two rows (deaths next to the bars, buybacks outside them) so a
  // death and its buyback a second later don't cover each other.
  const lane = (team: string) => {
    const el = html("div", { class: `strip-lane strip-lane--${team}` });
    const deathsRow = html("div", { class: "strip-row" });
    const buybacksRow = html("div", { class: "strip-row" });
    if (team === "radiant") el.append(buybacksRow, deathsRow);
    else el.append(deathsRow, buybacksRow);
    return { el, deathsRow, buybacksRow };
  };
  const lanes = { radiant: lane("radiant"), dire: lane("dire") };
  strip.before(lanes.radiant.el);
  strip.after(lanes.dire.el);
  const at = (t: number) => `${(100 * t) / data.duration}%`;
  for (const death of data.deaths) {
    const team = heroes[death.victim].team === "radiant" ? "radiant" : "dire";
    const mark = html(
      "span",
      { class: `strip-mark strip-mark--${death.aegis ? "aegis" : team}`, style: `left: ${at(death.t)}`, title: `${names[death.victim]} ${death.aegis ? "died (Aegis)" : "died"} at ${clockAt(data.start_s, death.t)}` },
      death.aegis ? "A" : "✕",
    );
    lanes[team].deathsRow.append(mark);
  }
  for (const [t, hero, cost] of data.buybacks) {
    const team = heroes[hero].team === "radiant" ? "radiant" : "dire";
    const mark = html(
      "span",
      { class: "strip-mark strip-mark--buyback", style: `left: ${at(t)}`, title: `${names[hero]} bought back at ${clockAt(data.start_s, t)} for ${number(cost)} gold` },
      `↺ ${number(cost)}`,
    );
    lanes[team].buybacksRow.append(mark);
  }
  const cursor = svg("line", { class: "strip-cursor", y1: 0, y2: 64 }, strip);

  // --- Status boxes ---
  const statusEl = $<HTMLElement>("[data-status]");
  const order = heroes.map((_, i) => i).sort((a, b) => Number(heroes[a].team === "dire") - Number(heroes[b].team === "dire"));
  const statusEls = order.map((i) => {
    const bar = (cls: string) => {
      const fill = html("i");
      return [html("span", { class: `fight-status-bar ${cls}` }, fill), fill] as const;
    };
    const [hpBar, hpFill] = bar("fight-status-hp");
    const [manaBar, manaFill] = bar("fight-status-mana");
    const text = html("span", { class: "fight-status-text" });
    const box = html("button", { type: "button", class: `fight-status-hero fight-status-hero--${heroes[i].team}`, "aria-pressed": "false", title: `Follow ${names[i]}` }, iconImg(i), hpBar, manaBar, text);
    box.addEventListener("click", () => setFollow(i));
    statusEl.append(box);
    return { i, box, hpFill, manaFill, text };
  });

  // --- Feed ---
  const filtersEl = $<HTMLElement>("[data-filters]");
  const followNote = html("span", { class: "follow-note" });
  filtersEl.append(
    ...FILTERS.map((filter) =>
      chip(filter.label, filter.on, (b) => {
        if (filters.has(filter.key)) filters.delete(filter.key);
        else filters.add(filter.key);
        b.setAttribute("aria-pressed", String(filters.has(filter.key)));
        applyFilters();
      }),
    ),
    followNote,
  );
  const feed = $<HTMLOListElement>("[data-feed]");
  const rowEls = rows.map((row) => {
    const li = html("li", { class: `feed-row feed-row--${row.kind}${row.death?.aegis ? " is-aegis" : ""}` }, html("time", {}, clockAt(data.start_s, row.t)), rowBody(row));
    feed.append(li);
    return { row, li };
  });

  function typeTag(type: string) {
    return type && type !== "others" ? html("span", { class: `dmg dmg--${type}` }, type) : "";
  }
  function tag(text: string) {
    return html("span", { class: "tag" }, text);
  }
  function castBody(cast: Cast) {
    const parts = castParts(cast, teams);
    const body = html("span", { class: "row-body", title: `${names[cast.by]}: ${castText(cast, names, teams)}` }, iconImg(cast.by));
    const itemSrc = cast.item ? view.icons.items[cast.item] : undefined;
    body.append(itemSrc ? html("img", { class: "item-icon", src: itemSrc, alt: "", width: "22", height: "16" }) : html("span", { class: "spell-mark", "aria-hidden": "true" }), html("b", {}, cast.what));
    if (cast.target !== undefined && !cast.hits.some(([h]) => h === cast.target)) {
      body.append(" → ", iconImg(cast.target), tag(heroes[cast.target].team === heroes[cast.by].team ? "ally" : "enemy"));
    } else if (cast.unit) {
      body.append(" → ", tag(cast.unit));
    } else if (cast.self && !cast.hits.length) {
      body.append(tag("on self"));
    }
    if (parts.allies.length) {
      body.append(tag("on"));
      for (const ally of parts.allies) body.append(iconImg(ally.hero));
    }
    if (parts.hits.length) {
      body.append(tag("hit"));
      for (const hit of parts.hits) {
        const piece = html("span", { class: "hit" }, iconImg(hit.hero));
        if (hit.damage) piece.append(html("span", { class: "hit-damage" }, number(hit.damage)));
        if (hit.damage && !parts.sharedType) piece.append(typeTag(hit.type));
        body.append(piece);
      }
      if (parts.sharedType) body.append(typeTag(parts.sharedType));
    }
    return body;
  }
  function deathBody(row: Row) {
    const death = row.death!;
    const victim = death.victim;
    const lead = html("span", { class: "row-body" }, html("span", { class: "death-mark", "aria-hidden": "true" }, "✕"), iconImg(victim), html("b", {}, death.aegis ? "died to" : "killed by"), death.killer !== null ? iconImg(death.killer) : tag(death.killer_name));
    const others = (death.tick_victims ?? []).filter((v) => v !== victim);
    if (death.aegis) lead.append(tag("Aegis · no gold lost"));
    else {
      lead.append(html("span", { class: "loss" }, `−${number(death.gold_lost)}`));
      for (const [hero, gold] of death.gold) lead.append(html("span", { class: "hit" }, iconImg(hero), html("span", { class: "gain" }, `+${number(gold)}`)));
    }
    // Same-tick deaths share one set of bounties: shown once, on the first death.
    if (others.length) lead.append(tag(death.gold.length ? "bounties shared with" : "bounties with"), ...others.map(iconImg));
    const toggle = html("button", { type: "button", class: "recap-toggle", "aria-expanded": "false" }, lead);
    const recap = html("div", { class: "recap", hidden: "" });
    const total = death.recent_total;
    const listed = death.recent.reduce((sum, r) => sum + r[3], 0);
    const barEl = html("span", { class: "recap-bar" });
    for (const [, , type, damage] of death.recent) barEl.append(html("i", { class: `dmg-fill dmg-fill--${type}`, style: `flex: ${damage}` }));
    if (total > listed) barEl.append(html("i", { class: "dmg-fill dmg-fill--others", style: `flex: ${total - listed}` }));
    recap.append(html("p", { class: "recap-label" }, `Damage taken, last 10 s · ${number(total)}`), barEl);
    for (const [who, source, type, damage] of death.recent) {
      recap.append(html("p", { class: "recap-row" }, html("span", {}, `${who} · ${source} `, typeTag(type)), html("b", {}, number(damage))));
    }
    if (total > listed) recap.append(html("p", { class: "recap-row" }, html("span", {}, "Other sources"), html("b", {}, number(total - listed))));
    const xp = death.xp[0]?.[1];
    recap.append(
      html("p", { class: "recap-label" }, "XP"),
      html(
        "p",
        {},
        death.aegis
          ? "None: the Aegis brought the hero back."
          : xp
            ? `+${number(xp)} each to ${death.xp.map(([h]) => names[h]).join(", ")}${others.length ? `, for this tick's ${others.length + 1} deaths` : ""}`
            : others.length
              ? `Shown with ${names[(death.tick_victims ?? [])[0]]}'s death, on the same tick.`
              : "None",
      ),
    );
    const buyback = buybackAfter(data, death);
    if (buyback) recap.append(html("p", { class: "gain" }, `Bought back at ${clockAt(data.start_s, buyback[0])} for ${number(buyback[2])} gold`));
    toggle.addEventListener("click", () => {
      recap.hidden = !recap.hidden;
      toggle.setAttribute("aria-expanded", String(!recap.hidden));
    });
    const wrap = html("div", { class: "row-death" }, toggle, recap);
    return wrap;
  }
  function rowBody(row: Row): HTMLElement {
    switch (row.kind) {
      case "spell":
      case "item":
        return castBody(row.cast!);
      case "death":
        return deathBody(row);
      case "buyback": {
        const [, hero, cost] = row.buyback!;
        return html("span", { class: "row-body" }, html("span", { class: "buyback-mark", "aria-hidden": "true" }, "↺"), iconImg(hero), html("b", {}, "bought back"), "for", html("span", { class: "loss" }, number(cost)), "gold");
      }
      case "disable":
      case "debuff":
      case "buff": {
        // "Lion · Hex on Ember Spirit 3.2s"; a hero's own buff is "on self".
        const { source, name, targets } = row.effect!;
        const body = html("span", { class: "row-body" });
        if (source !== null) body.append(iconImg(source));
        body.append(html("span", { class: `effect-mark effect-mark--${row.kind}`, "aria-hidden": "true" }), html("b", {}, name));
        const self = targets.length === 1 && targets[0].hero === source;
        body.append(tag(self ? "on self" : "on"));
        for (const { hero, seconds } of targets) {
          const piece = html("span", { class: "hit" });
          if (!self) piece.append(iconImg(hero));
          piece.append(html("span", { class: `effect-seconds effect-seconds--${row.kind}` }, `${seconds}s`));
          body.append(piece);
        }
        return body;
      }
      case "attack": {
        const attack = row.attack!;
        return html("span", { class: "row-body" }, iconImg(attack.by), " → ", iconImg(attack.target), html("span", { class: "hit-damage" }, number(attack.damage)), typeTag(attack.type), tag("attacks"));
      }
      case "smoke": {
        const { hero, seen } = row.smokeBreak!;
        const enemy = heroes[hero].team === "radiant" ? "Dire" : "Radiant";
        return html("span", { class: "row-body" }, iconImg(hero), html("b", {}, "smoke broke"), ...(seen ? [tag(`seen by ${enemy}`)] : []));
      }
    }
  }

  function applyFilters() {
    for (const { row, li } of rowEls) li.hidden = !rowShows(row, filters, follow);
    followNote.textContent = follow === null ? "" : `Following ${names[follow]}`;
    for (const s of statusEls) s.box.setAttribute("aria-pressed", String(s.i === follow));
    lastCurrent = undefined;
    render();
  }
  function setFollow(i: number) {
    follow = follow === i ? null : i;
    root.classList.toggle("is-following", follow !== null);
    applyFilters();
  }

  // --- Rendering a moment ---
  const latestCast = (hero: number) =>
    data.casts.filter((c) => c.by === hero && c.t <= t && t - c.t < CAST_POP_S && !(c.item && QUIET_ITEMS.has(c.item))).at(-1);

  function render() {
    const states = heroes.map((hero, i) => stateAt(hero, deaths[i], t));
    heroEls.forEach((el, i) => {
      const s = states[i];
      el.g.style.display = s ? "" : "none";
      if (!s) return;
      el.g.setAttribute("transform", `translate(${s.x} ${s.y})`);
      el.g.classList.toggle("is-dim", follow !== null && follow !== i);
      el.g.classList.toggle("is-smoked", layers.has("status") && isSmoked(data, i, t));
      el.g.classList.toggle("is-hidden", layers.has("status") && isHidden(data, i, t));
      el.bars.style.display = layers.has("hp") ? "" : "none";
      el.hp.setAttribute("width", String(Math.max(0, (26.8 * px * s.hp) / (s.maxHp || 1))));
      el.mana.setAttribute("width", String(Math.max(0, (26.8 * px * s.mana) / (s.maxMana || 1))));
      const ring = layers.has("status") ? activeModifier(data, i, t, (m) => m[6] !== null) : undefined;
      el.buff.setAttribute("class", ring ? `buff-ring buff-ring--${ring[6]}` : "buff-ring");
      const disable = layers.has("status") ? activeModifier(data, i, t, (m) => m[5] === "disable") : undefined;
      el.disable.style.display = el.disableArc.style.display = disable ? "" : "none";
      if (disable) {
        const left = (disable[1] - t) / (disable[1] - disable[0] || 1);
        el.disableArc.setAttribute("stroke-dasharray", `${circumference * left} ${circumference}`);
      }
      const took = layers.has("damage") && data.damage.some(([d0, , target, damage]) => target === i && d0 <= t && t - d0 < 0.3 && damage >= 120);
      el.flash.classList.toggle("is-on", took);
      // A cast's pop: its item icon, or (for the followed hero) the ability's
      // name; with the damage it did.
      el.chips.replaceChildren();
      const cast = layers.has("casts") ? latestCast(i) : undefined;
      if (cast) {
        const itemSrc = cast.item ? view.icons.items[cast.item] : undefined;
        const fade = 1 - (t - cast.t) / CAST_POP_S;
        const damage = castParts(cast, teams).damage;
        if (itemSrc || follow === i) {
          const g = svg("g", { class: "cast-pop", transform: `translate(0 ${-(21 + (1 - fade) * 4) * px})`, opacity: Math.min(1, fade * 2) }, el.chips);
          const label = itemSrc ? (damage ? number(damage) : "") : damage ? `${cast.what} ${number(damage)}` : cast.what;
          const textWidth = label.length * 5 * px;
          const iconWidth = itemSrc ? 20 * px : 0;
          const w = iconWidth + textWidth + (label ? 8 : 4) * px;
          svg("rect", { class: "pop-bg", x: -w / 2, y: -7.5 * px, width: w, height: 15 * px, rx: 3 * px }, g);
          if (itemSrc) svg("image", { href: itemSrc, x: -w / 2 + 2 * px, y: -6.5 * px, width: 18 * px, height: 13 * px }, g);
          if (label) {
            svg("text", { class: "pop-text", x: -w / 2 + iconWidth + 4 * px, y: 3 * px, "font-size": 9 * px }, g).textContent = label;
          }
        }
      }
    });

    gDamage.replaceChildren();
    gLinks.replaceChildren();
    gPops.replaceChildren();
    if (layers.has("damage")) {
      for (const [d0, by, target, damage, type, direct] of data.damage) {
        if (!direct || d0 > t || t - d0 >= DAMAGE_LINE_S) continue;
        const a = states[by];
        const b = states[target];
        if (!a || !b) continue;
        const fade = 1 - (t - d0) / DAMAGE_LINE_S;
        const dim = follow !== null && follow !== by && follow !== target;
        svg("line", { class: `dmg-line dmg-line--${type}`, x1: a.x, y1: a.y, x2: b.x, y2: b.y, "stroke-width": Math.min(4.5, 0.8 + Math.sqrt(damage) / 7) * px, opacity: (dim ? 0.15 : 0.9) * fade }, gDamage);
      }
    }
    if (layers.has("casts")) {
      for (const cast of data.casts) {
        if (cast.t > t || t - cast.t >= CAST_POP_S) continue;
        const a = states[cast.by];
        if (!a) continue;
        const targets = new Set([...(cast.target !== undefined ? [cast.target] : []), ...cast.hits.map(([h]) => h)]);
        for (const target of targets) {
          const b = states[target];
          if (!b || target === cast.by) continue;
          svg("line", { class: `cast-link cast-link--${heroes[cast.by].team}`, x1: a.x, y1: a.y, x2: b.x, y2: b.y, "stroke-width": 1.4 * px, "stroke-dasharray": `${4 * px} ${3 * px}`, opacity: 1 - (t - cast.t) / CAST_POP_S }, gLinks);
        }
      }
    }
    // A puff where a smoke breaks.
    if (layers.has("status")) {
      for (const [, , members] of data.smokes) {
        for (const [hero, , broke] of members) {
          const at = states[hero];
          if (broke === null || !at || broke > t || t - broke >= SMOKE_PUFF_S) continue;
          const k = (t - broke) / SMOKE_PUFF_S;
          svg("circle", { class: "smoke-puff", cx: at.x, cy: at.y, r: badge * (1.3 + 1.6 * k), "stroke-width": 2 * px, opacity: 1 - k }, gPops);
        }
      }
    }
    // A buyback pops where the hero died (it reappears at the fountain, off the map).
    if (layers.has("gold")) {
      for (const [b0, hero, cost] of data.buybacks) {
        if (b0 > t || t - b0 >= GOLD_POP_S) continue;
        const spot = deathMarks.filter((m) => m.death.victim === hero && !m.death.aegis && m.death.t <= b0 && m.spot).at(-1)?.spot;
        if (!spot) continue;
        const k = (t - b0) / GOLD_POP_S;
        const label = svg("text", { class: "gold-pop gold-pop--buyback", x: spot.x, y: spot.y - (20 + k * 16) * px, "text-anchor": "middle", "font-size": 11 * px, "stroke-width": 3 * px, opacity: 1 - k * k }, gPops);
        label.textContent = `↺ bought back · ${number(cost)}`;
      }
    }
    for (const mark of deathMarks) {
      const shown = mark.death.t <= t && mark.spot;
      mark.g.style.display = shown ? "" : "none";
      mark.g.classList.toggle("is-dim", follow !== null && follow !== mark.death.victim);
      if (!shown || !layers.has("gold") || t - mark.death.t >= GOLD_POP_S) continue;
      const k = (t - mark.death.t) / GOLD_POP_S;
      const rise = k * 16 * px;
      const pop = (x: number, y: number, text: string, cls: string, anchor = "middle") => {
        const el = svg("text", { class: `gold-pop ${cls}`, x, y: y - rise, "text-anchor": anchor, "font-size": 11 * px, "stroke-width": 3 * px, opacity: 1 - k * k }, gPops);
        el.textContent = text;
      };
      const spot = mark.spot!;
      if (mark.death.aegis) {
        pop(spot.x, spot.y - 14 * px, "Aegis", "gold-pop--gain");
        continue;
      }
      pop(spot.x, spot.y + 24 * px, `−${number(mark.death.gold_lost)}`, "gold-pop--loss");
      for (const [hero, gold] of mark.death.gold) {
        const at = states[hero];
        if (at) pop(at.x + 15 * px, at.y + 4 * px, `+${number(gold)}`, "gold-pop--gain", "start");
      }
    }

    for (const s of statusEls) {
      const state = states[s.i];
      s.box.classList.toggle("is-dead", !state);
      s.hpFill.style.width = state ? `${(100 * state.hp) / (state.maxHp || 1)}%` : "0%";
      s.manaFill.style.width = state ? `${(100 * state.mana) / (state.maxMana || 1)}%` : "0%";
      const disable = activeModifier(data, s.i, t, (m) => m[5] === "disable");
      const ring = activeModifier(data, s.i, t, (m) => m[6] !== null);
      s.text.textContent = !state
        ? "dead"
        : disable
          ? `${disable[4]} ${(disable[1] - t).toFixed(1)}s`
          : isSmoked(data, s.i, t)
            ? "Smoked"
            : ring
              ? (BUFF_LABELS[ring[6]!] ?? ring[4])
              : isHidden(data, s.i, t)
                ? "Hidden"
                : `${number(state.hp)} HP`;
    }

    let current: HTMLLIElement | undefined;
    for (const { row, li } of rowEls) {
      const past = row.t <= t;
      li.classList.toggle("is-past", past);
      if (past && !li.hidden) current = li;
    }
    for (const { li } of rowEls) li.classList.toggle("is-current", li === current);
    if (current && current !== lastCurrent) {
      // Keep the current row in view by scrolling the feed, not the page.
      feed.scrollTo({ top: current.offsetTop - feed.clientHeight / 2, behavior: playing ? "smooth" : "auto" });
      lastCurrent = current;
    }
    const x = (t / data.duration) * 1000;
    cursor.setAttribute("x1", String(x));
    cursor.setAttribute("x2", String(x));
    scrub.value = String(t);
    clock.value = clockAt(data.start_s, t);
  }

  // --- Playing ---
  function frame(now: number) {
    if (!playing) return;
    if (now < holdUntil) {
      requestAnimationFrame(frame);
      return;
    }
    if (holdUntil) {
      holdUntil = 0;
      t = 0;
    } else {
      t += ((now - (last || now)) / 1000) * speed;
    }
    last = now;
    if (t >= data.duration) {
      t = data.duration;
      holdUntil = now + HOLD_MS;
    }
    render();
    requestAnimationFrame(frame);
  }
  function play() {
    if (playing) return;
    if (t >= data.duration) t = 0;
    playing = true;
    last = 0;
    root.classList.add("is-live", "is-playing");
    button.setAttribute("aria-label", "Pause the fight");
    requestAnimationFrame(frame);
  }
  function pause() {
    playing = false;
    root.classList.remove("is-playing");
    button.setAttribute("aria-label", "Play the fight");
  }
  button.addEventListener("click", () => {
    pausedByReader = playing;
    if (playing) pause();
    else play();
  });
  scrub.addEventListener("input", () => {
    pausedByReader = true;
    pause();
    holdUntil = 0;
    t = Number(scrub.value);
    render();
  });

  root.classList.add("is-live");
  applyFilters();
  return {
    setVisible(visible: boolean) {
      if (visible && !pausedByReader) play();
      else if (!visible) pause();
    },
  };
}

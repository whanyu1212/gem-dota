/**
 * The fight player's markup that Figure 3 (FightFigure.astro) and the fights
 * recipe's panel share, with the `data-*` hooks fight-player.ts looks for. One
 * copy, so the two can't drift.
 */

/** Play/pause, the clock and the speed chips (filled in by the player). */
export function playbackControls(clock: string): string {
  return (
    `<div class="playback" data-playback hidden>` +
    `<button type="button" class="playback-button" data-play aria-label="Play the fight">` +
    `<svg class="icon-play" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l13-8z"></path></svg>` +
    `<svg class="icon-pause" width="14" height="14" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"></path></svg>` +
    `</button>` +
    `<output data-clock>${clock}</output>` +
    `<span class="playback-speeds" data-speeds></span>` +
    `</div>`
  );
}

/** The damage-per-second timeline and the scrubber under it. */
export function damageStrip(): string {
  return (
    `<div class="fight-strip" data-strip hidden>` +
    `<p class="strip-label">Damage per second` +
    `<span><i class="strip-key strip-key--radiant" aria-hidden="true"></i>Radiant above</span>` +
    `<span><i class="strip-key strip-key--dire" aria-hidden="true"></i>Dire below</span>` +
    `<span class="strip-hint">Drag, or click a ✕ or ↺, to pick a stretch</span>` +
    `</p>` +
    `<svg viewBox="0 0 1000 64" preserveAspectRatio="none" aria-hidden="true"></svg>` +
    `<input type="range" min="0" step="0.1" aria-label="Fight time" data-scrub>` +
    `</div>`
  );
}

const LEGEND: [string, string][] = [
  ["swatch-line swatch-line--physical", "Physical"],
  ["swatch-line swatch-line--magical", "Magical"],
  ["swatch-line swatch-line--pure", "Pure"],
  ["swatch-cast", "Cast, caster to target"],
  ["swatch-disable", "Disabled (the arc is the time left)"],
  ["swatch-ring swatch-ring--bkb", "Spell immune"],
  ["swatch-ring swatch-ring--hidden", "Hidden from the enemy"],
  ["swatch-smoke", "Smoked"],
];

/** The map's legend. */
export function fightLegend(): string {
  return (
    `<ul class="legend fight-legend" aria-label="Legend" data-legend hidden>` +
    LEGEND.map(([swatch, label]) => `<li class="legend-item"><i class="${swatch}" aria-hidden="true"></i>${label}</li>`).join("") +
    `</ul>`
  );
}

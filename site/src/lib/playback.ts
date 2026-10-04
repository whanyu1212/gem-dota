/**
 * The fight playback on the home page: where each hero is at a moment of the
 * fight, from its sampled path. Between samples (about one a second) the
 * position is interpolated, for display only.
 */
import type { Sample } from "./paths";

export interface HeroTrack {
  hero: string;
  team: string;
  /** Path segments in time order, each broken at a teleport or respawn. */
  runs: Sample[][];
  /** When the hero died, in seconds since the window started. */
  deaths: number[];
}

export function tracks(
  paths: { hero: string; team: string; points: number[][] }[],
  deaths: { hero: string; t: number }[],
): HeroTrack[] {
  const byHero = new Map<string, HeroTrack>();
  for (const path of paths) {
    const track = byHero.get(path.hero) ?? { hero: path.hero, team: path.team, runs: [], deaths: [] };
    track.runs.push(path.points as Sample[]);
    byHero.set(path.hero, track);
  }
  for (const death of deaths) byHero.get(death.hero)?.deaths.push(death.t);
  for (const track of byHero.values()) track.runs.sort((a, b) => a[0][2] - b[0][2]);
  return [...byHero.values()];
}

/** Whether the hero is dead at t: it died, and no path segment has started since. */
export function isDead(track: HeroTrack, t: number): boolean {
  const died = track.deaths.filter((d) => d <= t).at(-1);
  if (died === undefined) return false;
  return !track.runs.some((run) => run[0][2] > died && run[0][2] <= t);
}

/** The samples of a run up to t, ending exactly at t (interpolated). */
export function runUntil(run: Sample[], t: number): number[][] {
  if (!run.length || t < run[0][2]) return [];
  const out: number[][] = [];
  for (let i = 0; i < run.length; i++) {
    const p = run[i];
    if (p[2] <= t) {
      out.push(p);
      continue;
    }
    const q = run[i - 1];
    const k = (t - q[2]) / (p[2] - q[2] || 1);
    out.push([q[0] + (p[0] - q[0]) * k, q[1] + (p[1] - q[1]) * k, t]);
    break;
  }
  return out;
}

/** Where the hero is at t, or null when it is dead or has no sample around t. */
export function headAt(track: HeroTrack, t: number): number[] | null {
  if (isDead(track, t)) return null;
  const run = track.runs.find((r) => r[0][2] <= t && t <= r[r.length - 1][2]);
  return run ? runUntil(run, t).at(-1)! : null;
}

/** "42:34" plus t seconds, as "mm:ss" (a negative clock is not expected here). */
export function clockAt(start: string, t: number): string {
  const [m, s] = start.split(":").map(Number);
  const total = Math.max(0, Math.floor(m * 60 + s + t));
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

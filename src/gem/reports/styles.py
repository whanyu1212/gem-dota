"""CSS styles for the HTML match report."""

REPORT_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    background: #0d1117;
    color: #e6edf3;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 14px;
    padding: 16px;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

/* ---- Match header ---- */
.match-header {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    align-items: center;
}
.match-header h1 {
    font-size: 20px;
    font-weight: 700;
    flex: 1 1 100%;
}
.match-stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.match-stat .label {
    font-size: 11px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .05em;
}
.match-stat .value {
    font-size: 16px;
    font-weight: 600;
}

/* ---- Section cards ---- */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-bottom: 16px;
    overflow: hidden;
}

details > summary {
    list-style: none;
    cursor: pointer;
    padding: 14px 20px;
    font-weight: 600;
    font-size: 15px;
    border-bottom: 1px solid #30363d;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 8px;
}
details > summary::before {
    content: "\\25B6";
    font-size: 10px;
    transition: transform .15s;
    display: inline-block;
}
details[open] > summary::before {
    transform: rotate(90deg);
}
details > summary::-webkit-details-marker { display: none; }

.card-body {
    padding: 16px 20px;
    overflow-x: auto;
}

/* ---- Tables ---- */
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}
thead th {
    position: sticky;
    top: 0;
    background: #1c2128;
    color: #8b949e;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: .04em;
    padding: 8px 10px;
    text-align: left;
    white-space: nowrap;
}
thead th.r { text-align: right; }
tbody tr { border-top: 1px solid #21262d; }
tbody tr:hover { background: #1c2128; }
tbody td { padding: 7px 10px; white-space: nowrap; }
tbody td.r { text-align: right; font-variant-numeric: tabular-nums; }

.row-radiant { background: rgba(76,175,80,.07); }
.row-dire    { background: rgba(244,67,54,.07); }
.row-radiant:hover { background: rgba(76,175,80,.14) !important; }
.row-dire:hover    { background: rgba(244,67,54,.14) !important; }

/* ---- Dots / badges ---- */
.dot-obs { color: #ff9800; font-size: 16px; }
.dot-sen { color: #2196f3; font-size: 16px; }

/* ---- Draft section ---- */
.draft-sequence {
    display: flex; flex-wrap: wrap; gap: 6px;
    margin-bottom: 20px;
}
.draft-cell {
    display: flex; flex-direction: column; align-items: center;
    width: 72px; border-radius: 6px; overflow: hidden;
    border: 2px solid transparent; position: relative;
}
.draft-cell img { width: 72px; height: 42px; object-fit: cover; display: block; }
.draft-cell .dc-name {
    font-size: 0.6rem; font-weight: 600; text-align: center;
    padding: 2px 3px; width: 100%; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.draft-cell .dc-seq {
    position: absolute; top: 2px; left: 4px;
    font-size: 0.55rem; font-weight: 700; color: #fff;
    text-shadow: 0 0 3px #000;
}
.draft-cell .dc-type-badge {
    position: absolute; top: 2px; right: 4px;
    font-size: 0.48rem; font-weight: 800; letter-spacing: 0.04em;
    text-transform: uppercase; text-shadow: 0 0 3px #000;
}
.draft-cell.dc-ban-radiant .dc-type-badge { color: #4ade80; }
.draft-cell.dc-ban-dire    .dc-type-badge { color: #f87171; }
.draft-cell.dc-pick-radiant .dc-type-badge { color: #4ade80; }
.draft-cell.dc-pick-dire    .dc-type-badge { color: #f87171; }
.draft-cell .dc-time {
    font-size: 0.55rem; color: #484f58; font-family: monospace; padding-bottom: 3px;
}
/* Bans: greyscale image only — border/name keep team colour */
.draft-cell.dc-ban-radiant {
    background: #0e1610; border-color: #1e5c28;
}
.draft-cell.dc-ban-radiant img { filter: grayscale(100%) brightness(0.5); }
.draft-cell.dc-ban-radiant .dc-name { color: #4ade80; }
.draft-cell.dc-ban-dire {
    background: #160e0e; border-color: #5c1a1a;
}
.draft-cell.dc-ban-dire img { filter: grayscale(100%) brightness(0.5); }
.draft-cell.dc-ban-dire .dc-name { color: #f87171; }
/* ✕ overlay shared by both ban variants */
.draft-cell.dc-ban-radiant::after,
.draft-cell.dc-ban-dire::after {
    content: "✕";
    position: absolute; top: 0; left: 0; right: 0; bottom: 22px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 900; color: rgba(255,255,255,0.55);
    pointer-events: none;
}
.draft-cell.dc-pick-radiant {
    background: #111c18; border-color: #1a3a2a;
}
.draft-cell.dc-pick-radiant .dc-name { color: #4ade80; }
.draft-cell.dc-pick-dire {
    background: #1c1117; border-color: #3a1a1a;
}
.draft-cell.dc-pick-dire .dc-name { color: #f87171; }
.draft-team-row { margin-bottom: 14px; }
.draft-team-label {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em;
    margin-bottom: 6px; text-transform: uppercase;
}
.draft-team-label.radiant { color: #4caf50; }
.draft-team-label.dire    { color: #f44336; }
.draft-picks-row { display: flex; flex-wrap: wrap; gap: 8px; }
.draft-pick-card {
    display: flex; flex-direction: column; align-items: center;
    width: 88px; border-radius: 7px; overflow: hidden;
    border: 2px solid transparent;
}
.draft-pick-card img { width: 88px; height: 52px; object-fit: cover; display: block; }
.draft-pick-card .dp-name {
    font-size: 0.65rem; font-weight: 600; text-align: center;
    padding: 3px 4px 1px; width: 100%; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.draft-pick-card .dp-player {
    font-size: 0.6rem; color: #8b949e; text-align: center; padding-bottom: 2px;
}
.draft-pick-card .dp-time {
    font-size: 0.55rem; color: #484f58; font-family: monospace; padding-bottom: 4px;
}
.draft-pick-card.radiant { background: #111c18; border-color: #1a3a2a; }
.draft-pick-card.radiant .dp-name { color: #4ade80; }
.draft-pick-card.dire    { background: #1c1117; border-color: #3a1a1a; }
.draft-pick-card.dire    .dp-name { color: #f87171; }

/* ---- Inline damage bar ---- */
.dmg-bar-wrap { display: inline-block; width: 120px; height: 8px;
    background: #21262d; border-radius: 4px; vertical-align: middle; }
.dmg-bar-fill { height: 100%; border-radius: 4px; }

/* ---- Damage type mini bar ---- */
.dmg-type-mini {
    margin-top: 4px;
    width: 120px;
    height: 6px;
    background: #21262d;
    border-radius: 3px;
    overflow: hidden;
    display: inline-flex;
}
.dmg-type-seg { height: 100%; display: inline-block; }
.dmg-type-physical { background: #9aa4b2; }
.dmg-type-magical { background: #4ea1ff; }
.dmg-type-pure { background: #d946ef; }
.dmg-type-others { background: #4d5562; }

/* ---- Damage type legend ---- */
.dmg-legend {
    margin: 6px 0 0 0;
    font-size: 0.78em;
    color: #8b949e;
    display: flex;
    align-items: center;
    gap: 4px;
    flex-wrap: wrap;
}
.dmg-legend-swatch {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 2px;
    vertical-align: middle;
}
.dmg-legend-note {
    color: #555e6b;
    font-style: italic;
}

/* ---- Chart container ---- */
.chart-wrap {
    position: relative;
    height: 300px;
    padding: 8px 0;
}

/* ---- Sub-accordion (purchase per player) ---- */
.sub-accordion {
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-bottom: 8px;
    overflow: hidden;
}
.sub-accordion > summary {
    padding: 8px 14px;
    font-size: 13px;
    border-bottom: 1px solid #30363d;
}
.sub-accordion > summary::before {
    content: "\\25B6";
    font-size: 9px;
    display: inline-block;
    transition: transform .15s;
    margin-right: 6px;
}
details[open].sub-accordion > summary::before {
    transform: rotate(90deg);
}

/* ---- Laning tab ---- */
.lane-map-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 24px;
    margin-bottom: 16px;
    align-items: flex-start;
}
.lane-map-svg { flex-shrink: 0; }
.lane-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 14px;
    font-size: 12px;
    align-content: flex-start;
}
.lane-legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
}
.lane-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}
.lane-adv-pos { color: #4caf50; font-weight: 600; }
.lane-adv-neg { color: #f44336; font-weight: 600; }
.lane-adv-neu { color: #8b949e; }
.lane-eff-bar-wrap {
    display: inline-block; width: 80px; height: 6px;
    background: #21262d; border-radius: 3px; vertical-align: middle;
}
.lane-eff-bar-fill { height: 100%; border-radius: 3px; }

/* ---- Farming tab ---- */
.farm-select {
    background: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 6px 10px;
    min-width: 280px;
}
.farm-layout {
    display: block;
}
.farm-map-wrap { margin-bottom: 14px; }
.farm-map-shell {
    width: min(100%, 760px);
}
.farm-map-svg {
    display: block;
    width: 100%;
    height: auto;
    background: #0d1117;
}
.farm-toolbar {
    display: flex;
    gap: 12px;
    align-items: center;
    margin: 10px 0 12px 0;
    flex-wrap: wrap;
}
.farm-slider {
    flex: 1 1 420px;
    accent-color: #58a6ff;
}
.farm-play-btn {
    background: #1f6feb;
    color: #fff;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 6px 12px;
    cursor: pointer;
    font-weight: 600;
}
.farm-play-btn:hover {
    background: #388bfd;
}
.farm-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.farm-meta-chip {
    min-width: 140px;
    padding: 8px 10px;
    border: 1px solid #30363d;
    border-radius: 8px;
    background: #11161d;
}
.farm-meta-chip .label {
    display: block;
    font-size: 11px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .04em;
    margin-bottom: 4px;
}
.farm-meta-chip .value {
    display: block;
    font-weight: 600;
    color: #e6edf3;
    word-break: break-word;
}
.farm-table-wrap {
    overflow-x: auto;
    margin-top: 12px;
}
.farm-guide {
    margin: 12px 0 16px;
    padding: 12px;
    border: 1px solid #30363d;
    border-radius: 10px;
    background: #11161d;
}
.farm-guide-section + .farm-guide-section {
    margin-top: 12px;
}
.farm-guide-title {
    margin-bottom: 8px;
    color: #e6edf3;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
}
.farm-guide-table {
    width: 100%;
}
.farm-guide-table th,
.farm-guide-table td {
    vertical-align: top;
}
.farm-guide-table code {
    font-size: 11px;
    white-space: normal;
    word-break: break-word;
}
.farm-visit-row.farm-visit-active {
    background: rgba(88, 166, 255, 0.14) !important;
}
.farm-visit-row.farm-visit-active:hover {
    background: rgba(88, 166, 255, 0.2) !important;
}
.farm-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
    border: 1px solid transparent;
}
.farm-tag-safe {
    color: #4caf50;
    background: rgba(76, 175, 80, 0.12);
    border-color: rgba(76, 175, 80, 0.35);
}
.farm-tag-pressured {
    color: #ffb74d;
    background: rgba(255, 183, 77, 0.12);
    border-color: rgba(255, 183, 77, 0.35);
}
.farm-tag-defensive {
    color: #64b5f6;
    background: rgba(100, 181, 246, 0.12);
    border-color: rgba(100, 181, 246, 0.35);
}
.farm-tag-invade-safe {
    color: #f06292;
    background: rgba(240, 98, 146, 0.12);
    border-color: rgba(240, 98, 146, 0.35);
}
.farm-tag-invade-mid {
    color: #ef6c9a;
    background: rgba(239, 108, 154, 0.12);
    border-color: rgba(239, 108, 154, 0.35);
}
.farm-tag-invade-risk {
    color: #f06292;
    background: rgba(240, 98, 146, 0.2);
    border-color: rgba(240, 98, 146, 0.5);
}
@media (max-width: 980px) {
    .farm-map-wrap { min-width: 0; }
    .farm-toolbar { align-items: stretch; }
    .farm-play-btn { width: 100%; }
    .farm-select { min-width: 220px; width: 100%; }
    .farm-map-shell { width: 100%; }
    .farm-meta-chip { min-width: 0; flex: 1 1 160px; }
}

/* ---- Misc ---- */
.dim { color: #6e7681; font-style: italic; }
.radiant { color: #4caf50; }
.dire    { color: #f44336; }
.section-note { color: #8b949e; font-size: 12px; margin-top: 8px; }

/* ---- Teamfights ---- */
.tf-summary {
    margin-bottom: 10px;
    color: #8b949e;
    font-size: 12px;
}
.tf-filter-bar {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
    margin-bottom: 14px;
    padding: 10px 12px;
    border: 1px solid #30363d;
    border-radius: 6px;
    background: #11161d;
}
.tf-filter-group { min-width: 220px; }
.tf-filter-label {
    font-size: 12px;
    color: #8b949e;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    font-weight: 600;
}
.tf-filter-group input[type="range"] { width: 100%; accent-color: #58a6ff; }

.tf-fight-card {
    background: #11161d;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-bottom: 14px;
    overflow: hidden;
}
.tf-fight-card.hidden { display: none; }
.tf-fight-header {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    padding: 10px 12px;
    border-bottom: 1px solid #30363d;
    background: #161b22;
}
.tf-fight-index {
    color: #58a6ff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .05em;
    text-transform: uppercase;
}
.tf-fight-time {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 12px;
    color: #e6edf3;
}
.tf-fight-meta {
    margin-left: auto;
    color: #8b949e;
    font-size: 12px;
}
.tf-fight-body { display: flex; gap: 0; }
.tf-fight-map {
    padding: 10px;
    border-right: 1px solid #30363d;
    flex-shrink: 0;
}
.tf-fight-right { flex: 1; min-width: 0; }

.tf-participants {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    padding: 10px 12px;
    border-bottom: 1px solid #30363d;
}
.tf-participant {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 62px;
    gap: 3px;
}
.tf-participant img {
    width: 62px;
    height: 36px;
    object-fit: cover;
    border-radius: 4px;
    border: 2px solid transparent;
}
.tf-participant.radiant img { border-color: #4caf50; }
.tf-participant.dire img { border-color: #f44336; }
.tf-participant.died img { box-shadow: 0 0 0 2px #ffffff; }
.tf-participant-hero {
    font-size: 10px;
    font-weight: 600;
    text-align: center;
    width: 62px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.tf-participant-player {
    font-size: 10px;
    color: #8b949e;
    text-align: center;
    width: 62px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.tf-table-wrap { padding: 10px 12px 12px; overflow-x: auto; }
.tf-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.tf-table th, .tf-table td { padding: 6px 8px; white-space: nowrap; }
.tf-table thead th {
    color: #8b949e;
    text-transform: uppercase;
    font-size: 10px;
    letter-spacing: .04em;
    border-bottom: 1px solid #30363d;
}
.tf-table tbody td { border-top: 1px solid #21262d; }
.tf-table .r { text-align: right; font-variant-numeric: tabular-nums; }

.tf-log-expander {
    border-top: 1px solid #30363d;
    padding: 0 12px;
}
.tf-log-expander > summary {
    padding: 8px 0;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: #8b949e;
    cursor: pointer;
    user-select: none;
    list-style: none;
}
.tf-log-expander > summary::before {
    content: "▶ ";
    font-size: 9px;
}
.tf-log-expander[open] > summary::before { content: "▼ "; }
.tf-log-body {
    padding: 6px 0 12px;
    display: flex;
    flex-direction: column;
    gap: 3px;
    max-height: 320px;
    overflow-y: auto;
}
.tf-log-line {
    display: flex;
    gap: 10px;
    align-items: baseline;
    font-size: 12px;
    color: #c9d1d9;
    padding: 2px 0;
    border-bottom: 1px solid #21262d;
}
.tf-log-time {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 11px;
    color: #8b949e;
    flex-shrink: 0;
    min-width: 38px;
}
.tf-log-text { flex: 1; }

/* ---- Tab navigation ---- */
.tab-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 2px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 6px 8px;
    margin-bottom: 16px;
}
.tab-bar input[type="radio"] { display: none; }
.tab-bar label {
    padding: 7px 16px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    color: #8b949e;
    cursor: pointer;
    user-select: none;
    transition: background .15s, color .15s;
    white-space: nowrap;
}
.tab-bar label:hover { color: #e6edf3; background: #21262d; }
.tab-bar input[type="radio"]:checked + label {
    background: #21262d;
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}
.tab-page { display: none; }
.tab-page.active { display: block; }

/* ---- Roshan conversion ---- */
.rosh-card-grid {
    display: grid;
    gap: 14px;
}
.rosh-card {
    border: 1px solid #30363d;
    border-radius: 8px;
    background: #0f141b;
    padding: 14px;
}
.rosh-card-head {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}
.rosh-kicker {
    color: #8b949e;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .05em;
    margin-bottom: 4px;
}
.rosh-title {
    font-size: 18px;
    font-weight: 700;
}
.rosh-meta {
    margin-top: 4px;
    color: #8b949e;
    font-size: 12px;
}
.rosh-head-right {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
}
.rosh-badge {
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .04em;
    border: 1px solid #30363d;
}
.rosh-badge-empty_rosh { background: #1b1f24; color: #c9d1d9; }
.rosh-badge-low_conversion { background: #1b1f24; color: #c9d1d9; }
.rosh-badge-fight_conversion { background: rgba(76, 175, 80, .14); color: #7ee787; }
.rosh-badge-objective_conversion { background: rgba(255, 183, 77, .14); color: #ffb74d; }
.rosh-badge-map_squeeze { background: rgba(56, 139, 253, .14); color: #79c0ff; }
.rosh-badge-game_closing_rosh { background: rgba(201, 209, 217, .14); color: #e6edf3; }
.rosh-outcome-badge {
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid #30363d;
}
.rosh-outcome-consumed_in_fight { background: rgba(76, 175, 80, .14); color: #7ee787; }
.rosh-outcome-expired_after_use { background: rgba(255, 183, 77, .14); color: #ffb74d; }
.rosh-outcome-expired_unused { background: rgba(139, 148, 158, .16); color: #c9d1d9; }
.rosh-outcome-denied { background: rgba(244, 67, 54, .14); color: #ff7b72; }
.rosh-outcome-window_lost { background: rgba(244, 67, 54, .18); color: #ffa198; }
.rosh-outcome-game_ended { background: rgba(121, 192, 255, .14); color: #79c0ff; }
.rosh-outcome-unknown { background: rgba(139, 148, 158, .16); color: #c9d1d9; }
.rosh-guide-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 14px;
    margin-bottom: 14px;
}
.rosh-guide-block {
    border: 1px solid #30363d;
    border-radius: 8px;
    background: #0f141b;
    padding: 12px;
}
.rosh-guide-title {
    font-size: 12px;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .06em;
    margin-bottom: 10px;
}
.rosh-guide-table td, .rosh-guide-table th {
    vertical-align: top;
}
.rosh-metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
    gap: 10px;
    margin-bottom: 12px;
}
.rosh-metric {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 10px 12px;
}
.rosh-metric .label {
    display: block;
    color: #8b949e;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .04em;
    margin-bottom: 4px;
}
.rosh-metric .value {
    font-size: 15px;
    font-weight: 700;
}
.rosh-timeline {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
}
.rosh-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 9px;
    border-radius: 999px;
    border: 1px solid #30363d;
    font-size: 12px;
    background: #161b22;
}
.rosh-chip-time {
    color: #8b949e;
    font-variant-numeric: tabular-nums;
}
.rosh-chip-roshan { background: rgba(255, 183, 77, .14); }
.rosh-chip-aegis_pickup { background: rgba(201, 209, 217, .12); }
.rosh-chip-aegis_denied { background: rgba(244, 67, 54, .12); }
.rosh-chip-fight_win { background: rgba(76, 175, 80, .14); }
.rosh-chip-fight_loss { background: rgba(244, 67, 54, .14); }
.rosh-chip-fight_draw { background: rgba(121, 192, 255, .12); }
.rosh-chip-tower, .rosh-chip-barracks { background: rgba(56, 139, 253, .14); }
.rosh-chip-buyback { background: rgba(188, 140, 255, .12); }
.rosh-chip-aegis_end, .rosh-chip-game_end { background: rgba(139, 148, 158, .16); }
.rosh-driver-list {
    margin-left: 18px;
    color: #c9d1d9;
}
.rosh-driver-list li + li {
    margin-top: 4px;
}
.rosh-table-wrap {
    margin-top: 14px;
    overflow-x: auto;
}
"""

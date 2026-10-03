# Match Reports

gem can generate self-contained HTML reports from real `.dem` replay files.

The report shows facts from the replay. It leaves interpretation, such as
whether a Roshan "converted" or a farming pattern was safe, to you.

The `Farming` tab shows the camp-by-camp route of each team's cores. For each
team and lane role (safe lane → carry, mid → mid, off lane → offlaner), the
core is the player with the most last hits at 10:00. Each camp visit lists its
duration, the hero's neutral kills inside the camp zone, and the gold and XP the
hero earned during the visit. The route builder is documented in
[Experimental Features → Farming Patterns](../experimental/farming-patterns.md).

The `Roshan` tab lists each Roshan kill: who killed it, what it dropped, who
picked up the Aegis, and when and how the Aegis ended. While the Aegis was held
it also lists the fights that overlapped the hold and the enemy towers and
barracks the holder's team destroyed (denies excluded). A consumed Aegis that the replay infers from the holder's
death is marked `*`.

The `Fights` tab includes one positioning map per fight with pre-engagement,
engagement-start, first-death, and fight-end controls. Marker visibility,
position freshness, missing samples, and the current conservative
engagement-start fallback are documented in
[Experimental Features → Fight Positioning](../experimental/fight-positioning.md).
A fight card is badged "after Smoke #N" when it was that smoke's first fight,
and "during Aegis #N" when it overlapped an Aegis hold.

The **Smoke Operations** view in the `Vision` tab lists each smoke's time, team
and members, when it broke (the first member to lose it early, and how many
in-game seconds after activation), and its first fight: the first fight whose
first death came within 60 in-game seconds (pauses excluded). See
[Experimental Features → Smoke Analysis](../experimental/smoke-analysis.md).

The report embeds the map image at up to 4096 px wide. A wider image is
downscaled when the report is written; the file on disk is not changed.

## Hosted samples

Sample reports are not bundled into this VitePress site. They are large,
self-contained HTML artifacts and should be hosted separately from the docs.

To generate your own report:

```bash
python examples/match_report.py path/to/replay.dem --output ./my_match_report.html
```

Hero and item icons are Valve's artwork, so gem does not ship them. The script
downloads the icons the match needs into the report asset cache before rendering
(`--offline` skips this). From Python, call `gem.reports.fetch_match_icons(match)`
before `write_html_report`; any icon still missing is shown as a name, and the
report logs a warning listing them.

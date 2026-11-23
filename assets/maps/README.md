# Report map assets

`Game_map_7.41.jpg` is the default source-checkout background for map-backed
HTML report sections.

- Source page: <https://liquipedia.net/dota2/File:Game_map_7.41.jpg>
- Original file: `8,909 × 8,424`, SHA-256
  `84e6b8bd0f8a06548e45dbed94fb734ee280f3465bafef908f27889ccdd4d0b2`
- Repository export: `8,878 × 8,356`, JPEG quality 69, 4:2:0 sampling,
  SHA-256 `9fb56fc131acc161fb904f6c7189c6f37c57705bac752ccf9a47e01b1b079764`
- Transformation: exact Lanczos resample to the previous report-map canvas;
  no generative editing, relabeling, or content reconstruction
- Retrieved: 2026-09-22

The source file is © Valve Corporation, all rights reserved. Liquipedia's file
page records Valve's permission for Liquipedia's use and provides the source
licensing notice.

`Game_map_7.42.jpg` is the patch 7.42 map, for drawing 7.42 replays (for example
`scripts/render_camp_zones_overlay.py --patch 7.42`).

- Source: a full-map render shared on Reddit,
  <https://i.redd.it/ku78nii8ru2i1.jpeg>; same render style and framing as the
  7.41 original, at 1.5 times its size
- Original file: `13,364 × 12,634`, SHA-256
  `cca1fb8bcae1bfaa8f105756d3378823afd1eff3d42026195f2c40a03825eb16`
- Repository export: `2,400 × 2,259`, JPEG quality 80, 4:2:0 sampling, 1.3 MB,
  SHA-256 `cbc9590038d44ccb024f20dae10be198750e12b4fd8264aa208835947273d698`
- Transformation: Lanczos resample onto the 7.41 export's `8,878 × 8,356` canvas,
  then down to 2,400 pixels wide (the height rounds the canvas's aspect ratio by
  0.11 px); no other editing. On that canvas it registers against the 7.41
  export at scale 1.000 and offset (0, 0), so `gem.catalog.map`'s calibration
  applies to it as it is. 7.42 landmarks (the moved Dire fountain, mid towers,
  Twin Gates and the four moved camps) land on their structures.
- Retrieved: 2026-11-23

The map render is © Valve Corporation, all rights reserved.

`game_map_7.40_camp_annotated.jpg` and `camp_annotated.png` are legacy derived
camp-annotation assets and are not the default report background.

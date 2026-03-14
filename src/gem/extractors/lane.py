"""Lane role classification from a 10-minute position heatmap.

Classifies a player's lane role (safe, mid, off, jungle, roaming) by
aggregating their ``lane_pos`` heatmap into coarse lane zones and finding
the dominant zone.  This matches OpenDota's approach: each grid cell is
mapped to one of five zones; the hero is classified by whichever zone
accumulates the most dwell ticks; if the dominant zone covers less than
``_ZONE_DOMINANCE_FRAC`` of total ticks the hero is classified as roaming.

The coordinate system and map bounds are calibrated against Game_map_7.40.jpg:
  - Radiant fountain: (9684, 9684) — bottom-left
  - Dire fountain: (23120, 22350) — top-right
  - Map X range: 7563–25900, Y range: 7800–25600

No reference implementation exists in refs/; OpenDota performs lane
classification server-side as a post-processing step on the lane_pos heatmap.
"""

from __future__ import annotations

# Grid cell size must match match_builder._LANE_GRID
_GRID = 64
_HALF_GRID = _GRID // 2

# ---------------------------------------------------------------------------
# Zone boundary constants (world units)
# ---------------------------------------------------------------------------

# Mid lane: the diagonal corridor where Y ≈ X
_MID_BAND = 2000  # max |wx - wy| to be considered mid
_MID_X_MIN = 10500
_MID_X_MAX = 22000

# Radiant safe lane: bottom strip and bottom-right corner
_SAFE_R_Y_MAX = 12500  # below this Y is always safe-lane territory
_SAFE_R_X_MIN = 20000  # far right, even if Y is higher
_SAFE_R_Y_MID = 16000  # upper bound for the far-right safe check

# Radiant off lane: top-left corner
_OFF_R_X_MAX = 12500  # left of this X
_OFF_R_Y_MIN = 19000  # above this Y

# Roaming threshold: if the dominant zone covers less than this fraction
# of all dwell ticks, the hero is classified as roaming.
_ZONE_DOMINANCE_FRAC = 0.45


# Zone label constants used internally
_ZONE_MID = "mid"
_ZONE_SAFE_R = "safe_r"  # Radiant safe / Dire off
_ZONE_OFF_R = "off_r"  # Radiant off / Dire safe
_ZONE_JUNGLE = "jungle"
_ZONE_OTHER = "other"


def _cell_zone(wx: float, wy: float) -> str:
    """Map a world-coordinate position to a coarse lane zone label.

    Args:
        wx: World X coordinate (centre of a 64-unit grid cell).
        wy: World Y coordinate (centre of a 64-unit grid cell).

    Returns:
        One of ``"mid"``, ``"safe_r"``, ``"off_r"``, ``"jungle"``,
        or ``"other"``.
    """
    if abs(wx - wy) < _MID_BAND and _MID_X_MIN < wx < _MID_X_MAX:
        return _ZONE_MID

    is_safe_r = (wy < _SAFE_R_Y_MAX) or (wx > _SAFE_R_X_MIN and wy < _SAFE_R_Y_MID)
    is_off_r = (wx < _OFF_R_X_MAX) and (wy > _OFF_R_Y_MIN)

    if is_safe_r:
        return _ZONE_SAFE_R
    if is_off_r:
        return _ZONE_OFF_R
    if _OFF_R_X_MAX <= wx <= _SAFE_R_X_MIN and _SAFE_R_Y_MAX <= wy <= _OFF_R_Y_MIN:
        return _ZONE_JUNGLE

    return _ZONE_OTHER


def _zone_counts(lane_pos: dict[str, int]) -> dict[str, int]:
    """Aggregate cell dwell counts into coarse lane zones.

    Args:
        lane_pos: Dwell-tick counts keyed by ``"gx_gy"`` grid cell strings.

    Returns:
        Dict mapping zone label → total dwell ticks in that zone.
    """
    counts: dict[str, int] = {}
    for key, count in lane_pos.items():
        gx_s, gy_s = key.split("_", 1)
        wx = int(gx_s) * _GRID + _HALF_GRID
        wy = int(gy_s) * _GRID + _HALF_GRID
        zone = _cell_zone(wx, wy)
        counts[zone] = counts.get(zone, 0) + count
    return counts


def _centroid(lane_pos: dict[str, int]) -> tuple[float, float] | None:
    """Compute the dwell-weighted world-coordinate centroid of lane_pos.

    Args:
        lane_pos: Dwell-tick counts keyed by ``"gx_gy"`` grid cell strings.

    Returns:
        ``(wx, wy)`` weighted centroid in world units, or ``None`` if empty.
    """
    total = 0
    wx_sum = 0.0
    wy_sum = 0.0
    for key, count in lane_pos.items():
        gx_s, gy_s = key.split("_", 1)
        wx = int(gx_s) * _GRID + _HALF_GRID
        wy = int(gy_s) * _GRID + _HALF_GRID
        wx_sum += wx * count
        wy_sum += wy * count
        total += count
    if total == 0:
        return None
    return wx_sum / total, wy_sum / total


def classify_lane(lane_pos: dict[str, int], team: int) -> int:
    """Classify a player's lane role from their 10-minute position heatmap.

    Aggregates the ``lane_pos`` heatmap into coarse lane zones and finds the
    dominant zone.  If the dominant zone covers less than
    ``_ZONE_DOMINANCE_FRAC`` (45 %) of total dwell ticks the hero is
    classified as roaming (role 5).

    Lane roles mirror OpenDota's convention:
      1 = safe lane, 2 = mid, 3 = off lane, 4 = jungle, 5 = roaming, 0 = unknown.

    The Dire safe lane is the Radiant off-lane side (top-left) and vice versa.

    Args:
        lane_pos: Dwell-tick counts keyed by ``"gx_gy"`` (64-unit grid cells),
            restricted to the first 10 game-minutes.
        team: Team number (2=Radiant, 3=Dire).

    Returns:
        Lane role integer: 1=safe, 2=mid, 3=off, 4=jungle, 5=roaming, 0=unknown.
    """
    if not lane_pos:
        return 0

    zones = _zone_counts(lane_pos)
    total = sum(zones.values())
    if total == 0:
        return 0

    dominant_zone = max(zones, key=lambda z: zones[z])
    dominant_count = zones[dominant_zone]

    # Roaming: no single lane zone accounts for enough of the hero's time
    if dominant_count / total < _ZONE_DOMINANCE_FRAC:
        return 5

    # Map dominant zone to role number (team-dependent for safe/off)
    if dominant_zone == _ZONE_MID:
        return 2

    if team == 2:  # Radiant
        if dominant_zone == _ZONE_SAFE_R:
            return 1
        if dominant_zone == _ZONE_OFF_R:
            return 3
    else:  # Dire: zones are mirrored
        if dominant_zone == _ZONE_OFF_R:
            return 1
        if dominant_zone == _ZONE_SAFE_R:
            return 3

    if dominant_zone == _ZONE_JUNGLE:
        return 4

    return 0

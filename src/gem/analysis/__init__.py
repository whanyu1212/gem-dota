"""Post-parse analysis helpers for gem replay data."""

from gem._deprecation import renamed_module_attrs
from gem.analysis.abilities import ability_level_at_tick
from gem.analysis.bundle import MatchAnalysis, analyze
from gem.analysis.combat import (
    AbilityCast,
    fight_at_tick,
    find_fights,
    group_ability_hits,
    is_active_fight_participant,
)
from gem.analysis.farming import (
    DEFAULT_FARMING_ROUTE_CONFIG,
    FarmingBoundaryReason,
    FarmingCampZone,
    FarmingEvidenceStrength,
    FarmingRoute,
    FarmingRouteConfig,
    FarmingRoutePoint,
    FarmingRouteSegment,
    build_farming_routes,
)
from gem.analysis.fight_positioning import (
    EngagementStartSource,
    EvidenceCompleteness,
    FightPositioning,
    FightPositionSnapshot,
    HeroPositionEvidence,
    SnapshotKind,
    TeamPositionSummary,
    build_fight_positioning,
)
from gem.analysis.formatting import format_npc_name
from gem.analysis.regions import MAP_REGIONS, region_of
from gem.analysis.roshan import (
    AegisFateSource,
    RoshConversion,
    RoshDifferentialProfile,
    RoshFightEvidence,
    RoshFightRelation,
    RoshTeamAttributionSource,
    RoshTimelineEvent,
    build_rosh_conversions,
)
from gem.analysis.smoke import (
    SmokeAnalysis,
    SmokeGroupStatus,
    SmokeLifecycleStatus,
    SmokeMemberAnalysis,
    build_smoke_analysis,
)
from gem.analysis.spatial import (
    SampledPosition,
    heroes_near,
    net_worth_at,
    position_at_tick,
    position_sample_at_tick,
)
from gem.analysis.vision import (
    DirectTargetRevealEvidence,
    PointVisionAssessment,
    PointVisionGap,
    PointVisionSource,
    PointVisionStatus,
    VisionSource,
    _is_daytime,
    assess_point_vision,
    entity_visibility_at,
    hero_visibility_at,
    is_daytime,
    ward_vision_impact,
)

__all__ = [
    "MAP_REGIONS",
    "AbilityCast",
    "AegisFateSource",
    "DEFAULT_FARMING_ROUTE_CONFIG",
    "DirectTargetRevealEvidence",
    "EngagementStartSource",
    "EvidenceCompleteness",
    "FightPositionSnapshot",
    "FarmingBoundaryReason",
    "FarmingCampZone",
    "FarmingEvidenceStrength",
    "FarmingRoute",
    "FarmingRouteConfig",
    "FarmingRoutePoint",
    "FarmingRouteSegment",
    "HeroPositionEvidence",
    "PointVisionAssessment",
    "PointVisionGap",
    "PointVisionSource",
    "PointVisionStatus",
    "RoshConversion",
    "RoshDifferentialProfile",
    "RoshFightEvidence",
    "RoshFightRelation",
    "RoshTeamAttributionSource",
    "RoshTimelineEvent",
    "SmokeAnalysis",
    "SmokeGroupStatus",
    "SmokeLifecycleStatus",
    "SmokeMemberAnalysis",
    "SnapshotKind",
    "TeamPositionSummary",
    "FightPositioning",
    "SampledPosition",
    "VisionSource",
    "_is_daytime",
    "ability_level_at_tick",
    "assess_point_vision",
    "build_farming_routes",
    "build_rosh_conversions",
    "build_smoke_analysis",
    "build_fight_positioning",
    "MatchAnalysis",
    "analyze",
    "entity_visibility_at",
    "hero_visibility_at",
    "format_npc_name",
    "group_ability_hits",
    "heroes_near",
    "is_active_fight_participant",
    "is_daytime",
    "net_worth_at",
    "position_at_tick",
    "position_sample_at_tick",
    "region_of",
    "fight_at_tick",
    "find_fights",
    "ward_vision_impact",
]

#: Names gem 0.10 and earlier used for gem's own fights.
RENAMED_FIGHT_NAMES = {
    "TeamfightPositioning": "FightPositioning",
    "build_teamfight_positioning": "build_fight_positioning",
    "is_active_teamfight_participant": "is_active_fight_participant",
    "teamfight_at_tick": "fight_at_tick",
}

__getattr__ = renamed_module_attrs(__name__, RENAMED_FIGHT_NAMES, globals())

"""Post-parse analysis helpers for gem replay data."""

from gem._deprecation import deprecated, deprecated_module_attrs, renamed_module_attrs
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
    DEFAULT_FARMING_CONTEXT_CONFIG as _DEFAULT_FARMING_CONTEXT_CONFIG,
    DEFAULT_FARMING_ROUTE_CONFIG,
    FarmingBoundaryReason,
    FarmingCampZone,
    FarmingContextConfig as _FarmingContextConfig,
    FarmingContextTag as _FarmingContextTag,
    FarmingEvidenceStrength,
    FarmingRoute,
    FarmingRouteConfig,
    FarmingRoutePoint,
    FarmingRouteSegment,
    FarmingSegmentContext as _FarmingSegmentContext,
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
from gem.analysis.map_context import (
    CampVisitContext as _CampVisitContext,
    MapContextBucket as _MapContextBucket,
    build_map_context_timeline as _build_map_context_timeline,
    score_camp_visit_context as _score_camp_visit_context,
    world_in_bounds as _world_in_bounds,
)
from gem.analysis.regions import MAP_REGIONS, region_of
from gem.analysis.roshan import (
    DEFAULT_ROSH_TAG_THRESHOLDS as _DEFAULT_ROSH_TAG_THRESHOLDS,
    AegisFateSource,
    RoshConversion,
    RoshCoverageCell as _RoshCoverageCell,
    RoshDifferentialProfile,
    RoshFightEvidence,
    RoshFightRelation,
    RoshTagThresholds as _RoshTagThresholds,
    RoshTeamAttributionSource,
    RoshTerritoryConfig as _RoshTerritoryConfig,
    RoshTerritoryWindow as _RoshTerritoryWindow,
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
from gem.analysis.smoke_fight import (
    ExactEventEvidence as _ExactEventEvidence,
    ExactEventKind as _ExactEventKind,
    FightCentroidSource as _FightCentroidSource,
    FightOutcome as _FightOutcome,
    FollowUpBoundary as _FollowUpBoundary,
    FollowUpEvent as _FollowUpEvent,
    FollowUpKind as _FollowUpKind,
    FollowUpWindow as _FollowUpWindow,
    FormationEvidence as _FormationEvidence,
    MemberPositionEvidence as _MemberPositionEvidence,
    SampledNearFightEvidence as _SampledNearFightEvidence,
    SmokeFightInsight as _SmokeFightInsight,
    SmokeFightMemberInsight as _SmokeFightMemberInsight,
    SmokeFightStatus as _SmokeFightStatus,
    TeamRelation as _TeamRelation,
    build_smoke_fight_insights as _build_smoke_fight_insights,
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
    estimate_vision as _estimate_vision,
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

_FARMING_CONTEXT_ALTERNATIVE = (
    "FarmingRouteSegment's camp facts and gem's position, ward, tower and economy data"
)
_SMOKE_FIGHT_ALTERNATIVE = "SmokeAnalysis.first_fight from gem.build_smoke_analysis"
_MAP_CONTEXT_ALTERNATIVE = "gem.region_of and the match's wards, towers and position data"
_ROSH_TAG_ALTERNATIVE = "RoshConversion.differential_profile's raw counts and swings"
_ROSH_TERRITORY_ALTERNATIVE = "gem.region_of with the players' position_log"

#: Names deprecated in 0.12 and removed in 0.13 (HY-96), served with a warning:
#: name -> (object, alternative, warn on access). Functions warn when called.
DEPRECATED_ANALYSIS_NAMES = {
    "CampVisitContext": (_CampVisitContext, None, True),
    "MapContextBucket": (_MapContextBucket, _MAP_CONTEXT_ALTERNATIVE, True),
    "build_map_context_timeline": (_build_map_context_timeline, None, False),
    "score_camp_visit_context": (_score_camp_visit_context, None, False),
    "world_in_bounds": (_world_in_bounds, None, False),
    "estimate_vision": (_estimate_vision, None, False),
    "FarmingSegmentContext": (_FarmingSegmentContext, _FARMING_CONTEXT_ALTERNATIVE, True),
    "FarmingContextTag": (_FarmingContextTag, _FARMING_CONTEXT_ALTERNATIVE, True),
    "FarmingContextConfig": (_FarmingContextConfig, _FARMING_CONTEXT_ALTERNATIVE, True),
    "DEFAULT_FARMING_CONTEXT_CONFIG": (
        _DEFAULT_FARMING_CONTEXT_CONFIG,
        _FARMING_CONTEXT_ALTERNATIVE,
        True,
    ),
    "build_smoke_fight_insights": (
        deprecated("gem.build_smoke_fight_insights", alternative=_SMOKE_FIGHT_ALTERNATIVE)(
            _build_smoke_fight_insights
        ),
        None,
        False,
    ),
    "SmokeFightInsight": (_SmokeFightInsight, _SMOKE_FIGHT_ALTERNATIVE, True),
    "SmokeFightMemberInsight": (_SmokeFightMemberInsight, _SMOKE_FIGHT_ALTERNATIVE, True),
    "SmokeFightStatus": (_SmokeFightStatus, _SMOKE_FIGHT_ALTERNATIVE, True),
    "ExactEventEvidence": (_ExactEventEvidence, _SMOKE_FIGHT_ALTERNATIVE, True),
    "ExactEventKind": (_ExactEventKind, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FightCentroidSource": (_FightCentroidSource, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FightOutcome": (_FightOutcome, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FollowUpBoundary": (_FollowUpBoundary, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FollowUpEvent": (_FollowUpEvent, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FollowUpKind": (_FollowUpKind, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FollowUpWindow": (_FollowUpWindow, _SMOKE_FIGHT_ALTERNATIVE, True),
    "FormationEvidence": (_FormationEvidence, _SMOKE_FIGHT_ALTERNATIVE, True),
    "MemberPositionEvidence": (_MemberPositionEvidence, _SMOKE_FIGHT_ALTERNATIVE, True),
    "SampledNearFightEvidence": (_SampledNearFightEvidence, _SMOKE_FIGHT_ALTERNATIVE, True),
    "TeamRelation": (_TeamRelation, _SMOKE_FIGHT_ALTERNATIVE, True),
    "RoshTagThresholds": (_RoshTagThresholds, _ROSH_TAG_ALTERNATIVE, True),
    "DEFAULT_ROSH_TAG_THRESHOLDS": (_DEFAULT_ROSH_TAG_THRESHOLDS, _ROSH_TAG_ALTERNATIVE, True),
    "RoshTerritoryConfig": (_RoshTerritoryConfig, _ROSH_TERRITORY_ALTERNATIVE, True),
    "RoshTerritoryWindow": (_RoshTerritoryWindow, _ROSH_TERRITORY_ALTERNATIVE, True),
    "RoshCoverageCell": (_RoshCoverageCell, _ROSH_TERRITORY_ALTERNATIVE, True),
}

__getattr__ = deprecated_module_attrs(
    __name__,
    DEPRECATED_ANALYSIS_NAMES,
    renamed_module_attrs(__name__, RENAMED_FIGHT_NAMES, globals()),
)

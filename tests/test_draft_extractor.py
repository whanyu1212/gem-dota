"""Unit tests for src/gem/extractors/draft.py.

Covers helper functions, DraftExtractor resolution logic, idempotency,
finalize behaviour, and DraftEvent construction.  No integration markers
needed — all tests use fake objects and bundled data only.
"""

from __future__ import annotations

from gem.extractors.draft import (
    _HERO_ID_TO_NPC,
    DraftEvent,
    DraftExtractor,
    _class_to_npc,
    _class_to_npc_names,
)

# ---------------------------------------------------------------------------
# Shared fake helpers
# ---------------------------------------------------------------------------


class FakeClass:
    def __init__(self, name: str) -> None:
        self.name = name
        self.class_id = 1
        self.serializer = None


def _make_entity(class_name: str, state: dict | None = None):
    from gem.entities import Entity

    e = Entity(index=0, serial=0, cls=FakeClass(class_name))
    if state:
        e._state.update(state)
    return e


# ---------------------------------------------------------------------------
# _class_to_npc_names
# ---------------------------------------------------------------------------


class TestClassToNpcNames:
    def test_simple_single_word(self):
        # CDOTA_Unit_Hero_Axe: ending="Axe"
        # name1 = "npc_dota_hero_" + "axe" = "npc_dota_hero_axe"
        # name2 = "npc_dota_hero" + re.sub([A-Z] → _\1, "Axe").lower()
        #       = "npc_dota_hero" + "_axe" = "npc_dota_hero_axe"
        n1, n2 = _class_to_npc_names("CDOTA_Unit_Hero_Axe")
        assert n1 == "npc_dota_hero_axe"
        assert n2 == "npc_dota_hero_axe"

    def test_underscore_separated(self):
        # Anti_Mage: name1 = "npc_dota_hero_anti_mage" (simple lowercase)
        # name2: camelCase fold on "Anti_Mage" → "_Anti__Mage" lower → "_anti__mage"
        #        "npc_dota_hero_anti__mage"
        n1, n2 = _class_to_npc_names("CDOTA_Unit_Hero_Anti_Mage")
        assert n1 == "npc_dota_hero_anti_mage"
        assert n2 == "npc_dota_hero_anti__mage"

    def test_camelcase_hero(self):
        # AntiMage: name1 = "npc_dota_hero_antimage" (simple lowercase)
        # name2: camelCase fold on "AntiMage" → "_Anti_Mage" lower → "_anti_mage"
        #        "npc_dota_hero_anti_mage"
        n1, n2 = _class_to_npc_names("CDOTA_Unit_Hero_AntiMage")
        assert n1 == "npc_dota_hero_antimage"
        assert n2 == "npc_dota_hero_anti_mage"

    def test_returns_two_strings(self):
        result = _class_to_npc_names("CDOTA_Unit_Hero_Sven")
        assert len(result) == 2
        assert all(isinstance(s, str) for s in result)

    def test_both_start_with_npc_prefix(self):
        n1, n2 = _class_to_npc_names("CDOTA_Unit_Hero_Lina")
        assert n1.startswith("npc_dota_hero_")
        assert n2.startswith("npc_dota_hero")


# ---------------------------------------------------------------------------
# _class_to_npc
# ---------------------------------------------------------------------------


class TestClassToNpc:
    def test_known_hero_axe(self):
        # Axe is in HEROES; simple lowercase form should match
        result = _class_to_npc("CDOTA_Unit_Hero_Axe")
        assert result == "npc_dota_hero_axe"

    def test_known_hero_antimage_underscore(self):
        # CDOTA_Unit_Hero_Anti_Mage — n1="npc_dota_hero_anti_mage" (not in HEROES),
        # n2="npc_dota_hero_anti__mage" (not in HEROES) → fallback to n1
        result = _class_to_npc("CDOTA_Unit_Hero_Anti_Mage")
        assert result == "npc_dota_hero_anti_mage"

    def test_known_hero_antimage_camelcase(self):
        # CDOTA_Unit_Hero_AntiMage — simple lowercase = "antimage" which IS in HEROES
        result = _class_to_npc("CDOTA_Unit_Hero_AntiMage")
        assert result == "npc_dota_hero_antimage"

    def test_unknown_hero_fallback_to_name1(self):
        # Verify the fallback is the simple lowercased form
        result = _class_to_npc("CDOTA_Unit_Hero_Nonexistent")
        assert result == "npc_dota_hero_nonexistent"

    def test_known_hero_pudge(self):
        result = _class_to_npc("CDOTA_Unit_Hero_Pudge")
        assert result == "npc_dota_hero_pudge"

    def test_known_hero_shadow_demon(self):
        # Shadow_Demon uses underscore form
        result = _class_to_npc("CDOTA_Unit_Hero_Shadow_Demon")
        assert result == "npc_dota_hero_shadow_demon"


# ---------------------------------------------------------------------------
# _HERO_ID_TO_NPC
# ---------------------------------------------------------------------------


class TestHeroIdToNpc:
    def test_non_empty(self):
        assert len(_HERO_ID_TO_NPC) > 100

    def test_all_values_are_npc_strings(self):
        for npc in _HERO_ID_TO_NPC.values():
            assert npc.startswith("npc_dota_hero_"), f"Bad NPC name: {npc!r}"

    def test_all_keys_are_ints(self):
        for k in _HERO_ID_TO_NPC:
            assert isinstance(k, int), f"Non-int key: {k!r}"

    def test_axe_id_2(self):
        assert _HERO_ID_TO_NPC[2] == "npc_dota_hero_axe"

    def test_pudge_id_14(self):
        assert _HERO_ID_TO_NPC[14] == "npc_dota_hero_pudge"

    def test_antimage_id_1(self):
        assert _HERO_ID_TO_NPC[1] == "npc_dota_hero_antimage"

    def test_riki_id_32(self):
        assert _HERO_ID_TO_NPC[32] == "npc_dota_hero_riki"


# ---------------------------------------------------------------------------
# DraftEvent dataclass
# ---------------------------------------------------------------------------


class TestDraftEvent:
    def test_construction_pick(self):
        ev = DraftEvent(
            tick=100, slot_index=0, hero_id=2, hero_name="npc_dota_hero_axe", is_pick=True
        )
        assert ev.tick == 100
        assert ev.slot_index == 0
        assert ev.hero_id == 2
        assert ev.hero_name == "npc_dota_hero_axe"
        assert ev.is_pick is True

    def test_construction_ban(self):
        ev = DraftEvent(
            tick=200, slot_index=3, hero_id=14, hero_name="npc_dota_hero_pudge", is_pick=False
        )
        assert ev.is_pick is False
        assert ev.slot_index == 3

    def test_hero_name_mutable(self):
        ev = DraftEvent(tick=0, slot_index=0, hero_id=0, hero_name="", is_pick=False)
        ev.hero_name = "npc_dota_hero_axe"
        assert ev.hero_name == "npc_dota_hero_axe"

    def test_empty_hero_name_allowed(self):
        ev = DraftEvent(tick=0, slot_index=0, hero_id=9999, hero_name="", is_pick=False)
        assert ev.hero_name == ""


# ---------------------------------------------------------------------------
# DraftExtractor._resolve_name
# ---------------------------------------------------------------------------


class TestResolveNameLiveMapHit:
    """Live map (tier 1) takes priority over all other lookups."""

    def test_live_map_returns_mapped_name(self):
        ext = DraftExtractor()
        ext._live_id_to_npc[42] = "npc_dota_hero_skeleton_king"
        assert ext._resolve_name(42) == "npc_dota_hero_skeleton_king"

    def test_live_map_overrides_static_dict(self):
        # hero_id 2 is axe in static dict, but live map overrides it
        ext = DraftExtractor()
        ext._live_id_to_npc[2] = "npc_dota_hero_pudge"
        result = ext._resolve_name(2)
        assert result == "npc_dota_hero_pudge"

    def test_live_map_used_for_doubled_id(self):
        # Doubled IDs (api_id * 2) are typically what live map contains
        ext = DraftExtractor()
        ext._live_id_to_npc[158] = "npc_dota_hero_shadow_demon"  # 79 * 2
        assert ext._resolve_name(158) == "npc_dota_hero_shadow_demon"


class TestResolveNameHalving:
    """Halved lookup (tier 2): applied when direct ID is NOT in static dict.

    heroes.json uses sequential IDs (1=antimage, 2=axe, ... 155=largo).
    Modern replays store hero IDs as api_id*2, which exceed 155 and therefore
    fall outside the static dict — those get resolved via halving.
    """

    def test_doubled_shadow_demon_resolves_via_halving(self):
        # shadow_demon api_id=79; stored as 158 in modern replays
        # 158 is NOT in dict (max id is 155), but 158//2=79 IS → shadow_demon
        ext = DraftExtractor()
        assert 158 not in _HERO_ID_TO_NPC
        assert 79 in _HERO_ID_TO_NPC
        assert ext._resolve_name(158) == "npc_dota_hero_shadow_demon"

    def test_doubled_lone_druid_resolves_via_halving(self):
        # lone_druid api_id=80; stored as 160 in modern replays
        ext = DraftExtractor()
        assert 160 not in _HERO_ID_TO_NPC
        assert 80 in _HERO_ID_TO_NPC
        assert ext._resolve_name(160) == "npc_dota_hero_lone_druid"

    def test_doubled_dawnbreaker_resolves_via_halving(self):
        # dawnbreaker api_id=135; stored as 270 in modern replays
        ext = DraftExtractor()
        assert 270 not in _HERO_ID_TO_NPC
        assert 135 in _HERO_ID_TO_NPC
        assert ext._resolve_name(270) == "npc_dota_hero_dawnbreaker"

    def test_halving_always_applied_first(self):
        # hero_id=2: 2//2=1 → antimage. halving always takes priority over direct lookup.
        ext = DraftExtractor()
        assert ext._resolve_name(2) == "npc_dota_hero_antimage"

    def test_halving_applied_for_pudge_doubled(self):
        # pudge api_id=14; stored as 28 in modern replays (14*2); 28//2=14 → pudge
        ext = DraftExtractor()
        assert ext._resolve_name(28) == "npc_dota_hero_pudge"

    def test_axe_doubled_id_resolves_via_halving(self):
        # axe api_id=2; stored as 4 in modern replays (2*2); 4//2=2 → axe
        ext = DraftExtractor()
        assert ext._resolve_name(4) == "npc_dota_hero_axe"


class TestResolveNameDirectLookup:
    """Direct lookup (tier 3): fires when hero_id//2 is not in the dict.

    Halving always runs first. Direct lookup only applies when the halved value
    has no entry — e.g. odd IDs where (id//2) resolves to a different hero or
    doesn't exist. In practice this tier is a safety net for legacy replays.
    """

    def test_antimage_id_1_halved_to_0_falls_back_to_direct(self):
        # 1//2=0, which is not in the dict → falls back to direct lookup of 1 → antimage
        ext = DraftExtractor()
        assert ext._resolve_name(1) == "npc_dota_hero_antimage"

    def test_axe_doubled_resolves_via_halving_not_direct(self):
        # Confirm axe is reached via halving (4//2=2 → axe), not direct lookup of 4
        ext = DraftExtractor()
        assert ext._resolve_name(4) == "npc_dota_hero_axe"

    def test_riki_doubled_resolves_via_halving(self):
        # riki api_id=32; stored as 64 in modern replays; 64//2=32 → riki
        ext = DraftExtractor()
        assert ext._resolve_name(64) == "npc_dota_hero_riki"


class TestResolveNameUnknown:
    """Unknown hero_id returns empty string."""

    def test_unknown_id_returns_empty(self):
        ext = DraftExtractor()
        assert ext._resolve_name(9999) == ""

    def test_zero_id_returns_empty(self):
        ext = DraftExtractor()
        assert ext._resolve_name(0) == ""

    def test_very_large_id_returns_empty(self):
        ext = DraftExtractor()
        assert ext._resolve_name(100000) == ""


# ---------------------------------------------------------------------------
# DraftExtractor.finalize
# ---------------------------------------------------------------------------


class TestFinalize:
    def test_finalize_updates_empty_hero_name(self):
        ext = DraftExtractor()
        # Add event with empty hero_name (hero_id=158 → shadow_demon when live map set)
        ev = DraftEvent(tick=0, slot_index=0, hero_id=158, hero_name="", is_pick=False)
        ext.draft_events.append(ev)
        ext._live_id_to_npc[158] = "npc_dota_hero_shadow_demon"
        ext.finalize()
        assert ev.hero_name == "npc_dota_hero_shadow_demon"

    def test_finalize_overwrites_wrong_static_lookup(self):
        # hero_id=158 was resolved via halving, but live map corrects it
        ext = DraftExtractor()
        ev = DraftEvent(
            tick=0, slot_index=0, hero_id=158, hero_name="npc_dota_hero_wrong", is_pick=True
        )
        ext.draft_events.append(ev)
        ext._live_id_to_npc[158] = "npc_dota_hero_shadow_demon"
        ext.finalize()
        assert ev.hero_name == "npc_dota_hero_shadow_demon"

    def test_finalize_does_not_clear_unresolvable_names(self):
        # If resolution returns "" (unknown), existing name should be kept
        ext = DraftExtractor()
        ev = DraftEvent(
            tick=0, slot_index=0, hero_id=9999, hero_name="npc_dota_hero_existing", is_pick=False
        )
        ext.draft_events.append(ev)
        # No live map entry for 9999; _resolve_name returns ""
        ext.finalize()
        # hero_name should be unchanged because resolved == "" is falsy
        assert ev.hero_name == "npc_dota_hero_existing"

    def test_finalize_on_empty_events_is_no_op(self):
        ext = DraftExtractor()
        ext.finalize()  # Should not raise
        assert ext.draft_events == []

    def test_finalize_updates_multiple_events(self):
        ext = DraftExtractor()
        ev1 = DraftEvent(tick=0, slot_index=0, hero_id=158, hero_name="", is_pick=False)
        ev2 = DraftEvent(tick=0, slot_index=1, hero_id=160, hero_name="", is_pick=False)
        ext.draft_events.extend([ev1, ev2])
        ext._live_id_to_npc[158] = "npc_dota_hero_shadow_demon"
        ext._live_id_to_npc[160] = "npc_dota_hero_lone_druid"
        ext.finalize()
        assert ev1.hero_name == "npc_dota_hero_shadow_demon"
        assert ev2.hero_name == "npc_dota_hero_lone_druid"

    def test_finalize_resolves_all_events_not_just_empty(self):
        # finalize re-resolves ALL events to let live map override wrong static ones
        ext = DraftExtractor()
        ev = DraftEvent(
            tick=0, slot_index=0, hero_id=158, hero_name="npc_dota_hero_shadow_demon", is_pick=True
        )
        ext.draft_events.append(ev)
        ext._live_id_to_npc[158] = "npc_dota_hero_pudge"  # live map says pudge (hypothetical)
        ext.finalize()
        # finalize must re-resolve even non-empty names so live map wins
        assert ev.hero_name == "npc_dota_hero_pudge"


# ---------------------------------------------------------------------------
# DraftExtractor._check_draft — idempotency via _seen set
# ---------------------------------------------------------------------------


class TestCheckDraftIdempotency:
    def test_same_ban_not_duplicated(self):
        ext = DraftExtractor()
        ext._parser = None  # tick=0

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 2},  # axe (direct id)
        )
        ext._check_draft(entity)
        ext._check_draft(entity)
        ext._check_draft(entity)

        bans = [e for e in ext.draft_events if not e.is_pick]
        assert len(bans) == 1

    def test_same_pick_not_duplicated(self):
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_SelectedHeroes.0000": 14},  # pudge (direct id)
        )
        ext._check_draft(entity)
        ext._check_draft(entity)

        picks = [e for e in ext.draft_events if e.is_pick]
        assert len(picks) == 1

    def test_different_slot_creates_separate_events(self):
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {
                "m_pGameRules.m_BannedHeroes.0000": 2,  # axe, slot 0
                "m_pGameRules.m_BannedHeroes.0001": 14,  # pudge, slot 1
            },
        )
        ext._check_draft(entity)

        bans = [e for e in ext.draft_events if not e.is_pick]
        assert len(bans) == 2
        slots = {b.slot_index for b in bans}
        assert slots == {0, 1}

    def test_zero_hero_id_skipped(self):
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 0},
        )
        ext._check_draft(entity)
        assert ext.draft_events == []

    def test_pick_and_ban_same_hero_id_distinct(self):
        # Same hero_id in both ban and pick slots should yield two events
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {
                "m_pGameRules.m_BannedHeroes.0000": 2,
                "m_pGameRules.m_SelectedHeroes.0000": 2,
            },
        )
        ext._check_draft(entity)
        assert len(ext.draft_events) == 2
        is_picks = {e.is_pick for e in ext.draft_events}
        assert is_picks == {True, False}

    def test_hero_name_resolved_on_ban(self):
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 4},  # axe doubled id (2*2) → axe via halving
        )
        ext._check_draft(entity)
        assert ext.draft_events[0].hero_name == "npc_dota_hero_axe"

    def test_hero_name_resolved_on_pick(self):
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {
                "m_pGameRules.m_SelectedHeroes.0000": 28
            },  # pudge doubled id (14*2) → pudge via halving
        )
        ext._check_draft(entity)
        assert ext.draft_events[0].hero_name == "npc_dota_hero_pudge"

    def test_hero_name_resolved_for_doubled_id(self):
        # hero_id=158 (shadow_demon=79*2): not in dict, halved to 79 → shadow_demon
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 158},
        )
        ext._check_draft(entity)
        assert ext.draft_events[0].hero_name == "npc_dota_hero_shadow_demon"

    def test_tick_recorded_from_parser(self):
        from gem.extractors.draft import DraftExtractor as DE

        class FakeParser:
            tick = 777
            entity_manager = None

            def on_entity(self, _):
                pass

        ext = DE()
        fp = FakeParser()
        ext.attach(fp)
        ext._parser = fp

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 2},
        )
        ext._check_draft(entity)
        assert ext.draft_events[0].tick == 777

    def test_tick_zero_when_parser_is_none(self):
        ext = DraftExtractor()
        ext._parser = None

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 2},
        )
        ext._check_draft(entity)
        assert ext.draft_events[0].tick == 0


# ---------------------------------------------------------------------------
# DraftExtractor entity dispatch via _on_entity
# ---------------------------------------------------------------------------


class TestOnEntity:
    def _make_parser(self):
        class FakeParser:
            def __init__(self) -> None:
                self.tick = 0
                self.entity_manager = None
                self._handlers: list = []

            def on_entity(self, h):
                self._handlers.append(h)

        return FakeParser()

    def test_non_grp_entity_ignored(self):
        from gem.entities import EntityOp

        ext = DraftExtractor()
        parser = self._make_parser()
        ext.attach(parser)

        entity = _make_entity("CDOTA_Unit_Hero_Axe", {"m_pGameRules.m_BannedHeroes.0000": 2})
        ext._on_entity(entity, EntityOp.CREATED)
        assert ext.draft_events == []

    def test_grp_entity_triggers_check(self):
        from gem.entities import EntityOp

        ext = DraftExtractor()
        parser = self._make_parser()
        ext.attach(parser)

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 2},
        )
        ext._on_entity(entity, EntityOp.UPDATED)
        assert len(ext.draft_events) == 1

    def test_grp_deleted_clears_grp_ref(self):
        from gem.entities import EntityOp

        ext = DraftExtractor()
        parser = self._make_parser()
        ext.attach(parser)

        entity = _make_entity("CDOTAGamerulesProxy")
        ext._on_entity(entity, EntityOp.CREATED)
        assert ext._grp is entity

        ext._on_entity(entity, EntityOp.DELETED)
        assert ext._grp is None

    def test_grp_deleted_does_not_check_draft(self):
        from gem.entities import EntityOp

        ext = DraftExtractor()
        parser = self._make_parser()
        ext.attach(parser)

        entity = _make_entity(
            "CDOTAGamerulesProxy",
            {"m_pGameRules.m_BannedHeroes.0000": 2},
        )
        ext._on_entity(entity, EntityOp.DELETED)
        # DELETED should not produce draft events
        assert ext.draft_events == []

    def test_cdota_player_resource_does_not_trigger_draft(self):
        from gem.entities import EntityOp

        ext = DraftExtractor()
        parser = self._make_parser()
        ext.attach(parser)

        entity = _make_entity(
            "CDOTA_PlayerResource",
            {"m_pGameRules.m_BannedHeroes.0000": 2},
        )
        ext._on_entity(entity, EntityOp.UPDATED)
        assert ext.draft_events == []

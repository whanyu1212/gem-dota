"""Tests for high-level gem.parse neutral-item event wiring."""

from __future__ import annotations

import gem.results.models as model_module


def test_parse_collects_neutral_item_found_events(monkeypatch):
    import gem
    import gem.combat.aggregator
    import gem.extractors.courier
    import gem.extractors.draft
    import gem.extractors.intervals
    import gem.extractors.objectives
    import gem.extractors.players
    import gem.extractors.wards
    import gem.parser
    import gem.results.assembly

    neutral_event_cls = getattr(model_module, "NeutralItemFoundEvent", None)
    assert neutral_event_cls is not None
    event = neutral_event_cls(
        tick=29858,
        player_id=6,
        item_ability_id=1861,
        item_key="stonefeather_satchel",
        enhancement_ability_id=1865,
        enhancement_key="enhancement_vital",
    )

    class FakeParser:
        def __init__(self, source):
            self.source = source
            self.neutral_item_found_callbacks = []

        def on_combat_log_entry(self, _handler):
            return None

        def on_chat_message(self, _handler):
            return None

        def on_neutral_item_found(self, handler):
            self.neutral_item_found_callbacks.append(handler)

        def parse(self, *, allow_partial=False):
            self.allow_partial = allow_partial
            for callback in self.neutral_item_found_callbacks:
                callback(event)

    class FakeExtractor:
        def __init__(self):
            self.snapshots = []
            self.tower_kills = []
            self.barracks_kills = []
            self.roshan_kills = []
            self.aegis_events = []
            self.tormentor_kills = []
            self.shrine_kills = []
            self.ward_events = []
            self.draft_events = []

        def attach(self, _parser):
            return None

        def finalize(self):
            return None

    class FakeCombatAggregator:
        def __init__(self, _player_ext):
            return None

        def on_entry(self, _entry):
            return None

    captured = {}

    def fake_build_parsed_match(**kwargs):
        captured.update(kwargs)
        return gem.ParsedMatch(neutral_item_finds=kwargs["neutral_item_finds"])

    monkeypatch.setattr(gem.parser, "ReplayParser", FakeParser)
    monkeypatch.setattr(gem.extractors.players, "PlayerExtractor", FakeExtractor)
    monkeypatch.setattr(gem.extractors.objectives, "ObjectivesExtractor", FakeExtractor)
    monkeypatch.setattr(gem.extractors.wards, "WardsExtractor", FakeExtractor)
    monkeypatch.setattr(gem.extractors.courier, "CourierExtractor", FakeExtractor)
    monkeypatch.setattr(gem.extractors.draft, "DraftExtractor", FakeExtractor)
    monkeypatch.setattr(gem.extractors.intervals, "IntervalExtractor", FakeExtractor)
    monkeypatch.setattr(gem.combat.aggregator, "_CombatAggregator", FakeCombatAggregator)
    monkeypatch.setattr(gem.results.assembly, "build_parsed_match", fake_build_parsed_match)

    match = gem.parse("dummy.dem")

    assert captured["neutral_item_finds"] == [event]
    assert match.neutral_item_finds == [event]

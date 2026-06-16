"""Build-specific send-table field patches.

Some replay builds publish field metadata that is incomplete or inconsistent
with the decoder shape needed by Source 2. Patch functions normalize those
fields before decoder selection so old and new replay builds can share the same
reader logic.

Reference: manta/field_patch.go
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from gem.schema.sendtable.models import Field


@dataclass(frozen=True)
class _FieldPatch:
    """A field mutation that applies to an inclusive game-build range.

    The ``0, 0`` range is reserved for always-on patches.
    """

    min_build: int
    max_build: int
    patch: Callable[[Field], None]

    def should_apply(self, build: int) -> bool:
        """Return whether this patch should run for ``build``."""
        if self.min_build == 0 and self.max_build == 0:
            return True
        return self.min_build <= build <= self.max_build


def _make_patches() -> list[_FieldPatch]:
    """Build the ordered patch list applied to each parsed field."""

    def patch_pre991(f: Field) -> None:
        """Backfill encoder hints missing from builds up to 990."""
        if f.var_name in {
            "angExtraLocalAngles",
            "angLocalAngles",
            "m_angInitialAngles",
            "m_angRotation",
            "m_ragAngles",
            "m_vLightDirection",
        }:
            f.encoder = (
                "qangle_pitch_yaw"
                if f.parent_name == "CBodyComponentBaseAnimatingOverlay"
                else "QAngle"
            )
        elif f.var_name in {
            "dirPrimary",
            "localSound",
            "m_flElasticity",
            "m_location",
            "m_poolOrigin",
            "m_ragPos",
            "m_vecEndPos",
            "m_vecLadderDir",
            "m_vecPlayerMountPositionBottom",
            "m_vecPlayerMountPositionTop",
            "m_viewtarget",
            "m_WorldMaxs",
            "m_WorldMins",
            "origin",
            "vecLocalOrigin",
        }:
            f.encoder = "coord"
        elif f.var_name == "m_vecLadderNormal":
            f.encoder = "normal"

    def patch_pre955(f: Field) -> None:
        """Correct mana ranges for early builds."""
        if f.var_name in ("m_flMana", "m_flMaxMana"):
            f.low_value = None
            f.high_value = 8192.0

    def patch_1016_1027(f: Field) -> None:
        """Force selected 64-bit fields onto the fixed64 decoder path."""
        if f.var_name in {
            "m_bItemWhiteList",
            "m_bWorldTreeState",
            "m_iPlayerIDsInControl",
            "m_iPlayerSteamID",
            "m_ulTeamBannerLogo",
            "m_ulTeamBaseLogo",
            "m_ulTeamLogo",
        }:
            f.encoder = "fixed64"

    def patch_simtime(f: Field) -> None:
        """Normalize time fields that require specialized time decoders."""
        if f.var_name in ("m_flSimulationTime", "m_flAnimTime"):
            f.encoder = "simtime"
        elif f.var_name == "m_flRuneTime":
            f.encoder = "runetime"

    return [
        _FieldPatch(0, 990, patch_pre991),
        _FieldPatch(0, 954, patch_pre955),
        _FieldPatch(1016, 1027, patch_1016_1027),
        _FieldPatch(0, 0, patch_simtime),
    ]


_FIELD_PATCHES: list[_FieldPatch] = _make_patches()

# Tutorial 02 · Entity State

!!! warning "Coming in Phase 3"
    This tutorial requires Phases 2 and 3 to be complete.
    Phase 2 implements send table parsing and field decoders.
    Phase 3 implements the entity lifecycle and state tracking.

    Check the [implementation status](../index.md#implementation-status)
    for the current progress.

When Phase 3 lands, you'll be able to:

- Find any entity by class name (e.g. `CDOTA_Unit_Hero_Axe`)
- Read any field by name (e.g. `m_iHealth`, `m_flMana`)
- Subscribe to entity create/update/delete events
- Track hero position, HP, gold, and items on every tick

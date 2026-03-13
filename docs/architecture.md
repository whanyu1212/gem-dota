# Architecture

This document maps module interactions, key function flow, and core data relationships in `gem`.

## 1) Module Architecture and Data Flow

```mermaid
flowchart TD
    %% Entry points
    A["gem.parse / gem.parse_to_dataframe"] --> B[parser.py]
    A --> M[dataframes.py]

    %% Core parse pipeline
    B --> C[stream.py]
    B --> D[reader.py]
    B --> E[sendtable.py]
    E --> F[field_decoder.py]
    B --> G[string_table.py]
    B --> H[entities.py]
    H --> I[field_path.py]
    B --> J[game_events.py]
    B --> K[combatlog.py]

    %% Extractors
    B --> X1["extractors.players"]
    B --> X2["extractors.objectives"]
    B --> X3["extractors.wards"]
    B --> X4["extractors.courier"]
    B --> X5["extractors.draft"]
    B --> X6["extractors.teamfights"]

    %% Assembly + aggregation
    B --> L[combat_aggregator.py]
    B --> N[match_builder.py]
    L --> N
    X1 --> N
    X2 --> N
    X3 --> N
    X4 --> N
    X5 --> N
    X6 --> N
    K --> L
    K --> N
    J --> N
    H --> N

    %% Output
    N --> O["models.py · ParsedMatch"]
    O --> M
    M --> P["dict[str, DataFrame]"]
```

## 2) Key Function Interaction Flow

```mermaid
flowchart LR
    P0[ReplayParser.parse] --> P1[DemoStream iteration]
    P0 --> P2[_read_inner_messages]
    P0 --> P3[parse_send_tables]
    P0 --> P4[string_table.handle_update]
    P0 --> P5[EntityManager.on_packet_entities]
    P5 --> P6[field_path.read_field_paths]
    P0 --> P7[combatlog ingestion]
    P0 --> P8[game event ingestion]
    P0 --> P9[extractors polling/updates]
    P0 --> P10[_CombatAggregator.on_entry]
    P0 --> P11[build_parsed_match]
    P11 --> P12[ParsedMatch]
    P12 --> P13[parse_to_dataframe]
```

## 3) Data Model Relationships (ER View)

```mermaid
erDiagram
    ParsedMatch ||--o{ ParsedPlayer : contains
    ParsedMatch ||--o{ Teamfight : has
    ParsedMatch ||--o{ CombatLogEntry : includes
    ParsedMatch ||--o{ WardEvent : includes
    ParsedMatch ||--o{ TowerKill : includes
    ParsedMatch ||--o{ RoshanKill : includes
    ParsedMatch ||--o{ BarracksKill : includes
    ParsedMatch ||--o{ CourierEvent : includes
    ParsedMatch ||--o{ DraftEvent : includes

    ParsedPlayer ||--o{ WardEvent : places_or_destroys
    ParsedPlayer ||--o{ CombatLogEntry : attributed_events
    Teamfight ||--o{ TeamfightPlayer : participants

    CombatLogEntry }o--|| ParsedPlayer : actor_target_attribution
```

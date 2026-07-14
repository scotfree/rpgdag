# rpgdag Platform Design

## Concept

rpgdag is a platform for running tabletop RPG campaigns as a directed acyclic graph (DAG) of scenes. A campaign is a journey through nodes — each node is a scene played out at the table using whatever rules system the group prefers. The platform manages game state, tracks axes (bipolar stats representing world and character state), and generates HTML interfaces for players and the GM.

## Repository Structure

```
rotations/      ← rotations game system description
worlds/         ← campaign settings/worlds
DESIGN.md       ← this document
```

---

## Core Concepts

### The Game Graph

- A **campaign** is a DAG of **nodes** and **edges**
- A **node** represents a scene to be played at the table
- An **edge** represents a path/choice between scenes
- The party occupies one node at a time (the **current node**)
- A complete game is a path from the **start node** to a **destination node**

### Axes

Axes are bipolar stats that track world and character state over time.

Each axis has:
- `id` — machine key
- `name` — display name (e.g. "Magic / Technology")
- `description` — what the two poles represent
- `min`, `max` — range (defined per axis; varies by campaign)
- `start` — initial score
- `score` — current score (mutable)

There are two scopes:

- **Global axes** — shared environmental/party state visible to all (e.g. Magic vs Technology, Good vs Evil)
- **Per-character axes** — individual character state (e.g. loyalty, wealth, alignment shift)

Per-character axes may be hidden from other players, enabling hidden-objective and traitor mechanics. In the rotations game system this is especially interesting: the player acting as GM for a scene has private axis goals that may motivate them to steer the scene in specific directions.

### Victory Conditions

- **Party VC** — reaching the destination node
- **Character VCs** — defined as axis thresholds (e.g. `magic > 10`, `wealth >= 5`)

The party succeeds or fails together; individual characters win or lose independently. A character can win even if the party fails (traitor mechanic, if enabled).

### Fog of War

A node is **visible** to players if:
- The party has already visited it, **or**
- It is reachable in one move from the current node

### Event Chunks

Each turn the platform generates **event chunks** — structured JSON blobs describing what's happening at each visible node. These are the raw material for scene headlines and flavor text. For now they are rendered directly into the views with simple templates; eventually they will be passed to an LLM.

Event chunks are built from **word lists** defined in the game config:

- **Global lists** — always included (e.g. general nouns and verbs for the setting)
- **Axis-keyed lists** — included when an axis score falls within a specified range (e.g. nouns tagged to `regionality > 5` carry East Coast flavor; `regionality < -5` carry West Coast flavor)

Event chunks are regenerated for all visible nodes each turn.

---

## Data Model

### `game_config.json`

Defines the static campaign structure. Authored once; not modified during play.

```json
{
  "meta": {
    "name": "Highway Magic",
    "description": "1976 America, east to west.",
    "start_node": "new_york",
    "destination_node": "mount_oumalouma"
  },
  "global_axes": [
    {
      "id": "magic_tech",
      "name": "Magic / Technology",
      "description": "Negative = Technology dominant. Positive = Magic rising.",
      "min": -10,
      "max": 10,
      "start": 0
    },
    {
      "id": "regionality",
      "name": "East / West",
      "description": "Negative = deep West Coast. Positive = East Coast.",
      "min": -10,
      "max": 10,
      "start": 8
    }
  ],
  "nodes": [
    {
      "id": "chicago",
      "name": "Chicago",
      "description": "Crossroads of America. Blues bars and meat-packing plants.",
      "art": null,
      "color": null,
      "outcomes": [
        {
          "question": "Did the party evade the FBI tail?",
          "on_true": [{"axis": "magic_tech", "delta": 1}],
          "on_false": [{"axis": "magic_tech", "delta": -1}]
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "chicago_to_st_louis",
      "from": "chicago",
      "to": "st_louis",
      "name": "Route 66",
      "axis_impacts": [{"axis": "regionality", "delta": -1}]
    }
  ],
  "word_lists": [
    {"type": "noun", "words": ["drifter", "trucker", "highway patrol"]},
    {"type": "verb", "words": ["ambushes", "warns", "tails", "recruits"]},
    {"type": "noun", "axis": "regionality", "min": 5,
      "words": ["dive bar", "punk show", "city gutter", "tenement"]},
    {"type": "noun", "axis": "regionality", "max": -5,
      "words": ["canyon", "surf shack", "commune", "desert shrine"]},
    {"type": "noun", "axis": "magic_tech", "min": 5,
      "words": ["ley line", "death witch", "ritual circle", "oracle"]},
    {"type": "noun", "axis": "magic_tech", "max": -5,
      "words": ["surveillance van", "radio tower", "federal agent", "wiretap"]}
  ]
}
```

### `game_state.json`

Tracks mutable state. Updated each turn by `update_game.py`.

```json
{
  "turn": 3,
  "current_node": "chicago",
  "visited_nodes": ["new_york", "philadelphia", "chicago"],
  "global_axes": {
    "magic_tech": 2,
    "regionality": 4
  },
  "characters": [
    {
      "id": "alice",
      "name": "Alice",
      "axes": {
        "loyalty": 1,
        "wealth": -2
      },
      "axes_visible": false
    }
  ],
  "node_events": {
    "chicago": {
      "nouns": ["trucker", "federal agent"],
      "verbs": ["tails", "warns"],
      "axes_snapshot": {"magic_tech": 2, "regionality": 4}
    }
  }
}
```

### `turn_update.json`

Input to `update_game.py` for a single turn.

```json
{
  "move_to": "st_louis",
  "outcomes": {
    "magic_tech": 1,
    "regionality": -1
  },
  "character_updates": {
    "alice": {"loyalty": 2}
  }
}
```

---

## Scripts

### `scaffold_game.py`

Generates a starter `game_config.json`. Defaults to the Highway Magic world.

```
python scaffold_game.py [--world highway_magic] [--output game_config.json]
```

### `update_game.py`

Processes a turn: updates `game_state.json`, regenerates event chunks for visible nodes, writes `player_view.html` and `gm_view.html`.

```
python update_game.py --turn turn_update.json
python update_game.py --move-to st_louis --outcomes "magic_tech=+1,regionality=-1" --char alice loyalty=+2
```

Flags: `--config game_config.json`, `--state game_state.json`, `--out-dir ./out`

---

## Views

Both views are static HTML files generated by `update_game.py` — no server required.

**`player_view.html`**
- DAG showing only visible nodes (fog of war)
- Click a node to see its event chunk rendered as readable text
- No axis values shown

**`gm_view.html`**
- Full DAG, all nodes
- Sidebar: global axis values and per-character state
- Node popups show full outcome definitions

Both views use **Cytoscape.js** with the **dagre** layout plugin (top-down DAG layout, no framework dependency).

---

## Roadmap

**Stage 1 — Local**
- `scaffold_game.py` generates `game_config.json` (Highway Magic default)
- `update_game.py` processes a turn and writes static HTML views
- Event chunks generated from word lists + axis-keyed weights
- Everything runs locally, no server, no cloud

**Stage 2 — Polish**
- Improve view styling and interaction
- Refine event chunk generation and template rendering

**Stage 3 — Cloud**
- Push HTML views to S3 (publicly accessible)
- Scripts still run locally and push to S3

**Stage 4 — Service**
- Lightweight FastAPI server
- GM updates via web form
- Google SSO
- Game state in cloud storage

---

## Game System Types

The platform is system-agnostic at Stage 1. Game system types describe how scenes are run and who acts as GM.

- **rotations** (`rotations/`) — rotating GM per scene; see `rotations/README.md`
- **single-GM** — one GM runs the full campaign; not yet designed

Worlds (`worlds/`) are independent of game system type — any world can be run under any system.

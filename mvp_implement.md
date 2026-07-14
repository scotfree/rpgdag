# mvp_implement.md — Overworld MVP Implementation Spec

Audience: a coding agent (Claude Code) starting work in this repo with no conversational history.

**Read first:** `overworld_mvp.md` (the game rules — authoritative for semantics), then this document (authoritative for implementation). `highway_magic.md` and the Warrens of Skarn example inside `overworld_mvp.md` are reference campaigns.

**Precedence:** This spec and `overworld_mvp.md` **supersede `DESIGN.md`** wherever they conflict. `DESIGN.md` is an earlier design generation kept for historical context. Known stale elements there: bipolar axes with min/max, per-character axes in overworld state, outcome lists without edge gating, event chunks / word lists, and the FastAPI/SSO architecture. Do not implement those.

---

## 1. What to Build (Stage 1)

A local, serverless Python toolchain:

1. `rpgdag/` — a small Python package: data model, validation, turn engine, scoring
2. `cli.py` — command-line driver for authoring-time validation and play-time turn processing
3. Static HTML view generation — `player_view.html` and `gm_view.html`, regenerated after every state change
4. A bundled test campaign — **The Warrens of Skarn** exactly as specified in `overworld_mvp.md`, as `campaigns/skarn/game_config.json`
5. Tests — pytest, covering validation, the turn engine, gating, scoring, and a full Skarn playthrough

No server, no database, no auth, no LLM calls. State is JSON on disk. Python 3.11+, stdlib preferred; `pytest` is the only expected dependency (views use CDN JS, see §7).

---

## 2. Core Semantics (summary — rules doc governs)

- Global **axes** only, each an integer clamped to 0–10.
- A **node** has a premise and 1–3 yes/no **questions**; each answer side carries a (possibly empty) list of axis impacts.
- **Edges** carry impacts and optional **requirements**: `(question, answer)` pairs over their source node's questions. An edge is *unlocked* iff all its requirements match the recorded answers. Every node must have at least one requirement-free edge.
- **Terminals** end the campaign and determine the binary party result, optionally gated by an axis threshold, or via an ordered **ending table** (see §4, `endings`).
- **Goal cards** are hidden per-player conditions over final axis values and/or the impact log, worth VP.
- The **impact log** is append-only and is the complete scoring record.
- Turn flow (the "ritual"): answer questions → apply question impacts → compute unlocked edges → party chooses an unlocked edge → apply edge impacts → move → reveal fog of war at new node. Opposed pairs (e.g. Magic/Technology) are expressed as explicit paired impacts in the config, never as engine logic.

---

## 3. Repository Layout

```
rpgdag/
  __init__.py
  model.py        # dataclasses + JSON (de)serialization
  validate.py     # config validation (§5)
  engine.py       # turn processing (§6)
  score.py        # goal-card evaluation (§8)
  render.py       # HTML view generation (§7)
cli.py
campaigns/
  skarn/game_config.json
tests/
out/              # generated: game_state.json, player_view.html, gm_view.html (gitignored)
```

---

## 4. File Formats

### 4.1 `game_config.json` (static, authored)

```json
{
  "meta": {
    "name": "The Warrens of Skarn",
    "description": "End the goblin raids.",
    "start_node": "gatehouse",
    "players": ["alice", "bob", "carol"]
  },
  "axes": [
    {"id": "fear", "name": "Fear", "start": 6},
    {"id": "hope", "name": "Hope", "start": 4}
  ],
  "nodes": [
    {
      "id": "gatehouse",
      "name": "The Gatehouse",
      "premise": "A ruined watchtower guards the only known entrance...",
      "questions": [
        {
          "id": "q1",
          "text": "Did the party take the gatehouse?",
          "yes": [{"axis": "fear", "delta": -1}],
          "no":  [{"axis": "fear", "delta": 1}]
        },
        {
          "id": "q2",
          "text": "Did anyone discover the passage behind the waterfall?",
          "yes": [],
          "no": []
        }
      ]
    }
  ],
  "edges": [
    {
      "id": "behind_the_falls",
      "from": "gatehouse",
      "to": "grotto",
      "name": "Behind the Falls",
      "flavor": "A black slit in wet stone.",
      "requires": [{"question": "q2", "answer": "yes"}],
      "impacts": [{"axis": "hope", "delta": 1}]
    }
  ],
  "terminals": [
    {
      "id": "throne",
      "name": "The Chieftain's Throne",
      "premise": "The chief falls; the raids end.",
      "endings": [
        {"when": [{"axis": "hope", "op": ">=", "value": 5}],
         "party_result": "win",
         "text": "The villages rebuild. Songs are sung."},
        {"when": [],
         "party_result": "loss",
         "text": "A hollow victory: the villages are too broken to rebuild."}
      ]
    }
  ],
  "goal_cards": [
    {
      "id": "dread_cultist",
      "name": "Dread Cultist",
      "vp": 3,
      "conditions": [{"type": "final_value", "axis": "fear", "op": ">=", "value": 7}]
    }
  ]
}
```

Notes:
- Terminals are nodes without questions or outgoing edges; they live in `terminals`, not `nodes`. Their `endings` list is evaluated **in order**; first matching `when` (all clauses true, empty = always) wins. This single mechanism covers both the multi-terminal pattern (Skarn) and the one-terminal-many-endings pattern (Highway Magic).
- A **terminal with questions** (Highway Magic's summit show) is allowed: it may carry `questions` like a node; its question impacts are applied *before* evaluating `endings`. It still has no outgoing edges.
- Impacts are always lists of `{"axis": id, "delta": int}`. Deltas may be any nonzero integer; applied values clamp to [0, 10].
- Goal-card assignment (deal/draft) is out of scope for the engine; `game_state` simply records who holds what, assigned at `new-game` time via CLI flags or a default random deal.

### 4.2 `game_state.json` (mutable, engine-owned)

```json
{
  "config_name": "The Warrens of Skarn",
  "turn": 2,
  "current_node": "great_hall",
  "phase": "awaiting_answers",
  "visited": ["gatehouse", "great_hall"],
  "axes": {"fear": 5, "hope": 5},
  "answers": {"gatehouse": {"q1": "yes", "q2": "yes"}},
  "goal_assignment": {"alice": ["dread_cultist"]},
  "log": [
    {"turn": 1, "node": "gatehouse", "kind": "question", "question": "q1",
     "answer": "yes", "impacts": [{"axis": "fear", "delta": -1}],
     "axes_after": {"fear": 5, "hope": 4}},
    {"turn": 1, "kind": "edge", "edge": "behind_the_falls",
     "impacts": [{"axis": "hope", "delta": 1}],
     "axes_after": {"fear": 5, "hope": 5}}
  ],
  "result": null
}
```

- `phase` is `awaiting_answers` | `awaiting_edge` | `over`.
- Every impact application appends one log entry, including zero-impact answers (they matter for gating and goal cards).
- `result`, once set: `{"terminal": id, "ending_index": n, "party_result": "win"|"loss", "text": "..."}`.

---

## 5. Validation (`validate.py`)

`validate(config) -> list[Problem]` where Problem has `severity` (`error`|`warning`), `where`, `message`. CLI exits nonzero on any error.

Errors:
- Duplicate ids anywhere; unknown axis/node/question references; `start_node` missing
- Graph (nodes + terminals, edges) is not a DAG (cycle detection)
- Any node with zero outgoing edges that is not a terminal
- Any node lacking at least one requirement-free outgoing edge
- Node with 0 or >3 questions; terminal `endings` empty or final entry has non-empty `when` (must guarantee a result)
- Edge requirement referencing a question not on its `from` node
- Axis `start` outside 0–10; any edge whose `from` is a terminal id

Warnings:
- Terminal unreachable from start; node unreachable from start
- An edge whose requirements can never all hold (same question required with conflicting answers)
- Axis never referenced by any impact or goal card

---

## 6. Turn Engine (`engine.py`)

Pure functions over (config, state); no I/O. CLI handles files.

- `new_game(config, goal_assignment) -> state`
- `record_answers(config, state, {question_id: "yes"|"no"}) -> state`
  - Valid only in `awaiting_answers`; must answer **all** questions of `current_node` at once
  - Applies each question's impacts in the node's question order, clamping and logging each
  - If current node is a terminal: evaluate `endings`, set `result`, phase → `over`
  - Else phase → `awaiting_edge`
- `unlocked_edges(config, state) -> [edge]` — edges from `current_node` whose requirements all match recorded answers
- `traverse(config, state, edge_id) -> state`
  - Valid only in `awaiting_edge`; edge must be unlocked
  - Applies edge impacts (log), moves `current_node`, appends to `visited`, increments `turn`
  - If destination is a terminal **without questions**: evaluate endings immediately, phase → `over`
  - Otherwise (regular node, or terminal with questions) phase → `awaiting_answers`

All invalid operations raise typed exceptions with table-readable messages (these surface in the CLI verbatim).

---

## 7. Views (`render.py`)

Regenerate both files into `out/` after every successful CLI mutation. Static, self-contained HTML; graph rendered with **Cytoscape.js + dagre** loaded from CDN (per DESIGN.md's still-valid choice). No build step.

**Fog of war rule (player view):** visible = visited nodes ∪ current node ∪ edges out of *visited* nodes ∪ those edges' destination nodes shown as **name-only silhouettes** (no premise). For visible edges: show name, flavor, impacts, and requirements (MVP default is open information). Unvisited-unadjacent nodes/edges are absent entirely.

`player_view.html`: the fogged DAG; current axis values (large, prominent — this is the scoreboard); current node premise; during `awaiting_edge`, unlocked edges highlighted and locked-but-visible edges greyed with their unmet requirements shown; the public impact log.

`gm_view.html`: full DAG; everything in the config including all questions and endings; the log; current phase and legal next actions. (Goal-card *assignments* appear here too — the scene GM rotates, so true secrecy is handled socially, by players keeping cards private; the file is a debugging aid, not a security boundary.)

---

## 8. Scoring (`score.py`)

`score(config, state) -> {player: {"cards": [...], "vp": int}}`, valid when phase is `over`.

Goal-card condition types (all conditions on a card must hold for it to score):

| type | fields | meaning |
|---|---|---|
| `final_value` | axis, op, value | final axis vs value (`op` ∈ `>= > <= < ==`) |
| `never` | axis, op, value | at **no** point (start value or any log `axes_after`) did the comparison hold |
| `always` | axis, op, value | at every point it held |
| `total_change` | axis, direction (`up`\|`down`), op, value | sum of positive deltas (or magnitude of negative deltas) applied to axis |
| `question` | node, question, answer | that answer was recorded |
| `edge` | edge | that edge was traversed |
| `count` | of: [subconditions of type question/edge], op, value | number of matching log events |

This covers every card in both reference campaigns; do not add more types speculatively.

---

## 9. CLI (`cli.py`)

```
python cli.py validate  --config PATH
python cli.py new-game  --config PATH --out DIR [--assign player=card_id ...]
python cli.py answer    --config PATH --state PATH q1=yes q2=no
python cli.py move      --config PATH --state PATH --edge EDGE_ID
python cli.py status    --config PATH --state PATH        # phase, axes, unlocked edges
python cli.py score     --config PATH --state PATH
```

`answer` and `move` print the ritual text for reading aloud: each question, its answer, its impacts, new axis values; then (after `answer`) the newly unlocked edges with flavor; then (after `move`) the edge flavor and the new node's premise plus fog-of-war reveals. This CLI output *is* the GM's script for the table ritual — treat its readability as a feature, not logging.

---

## 10. Testing Expectations

- Validation: fixtures for each error/warning in §5
- Engine: phase transitions, gating (edge locked/unlocked by answers), clamping at 0 and 10, terminal-with-questions flow
- Scoring: one test per condition type; the full Skarn goal-card set against a scripted playthrough
- End-to-end: script a complete Skarn game via the public API (both a win path through the Throne Door and a loss via the Smoke-Choked Run), assert final axes, result, and VP totals
- Golden-file test on CLI ritual output for one turn (keeps the read-aloud script stable)

---

## 11. Explicitly Out of Scope (do not build)

Per-character axes; the Axis scene-resolution ruleset; hosted-system integration beyond "answers arrive via the CLI"; word lists / event chunks / procedural flavor; hidden edge data and traitor mode; between-campaign advancement; GM regulation mechanics; any server, auth, or cloud storage (Stages 3–4 of DESIGN.md remain the eventual direction, but not now).

## 12. Suggested Order of Work

model.py + skarn config → validate.py + its tests → engine.py + tests → score.py + tests → cli.py with ritual output → render.py views → end-to-end tests. Authoring `campaigns/highway_magic/game_config.json` from `highway_magic.md` is a good final validation exercise of the whole schema (it exercises the terminal-with-questions and ending-table paths).

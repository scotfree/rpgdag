# rpgdag — Overworld MVP

The minimal board game that drives a campaign. It connects tight roleplaying scenes (played in a **hosted system** — D&D, Axis, or anything else) into a single evening-scale campaign with a beginning, an end, a winner-or-loser party, and a secretly-scored individual winner.

The overworld's whole job: give each scene its context and stakes, turn scene results into world change, and give the party a meaningful move between scenes.

---

## The Game in One Breath

Pick a GM (their character sits out). Play the scene in the hosted system until the node's printed questions are answered. The GM reads each question aloud, answers it, and applies its printed axis impacts. Answers unlock edges. The party debates and picks an edge; its impacts apply and the fog lifts on the next node. Repeat until a terminal node ends the campaign. Reveal goal cards, tally victory points from the impact log.

---

## Objects

The entire game state is five kinds of objects plus one log.

### Axes
Global, monopolar, shared world state.

| Field | Meaning |
|---|---|
| `name` | Single adjective (e.g. Fear, Hope, Order) |
| `range` | Always 0–10 |
| `start` | Initial value |

There are **no per-character axes in the overworld**. Health, inventory, spell slots — all of that lives inside the hosted system and never touches the board game.

### Nodes
A scene to be played at the table.

| Field | Meaning |
|---|---|
| `premise` | A short paragraph handed to the Scene GM: situation, location, key NPCs |
| `questions` | **1–3 yes/no questions**, each with printed axis impacts for yes and for no |

Hard limits, on purpose: max three questions, one line each, strictly yes/no, no branching, no partial credit. If a scene needs nuance, spend a second question — never more machinery.

Questions do double duty:
- **Impacts** — each answer applies its printed axis shifts (either side may be empty)
- **Keys** — edges may require specific answers to become available

### Edges
The party's move. This is where campaign choice lives.

| Field | Meaning |
|---|---|
| `from`, `to` | Node ids |
| `requires` | Zero or more `(question, answer)` pairs from the source node. Empty = always available |
| `impacts` | Printed axis shifts applied when traversed |
| `flavor` | Name + one line of description, revealed by fog of war |

Every node must have **at least one edge with no requirements**. The party can always move; failure changes *where you can go*, never whether you can go.

### Terminals
Nodes with no exits. Reaching one ends the campaign.

| Field | Meaning |
|---|---|
| `ending` | Closing narration |
| `party_result` | `win` / `loss` (optionally gated: "win only if Hope ≥ 5, else loss") |

Party victory is **binary** and encoded in the map: which terminal you reach (plus an optional axis threshold) is the whole party outcome.

### Goal Cards
Individual hidden objectives. Dealt (or drafted) one or two per player at campaign start.

| Field | Meaning |
|---|---|
| `condition` | A check against final axis values or the impact log (e.g. "Fear ≥ 7 at end", "Hope never dropped below 3", "total Fear increases ≥ 4") |
| `vp` | Victory points if met |

Goals are conditions over **global** axes — that's why no per-player tracking is ever needed during play.

### The Impact Log
One sheet. The GM of each scene appends every applied impact (question answers and edge traversal), publicly. At campaign end it is the complete, auditable scoring record.

---

## Roles & Rotation

- Before each scene, the party chooses the **Scene GM** for that node. Any player may GM; the same player may GM repeatedly if the party agrees.
- The Scene GM's **character does not appear in the scene**. Explaining why is encouraged roleplay ("Torvald stays with the horses").
- The Scene GM receives the node premise and questions, preps briefly, and runs the scene in the hosted system.
- The Scene GM performs the end-of-node ritual (below).

Choosing the GM is itself a tactical move: bench the character least useful for the scene the fog of war hints at — or grab the chair because you secretly want to color this scene.

**No veto or fairness mechanics in the MVP.** All axis impacts are printed on the map in advance; the GM only answers factual questions the whole table just watched play out. There is nothing to veto. (If a table wants more, see the GM Regulation Mechanics catalog — advanced play.)

---

## The Ritual (end of every node)

Performed aloud by the Scene GM, in order:

1. **Answer.** Read each printed question and answer it yes or no, based on what happened in the scene.
2. **Apply.** For each answer, read its printed impacts and update the axes. Log them.
3. **Unlock.** Reveal which outgoing edges are now available, with names and flavor.
4. **Choose.** The party debates and picks one available edge. (Lobby carefully — your goal card is showing in your arguments.)
5. **Traverse.** Apply and log the edge's impacts. Read its flavor as the journey narration.
6. **Lift the fog.** Reveal the destination node's name and premise, and the names + flavor of *its* outgoing edges. (Edge impacts and requirements may be printed openly or kept hidden — map author's choice; MVP default is **open**.)
7. **Seat the next GM.**

At a terminal node: read the ending, declare the party result, then every player reveals their goal cards and scores them against the final axes and the log. Highest VP total is the individual winner. Traditional taunting follows.

---

## The Hosted-System Socket

The overworld makes exactly one demand of whatever rules run inside a node:

> **The scene must produce a yes/no answer to each of the node's printed questions.**

That's the entire contract. How the answers arise — D&D combat and skill checks, Axis rolls, pure freeform narration — is internal to the hosted system. The hosted system may consult the current axis values for color if it likes; it may not modify them. Nothing else crosses the boundary in either direction: no hit points out, no axis math in.

Practical corollaries:
- A question like "Did anyone find the passage behind the falls?" is a *side challenge* — the scene can mainly be about fighting the warband or persuading the mayor, and the hosted system resolves the side question with a search check, a clever plan, or a die roll as it sees fit.
- The map author should write questions that are **publicly verifiable facts of the fiction** ("Was the hostage recovered alive?"), never judgment calls ("Did the party behave honorably?").

---

## Worked Example — *The Warrens of Skarn* (5 nodes)

**Axes:** Fear (start 6), Hope (start 4). Party goal: end the goblin raids.

### Nodes

**N1 · The Gatehouse** *(start)*
Premise: A ruined watchtower guards the only known entrance to the warrens. Goblin sentries hold it; an old waterfall pounds the cliff beside it.
- Q1 *Did the party take the gatehouse?* — yes: Fear −1 · no: Fear +1
- Q2 *Did anyone discover the passage behind the waterfall?* — yes: (no impact) · no: (no impact)

**N2 · The Great Hall**
Premise: The warband feasts. Their war-drums drive the raids. A frontal battle, or something cleverer.
- Q1 *Were the war-drums destroyed?* — yes: Fear −2 · no: Fear +1
- Q2 *Did the warband's shaman escape?* — yes: Fear +1 · no: Hope +1

**N3 · The Flooded Grotto**
Premise: A drowned shrine beneath the falls. Something older than goblins is chained here, and it wants to bargain.
- Q1 *Did the party strike the bargain?* — yes: Hope +2, Fear +1 · no: (no impact)

**N4 · The Warrens**
Premise: Tunnels, cages, the missing villagers — and the goblin chief's rearguard.
- Q1 *Were the villagers freed alive?* — yes: Hope +2 · no: Hope −2, Fear +1
- Q2 *Did the chief's rearguard rout?* — yes: Fear −1 · no: (no impact)

### Edges

| From → To | Name / flavor | Requires | Impacts |
|---|---|---|---|
| N1 → N2 | **The Broken Stair** — the direct ascent, drums growing louder | Q1 = yes | — |
| N1 → N2 | **The Long Crawl** — a night circling the cliffs, watched from above | — | Fear +1 |
| N1 → N3 | **Behind the Falls** — a black slit in wet stone | Q2 = yes | Hope +1 |
| N3 → N4 | **The Drowned Way** — the grotto's far channel, silent and cold | — | Fear −1 |
| N2 → N4 | **The Chief's Road** — banners torn down as you pass | Q1 = yes | Hope +1 |
| N2 → N4 | **The Midden Gate** — through the filth, heads down | — | — |
| N4 → T1 | **The Throne Door** — iron-bound, ready to fall | Q2 = yes | — |
| N4 → T2 | **The Smoke-Choked Run** — out, alive, empty-handed | — | Hope −1 |

### Terminals

**T1 · The Chieftain's Throne** — The chief falls; the raids end. **Party wins if Hope ≥ 5**, otherwise a hollow victory (loss): the villages are too broken to rebuild.
**T2 · Bitter Retreat** — The warrens stand. **Party loss.**

### Goal cards (deal 1 each, examples)

- *Dread Cultist* — Fear ≥ 7 at campaign end: **3 VP**
- *The Optimist* — Hope ≥ 7 at campaign end: **3 VP**
- *Warmonger* — Fear shifted by ±2 or more in at least two scenes (per log): **2 VP**
- *Deep Bargainer* — the Grotto bargain was struck (per log): **3 VP**
- *Steady Hand* — Hope never dropped below 3 (per log): **2 VP**

Note the shape of play this produces: the Dread Cultist quietly argues *against* destroying the war-drums and *for* the Long Crawl; the Deep Bargainer desperately needs someone to search near that waterfall in scene one without saying why; everyone still wants to reach the throne.

---

## Explicitly Deferred (not MVP)

- **Between-campaign advancement** — character axis bumps earned via goal cards across multiple DAGs
- **Travel as a move** — richer edge mechanics (mode of travel, distance as resource)
- **GM regulation mechanics** — the full A–O catalog; unnecessary while impacts are map-printed
- **Procedural events / word lists** — fog-of-war flavor generation; MVP uses hand-authored edge flavor
- **Hidden edge data, traitor mode, per-character overworld axes** — advanced map-author options
- **The Axis ruleset itself** — a hosted system, specified separately

"""Generate game_config.json for Asteroid Boys and print balance stats.

The 25 asteroids are hand-authored in LAYERS below; everything else (nodes,
the 67 edges, goal-card count lists) is derived. Edit the table, re-run:

    python3 campaigns/asteroid_boys/generate.py [OUT_PATH]

OUT_PATH defaults to game_config.json next to this script. Hand edits to the
JSON are overwritten on the next run.
"""

import json
import sys
from collections import Counter
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "game_config.json"

# Each asteroid: name, premise, approach flavor (used on every edge into it),
# and its two effects keyed by session question: m = mining, f = fight,
# s = science. Axes: cr = Credits, bs = Base Ship, fb = Force Balance.
LAYERS = [
    [  # layer 1: outer belt (no Credits costs here)
        ("Claim Seven", "A squatted mining claim; the squatters say they filed first.",
         "Old claim beacons blink you in.", {"m": ("cr", 2), "f": ("fb", -1)}),
        ("The Tollhouse", "Ex-militia run a toll gate across the only clear lane.",
         "Floodlights sweep across the lane.", {"f": ("bs", 1), "s": ("fb", 1)}),
        ("Hollow Saint", "A shrine carved into a hollow rock, tended by the Quiet Ones.",
         "Chanting on an open channel.", {"s": ("fb", 2), "m": ("bs", -1)}),
        ("Glimmer Drift", "A slow ice field shot through with singing crystal.",
         "The hull rings like a struck bell.", {"m": ("bs", 2), "s": ("cr", 1)}),
        ("Wreck of the Patience", "A gutted ore hauler, still venting. Someone got here first.",
         "Debris tumbles past the viewport.", {"m": ("bs", 1), "f": ("fb", -2)}),
    ],
    [  # layer 2
        ("Ma Kessler's Still", "A moonshine depot and the belt's only honest bar.",
         "Running lights strung like a carnival.", {"s": ("fb", 1), "m": ("bs", -1)}),
        ("The Drum", "A spinning rock where the Drummers keep time for the end of the world.",
         "A heavy pulse through the deck plates.", {"f": ("fb", -3), "s": ("cr", -1)}),
        ("Scrapyard Nine", "A salvage co-op that pays in parts, not credits.",
         "A tangle of tethered hulks.", {"m": ("bs", 2), "f": ("cr", -1)}),
        ("Pilgrim's Rest", "Cultists waiting for a ship that will carry them out.",
         "Hand-painted signs: WE ARE READY.", {"s": ("fb", 3), "m": ("cr", 1)}),
        ("Cold Vein", "A rich nickel seam under a rival crew's flag.",
         "Drill dust hangs in the dark.", {"m": ("cr", 2), "f": ("bs", -1)}),
    ],
    [  # layer 3: the deep middle
        ("The Choir", "A colony that broadcasts hymns into the dark and won't stop.",
         "The hymn fills every channel.", {"s": ("fb", 1), "f": ("bs", -2)}),
        ("Hangman's Spur", "Belt justice: the rope lane where claim-jumpers end up.",
         "Shapes drift on long tethers.", {"f": ("fb", -1), "m": ("cr", 2)}),
        ("The Foundry", "An abandoned smelter that still works, if anyone can wake it.",
         "Slag glows faint red.", {"s": ("bs", 2), "m": ("cr", -2)}),
        ("Mother's Eye", "A cult observatory that claims to see the Force itself.",
         "A lens the size of a town turns to watch you.", {"s": ("fb", 2), "f": ("cr", -1)}),
        ("Black Market Hub", "Everything is for sale, including you.",
         "A hundred transponders, all fake.", {"m": ("cr", -2), "f": ("bs", 1)}),
    ],
    [  # layer 4
        ("Dead Man's Lode", "Platinum, and a claim whose last owner died mid-shift.",
         "Rescue flares, decades old.", {"m": ("cr", 2), "s": ("fb", -2)}),
        ("The Reliquary", "Cultists guard a drive core they believe is holy.",
         "Candles flicker in vacuum, impossibly.", {"f": ("bs", 2), "s": ("fb", -1)}),
        ("Sawtooth", "A broken rock crawling with pirate skiffs.",
         "Jagged silhouettes, engines cold.", {"f": ("cr", 1), "m": ("bs", -1)}),
        ("The Quiet Field", "A dead-calm pocket where instruments read things that aren't there.",
         "Every instrument goes silent at once.", {"s": ("fb", 3), "m": ("cr", -1)}),
        ("Last Chance Depot", "The final fuel stop before the inner edge. Prices to match.",
         "A hand-lettered sign: LAST FUEL.", {"m": ("bs", 1), "f": ("cr", -2)}),
    ],
    [  # layer 5: the inner edge
        ("Ghost Shipyard", "Half-built hulls from a company that went bust mid-contract.",
         "Unfinished ribs against the stars.", {"m": ("bs", 2), "f": ("fb", -1)}),
        ("The Prophet's Rock", "The cult's founder lives here and wants a ride out.",
         "A lone figure stands on the surface, waving.", {"s": ("fb", -3), "f": ("cr", 1)}),
        ("Breaker's Yard", "Ship-breakers who will strip anything that docks.",
         "Cutting torches spark everywhere.", {"f": ("bs", -2), "m": ("cr", 1)}),
        ("The Lantern", "A lighthouse beacon kept by a lone, strange keeper.",
         "One steady light in all that dark.", {"s": ("fb", 1), "m": ("bs", 1)}),
        ("Gate Rock", "Customs post on the edge of the belt. Bribes accepted.",
         "Clear lanes beyond, at last.", {"f": ("cr", -1), "s": ("bs", 1)}),
    ],
]

QTEXT = {
    "m": "Did the crew mine or salvage here?",
    "f": "Was there a fight?",
    "s": "Did anyone do science here?",
}
AXIS_IDS = {"cr": "credits", "bs": "base_ship", "fb": "force_balance"}
AXIS_STARTS = {"cr": 3, "bs": 0, "fb": 5}


def node_id(layer, col):
    return f"a{layer + 1}{col + 1}"


def next_cols(col):
    """Same column and its neighbours in the next layer; no wraparound."""
    return [c for c in (col - 1, col, col + 1) if 0 <= c < 5]


nodes = [{
    "id": "departure",
    "name": "Departure",
    "premise": "The crew's base ship sits half-finished at the dock. Out there, the belt.",
    "questions": [{
        "id": "q1",
        "text": "Did the crew settle their dock debts before leaving?",
        "yes": [{"axis": "credits", "delta": -1}],
        "no": [{"axis": "force_balance", "delta": -1}],
    }],
}]
for li, layer in enumerate(LAYERS):
    for ci, (name, premise, _approach, effects) in enumerate(layer):
        questions = []
        for q in "mfs":
            yes = []
            if q in effects:
                axis, delta = effects[q]
                yes = [{"axis": AXIS_IDS[axis], "delta": delta}]
            questions.append({"id": q, "text": QTEXT[q], "yes": yes, "no": []})
        nodes.append({"id": node_id(li, ci), "name": name, "premise": premise,
                      "questions": questions})


def edge_to(src, li, ci):
    name, _premise, approach, _effects = LAYERS[li][ci]
    return {"id": f"{src}__{node_id(li, ci)}", "from": src, "to": node_id(li, ci),
            "name": f"Burn for {name}", "flavor": approach, "requires": [], "impacts": []}


edges = [edge_to("departure", 0, c) for c in range(5)]
for li in range(4):
    for ci in range(5):
        for cj in next_cols(ci):
            edges.append(edge_to(node_id(li, ci), li + 1, cj))
for ci in range(5):
    src = node_id(4, ci)
    edges.append({"id": f"{src}__fly_out", "from": src, "to": "fly_out",
                  "name": "Fly the Base Ship Out", "flavor": "Light the drive and go.",
                  "requires": [], "impacts": []})
    edges.append({"id": f"{src}__stuck", "from": src, "to": "stuck",
                  "name": "Stay in the Belt", "flavor": "One more rock. Always one more rock.",
                  "requires": [], "impacts": []})

terminals = [
    {"id": "fly_out", "name": "Fly Base Ship Out",
     "premise": "The crew lights the drive and points the base ship at open space.",
     "endings": [
         {"when": [{"axis": "base_ship", "op": ">=", "value": 4}], "party_result": "win",
          "text": "She holds together. The belt shrinks behind you."},
         {"when": [], "party_result": "loss",
          "text": "She breaks up past the last rock. The belt keeps what it catches."},
     ]},
    {"id": "stuck", "name": "Stuck in the Belt",
     "premise": "The crew never makes it out.",
     "endings": [{"when": [], "party_result": "loss",
                  "text": "Another crew of rock-rats, another shrine in the dark."}]},
]


def session_count(q, n):
    """At least n 'yes' answers to session question q, across all asteroids."""
    return {"type": "count", "op": ">=", "value": n, "of": [
        {"type": "question", "node": node_id(li, ci), "question": q, "answer": "yes"}
        for li in range(5) for ci in range(5)]}


goal_cards = [
    {"id": "jedi_master", "name": "Jedi Master", "vp": 3,
     "conditions": [{"type": "final_value", "axis": "force_balance", "op": ">=", "value": 8}]},
    {"id": "force_anomaly", "name": "Force Anomaly", "vp": 3,
     "conditions": [{"type": "final_value", "axis": "force_balance", "op": "==", "value": 0}]},
    {"id": "wealthy", "name": "Wealthy", "vp": 2,
     "conditions": [{"type": "final_value", "axis": "credits", "op": ">", "value": 6}]},
    {"id": "big_spender", "name": "Big Spender", "vp": 2,
     "conditions": [{"type": "total_change", "axis": "credits", "direction": "down",
                     "op": ">=", "value": 6}]},
    {"id": "miner", "name": "Miner", "vp": 2, "conditions": [session_count("m", 2)]},
    {"id": "hot_blooded", "name": "Hot Blooded", "vp": 2, "conditions": [session_count("f", 3)]},
    {"id": "brainy", "name": "Brainy", "vp": 2, "conditions": [session_count("s", 2)]},
]

config = {
    "meta": {"name": "Asteroid Boys",
             "description": "Finish the base ship and fly it out of the belt.",
             "start_node": "departure", "players": ["alice", "bob", "carol"]},
    "axes": [
        {"id": "credits", "name": "Credits", "start": AXIS_STARTS["cr"]},
        {"id": "base_ship", "name": "Base Ship", "start": AXIS_STARTS["bs"]},
        {"id": "force_balance", "name": "Force Balance", "start": AXIS_STARTS["fb"]},
    ],
    "nodes": nodes, "edges": edges, "terminals": terminals, "goal_cards": goal_cards,
}
with open(OUT, "w") as f:
    json.dump(config, f, indent=2)
    f.write("\n")
print(f"wrote {OUT}")

# ---- balance report ----
all_fx = [fx for layer in LAYERS for (_n, _p, _a, e) in layer for fx in e.values()]
print("effects per axis:", Counter(a for a, _ in all_fx))
for ax in ("cr", "bs", "fb"):
    print(f"  {ax}:", sorted(d for a, d in all_fx if a == ax))
print("session questions carrying effects:",
      Counter(q for layer in LAYERS for (_n, _p, _a, e) in layer for q in e))
for li, layer in enumerate(LAYERS):
    pairs = [tuple(sorted(a for a, _ in e.values())) for (_n, _p, _a, e) in layer]
    print(f"layer {li + 1} axis pairs:", pairs)

# Every column path through the field (5 asteroids, one per layer).
paths = [[c] for c in range(5)]
for _ in range(4):
    paths = [p + [c] for p in paths for c in next_cols(p[-1])]
print("paths:", len(paths))

# Best gain / worst drop per axis on any path, assuming every effect on the
# path fires (an upper bound; ignores clamping and the Departure question).
for ax in ("cr", "bs", "fb"):
    deltas = [[d for li, ci in enumerate(p) for a, d in LAYERS[li][ci][3].values() if a == ax]
              for p in paths]
    gain = max(sum(d for d in ds if d > 0) for ds in deltas)
    drop = min(sum(d for d in ds if d < 0) for ds in deltas)
    print(f"{ax}: max reachable ~{AXIS_STARTS[ax] + gain}, max drop {drop}")

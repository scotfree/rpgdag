"""Data model for game_config.json. See mvp_implement.md §4.1."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Axis:
    id: str
    name: str
    start: int


@dataclass
class Impact:
    axis: str
    delta: int


@dataclass
class Question:
    id: str
    text: str
    yes: list[Impact]
    no: list[Impact]


@dataclass
class Node:
    id: str
    name: str
    premise: str
    questions: list[Question]


@dataclass
class Requirement:
    question: str
    answer: str  # "yes" | "no"


@dataclass
class Edge:
    id: str
    from_: str
    to: str
    name: str
    flavor: str
    requires: list[Requirement]
    impacts: list[Impact]


@dataclass
class EndingClause:
    axis: str
    op: str
    value: int


@dataclass
class Ending:
    when: list[EndingClause]
    party_result: str  # "win" | "loss"
    text: str


@dataclass
class Terminal:
    id: str
    name: str
    premise: str
    endings: list[Ending]
    questions: list[Question] = field(default_factory=list)


@dataclass
class GoalCard:
    id: str
    name: str
    vp: int
    conditions: list[dict]  # heterogeneous; interpreted by score.py


@dataclass
class Meta:
    name: str
    description: str
    start_node: str
    players: list[str]


@dataclass
class Config:
    meta: Meta
    axes: list[Axis]
    nodes: list[Node]
    edges: list[Edge]
    terminals: list[Terminal]
    goal_cards: list[GoalCard]


def _impacts(raw: list[dict]) -> list[Impact]:
    return [Impact(axis=i["axis"], delta=i["delta"]) for i in raw]


def _questions(raw: list[dict]) -> list[Question]:
    return [
        Question(id=q["id"], text=q["text"], yes=_impacts(q["yes"]), no=_impacts(q["no"]))
        for q in raw
    ]


def config_from_dict(data: dict) -> Config:
    meta = Meta(
        name=data["meta"]["name"],
        description=data["meta"].get("description", ""),
        start_node=data["meta"]["start_node"],
        players=data["meta"].get("players", []),
    )
    axes = [Axis(id=a["id"], name=a["name"], start=a["start"]) for a in data["axes"]]
    nodes = [
        Node(id=n["id"], name=n["name"], premise=n["premise"], questions=_questions(n["questions"]))
        for n in data["nodes"]
    ]
    edges = [
        Edge(
            id=e["id"],
            from_=e["from"],
            to=e["to"],
            name=e["name"],
            flavor=e.get("flavor", ""),
            requires=[Requirement(question=r["question"], answer=r["answer"]) for r in e.get("requires", [])],
            impacts=_impacts(e.get("impacts", [])),
        )
        for e in data["edges"]
    ]
    terminals = [
        Terminal(
            id=t["id"],
            name=t["name"],
            premise=t.get("premise", ""),
            endings=[
                Ending(
                    when=[EndingClause(axis=c["axis"], op=c["op"], value=c["value"]) for c in e["when"]],
                    party_result=e["party_result"],
                    text=e["text"],
                )
                for e in t["endings"]
            ],
            questions=_questions(t.get("questions", [])),
        )
        for t in data["terminals"]
    ]
    goal_cards = [
        GoalCard(id=g["id"], name=g["name"], vp=g["vp"], conditions=g["conditions"])
        for g in data.get("goal_cards", [])
    ]
    return Config(meta=meta, axes=axes, nodes=nodes, edges=edges, terminals=terminals, goal_cards=goal_cards)


def load_config(path: str | Path) -> Config:
    with open(path) as f:
        return config_from_dict(json.load(f))

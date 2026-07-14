"""GM view HTML generation. See mvp_implement.md §7.

Renders the full DAG with Cytoscape.js + dagre (CDN). Node premise on hover,
questions in a popup on click, axes displayed across the top.
"""

from __future__ import annotations

import html
import json
from pathlib import Path
from string import Template

from .model import Config, Impact

_OPS = {">=": "≥", "<=": "≤", "==": "=", ">": ">", "<": "<"}


def _fmt_impacts(impacts: list[Impact], axis_names: dict[str, str]) -> str:
    if not impacts:
        return "no impact"
    parts = []
    for i in impacts:
        sign = "+" if i.delta > 0 else "−"
        parts.append(f"{axis_names[i.axis]} {sign}{abs(i.delta)}")
    return ", ".join(parts)


def _axes_tiles(config: Config) -> str:
    tiles = []
    for axis in config.axes:
        cells = "".join(
            f'<span class="cell{" filled" if i < axis.start else ""}"></span>' for i in range(10)
        )
        tiles.append(
            f'<div class="axis-tile">'
            f'<div class="axis-name">{html.escape(axis.name)}</div>'
            f'<div class="axis-value">{axis.start}</div>'
            f'<div class="axis-meter">{cells}</div>'
            f"</div>"
        )
    return "\n".join(tiles)


def _question_block(q, axis_names: dict[str, str]) -> str:
    return (
        f'<div class="q"><div class="q-text">{html.escape(q.text)}</div>'
        f'<div class="q-side"><span class="ans">Yes</span> {html.escape(_fmt_impacts(q.yes, axis_names))}</div>'
        f'<div class="q-side"><span class="ans">No</span> {html.escape(_fmt_impacts(q.no, axis_names))}</div>'
        f"</div>"
    )


def _build_graph_data(config: Config) -> tuple[list[dict], dict[str, dict]]:
    """Cytoscape elements plus per-element hover/click HTML, keyed by element id."""
    axis_names = {a.id: a.name for a in config.axes}
    questions_by_node = {n.id: {q.id: q for q in n.questions} for n in config.nodes}

    elements = []
    details = {}

    for node in config.nodes:
        elements.append(
            {"data": {"id": node.id, "label": node.name, "kind": "scene",
                      "start": "yes" if node.id == config.meta.start_node else "no"}}
        )
        details[node.id] = {
            "title": node.name,
            "hover": f"<p>{html.escape(node.premise)}</p>",
            "click": (
                f'<p class="premise">{html.escape(node.premise)}</p>'
                + "".join(_question_block(q, axis_names) for q in node.questions)
            ),
        }

    for term in config.terminals:
        elements.append(
            {"data": {"id": term.id, "label": term.name, "kind": "terminal", "start": "no"}}
        )
        endings_html = []
        for e in term.endings:
            if e.when:
                cond = " and ".join(
                    f"{axis_names[c.axis]} {_OPS[c.op]} {c.value}" for c in e.when
                )
            else:
                cond = "Otherwise"
            endings_html.append(
                f'<div class="q"><div class="q-text">{html.escape(cond)}</div>'
                f'<div class="q-side"><span class="ans {e.party_result}">{e.party_result.upper()}</span> '
                f"{html.escape(e.text)}</div></div>"
            )
        details[term.id] = {
            "title": term.name,
            "hover": f"<p>{html.escape(term.premise)}</p>",
            "click": (
                f'<p class="premise">{html.escape(term.premise)}</p>'
                + "".join(_question_block(q, axis_names) for q in term.questions)
                + "".join(endings_html)
            ),
        }

    for edge in config.edges:
        gated = "yes" if edge.requires else "no"
        elements.append(
            {"data": {"id": edge.id, "source": edge.from_, "target": edge.to,
                      "label": edge.name, "gated": gated}}
        )
        lines = [f"<p><em>{html.escape(edge.flavor)}</em></p>"]
        for r in edge.requires:
            q = questions_by_node.get(edge.from_, {}).get(r.question)
            q_text = q.text if q else r.question
            lines.append(
                f'<p class="req">Requires: “{html.escape(q_text)}” = {r.answer}</p>'
            )
        lines.append(f"<p>Impacts: {html.escape(_fmt_impacts(edge.impacts, axis_names))}</p>")
        details[edge.id] = {"title": edge.name, "hover": "".join(lines), "click": None}

    return elements, details


_TEMPLATE = Template("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title — GM View</title>
<script src="https://unpkg.com/cytoscape@3.30.2/dist/cytoscape.min.js"></script>
<script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
<style>
  :root {
    --page: #f9f9f7;
    --surface: #fcfcfb;
    --ink: #0b0b0b;
    --ink-2: #52514e;
    --muted: #898781;
    --hairline: #e1e0d9;
    --border: rgba(11, 11, 11, 0.10);
    --meter-fill: #2a78d6;
    --scene-fill: #2a78d6;
    --scene-text: #ffffff;
    --terminal-fill: #4a3aa7;
    --terminal-text: #ffffff;
    --start-ring: #eda100;
    --edge-line: #c3c2b7;
    --win: #006300;
    --loss: #d03b3b;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --page: #0d0d0d;
      --surface: #1a1a19;
      --ink: #ffffff;
      --ink-2: #c3c2b7;
      --muted: #898781;
      --hairline: #2c2c2a;
      --border: rgba(255, 255, 255, 0.10);
      --meter-fill: #3987e5;
      --scene-fill: #3987e5;
      --terminal-fill: #9085e9;
      --terminal-text: #1a1a19;
      --start-ring: #c98500;
      --edge-line: #383835;
      --win: #0ca30c;
    }
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; }
  body {
    margin: 0;
    background: var(--page);
    color: var(--ink);
    font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
    display: flex;
    flex-direction: column;
  }
  header {
    padding: 14px 20px 10px;
    border-bottom: 1px solid var(--hairline);
    background: var(--surface);
  }
  .head-row { display: flex; align-items: flex-start; gap: 24px; flex-wrap: wrap; }
  .title-block { min-width: 200px; }
  h1 { font-size: 18px; margin: 0; }
  .subtitle { color: var(--ink-2); font-size: 13px; margin-top: 2px; }
  .axes { display: flex; gap: 12px; flex-wrap: wrap; margin-left: auto; }
  .axis-tile {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 14px 10px;
    display: grid;
    grid-template-columns: auto auto;
    grid-template-areas: "name value" "meter meter";
    column-gap: 12px;
    align-items: baseline;
  }
  .axis-name { grid-area: name; color: var(--ink-2); font-size: 12px; }
  .axis-value { grid-area: value; font-size: 24px; font-weight: 600; justify-self: end; }
  .axis-meter { grid-area: meter; display: flex; gap: 2px; margin-top: 6px; }
  .cell { width: 12px; height: 6px; border-radius: 2px; background: var(--hairline); }
  .cell.filled { background: var(--meter-fill); }
  .legend { display: flex; gap: 16px; margin-top: 8px; font-size: 11px; color: var(--muted); }
  .legend span { display: inline-flex; align-items: center; gap: 5px; }
  .swatch { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
  .swatch.scene { background: var(--scene-fill); }
  .swatch.terminal { background: var(--terminal-fill); }
  .swatch.start { background: var(--scene-fill); outline: 2px solid var(--start-ring); }
  .dash {
    width: 18px; height: 0; display: inline-block;
    border-top: 2px dashed var(--muted);
  }
  #cy { flex: 1; min-height: 0; }
  #tooltip {
    position: fixed;
    display: none;
    max-width: 320px;
    background: var(--surface);
    color: var(--ink);
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.18);
    padding: 10px 12px;
    font-size: 13px;
    pointer-events: none;
    z-index: 10;
  }
  #tooltip h3 { margin: 0 0 4px; font-size: 13px; }
  #tooltip p { margin: 4px 0; color: var(--ink-2); }
  #tooltip .req { color: var(--muted); }
  #overlay {
    position: fixed;
    inset: 0;
    display: none;
    background: rgba(0, 0, 0, 0.35);
    z-index: 20;
    align-items: center;
    justify-content: center;
  }
  #modal {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    max-width: 480px;
    width: calc(100% - 40px);
    max-height: 80vh;
    overflow-y: auto;
    padding: 18px 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }
  #modal h2 { margin: 0 0 6px; font-size: 16px; }
  #modal .premise { color: var(--ink-2); font-size: 13px; margin: 0 0 12px; }
  .q { border-top: 1px solid var(--hairline); padding: 10px 0; font-size: 13px; }
  .q-text { font-weight: 600; margin-bottom: 4px; }
  .q-side { color: var(--ink-2); margin: 2px 0; }
  .ans {
    display: inline-block;
    min-width: 34px;
    font-weight: 600;
    color: var(--ink);
  }
  .ans.win { color: var(--win); }
  .ans.loss { color: var(--loss); }
  .hint { color: var(--muted); font-size: 11px; margin-top: 10px; }
</style>
</head>
<body>
<header>
  <div class="head-row">
    <div class="title-block">
      <h1>$title <span style="color: var(--muted); font-weight: 400;">· GM View</span></h1>
      <div class="subtitle">$description</div>
    </div>
    <div class="axes">
$axes_tiles
    </div>
  </div>
  <div class="legend">
    <span><i class="swatch start"></i> Start</span>
    <span><i class="swatch scene"></i> Scene</span>
    <span><i class="swatch terminal"></i> Terminal</span>
    <span><i class="dash"></i> Gated edge (requires an answer)</span>
    <span>Hover for premise · click a node for its questions</span>
  </div>
</header>
<div id="cy"></div>
<div id="tooltip"></div>
<div id="overlay"><div id="modal"></div></div>
<script>
  var ELEMENTS = $elements;
  var DETAILS = $details;

  var css = getComputedStyle(document.documentElement);
  function v(name) { return css.getPropertyValue(name).trim(); }

  var cy = cytoscape({
    container: document.getElementById("cy"),
    elements: ELEMENTS,
    layout: { name: "dagre", rankDir: "LR", nodeSep: 90, rankSep: 170, padding: 30 },
    maxZoom: 2,
    autoungrabify: true,
    style: [
      { selector: "node", style: {
          "shape": "round-rectangle",
          "label": "data(label)",
          "background-color": v("--scene-fill"),
          "color": v("--scene-text"),
          "font-size": 13,
          "font-family": "system-ui, sans-serif",
          "text-valign": "center",
          "text-halign": "center",
          "width": "label",
          "height": "label",
          "padding": "14px"
      }},
      { selector: 'node[kind="terminal"]', style: {
          "background-color": v("--terminal-fill"),
          "color": v("--terminal-text")
      }},
      { selector: 'node[start="yes"]', style: {
          "border-width": 3,
          "border-color": v("--start-ring")
      }},
      { selector: "edge", style: {
          "curve-style": "bezier",
          "control-point-step-size": 60,
          "width": 2,
          "line-color": v("--edge-line"),
          "target-arrow-color": v("--edge-line"),
          "target-arrow-shape": "triangle",
          "label": "data(label)",
          "font-size": 11,
          "font-family": "system-ui, sans-serif",
          "color": v("--ink-2"),
          "text-rotation": "autorotate",
          "text-background-color": v("--page"),
          "text-background-opacity": 1,
          "text-background-padding": "3px"
      }},
      { selector: 'edge[gated="yes"]', style: {
          "line-style": "dashed"
      }}
    ]
  });

  var tooltip = document.getElementById("tooltip");
  var overlay = document.getElementById("overlay");
  var modal = document.getElementById("modal");

  cy.on("mouseover", "node, edge", function (evt) {
    var d = DETAILS[evt.target.id()];
    if (!d) return;
    tooltip.innerHTML = "<h3>" + d.title + "</h3>" + d.hover;
    tooltip.style.display = "block";
  });
  cy.on("mousemove", "node, edge", function (evt) {
    var e = evt.originalEvent;
    var pad = 14;
    var x = e.clientX + pad, y = e.clientY + pad;
    var r = tooltip.getBoundingClientRect();
    if (x + r.width > window.innerWidth - 8) x = e.clientX - r.width - pad;
    if (y + r.height > window.innerHeight - 8) y = e.clientY - r.height - pad;
    tooltip.style.left = x + "px";
    tooltip.style.top = y + "px";
  });
  cy.on("mouseout", "node, edge", function () {
    tooltip.style.display = "none";
  });
  cy.on("tap", "node", function (evt) {
    var d = DETAILS[evt.target.id()];
    if (!d || !d.click) return;
    tooltip.style.display = "none";
    modal.innerHTML = "<h2>" + d.title + "</h2>" + d.click;
    overlay.style.display = "flex";
  });
  overlay.addEventListener("click", function (evt) {
    if (evt.target === overlay) overlay.style.display = "none";
  });
  document.addEventListener("keydown", function (evt) {
    if (evt.key === "Escape") overlay.style.display = "none";
  });
</script>
</body>
</html>
""")


def render_gm_view(config: Config) -> str:
    elements, details = _build_graph_data(config)
    return _TEMPLATE.safe_substitute(
        title=html.escape(config.meta.name),
        description=html.escape(config.meta.description),
        axes_tiles=_axes_tiles(config),
        elements=json.dumps(elements).replace("</", "<\\/"),
        details=json.dumps(details).replace("</", "<\\/"),
    )


def write_views(config: Config, out_dir: str | Path) -> list[Path]:
    """Write all views into out_dir; returns written paths. (Player view: issue #TBD.)"""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    gm_path = out / "gm_view.html"
    gm_path.write_text(render_gm_view(config))
    return [gm_path]

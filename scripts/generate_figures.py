#!/usr/bin/env python3
"""Generate deterministic SVG figures for the experimental agentic CMMS paper.

The figures are intentionally generated from small JSON data files so the paper
can be versioned, reviewed, and changed without manual graphics editing.
"""

from __future__ import annotations

import html
import json
import math
import textwrap
from pathlib import Path
from typing import Iterable, Sequence

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"

COLORS = {
    "navy": "#0f172a",
    "muted": "#475569",
    "soft": "#f8fafc",
    "line": "#cbd5e1",
    "grid": "#e2e8f0",
    "blue": "#2563eb",
    "blue2": "#dbeafe",
    "green": "#059669",
    "green2": "#d1fae5",
    "amber": "#d97706",
    "amber2": "#fef3c7",
    "purple": "#7c3aed",
    "purple2": "#ede9fe",
    "red": "#dc2626",
    "red2": "#fee2e2",
    "teal": "#0f766e",
    "teal2": "#ccfbf1",
    "orange": "#ea580c",
    "orange2": "#ffedd5",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap_text(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for para in str(text).split("\n"):
        if not para:
            lines.append("")
        else:
            lines.extend(textwrap.wrap(para, width=width, break_long_words=False))
    return lines


def svg_root(width: int, height: int, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#eff6ff"/>
    </linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#f8fbff"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#2563eb"/>
    </marker>
  </defs>
  <rect width="{width}" height="{height}" rx="34" fill="url(#bg)"/>
  {body}
</svg>
'''


def text(x: float, y: float, content: str, size: int = 18, weight: int | str = 400,
         fill: str = COLORS["navy"], anchor: str = "start", family: str = "Inter, Segoe UI, Arial, sans-serif") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(content)}</text>'


def lines(x: float, y: float, content: str, width: int, size: int = 17,
          fill: str = COLORS["muted"], weight: int | str = 400, line_height: int | None = None,
          anchor: str = "start", max_lines: int | None = None) -> str:
    line_height = line_height or int(size * 1.35)
    wrapped = wrap_text(content, width)
    if max_lines is not None and len(wrapped) > max_lines:
        wrapped = wrapped[: max_lines]
        if wrapped:
            wrapped[-1] = wrapped[-1].rstrip(" .,") + "..."
    out = []
    for i, ln in enumerate(wrapped):
        out.append(text(x, y + i * line_height, ln, size, weight, fill, anchor))
    return "\n".join(out)


def rect(x: float, y: float, w: float, h: float, rx: float = 18, fill: str = "#ffffff",
         stroke: str = COLORS["line"], sw: float = 1.4, extra: str = "") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'


def circle(x: float, y: float, r: float, fill: str = COLORS["blue2"], stroke: str = COLORS["blue"], sw: float = 1.5) -> str:
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1: float, y1: float, x2: float, y2: float, color: str = COLORS["blue"], sw: float = 3,
         dashed: bool = False, arrow: bool = False) -> str:
    dash = ' stroke-dasharray="8 8"' if dashed else ""
    marker = ' marker-end="url(#arrow)"' if arrow else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{dash}{marker}/>'


def pill(x: float, y: float, w: float, h: float, label: str, fill: str = "#eff6ff", stroke: str = "#bfdbfe", color: str = COLORS["navy"], size: int = 15) -> str:
    return rect(x, y, w, h, h / 2, fill, stroke, 1.2) + text(x + w / 2, y + h / 2 + size / 3, label, size, 600, color, "middle")


def metric_bar(x: float, y: float, w: float, label: str, value: float, max_value: float = 5.0) -> str:
    pct = max(0.0, min(1.0, value / max_value))
    color = COLORS["green"] if value >= 4 else COLORS["blue"] if value >= 3 else COLORS["amber"]
    return "\n".join([
        text(x, y, label, 14, 600, COLORS["muted"]),
        rect(x, y + 9, w, 9, 4.5, "#e2e8f0", "#e2e8f0", 0),
        rect(x, y + 9, w * pct, 9, 4.5, color, color, 0),
        text(x + w + 8, y + 17, f"{value:.0f}", 13, 700, color),
    ])


def title_block(title: str, subtitle: str, w: int) -> str:
    return "\n".join([
        text(44, 70, title, 42, 800, COLORS["navy"]),
        lines(46, 104, subtitle, 120, 18, COLORS["muted"], 400, 26),
        line(44, 130, w - 44, 130, "#dbeafe", 2),
    ])


def create_value_loop() -> None:
    width, height = 1500, 900
    steps = [
        ("1", "Signal intake", "Work requests, alarms, inspections, operator notes", "Normalized incident", "#dbeafe", COLORS["blue"]),
        ("2", "Context retrieval", "Assets, history, PMs, parts, policies, manuals", "Grounded context", "#e0f2fe", "#0284c7"),
        ("3", "Agent collaboration", "Specialists exchange evidence and challenge assumptions", "Shared findings", "#ecfdf5", COLORS["green"]),
        ("4", "Debate + policy gate", "Risk, compliance, budget, approval and write permissions", "Validated recommendation", "#fff7ed", COLORS["orange"]),
        ("5", "Recommendation package", "Draft WO, parts, options, trade-offs, confidence", "Planner-ready package", "#f5f3ff", COLORS["purple"]),
        ("6", "Approval / bounded automation", "Human review or low-risk auto-execution", "Approved action", "#f0fdf4", COLORS["green"]),
        ("7", "Learning + audit", "Outcome, feedback, traceability, policy/model improvement", "Better future runs", "#eff6ff", COLORS["blue"]),
    ]
    body = [title_block("Future CMMS/EAM as a Multi-Agent Value Loop", "A controlled loop for sensing, reasoning, deciding, and learning across maintenance operations.", width)]
    x_positions = [55, 260, 465, 860, 260, 565, 870]
    y_positions = [175, 175, 175, 175, 545, 545, 545]
    card_w, card_h = 175, 230
    for idx, ((num, name, desc, out, fill, color), x, y) in enumerate(zip(steps, x_positions, y_positions)):
        if num == "3":
            body.append(rect(x, y, 350, card_h, 24, "url(#card)", color, 1.7, 'filter="url(#shadow)"'))
            body.append(circle(x + 30, y + 34, 20, fill, color))
            body.append(text(x + 30, y + 41, num, 18, 800, color, "middle"))
            body.append(text(x + 65, y + 45, name, 24, 800, COLORS["navy"]))
            body.append(lines(x + 25, y + 83, desc, 44, 15, COLORS["muted"], 400, 21, max_lines=2))
            agents = [("Intake", COLORS["blue2"], COLORS["blue"]), ("Asset", COLORS["green2"], COLORS["green"]), ("Inventory", COLORS["amber2"], COLORS["amber"]), ("Policy", COLORS["purple2"], COLORS["purple"])]
            for j, (a, afill, acolor) in enumerate(agents):
                ax = x + 22 + j * 78
                body.append(rect(ax, y + 130, 68, 54, 12, afill, acolor, 1.1))
                body.append(text(ax + 34, y + 163, a, 13, 800, acolor, "middle"))
                if j < len(agents) - 1:
                    body.append(line(ax + 68, y + 157, ax + 78, y + 157, COLORS["line"], 1.5, dashed=True, arrow=True))
            body.append(pill(x + 70, y + 196, 210, 28, out, "#f8fafc", COLORS["line"], COLORS["navy"], 13))
        else:
            body.append(rect(x, y, card_w, card_h, 24, "url(#card)", color, 1.5, 'filter="url(#shadow)"'))
            body.append(circle(x + 30, y + 34, 20, fill, color))
            body.append(text(x + 30, y + 41, num, 18, 800, color, "middle"))
            body.append(lines(x + 22, y + 72, name, 18, 22, COLORS["navy"], 800, 27, max_lines=2))
            body.append(lines(x + 22, y + 130, desc, 24, 14, COLORS["muted"], 400, 20, max_lines=3))
            body.append(pill(x + 18, y + 188, card_w - 36, 30, out, fill, color, COLORS["navy"], 12))
    # Connectors
    body.append(line(230, 290, 258, 290, arrow=True))
    body.append(line(435, 290, 463, 290, arrow=True))
    body.append(line(815, 290, 858, 290, arrow=True))
    body.append(line(948, 405, 348, 545, COLORS["blue"], 2.5, dashed=True, arrow=True))
    body.append(line(435, 660, 563, 660, arrow=True))
    body.append(line(740, 660, 868, 660, arrow=True))
    # Feedback loop
    body.append(f'<path d="M1045 660 C1300 760, 1320 835, 1450 835 L1450 850 L80 850 C45 850, 45 810, 45 760 L45 425" fill="none" stroke="#2563eb" stroke-width="4" stroke-linecap="round" marker-end="url(#arrow)" opacity="0.8"/>')
    body.append(rect(360, 810, 780, 52, 26, COLORS["blue"], COLORS["blue"], 0))
    body.append(text(750, 842, "Continuous improvement: better data -> better decisions -> better outcomes", 18, 800, "#ffffff", "middle"))
    # Side panel
    sx, sy = 1110, 175
    body.append(rect(sx, sy, 335, 600, 26, "url(#card)", COLORS["line"], 1.4, 'filter="url(#shadow)"'))
    body.append(text(sx + 34, sy + 55, "Why MAS beats", 26, 800, COLORS["navy"]))
    body.append(text(sx + 34, sy + 86, "single-agent AI", 26, 800, COLORS["navy"]))
    benefits = [
        ("Better decomposition", "Complex requests split into testable expert tasks."),
        ("Grounded decisions", "Each agent cites system data, policies, or evidence."),
        ("Safer write actions", "Policy and human gates stand before side effects."),
        ("Controllable cost", "Budgets, timeouts, and tool-call limits are explicit."),
        ("Learning loop", "Outcomes improve agents, rules, and retrieval."),
    ]
    for i, (b, d) in enumerate(benefits):
        yy = sy + 130 + i * 87
        body.append(circle(sx + 47, yy + 17, 20, COLORS["blue2"], COLORS["blue"] if i % 2 == 0 else COLORS["green"]))
        body.append(text(sx + 47, yy + 24, str(i + 1), 15, 800, COLORS["blue"], "middle"))
        body.append(text(sx + 82, yy + 10, b, 17, 800, COLORS["navy"]))
        body.append(lines(sx + 82, yy + 34, d, 32, 13, COLORS["muted"], 400, 17, max_lines=2))
    body.append(lines(70, 882, "Generated from scripts/generate_figures.py. Conceptual diagram; not an operational claim.", 150, 13, "#64748b", 400, 18))
    (ASSETS / "mas-value-loop-expanded.svg").write_text(svg_root(width, height, "\n".join(body)), encoding="utf-8")


def create_china_exemplars() -> None:
    data = json.loads((DATA / "china_industrial_examples.json").read_text(encoding="utf-8"))
    examples = data["examples"]
    width, height = 1600, 1020
    body = [title_block("Chinese Industrial Exemplars for Agentic CMMS/EAM", "Public digitalization signals mapped to future multi-agent maintenance and asset-management patterns.", width)]
    card_w, card_h = 286, 270
    start_x, start_y = 55, 175
    gap_x, gap_y = 26, 30
    colors = [COLORS["blue"], COLORS["green"], COLORS["amber"], COLORS["purple"], COLORS["teal"], COLORS["orange"], COLORS["blue"], COLORS["green"]]
    for i, ex in enumerate(examples):
        row, col = divmod(i, 4)
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        color = colors[i]
        fill = [COLORS["blue2"], COLORS["green2"], COLORS["amber2"], COLORS["purple2"], COLORS["teal2"], COLORS["orange2"], COLORS["blue2"], COLORS["green2"]][i]
        body.append(rect(x, y, card_w, card_h, 24, "url(#card)", color, 1.2, 'filter="url(#shadow)"'))
        body.append(circle(x + 34, y + 36, 20, fill, color))
        body.append(text(x + 34, y + 43, str(i + 1), 17, 800, color, "middle"))
        body.append(lines(x + 65, y + 42, ex["company"], 18, 24, COLORS["navy"], 800, 28, max_lines=2))
        body.append(line(x + 22, y + 80, x + card_w - 22, y + 80, "#e2e8f0", 1.2))
        body.append(text(x + 22, y + 112, "Sector", 14, 800, color))
        body.append(lines(x + 22, y + 136, ex["sector"], 36, 13, COLORS["muted"], 400, 17, max_lines=2))
        body.append(text(x + 22, y + 177, "Public digital / AI signal", 14, 800, color))
        body.append(lines(x + 22, y + 201, ex["public_signal"], 36, 13, COLORS["muted"], 400, 17, max_lines=3))
        # mini score bars
        sx = x + 22
        sy = y + 248
        avg = sum(ex["scores"]) / len(ex["scores"])
        body.append(rect(sx, sy, 180, 8, 4, "#e2e8f0", "#e2e8f0", 0))
        body.append(rect(sx, sy, 180 * avg / 5, 8, 4, color, color, 0))
        body.append(text(sx + 190, sy + 8, f"MAS fit {avg:.1f}/5", 12, 800, color))
    # Right-side insight panel
    sx, sy = 1315, 175
    body.append(rect(sx, sy, 230, 570, 26, "#ffffff", COLORS["line"], 1.4, 'filter="url(#shadow)"'))
    body.append(text(sx + 28, sy + 46, "Why China", 24, 800, COLORS["navy"]))
    body.append(text(sx + 28, sy + 76, "matters", 24, 800, COLORS["navy"]))
    bullets = [
        ("Huge installed base", "More assets, more histories, more repeat patterns."),
        ("Fast digitalization", "Industrial Internet, 5G, IoT, AI, cloud and edge adoption."),
        ("Policy direction", "Made in China 2025 prioritized intelligent manufacturing."),
        ("Safety pressure", "Grid, rail, petrochemical and steel assets need guardrails."),
        ("Human + AI fit", "Skilled planners can supervise agent recommendations."),
    ]
    for j, (h, d) in enumerate(bullets):
        yy = sy + 120 + j * 84
        body.append(circle(sx + 32, yy + 12, 16, COLORS["blue2"], COLORS["blue"] if j < 3 else COLORS["green"]))
        body.append(text(sx + 32, yy + 18, str(j + 1), 12, 800, COLORS["blue"], "middle"))
        body.append(text(sx + 58, yy + 5, h, 15, 800, COLORS["navy"]))
        body.append(lines(sx + 58, yy + 27, d, 23, 12, COLORS["muted"], 400, 16, max_lines=2))
    # Footer
    body.append(rect(55, 875, 1490, 86, 22, "#f8fafc", COLORS["line"], 1.2))
    body.append(text(82, 910, "Important boundary", 18, 800, COLORS["navy"]))
    body.append(lines(82, 938, "The chart maps public signals to a future CMMS/EAM architecture. It does not claim that any listed company operates this exact multi-agent system today.", 160, 15, COLORS["muted"], 400, 20))
    (ASSETS / "china-industrial-exemplars.svg").write_text(svg_root(width, height, "\n".join(body)), encoding="utf-8")


def create_made_in_china_roadmap() -> None:
    width, height = 2200, 1040
    body = [title_block("Made in China 2025 as a Launchpad for Agentic EAM", "From policy-led intelligent manufacturing to future CMMS/EAM systems that reason across assets, parts, people, and risk.", width)]
    # Timeline
    x0, x1, y = 340, 1580, 170
    body.append(line(x0, y, x1, y, COLORS["blue"], 4, arrow=True))
    years = ["2015", "2020", "2025", "2030+"]
    xs = [x0, 750, 1160, 1570]
    for yr, x in zip(years, xs):
        body.append(circle(x, y, 14, COLORS["blue"], COLORS["blue"], 0))
        body.append(text(x, y - 26, yr, 24, 800, COLORS["blue"], "middle"))
        body.append(line(x, y + 25, x, 875, "#bfdbfe", 1.4, dashed=True))
    lanes = [
        ("1", "Policy and industrial strategy", "State Council launches Made in China 2025", "Wider adoption of industrial Internet and smart-factory pilots", "Intelligent manufacturing becomes mainstream in more sectors", "2030+ vision: multi-agent CMMS/EAM with bounded autonomy"),
        ("2", "Enterprise digital capability", "Digitization begins: asset data, standards, governance", "Platformization: IIoT, data platforms, analytics, edge", "AI and analytics at scale: monitoring, prediction, compliance", "Autonomous operations ready: digital twins and cross-functional agents"),
        ("3", "CMMS/EAM evolution", "Traditional CMMS: WOs, PMs, spares, basic reporting", "Integrated EAM: mobile, IoT, condition monitoring", "Intelligent EAM: predictive, policy-aware, risk-based workflows", "Agentic EAM: planning, scheduling, MRO optimization, explainability")
    ]
    lane_y = [230, 465, 700]
    cell_w, cell_h = 300, 170
    for row, lane in enumerate(lanes):
        num, lane_title, *cells = lane
        ly = lane_y[row]
        body.append(rect(45, ly, 220, cell_h, 24, "#eff6ff", "#bfdbfe", 1.2))
        body.append(circle(72, ly + 34, 18, COLORS["blue"], COLORS["blue"], 0))
        body.append(text(72, ly + 41, num, 15, 800, "#ffffff", "middle"))
        body.append(lines(95, ly + 50, lane_title, 15, 18, COLORS["navy"], 800, 24, max_lines=4))
        for col, cell in enumerate(cells):
            x = 325 + col * 410
            body.append(rect(x, ly, cell_w, cell_h, 22, "#ffffff", COLORS["line"], 1.2, 'filter="url(#shadow)"'))
            accent = [COLORS["blue"], COLORS["teal"], COLORS["green"], COLORS["purple"]][col]
            body.append(circle(x + 32, ly + 38, 19, "#f8fafc", accent))
            body.append(text(x + 32, ly + 45, str(col + 1), 14, 800, accent, "middle"))
            body.append(lines(x + 65, ly + 48, cell, 29, 15, COLORS["navy"], 700, 21, max_lines=5))
    # Side sector panel
    sx, sy = 1870, 210
    body.append(rect(sx, sy, 285, 415, 24, "#ffffff", COLORS["line"], 1.2, 'filter="url(#shadow)"'))
    body.append(text(sx + 142, sy + 38, "Priority sectors", 20, 800, COLORS["navy"], "middle"))
    sectors = json.loads((DATA / "made_in_china_2025_mapping.json").read_text(encoding="utf-8"))["priority_sectors"]
    for i, s in enumerate(sectors):
        py = sy + 62 + i * 32
        body.append(pill(sx + 22, py, 241, 24, s, "#f8fafc", "#bfdbfe", COLORS["navy"], 12))
    # Meaning panel
    sy2 = 655
    body.append(rect(sx, sy2, 285, 240, 24, "#ffffff", COLORS["line"], 1.2, 'filter="url(#shadow)"'))
    body.append(text(sx + 24, sy2 + 38, "What this means", 20, 800, COLORS["navy"]))
    body.append(text(sx + 24, sy2 + 64, "for CMMS/EAM", 20, 800, COLORS["navy"]))
    implications = ["More connected assets", "More complex compliance", "Higher uptime expectations", "Explainable automation", "Cross-agent collaboration"]
    for i, imp in enumerate(implications):
        yy = sy2 + 96 + i * 27
        body.append(circle(sx + 32, yy - 5, 10, COLORS["blue"], COLORS["blue"], 0))
        body.append(text(sx + 52, yy, imp, 13, 700, COLORS["muted"]))
    body.append(rect(45, 940, 2110, 58, 22, "#eff6ff", "#bfdbfe", 1.2))
    body.append(lines(72, 974, "2015-2025 is treated here as the policy and digitalization foundation; 2030+ is a forward-looking platform vision for agentic EAM, not an official policy forecast.", 230, 15, COLORS["muted"], 400, 20))
    (ASSETS / "made-in-china-2025-agentic-eam-roadmap.svg").write_text(svg_root(width, height, "\n".join(body)), encoding="utf-8")


def create_leverage_matrix() -> None:
    data = json.loads((DATA / "use_case_scores.json").read_text(encoding="utf-8"))
    cases = data["use_cases"]
    width, height = 1350, 820
    body = [title_block("High-Leverage Maintenance Use Cases for Multi-Agent AI", "Illustrative prioritization framework for future CMMS/EAM programs.", width)]
    left, top, plot_w, plot_h = 95, 185, 850, 500
    body.append(rect(left - 45, top - 35, plot_w + 90, plot_h + 90, 24, "#ffffff", COLORS["line"], 1.2, 'filter="url(#shadow)"'))
    # Grid and axes
    for i in range(1, 7):
        x = left + plot_w * i / 7
        y = top + plot_h * i / 7
        body.append(line(x, top, x, top + plot_h, COLORS["grid"], 1, dashed=True))
        body.append(line(left, y, left + plot_w, y, COLORS["grid"], 1, dashed=True))
    body.append(line(left, top + plot_h, left + plot_w, top + plot_h, COLORS["blue"], 3.2, arrow=True))
    body.append(line(left, top + plot_h, left, top, COLORS["blue"], 3.2, arrow=True))
    body.append(text(left + plot_w / 2, top + plot_h + 54, "Decision complexity", 22, 800, COLORS["navy"], "middle"))
    body.append(lines(left - 42, top + plot_h / 2 - 8, "Operational\nimpact", 12, 18, COLORS["navy"], 800, 22, "middle"))
    body.append(text(left, top + plot_h + 30, "Low", 16, 700, COLORS["blue"], "middle"))
    body.append(text(left + plot_w, top + plot_h + 30, "High", 16, 700, COLORS["blue"], "middle"))
    body.append(text(left - 28, top + plot_h, "Low", 16, 700, COLORS["blue"], "middle"))
    body.append(text(left - 32, top + 8, "High", 16, 700, COLORS["blue"], "middle"))
    color_by_category = {
        "near-term": (COLORS["purple"], COLORS["purple2"]),
        "diagnostic": (COLORS["teal"], COLORS["teal2"]),
        "safety-critical": (COLORS["blue"], COLORS["blue2"]),
        "optimization": (COLORS["green"], COLORS["green2"]),
    }
    for c in cases:
        x = left + (c["complexity"] - 1) / 6 * plot_w
        y = top + plot_h - (c["impact"] - 1) / 6 * plot_h
        stroke, fill = color_by_category[c["category"]]
        r = 48 if c["category"] == "safety-critical" else 42
        body.append(circle(x, y, r, fill, stroke, 2.0))
        body.append(lines(x, y - 8, c["name"], 14, 12, COLORS["navy"], 800, 14, "middle", max_lines=3))
    # Side panel
    sx, sy = 1010, 185
    body.append(rect(sx, sy, 285, 250, 24, "#f0fdf4", "#bbf7d0", 1.2, 'filter="url(#shadow)"'))
    body.append(text(sx + 28, sy + 44, "Best near-term wins", 22, 800, COLORS["green"]))
    for i, item in enumerate(["Work-order triage", "Policy-aware packages", "Spare-parts coordination", "Inspection scheduling"]):
        yy = sy + 82 + i * 36
        body.append(circle(sx + 34, yy - 5, 11, "#ffffff", COLORS["green"]))
        body.append(text(sx + 34, yy, "鉁?, 12, 800, COLORS["green"], "middle"))
        body.append(text(sx + 56, yy, item, 15, 600, COLORS["muted"]))
    sy2 = 465
    body.append(rect(sx, sy2, 285, 250, 24, "#fff7ed", "#fed7aa", 1.2, 'filter="url(#shadow)"'))
    body.append(text(sx + 28, sy2 + 44, "Needs tighter governance", 22, 800, COLORS["orange"]))
    for i, item in enumerate(["Live write actions", "Shutdown planning", "Rail and grid decisions", "Autonomous optimization"]):
        yy = sy2 + 82 + i * 36
        body.append(text(sx + 34, yy, "鈻?, 20, 800, COLORS["orange"], "middle"))
        body.append(text(sx + 56, yy, item, 15, 600, COLORS["muted"]))
    body.append(rect(55, 740, 1240, 50, 20, "#f8fafc", COLORS["line"], 1.2))
    body.append(text(85, 772, "Legend:", 15, 800, COLORS["navy"]))
    body.append(lines(150, 772, "Lower-left decisions are good starting points. Upper-right decisions create high value but need stronger approval, policy, and audit controls.", 135, 14, COLORS["muted"], 400, 18))
    (ASSETS / "maintenance-use-case-leverage-matrix.svg").write_text(svg_root(width, height, "\n".join(body)), encoding="utf-8")


def heat_color(score: int) -> str:
    palette = {1: "#eff6ff", 2: "#bfdbfe", 3: "#93c5fd", 4: "#60a5fa", 5: "#2563eb"}
    return palette.get(int(score), "#eff6ff")


def create_company_heatmap() -> None:
    data = json.loads((DATA / "china_industrial_examples.json").read_text(encoding="utf-8"))
    examples = data["examples"]
    dims = data["dimensions"]
    width, height = 1500, 880
    body = [title_block("Agentic EAM Fit Matrix for Chinese Industrial Examples", "Illustrative scores show where multi-agent maintenance reasoning has the strongest structural fit.", width)]
    left, top = 300, 200
    cell_w, cell_h = 168, 58
    # Headers
    body.append(rect(55, 175, 1390, 590, 24, "#ffffff", COLORS["line"], 1.2, 'filter="url(#shadow)"'))
    body.append(text(90, 226, "Company", 17, 800, COLORS["navy"]))
    for j, d in enumerate(dims):
        x = left + j * cell_w
        body.append(lines(x + cell_w / 2, 215, d, 18, 13, COLORS["navy"], 800, 15, "middle", max_lines=3))
    for i, ex in enumerate(examples):
        y = top + 55 + i * cell_h
        body.append(text(90, y + 34, ex["company"], 16, 800, COLORS["navy"]))
        body.append(lines(90, y + 56, ex["sector"], 28, 11, COLORS["muted"], 400, 14, max_lines=1))
        for j, s in enumerate(ex["scores"]):
            x = left + j * cell_w
            color = heat_color(s)
            text_fill = "#ffffff" if s >= 4 else COLORS["navy"]
            body.append(rect(x + 8, y, cell_w - 16, 42, 12, color, "#ffffff", 1.0))
            body.append(text(x + cell_w / 2, y + 28, str(s), 18, 800, text_fill, "middle"))
    # Scale legend
    lx, ly = 970, 785
    body.append(text(65, 800, "Scale: 1 = low structural fit, 5 = very strong structural fit. Scores are analytical, not public company KPIs.", 15, 600, COLORS["muted"]))
    for s in range(1, 6):
        body.append(rect(lx + (s - 1) * 46, ly - 18, 36, 24, 6, heat_color(s), "#ffffff", 1))
        body.append(text(lx + (s - 1) * 46 + 18, ly - 1, str(s), 12, 800, "#ffffff" if s >= 4 else COLORS["navy"], "middle"))
    (ASSETS / "china-agentic-eam-fit-heatmap.svg").write_text(svg_root(width, height, "\n".join(body)), encoding="utf-8")


def create_data_flywheel() -> None:
    width, height = 1350, 850
    body = [title_block("Industrial Maintenance Data Flywheel", "How real-world examples translate into repeatable agentic CMMS/EAM capability.", width)]
    cx, cy = 610, 440
    r = 245
    nodes = [
        ("Signals", "IoT, alarms, inspections, images, operator notes"),
        ("Context", "Asset hierarchy, history, PM plans, manuals, policies"),
        ("Agents", "Intake, asset, inventory, policy, risk, schedule"),
        ("Review", "Evidence, disagreement, options, confidence, risk"),
        ("Action", "Approval, work order, parts, schedule, notification"),
        ("Outcome", "Fix result, MTTR, failure recurrence, feedback"),
    ]
    # circular arrows
    body.append(f'<path d="M {cx-r} {cy} A {r} {r} 0 1 1 {cx-r+1} {cy}" fill="none" stroke="#bfdbfe" stroke-width="28" stroke-linecap="round" opacity="0.55"/>')
    for i, (h, d) in enumerate(nodes):
        angle = -math.pi / 2 + i * (2 * math.pi / len(nodes))
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        color = [COLORS["blue"], COLORS["teal"], COLORS["green"], COLORS["amber"], COLORS["purple"], COLORS["orange"]][i]
        fill = [COLORS["blue2"], COLORS["teal2"], COLORS["green2"], COLORS["amber2"], COLORS["purple2"], COLORS["orange2"]][i]
        body.append(circle(x, y, 58, fill, color, 2.0))
        body.append(text(x, y - 5, h, 17, 800, COLORS["navy"], "middle"))
        body.append(lines(x, y + 19, d, 18, 10, COLORS["muted"], 400, 13, "middle", max_lines=2))
    body.append(circle(cx, cy, 100, "#ffffff", COLORS["blue"], 2.0))
    body.append(text(cx, cy - 20, "Agentic", 25, 800, COLORS["navy"], "middle"))
    body.append(text(cx, cy + 12, "CMMS/EAM", 25, 800, COLORS["navy"], "middle"))
    body.append(text(cx, cy + 44, "control plane", 15, 700, COLORS["blue"], "middle"))
    # Right panel with examples
    sx, sy = 945, 220
    body.append(rect(sx, sy, 330, 430, 26, "#ffffff", COLORS["line"], 1.2, 'filter="url(#shadow)"'))
    body.append(text(sx + 32, sy + 46, "Example translations", 23, 800, COLORS["navy"]))
    mapping = [
        ("Midea", "Chiller signals -> energy-aware reliability package"),
        ("State Grid", "Drone defect -> risk-ranked work order"),
        ("CRRC", "Vehicle + depot data -> fleet O&M plan"),
        ("Sinopec", "Plant constraints -> shutdown and permit package"),
        ("SANY", "Equipment telemetry -> field-service coordination"),
    ]
    for i, (h, d) in enumerate(mapping):
        yy = sy + 90 + i * 62
        body.append(circle(sx + 36, yy - 4, 14, COLORS["blue2"], COLORS["blue"]))
        body.append(text(sx + 36, yy + 2, str(i + 1), 11, 800, COLORS["blue"], "middle"))
        body.append(text(sx + 60, yy - 8, h, 15, 800, COLORS["navy"]))
        body.append(lines(sx + 60, yy + 14, d, 32, 12, COLORS["muted"], 400, 16, max_lines=2))
    body.append(rect(70, 730, 1200, 55, 22, "#eff6ff", "#bfdbfe", 1.2))
    body.append(lines(98, 764, "The platform advantage compounds when every approved action feeds outcomes back into asset models, policies, retrieval, and planner trust.", 140, 16, COLORS["navy"], 700, 21))
    (ASSETS / "industrial-maintenance-data-flywheel.svg").write_text(svg_root(width, height, "\n".join(body)), encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    create_value_loop()
    create_china_exemplars()
    create_made_in_china_roadmap()
    create_leverage_matrix()
    create_company_heatmap()
    create_data_flywheel()
    print("Generated SVG figures in", ASSETS)


if __name__ == "__main__":
    main()


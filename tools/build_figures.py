#!/usr/bin/env python3
"""Generate lightweight SVG figures for the NextCMMS MAAI paper.

The script is intentionally dependency-free so the repository can be cloned and
re-rendered in any basic Python 3 environment. The PNG figures in assets/ are
publication-ready images, while these SVGs are editable source-style diagrams.
"""
from __future__ import annotations

import csv
import html
import json
from pathlib import Path
from textwrap import wrap

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"

FONT = "Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, Segoe UI, Arial, sans-serif"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def tspans(text: str, x: float, y: float, width_chars: int = 34, line_height: int = 17,
           klass: str = "small", anchor: str = "start") -> str:
    lines = []
    for part in str(text).split("\n"):
        wrapped = wrap(part, width=width_chars) or [""]
        lines.extend(wrapped)
    out = [f'<text class="{klass}" text-anchor="{anchor}" x="{x}" y="{y}">']
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else line_height
        out.append(f'<tspan x="{x}" dy="{dy}">{esc(line)}</tspan>')
    out.append("</text>")
    return "".join(out)


def svg_header(width: int, height: int) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="NextCMMS MAAI figure">
  <defs>
    <style>
      text {{ font-family: {FONT}; }}
      .title {{ font-size: 32px; font-weight: 800; fill: #0f172a; }}
      .subtitle {{ font-size: 15px; fill: #475569; }}
      .h2 {{ font-size: 18px; font-weight: 800; fill: #0f172a; }}
      .h3 {{ font-size: 14px; font-weight: 800; fill: #1d4ed8; }}
      .small {{ font-size: 12px; fill: #334155; }}
      .tiny {{ font-size: 10.5px; fill: #475569; }}
      .badge {{ font-size: 13px; font-weight: 800; fill: #ffffff; }}
      .card {{ fill: #ffffff; stroke: #cbd5e1; stroke-width: 1.2; }}
      .soft {{ fill: #f8fafc; stroke: #dbeafe; }}
      .axis {{ stroke: #1d4ed8; stroke-width: 2.2; fill: none; }}
      .grid {{ stroke: #cbd5e1; stroke-width: 1; stroke-dasharray: 5 7; }}
      .line {{ stroke: #94a3b8; stroke-width: 1.2; fill: none; }}
      .arrow {{ stroke: #2563eb; stroke-width: 2.2; fill: none; marker-end: url(#arrowhead); }}
    </style>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#eff6ff"/>
    </linearGradient>
    <linearGradient id="blueFill" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#eff6ff"/>
      <stop offset="1" stop-color="#dbeafe"/>
    </linearGradient>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg)"/>
'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)}")


def rounded_rect(x: float, y: float, w: float, h: float, r: float = 18,
                 fill: str = "#ffffff", stroke: str = "#cbd5e1", klass: str = "") -> str:
    cls = f' class="{klass}"' if klass else ""
    return f'<rect{cls} x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'


def maintenance_leverage_scatter() -> None:
    rows = list(csv.DictReader((DATA / "mas_use_case_scoring.csv").open()))
    W, H = 1200, 760
    x0, y0, cw, ch = 110, 155, 710, 455
    svg = [svg_header(W, H)]
    svg.append('<text class="title" x="42" y="58">Where Multi-Agent AI Creates the Highest Leverage</text>')
    svg.append('<text class="subtitle" x="44" y="86">Illustrative prioritization map for future CMMS/EAM programs. Scores are design heuristics, not benchmarks.</text>')
    svg.append(rounded_rect(36, 120, 820, 535, 22, "#ffffff", "#bfdbfe"))
    for i in range(1, 5):
        x = x0 + cw * i / 5
        y = y0 + ch * i / 5
        svg.append(f'<line class="grid" x1="{x}" y1="{y0}" x2="{x}" y2="{y0+ch}"/>')
        svg.append(f'<line class="grid" x1="{x0}" y1="{y}" x2="{x0+cw}" y2="{y}"/>')
    svg.append(f'<line class="axis" x1="{x0}" y1="{y0+ch}" x2="{x0+cw+28}" y2="{y0+ch}" marker-end="url(#arrowhead)"/>')
    svg.append(f'<line class="axis" x1="{x0}" y1="{y0+ch}" x2="{x0}" y2="{y0-28}" marker-end="url(#arrowhead)"/>')
    svg.append('<text class="h2" x="396" y="646">Decision complexity</text>')
    svg.append('<text class="h2" x="18" y="365" transform="rotate(-90 18 365)">Operational impact</text>')
    svg.append('<text class="small" x="96" y="637">Low</text><text class="small" x="790" y="637">High</text>')
    svg.append('<text class="small" x="70" y="605">Low</text><text class="small" x="70" y="140">High</text>')
    colors = ["#ede9fe", "#d1fae5", "#dbeafe", "#ffedd5"]
    strokes = ["#7c3aed", "#059669", "#2563eb", "#ea580c"]
    for r in rows:
        cx = x0 + ((float(r["decision_complexity"]) - 1) / 4) * cw
        cy = y0 + ch - ((float(r["operational_impact"]) - 1) / 4) * ch
        gov = float(r["governance_need"])
        idx = min(3, max(0, int((gov - 1) // 1.1)))
        radius = 31 + 4 * (float(r["operational_impact"]) / 5)
        svg.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{radius:.1f}" fill="{colors[idx]}" stroke="{strokes[idx]}" stroke-width="2" opacity="0.96"/>')
        svg.append(tspans(r["use_case"], cx, cy - 3, 16, 13, "tiny", "middle"))
    # right panels
    svg.append(rounded_rect(875, 120, 290, 232, 22, "#f0fdf4", "#86efac"))
    svg.append('<circle cx="918" cy="163" r="24" fill="#10b981"/><text class="badge" x="918" y="168" text-anchor="middle">✓</text>')
    svg.append('<text class="h2" x="954" y="169">Best near-term wins</text>')
    for i, t in enumerate(["Work-order triage", "Policy-aware recommendation packages", "Spare-parts coordination", "Field inspection scheduling"]):
        y = 213 + i * 34
        svg.append(f'<text class="h3" x="904" y="{y}" fill="#059669">✓</text>')
        svg.append(tspans(t, 930, y, 30, 13, "small"))
    svg.append(rounded_rect(875, 380, 290, 228, 22, "#fff7ed", "#fdba74"))
    svg.append('<circle cx="918" cy="423" r="24" fill="#f97316"/><text class="badge" x="918" y="428" text-anchor="middle">!</text>')
    svg.append('<text class="h2" x="954" y="429">Tighter governance</text>')
    for i, t in enumerate(["Live write actions", "Shutdown planning", "Safety-critical rail and grid actions", "Autonomous optimization loops"]):
        y = 473 + i * 34
        svg.append(f'<text class="h3" x="904" y="{y}" fill="#ea580c">△</text>')
        svg.append(tspans(t, 930, y, 31, 13, "small"))
    svg.append(rounded_rect(36, 675, 1128, 60, 18, "#f8fafc", "#cbd5e1"))
    svg.append('<text class="h3" x="64" y="711">Legend:</text>')
    svg.append('<text class="small" x="124" y="711">Left-bottom cases are safer starting points. Upper-right cases usually create more value but require stronger policy gates, human approval, and audit evidence.</text>')
    svg.append("</svg>")
    write(ASSETS / "maintenance-leverage-scatter.svg", "\n".join(svg))


def china_exemplars() -> None:
    examples = json.loads((DATA / "chinese_industrial_examples.json").read_text(encoding="utf-8"))
    W, H = 1400, 1040
    svg = [svg_header(W, H)]
    svg.append('<text class="title" x="42" y="58">Chinese Industrial Exemplars for MAS-enabled CMMS/EAM</text>')
    svg.append('<text class="subtitle" x="44" y="88">Public examples from smart manufacturing, grid operations, rail, process industry, industrial internet, and battery manufacturing.</text>')
    card_w, card_h = 320, 205
    start_x, start_y = 42, 130
    gap_x, gap_y = 24, 24
    palette = ["#eff6ff", "#ecfdf5", "#fff7ed", "#f5f3ff"]
    stroke = ["#93c5fd", "#6ee7b7", "#fdba74", "#c4b5fd"]
    for i, ex in enumerate(examples):
        col, row = i % 4, i // 4
        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y)
        color_i = i % 4
        svg.append(rounded_rect(x, y, card_w, card_h, 20, "#ffffff", stroke[color_i]))
        svg.append(f'<circle cx="{x+28}" cy="{y+32}" r="18" fill="#2563eb"/><text class="badge" x="{x+28}" y="{y+37}" text-anchor="middle">{i+1}</text>')
        svg.append(tspans(ex["company"], x + 56, y + 38, 26, 17, "h2"))
        svg.append(f'<rect x="{x+20}" y="{y+68}" width="{card_w-40}" height="1" fill="#dbeafe"/>')
        svg.append(tspans("Sector: " + ex["sector"], x + 22, y + 94, 38, 14, "small"))
        svg.append(tspans("Signal: " + ex["public_signal"], x + 22, y + 134, 39, 13, "tiny"))
        svg.append(f'<rect x="{x+18}" y="{y+165}" width="{card_w-36}" height="28" rx="10" fill="{palette[color_i]}" stroke="{stroke[color_i]}"/>')
        svg.append(tspans(ex["agentic_use_case"], x + 28, y + 184, 38, 12, "tiny"))
    svg.append(rounded_rect(42, 615, 1314, 335, 24, "#ffffff", "#bfdbfe"))
    svg.append('<text class="h2" x="72" y="655">Interpretation for a future CMMS/EAM platform</text>')
    bullets = [
        "China's installed asset base spans factories, power grids, rail systems, process plants, and new-energy production. This creates many high-value contexts for multi-agent maintenance.",
        "The common pattern is not a single chatbot. It is a loop: connected assets create signals; agents retrieve context; specialists debate; policy gates decisions; humans approve high-impact actions.",
        "The best early product surface is a review package, not full automation: evidence, candidate work order, parts constraints, safety gates, confidence, and traceability.",
        "Mature deployments should connect AI to CMMS/EAM through narrow tools and tenant-scoped policy rather than broad database access or uncontrolled write actions."
    ]
    for i, b in enumerate(bullets):
        y = 700 + i * 55
        svg.append(f'<circle cx="78" cy="{y-6}" r="12" fill="#2563eb"/><text class="badge" x="78" y="{y-2}" text-anchor="middle">{i+1}</text>')
        svg.append(tspans(b, 105, y, 138, 16, "small"))
    svg.append(rounded_rect(42, 970, 1314, 40, 14, "#f8fafc", "#dbeafe"))
    svg.append('<text class="tiny" x="64" y="995">Sources are listed in data/chinese_industrial_examples.json and in the paper references.</text>')
    svg.append("</svg>")
    write(ASSETS / "chinese-industrial-exemplars.svg", "\n".join(svg))


def made_in_china_roadmap() -> None:
    rows = list(csv.DictReader((DATA / "made_in_china_2025_timeline.csv").open()))
    W, H = 1400, 850
    years = ["2015", "2020", "2025", "2030+"]
    keys = ["2015", "2020", "2025", "2030_plus"]
    svg = [svg_header(W, H)]
    svg.append('<text class="title" x="42" y="58">Made in China 2025 as a Launchpad for Agentic EAM</text>')
    svg.append('<text class="subtitle" x="44" y="88">From manufacturing upgrading to connected, policy-aware, multi-agent asset operations.</text>')
    x0, col_w, y0, row_h = 250, 235, 150, 185
    svg.append('<line x1="250" y1="120" x2="1190" y2="120" stroke="#2563eb" stroke-width="3" marker-end="url(#arrowhead)"/>')
    for i, year in enumerate(years):
        x = x0 + i * col_w + col_w / 2
        svg.append(f'<circle cx="{x}" cy="120" r="14" fill="#2563eb"/><text class="h2" x="{x}" y="98" text-anchor="middle">{year}</text>')
        svg.append(f'<line class="grid" x1="{x}" y1="135" x2="{x}" y2="{y0 + row_h*3 - 20}"/>')
    for r_i, row in enumerate(rows):
        y = y0 + r_i * row_h
        svg.append(rounded_rect(42, y, 175, row_h - 24, 20, "#eff6ff", "#bfdbfe"))
        svg.append(f'<circle cx="72" cy="{y+34}" r="16" fill="#2563eb"/><text class="badge" x="72" y="{y+39}" text-anchor="middle">{r_i+1}</text>')
        svg.append(tspans(row["lane"], 98, y + 43, 18, 19, "h2"))
        for c_i, key in enumerate(keys):
            x = x0 + c_i * col_w
            svg.append(rounded_rect(x, y, col_w - 20, row_h - 24, 18, "#ffffff", "#cbd5e1"))
            svg.append(tspans(row[key], x + 18, y + 42, 26, 16, "small"))
    # side panel
    svg.append(rounded_rect(1212, 150, 145, 520, 20, "#ffffff", "#bfdbfe"))
    svg.append('<text class="h2" x="1232" y="185">Priority sectors</text>')
    sectors = ["Next-gen IT", "CNC & robotics", "Aerospace", "Ocean engineering", "Advanced rail", "Energy-saving & NEV", "Power equipment", "Agricultural machinery", "New materials", "Biopharma & devices"]
    for i, s in enumerate(sectors):
        y = 220 + i * 42
        svg.append(f'<rect x="1230" y="{y-20}" width="110" height="28" rx="14" fill="#eff6ff" stroke="#bfdbfe"/>')
        svg.append(tspans(s, 1241, y - 1, 17, 12, "tiny"))
    svg.append(rounded_rect(42, 725, 1315, 70, 18, "#f8fafc", "#dbeafe"))
    svg.append('<text class="h3" x="70" y="755">CMMS/EAM meaning:</text>')
    svg.append('<text class="small" x="210" y="755">More connected assets → more complex compliance → higher uptime expectations → greater value from cross-agent collaboration and explainable automation.</text>')
    svg.append("</svg>")
    write(ASSETS / "made-in-china-2025-roadmap.svg", "\n".join(svg))


def automation_governance_matrix() -> None:
    W, H = 1100, 720
    svg = [svg_header(W, H)]
    svg.append('<text class="title" x="42" y="58">Automation Permission Matrix for Agentic CMMS/EAM</text>')
    svg.append('<text class="subtitle" x="44" y="88">A practical guardrail: increase autonomy only when risk is low, reversibility is high, and policy evidence is complete.</text>')
    x0, y0, w, h = 100, 145, 650, 430
    fills = [["#ecfdf5", "#fffbeb"], ["#fef2f2", "#fff7ed"]]
    labels = [
        ["Auto-draft and optionally auto-create", "Draft only; human validates before write"],
        ["Human approval required", "Blocked unless formal workflow approves"]
    ]
    notes = [
        ["Low-risk, reversible, tenant-enabled tasks such as duplicate detection or low-priority work request drafts.", "Moderate complexity or weak evidence. Agents may recommend, but the planner approves the work order or part reservation."],
        ["Safety, compliance, or production-impacting actions. The agent package must show evidence, assumptions, and alternatives.", "Shutdowns, OT commands, critical rail/grid actions, budget-heavy commitments, or policy exceptions."]
    ]
    for row in range(2):
        for col in range(2):
            x = x0 + col * w / 2
            y = y0 + row * h / 2
            svg.append(rounded_rect(x, y, w / 2 - 10, h / 2 - 10, 18, fills[row][col], "#cbd5e1"))
            svg.append(tspans(labels[row][col], x + 22, y + 45, 32, 18, "h2"))
            svg.append(tspans(notes[row][col], x + 22, y + 103, 40, 16, "small"))
    svg.append(f'<line class="axis" x1="{x0}" y1="{y0+h+35}" x2="{x0+w+20}" y2="{y0+h+35}" marker-end="url(#arrowhead)"/>')
    svg.append(f'<line class="axis" x1="{x0-35}" y1="{y0+h}" x2="{x0-35}" y2="{y0-20}" marker-end="url(#arrowhead)"/>')
    svg.append('<text class="h2" x="330" y="638">Action side-effect / irreversibility</text>')
    svg.append('<text class="h2" x="38" y="420" transform="rotate(-90 38 420)">Operational and safety risk</text>')
    svg.append(rounded_rect(800, 145, 250, 430, 22, "#ffffff", "#bfdbfe"))
    svg.append('<text class="h2" x="825" y="184">Approval signals</text>')
    signals = ["Tenant feature flag enabled", "Role has scope for tool", "Evidence is fresh and cited", "Policy checks pass", "Budget and threshold pass", "Audit event is written", "Human can reverse or override"]
    for i, s in enumerate(signals):
        y = 228 + i * 45
        svg.append(f'<circle cx="828" cy="{y-5}" r="12" fill="#2563eb"/><text class="badge" x="828" y="{y}" text-anchor="middle">✓</text>')
        svg.append(tspans(s, 850, y, 25, 14, "small"))
    svg.append("</svg>")
    write(ASSETS / "automation-governance-matrix.svg", "\n".join(svg))


def agent_debate_sequence() -> None:
    W, H = 1300, 680
    svg = [svg_header(W, H)]
    svg.append('<text class="title" x="42" y="58">Agent Debate Protocol for a Noisy Compressor Request</text>')
    svg.append('<text class="subtitle" x="44" y="88">A concrete example of how specialized agents challenge each other before producing a review package.</text>')
    agents = ["Intake", "Asset", "Inventory", "Policy", "Cost/Risk", "Human"]
    x0, y0, col_w, card_h = 60, 150, 190, 90
    for i, agent in enumerate(agents):
        x = x0 + i * col_w
        svg.append(rounded_rect(x, y0, 150, 60, 18, "#eff6ff" if agent != "Human" else "#f0fdf4", "#93c5fd" if agent != "Human" else "#86efac"))
        svg.append(f'<text class="h2" x="{x+75}" y="{y0+37}" text-anchor="middle">{agent}</text>')
        svg.append(f'<line class="line" x1="{x+75}" y1="{y0+70}" x2="{x+75}" y2="600" stroke-dasharray="4 7"/>')
    steps = [
        (0, 1, 260, "Parse symptom and asset hint"),
        (1, 2, 325, "Request BOM and part risk"),
        (2, 3, 390, "Return shortage / lead-time constraints"),
        (3, 4, 455, "Apply approval, safety, and budget gates"),
        (4, 1, 520, "Challenge: risk too high for auto-write"),
        (1, 5, 585, "Review package with evidence and alternatives")
    ]
    for start, end, y, label in steps:
        sx = x0 + start * col_w + 75
        ex = x0 + end * col_w + 75
        if ex > sx:
            svg.append(f'<path class="arrow" d="M {sx} {y} C {(sx+ex)/2} {y-28}, {(sx+ex)/2} {y-28}, {ex-10} {y}"/>')
            tx = (sx + ex) / 2 - 80
        else:
            svg.append(f'<path class="arrow" d="M {sx} {y} C {(sx+ex)/2} {y+34}, {(sx+ex)/2} {y+34}, {ex+10} {y}"/>')
            tx = (sx + ex) / 2 - 80
        svg.append(rounded_rect(tx, y - 30, 160, 34, 14, "#ffffff", "#dbeafe"))
        svg.append(tspans(label, tx + 10, y - 10, 24, 12, "tiny"))
    svg.append(rounded_rect(60, 610, 1120, 42, 15, "#f8fafc", "#dbeafe"))
    svg.append('<text class="small" x="84" y="636">Key design rule: disagreement is not a failure. It is the mechanism that turns a loose AI answer into an auditable maintenance recommendation.</text>')
    svg.append("</svg>")
    write(ASSETS / "agent-debate-sequence.svg", "\n".join(svg))


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    maintenance_leverage_scatter()
    china_exemplars()
    made_in_china_roadmap()
    automation_governance_matrix()
    agent_debate_sequence()


if __name__ == "__main__":
    main()

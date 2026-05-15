# Visuals and Charts

The repository now includes a generated figure set for the paper. The SVG charts are deterministic, reviewable, and generated from small JSON files in `data/`.

## Figure gallery

### 1. Multi-agent value loop

![Future CMMS/EAM as a Multi-Agent Value Loop](../assets/mas-value-loop-expanded.svg)

Shows the full loop from signal intake to context retrieval, agent collaboration, policy debate, recommendation package, approval/bounded automation, and learning/audit feedback.

### 2. Made in China 2025 roadmap to agentic EAM

![Made in China 2025 as a Launchpad for Agentic EAM](../assets/made-in-china-2025-agentic-eam-roadmap.svg)

Connects the policy foundation of 中国制造2025 to a forward-looking 2030+ vision of multi-agent CMMS/EAM. The 2030+ portion is an analytical platform vision, not an official policy forecast.

### 3. Chinese industrial exemplars

![Chinese Industrial Exemplars for Agentic CMMS/EAM](../assets/china-industrial-exemplars.svg)

Summarizes Midea/MBT, SANY, State Grid, CRRC, Huawei, Sinopec, Haier COSMOPlat, and Baowu/Baosteel as public digitalization signals relevant to future agentic maintenance.

### 4. Maintenance leverage matrix

![Maintenance Use Case Leverage Matrix](../assets/maintenance-use-case-leverage-matrix.svg)

An illustrative prioritization matrix: low-risk repetitive decisions are near-term wins; safety-critical high-complexity areas need stronger governance and human approval.

### 5. China agentic EAM fit heatmap

![Agentic EAM Fit Matrix](../assets/china-agentic-eam-fit-heatmap.svg)

Shows qualitative structural-fit scores across five dimensions: connected asset signal, safety criticality, parts/service complexity, policy/compliance intensity, and lifecycle learning loop. The scores are analytical, not public company KPIs.

### 6. Industrial maintenance data flywheel

![Industrial Maintenance Data Flywheel](../assets/industrial-maintenance-data-flywheel.svg)

Shows how signals, context, agents, review, action, and outcomes reinforce each other over time.

## Regenerating the figures

From the repository root:

```bash
python scripts/generate_figures.py
```

Input files:

- `data/china_industrial_examples.json`
- `data/use_case_scores.json`
- `data/made_in_china_2025_mapping.json`

Output files:

- `assets/mas-value-loop-expanded.svg`
- `assets/china-industrial-exemplars.svg`
- `assets/made-in-china-2025-agentic-eam-roadmap.svg`
- `assets/maintenance-use-case-leverage-matrix.svg`
- `assets/china-agentic-eam-fit-heatmap.svg`
- `assets/industrial-maintenance-data-flywheel.svg`

## Presentation-style PNG renders

The `assets/renders/` folder also includes richer presentation-style PNG renders. The SVGs are preferred for GitHub paper readability and version control; PNGs are useful for slides and social previews.

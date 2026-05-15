# Source Code Walkthrough

The demo is intentionally small. Its purpose is to show how a CMMS/EAM agent runtime can be contract-first before any LLM provider is connected.

## Files

| File | Purpose |
| --- | --- |
| `models.py` | Dataclasses for work requests, assets, inventory, guardrails, findings, recommendations, and orchestration runs. |
| `agents.py` | Deterministic Intake, Asset, Inventory, Policy, and DebateModerator implementations. |
| `orchestrator.py` | Runs agents, applies guardrails, and returns an `OrchestrationRun`. |
| `sample_data.py` | Synthetic asset and inventory records. |
| `cli.py` | Command line interface. |
| `china_cases.py` | Loads and ranks the Chinese industrial example dataset for tests or demos. |
| `scripts/generate_figures.py` | Generates richer SVG charts such as the China heatmap, value loop, roadmap, and data flywheel. |
| `tools/build_figures.py` | Generates compact SVG charts from CSV/JSON data with no third-party dependencies. |
| `tests/test_orchestrator.py` | Basic test that confirms the compressor noise case blocks live writes. |
| `tests/test_china_examples.py` | Confirms that China examples have sources, scores, and descending ranking behavior. |

## Why deterministic first?

A production platform may use LLMs for language understanding, retrieval synthesis, and explanation. But the platform should first prove that:

- Agent responsibilities are separated.
- Output schemas are stable.
- Tool actions are proposed rather than executed.
- Policy can block writes independently of model text.
- Runs are auditable.

This demo proves those contracts without external dependencies.

## How to extend

### Add a SchedulerAgent

1. Create a class in `agents.py` with a `run(ctx)` method.
2. Return an `AgentFinding`.
3. Add the agent to `Orchestrator.agents`.
4. Add tests for schedule conflicts and approval gates.

### Add a real LLM-backed agent

1. Keep the same `AgentFinding` schema.
2. Add an LLM provider adapter outside the agent contract.
3. Validate model output before accepting it.
4. Never let the model call production tools directly.
5. Add offline replay tests before enabling live tenants.

### Add a tool gateway

1. Define a tool schema.
2. Validate payloads.
3. Check tenant and RBAC.
4. Require approval state for writes.
5. Emit an audit event.
6. Return a structured tool result.

## Example extension: SchedulerAgent stub

```python
class SchedulerAgent:
    name = "Scheduler"

    def run(self, ctx: AgentContext) -> AgentFinding:
        return AgentFinding(
            agent_name=self.name,
            verdict="Scheduling requires planner review because asset risk is elevated.",
            confidence=0.78,
            severity=Severity.MEDIUM,
            evidence=["criticality=4/5", "human_approval_gate=True"],
            recommended_actions=["Suggest next available technician with compressor skill"],
        )
```


## Regenerate figures

The repository contains editable SVG charts generated from small data files. From the repository root:

```bash
python tools/build_figures.py
python scripts/generate_figures.py
```

The figure code is intentionally simple so a reviewer can inspect the data and modify the diagrams without a design tool.

## Production note

The biggest leap from this demo to production is not adding an LLM. It is building the tool gateway, audit store, retrieval governance, tenant isolation, and evaluation pipeline.

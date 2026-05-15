# Agent Contracts

This document defines practical contracts for CMMS/EAM agents. The contracts are intentionally independent of any LLM framework.

## 1. AgentContext

`AgentContext` is the complete tenant-scoped state passed into an agent.

```json
{
  "tenant_id": "demo-tenant",
  "site_id": "PLANT-01",
  "request": {
    "request_id": "REQ-1001",
    "asset_id": "COMP-04",
    "description": "Compressor noisy"
  },
  "asset": {
    "asset_id": "COMP-04",
    "criticality": 4,
    "last_pm_days_ago": 104
  },
  "retrieval": [
    {"source_id": "manual:comp-04:page-12", "title": "Compressor inspection checklist"}
  ],
  "guardrails": {
    "human_approval_gate": true,
    "allow_live_writes": false,
    "max_tool_calls": 5
  }
}
```

## 2. AgentTask

An `AgentTask` is narrow and testable.

Bad task:

```text
Figure out what to do with this compressor and take action.
```

Good task:

```text
Given the work request, asset record, telemetry, and work history, assess whether the request indicates elevated asset risk. Return only the AgentResult schema. Do not propose inventory actions or create work orders.
```

## 3. AgentResult

Every agent returns the same top-level structure.

```json
{
  "agent_name": "Asset",
  "verdict": "Asset risk is elevated.",
  "confidence": 0.92,
  "severity": "high",
  "evidence": ["asset criticality 4/5", "vibration 8.1 mm/s"],
  "risks": ["possible bearing wear", "PM is overdue"],
  "recommended_actions": ["schedule inspection"],
  "proposed_writes": []
}
```

Rules:

- `confidence` is a calibration hint, not a truth guarantee.
- `evidence` must refer to actual retrieved or provided context.
- `proposed_writes` are not executed by the agent.
- `severity` should reflect operational impact, not model confidence.

## 4. ToolAction

A `ToolAction` is either a proposed write or a safe read.

```json
{
  "system": "cmms",
  "operation": "draft_work_order",
  "payload": {
    "asset_id": "COMP-04",
    "description": "Compressor noisy",
    "priority": "normal"
  },
  "requires_approval": true,
  "idempotency_key": "draft-REQ-1001"
}
```

Every write-capable tool must be idempotent or protected by a duplicate check.

## 5. Prompt pattern for LLM-backed agents

Use a strict role and schema prompt. Example:

```text
You are the Asset Reliability Agent for a CMMS/EAM platform.
Your task is to assess asset risk for a work request.
Use only the provided context.
Do not invent parts, policies, work history, or telemetry.
Do not create or approve work orders.
Return JSON that matches the AgentResult schema.
If evidence is insufficient, lower confidence and request human review.
```

## 6. Quality checklist

Before accepting an agent result, validate:

- JSON schema is valid.
- Agent stayed within role.
- Evidence references exist.
- Confidence is within range.
- Proposed writes are allowed for that agent.
- No forbidden tool is requested.
- No cross-tenant identifiers appear.
- No policy is waived by model text.

## 7. Cross-agent conflict examples

| Conflict | Example | Resolution |
| --- | --- | --- |
| Asset vs Intake | Intake says normal priority; asset is critical and vibration is high. | Escalate to planner review. |
| Inventory vs Asset | Asset suggests bearing inspection; part is out of stock. | Inspect first, draft procurement after diagnosis. |
| Policy vs Scheduler | Scheduler finds crew slot; policy requires permit. | Permit gate blocks scheduling confirmation. |
| Budget vs Reliability | Replacement is expensive; repeat failures are rising. | Route to reliability engineer and finance review. |

## 8. Contract-first development

Build and test contracts before adding models. A deterministic agent that returns correct schemas is more valuable than a powerful model with unbounded side effects.

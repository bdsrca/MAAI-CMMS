"""Core data contracts for the experimental agentic CMMS demo.

The demo is intentionally deterministic: no network calls, no LLM calls, and no
writes to real systems. It models the contracts a production CMMS/EAM agent
runtime would need before connecting to LLM providers and live CMMS tools.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class WritePolicy(str, Enum):
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    APPROVED = "approved"


@dataclass(frozen=True)
class WorkRequest:
    request_id: str
    tenant_id: str
    site_id: str
    asset_id: str
    description: str
    reported_by: str = "operator"
    priority: str = "normal"
    telemetry: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssetRecord:
    asset_id: str
    name: str
    class_code: str
    site_id: str
    criticality: int
    status: str
    last_pm_days_ago: int
    failure_modes: List[str]
    safety_notes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class InventoryItem:
    part_no: str
    description: str
    on_hand: int
    reorder_point: int
    lead_time_days: int
    compatible_asset_classes: List[str]


@dataclass(frozen=True)
class TenantGuardrails:
    tenant_id: str
    budget_cap_cents: int
    max_tool_calls: int
    human_approval_gate: bool
    allow_live_writes: bool
    high_risk_threshold: float = 0.65
    low_confidence_threshold: float = 0.72


@dataclass(frozen=True)
class ToolAction:
    system: str
    operation: str
    payload: Dict[str, Any]
    requires_approval: bool = True
    idempotency_key: Optional[str] = None


@dataclass(frozen=True)
class AgentFinding:
    agent_name: str
    verdict: str
    confidence: float
    severity: Severity
    evidence: List[str]
    risks: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    proposed_writes: List[ToolAction] = field(default_factory=list)


@dataclass(frozen=True)
class Recommendation:
    summary: str
    confidence: float
    automation_risk: float
    write_policy: WritePolicy
    approval_required: bool
    next_steps: List[str]
    blocked_reason: Optional[str] = None


@dataclass(frozen=True)
class AgentContext:
    request: WorkRequest
    asset: Optional[AssetRecord]
    inventory: List[InventoryItem]
    guardrails: TenantGuardrails
    prior_findings: List[AgentFinding] = field(default_factory=list)


@dataclass(frozen=True)
class OrchestrationRun:
    run_id: str
    estimated_budget_used_pct: int
    tool_calls_used: int
    findings: List[AgentFinding]
    recommendation: Recommendation
    audit: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


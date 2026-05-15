"""Deterministic agent roles for the NextCMMS MAAI proof-of-concept.

A production implementation can keep the same class boundaries and replace the
heuristic logic with LLM-backed reasoning, retrieval, and tool use. The key idea
is not that every agent needs to be an LLM. The key idea is that each role has a
bounded scope, a typed output, and a visible audit trail.
"""

from __future__ import annotations

from dataclasses import replace
from statistics import mean
from typing import Iterable, List

from .models import (
    AgentContext,
    AgentFinding,
    InventoryItem,
    Recommendation,
    Severity,
    ToolAction,
    WritePolicy,
)


class IntakeAgent:
    name = "Intake"

    def run(self, ctx: AgentContext) -> AgentFinding:
        desc = ctx.request.description.lower()
        evidence = [f"request='{ctx.request.description}'", f"asset_id={ctx.request.asset_id}"]
        missing = []
        if not ctx.request.asset_id:
            missing.append("asset_id")
        if not ctx.request.description:
            missing.append("description")

        severity = Severity.MEDIUM
        confidence = 0.86
        recommended = ["Create a review package for maintenance planner"]
        risks = []

        if any(word in desc for word in ["noisy", "noise", "vibration", "rattle"]):
            evidence.append("symptom=noise/vibration")
            recommended.append("Ask technician to capture vibration, temperature, and operating load")
        if any(word in desc for word in ["smoke", "fire", "sparks", "burning"]):
            severity = Severity.CRITICAL
            confidence = 0.92
            risks.append("possible immediate safety hazard")
            recommended.insert(0, "Escalate to emergency response workflow")
        if missing:
            confidence -= 0.2
            risks.append("missing fields: " + ", ".join(missing))

        proposed = ToolAction(
            system="cmms",
            operation="draft_work_order",
            payload={
                "asset_id": ctx.request.asset_id,
                "description": ctx.request.description,
                "priority": ctx.request.priority,
                "source": "maai_intake_agent",
            },
            requires_approval=True,
            idempotency_key=f"draft-{ctx.request.request_id}",
        )
        return AgentFinding(
            agent_name=self.name,
            verdict="Work request parsed; work-order draft is possible but not auto-created.",
            confidence=max(0.0, min(confidence, 1.0)),
            severity=severity,
            evidence=evidence,
            risks=risks,
            recommended_actions=recommended,
            proposed_writes=[proposed],
        )


class AssetAgent:
    name = "Asset"

    def run(self, ctx: AgentContext) -> AgentFinding:
        if ctx.asset is None:
            return AgentFinding(
                agent_name=self.name,
                verdict="Asset record not found.",
                confidence=0.55,
                severity=Severity.HIGH,
                evidence=["no asset record available"],
                risks=["cannot validate criticality, PM status, or failure modes"],
                recommended_actions=["Route to planner for asset lookup before scheduling"],
            )

        asset = ctx.asset
        evidence = [
            f"asset={asset.name}",
            f"class={asset.class_code}",
            f"criticality={asset.criticality}/5",
            f"last_pm_days_ago={asset.last_pm_days_ago}",
        ]
        risks = []
        severity = Severity.MEDIUM
        confidence = 0.88

        vibration = ctx.request.telemetry.get("vibration_mm_s")
        temp = ctx.request.telemetry.get("temperature_c")
        if vibration is not None:
            evidence.append(f"vibration_mm_s={vibration}")
            if vibration >= 7.1:
                risks.append("vibration above common alarm band for rotating equipment")
                severity = Severity.HIGH
                confidence += 0.04
        if temp is not None:
            evidence.append(f"temperature_c={temp}")
            if temp >= 80:
                risks.append("temperature approaching thermal inspection threshold")
                severity = Severity.HIGH

        if asset.criticality >= 4:
            risks.append("high criticality asset; unplanned downtime may affect production")
        if asset.last_pm_days_ago > 90:
            risks.append("preventive maintenance is overdue or near overdue")

        recommended = [
            "Review last failure history and PM checklist before dispatch",
            "Inspect bearings, coupling alignment, lubrication, and mounting bolts",
        ]
        if asset.safety_notes:
            recommended.append("Include asset safety notes in technician package")

        return AgentFinding(
            agent_name=self.name,
            verdict="Asset risk is elevated; inspection should be planned before auto-closing the request.",
            confidence=min(confidence, 0.96),
            severity=severity,
            evidence=evidence,
            risks=risks,
            recommended_actions=recommended,
        )


class InventoryAgent:
    name = "Inventory"

    def run(self, ctx: AgentContext) -> AgentFinding:
        asset_class = ctx.asset.class_code if ctx.asset else "unknown"
        compatible = [item for item in ctx.inventory if asset_class in item.compatible_asset_classes]
        evidence = [f"compatible_parts={len(compatible)}", f"asset_class={asset_class}"]
        risks: List[str] = []
        recommended: List[str] = []
        severity = Severity.LOW
        confidence = 0.81

        bearing_like = self._find_part(compatible, ["bearing", "seal", "coupling"])
        if bearing_like:
            evidence.append(f"candidate_part={bearing_like.part_no}:{bearing_like.description}")
            evidence.append(f"on_hand={bearing_like.on_hand}, reorder_point={bearing_like.reorder_point}")
            if bearing_like.on_hand <= 0:
                risks.append(f"part {bearing_like.part_no} is out of stock")
                severity = Severity.HIGH
                recommended.append("Create purchase requisition draft after planner approval")
            elif bearing_like.on_hand <= bearing_like.reorder_point:
                risks.append(f"part {bearing_like.part_no} is below or at reorder point")
                severity = Severity.MEDIUM
                recommended.append("Reserve one unit only after planner confirms diagnosis")
            else:
                recommended.append("Part appears available; do not reserve until diagnosis is confirmed")
        else:
            confidence = 0.66
            severity = Severity.MEDIUM
            risks.append("no compatible part candidates found from local catalog")
            recommended.append("Ask planner to map likely spares before technician dispatch")

        proposed = []
        if bearing_like:
            proposed.append(
                ToolAction(
                    system="inventory",
                    operation="reserve_part_draft",
                    payload={"part_no": bearing_like.part_no, "quantity": 1, "asset_id": ctx.request.asset_id},
                    requires_approval=True,
                    idempotency_key=f"reserve-{ctx.request.request_id}-{bearing_like.part_no}",
                )
            )

        return AgentFinding(
            agent_name=self.name,
            verdict="Parts check completed; reservation remains gated by diagnosis and approval.",
            confidence=confidence,
            severity=severity,
            evidence=evidence,
            risks=risks,
            recommended_actions=recommended,
            proposed_writes=proposed,
        )

    @staticmethod
    def _find_part(items: Iterable[InventoryItem], keywords: List[str]) -> InventoryItem | None:
        for item in items:
            text = f"{item.part_no} {item.description}".lower()
            if any(word in text for word in keywords):
                return item
        return None


class PolicyAgent:
    name = "Policy"

    def run(self, ctx: AgentContext) -> AgentFinding:
        findings = ctx.prior_findings
        severe = [f for f in findings if f.severity in (Severity.HIGH, Severity.CRITICAL)]
        proposed_writes = [write for f in findings for write in f.proposed_writes]
        risks = []
        evidence = [
            f"human_approval_gate={ctx.guardrails.human_approval_gate}",
            f"allow_live_writes={ctx.guardrails.allow_live_writes}",
            f"proposed_writes={len(proposed_writes)}",
            f"high_or_critical_findings={len(severe)}",
        ]
        confidence = 0.93
        severity = Severity.LOW

        if ctx.guardrails.human_approval_gate:
            risks.append("human approval is required by tenant guardrail")
        if not ctx.guardrails.allow_live_writes:
            risks.append("live writes are disabled for this tenant or environment")
        if severe:
            severity = Severity.MEDIUM
            risks.append("high severity finding requires planner or supervisor review")

        recommended = [
            "Block live writes and produce a review package",
            "Record an audit event with evidence, confidence, risk, and proposed actions",
        ]
        return AgentFinding(
            agent_name=self.name,
            verdict="Approval gate blocks autonomous write actions for this run.",
            confidence=confidence,
            severity=severity,
            evidence=evidence,
            risks=risks,
            recommended_actions=recommended,
        )


class DebateModerator:
    """Combines findings into a final recommendation.

    This is intentionally not a free-form debate. It is a bounded synthesis step:
    summarize agreements, expose conflicts, and convert them into a recommendation
    the user can approve or reject.
    """

    def synthesize(self, ctx: AgentContext, findings: List[AgentFinding]) -> Recommendation:
        confidence = round(mean(f.confidence for f in findings), 2)
        high_count = sum(1 for f in findings if f.severity in (Severity.HIGH, Severity.CRITICAL))
        missing_or_stockout = any("out of stock" in risk.lower() for f in findings for risk in f.risks)
        automation_risk = 0.12 + high_count * 0.16 + (0.12 if missing_or_stockout else 0.0)
        automation_risk = round(min(automation_risk, 0.95), 2)

        approval_required = ctx.guardrails.human_approval_gate or automation_risk >= ctx.guardrails.high_risk_threshold
        write_policy = WritePolicy.BLOCKED
        blocked_reason = None
        if not ctx.guardrails.allow_live_writes:
            blocked_reason = "Tenant or environment disables live writes."
        elif approval_required:
            write_policy = WritePolicy.REVIEW_REQUIRED
            blocked_reason = "Human approval is required before writes."
        else:
            write_policy = WritePolicy.APPROVED

        next_steps = [
            "Show planner a review package with evidence from intake, asset, inventory, and policy agents",
            "Dispatch inspection focused on bearing noise, vibration, lubrication, alignment, and mounting",
            "Defer inventory reservation until technician confirms the failure mode",
            "After approval, convert the draft into a CMMS work order and attach audit context",
        ]

        if high_count:
            next_steps.insert(1, "Treat as elevated asset risk; avoid auto-close or auto-defer")

        return Recommendation(
            summary="Compressor noise request is credible and should become a human-reviewed maintenance package.",
            confidence=confidence,
            automation_risk=automation_risk,
            write_policy=write_policy,
            approval_required=approval_required,
            next_steps=next_steps,
            blocked_reason=blocked_reason,
        )

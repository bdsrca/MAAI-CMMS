"""Orchestration runtime for the deterministic MAAI demo."""

from __future__ import annotations

from dataclasses import replace
from typing import Dict, List
from uuid import uuid4

from .agents import AssetAgent, DebateModerator, IntakeAgent, InventoryAgent, PolicyAgent
from .models import AgentContext, AssetRecord, InventoryItem, OrchestrationRun, TenantGuardrails, WorkRequest


class Orchestrator:
    def __init__(
        self,
        assets: Dict[str, AssetRecord],
        inventory: List[InventoryItem],
        guardrails: TenantGuardrails,
    ) -> None:
        self.assets = assets
        self.inventory = inventory
        self.guardrails = guardrails
        self.agents = [IntakeAgent(), AssetAgent(), InventoryAgent()]
        self.policy_agent = PolicyAgent()
        self.moderator = DebateModerator()

    def run(self, request: WorkRequest) -> OrchestrationRun:
        asset = self.assets.get(request.asset_id)
        ctx = AgentContext(request=request, asset=asset, inventory=self.inventory, guardrails=self.guardrails)
        findings = []
        tool_calls = 0

        for agent in self.agents:
            if tool_calls >= self.guardrails.max_tool_calls:
                break
            finding = agent.run(ctx)
            findings.append(finding)
            tool_calls += 1
            ctx = replace(ctx, prior_findings=findings)

        policy_finding = self.policy_agent.run(ctx)
        findings.append(policy_finding)
        tool_calls += 1

        recommendation = self.moderator.synthesize(ctx, findings)
        estimated_budget_pct = min(100, int(round((tool_calls / max(self.guardrails.max_tool_calls, 1)) * 20)))
        # In the screenshot, the POC shows 16 percent. Keep the demo close to that
        # low-budget concept while still deriving it from tool-call count.
        estimated_budget_pct = min(16, estimated_budget_pct)

        return OrchestrationRun(
            run_id=f"run_{uuid4().hex[:12]}",
            estimated_budget_used_pct=estimated_budget_pct,
            tool_calls_used=tool_calls,
            findings=findings,
            recommendation=recommendation,
            audit={
                "tenant_id": request.tenant_id,
                "site_id": request.site_id,
                "write_action": recommendation.write_policy.value,
                "audit_status": "planned",
                "source": "deterministic_poc_no_ai_calls_no_writes",
            },
        )

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
        if self.guardrails.max_tool_calls < 1:
            raise ValueError("max_tool_calls must be at least 1 so the policy gate can run")

        asset = self.assets.get(request.asset_id)
        self._validate_boundaries(request, asset)

        ctx = AgentContext(request=request, asset=asset, inventory=self.inventory, guardrails=self.guardrails)
        findings = []
        tool_calls = 0

        # Reserve one call for the mandatory policy gate. Operational agents may
        # consume only the remaining budget, so the configured maximum is a hard
        # cap across the entire orchestration run.
        operational_budget = max(self.guardrails.max_tool_calls - 1, 0)
        for agent in self.agents:
            if tool_calls >= operational_budget:
                break
            finding = agent.run(ctx)
            findings.append(finding)
            tool_calls += 1
            ctx = replace(ctx, prior_findings=findings)

        policy_finding = self.policy_agent.run(ctx)
        findings.append(policy_finding)
        tool_calls += 1

        recommendation = self.moderator.synthesize(ctx, findings)
        estimated_budget_pct = min(100, int(round((tool_calls / self.guardrails.max_tool_calls) * 20)))
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
                "asset_id": request.asset_id,
                "tenant_boundary": "validated",
                "site_boundary": "validated" if asset is not None else "asset_not_found",
                "write_action": recommendation.write_policy.value,
                "audit_status": "planned",
                "source": "deterministic_poc_no_ai_calls_no_writes",
            },
        )

    def _validate_boundaries(self, request: WorkRequest, asset: AssetRecord | None) -> None:
        if request.tenant_id != self.guardrails.tenant_id:
            raise ValueError(
                f"tenant boundary violation: request tenant '{request.tenant_id}' "
                f"does not match guardrail tenant '{self.guardrails.tenant_id}'"
            )

        if asset is None:
            return

        if asset.tenant_id != request.tenant_id:
            raise ValueError(
                f"tenant boundary violation: asset '{asset.asset_id}' belongs to tenant "
                f"'{asset.tenant_id}', not '{request.tenant_id}'"
            )

        if asset.site_id != request.site_id:
            raise ValueError(
                f"site boundary violation: asset '{asset.asset_id}' belongs to site "
                f"'{asset.site_id}', not '{request.site_id}'"
            )

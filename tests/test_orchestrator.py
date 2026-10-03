import unittest
from dataclasses import replace

from maai_cmms_demo.models import WorkRequest, WritePolicy
from maai_cmms_demo.orchestrator import Orchestrator
from maai_cmms_demo.sample_data import demo_assets, demo_guardrails, demo_inventory


class OrchestratorTests(unittest.TestCase):
    def make_request(self, **overrides) -> WorkRequest:
        values = {
            "request_id": "REQ-1001",
            "tenant_id": "demo-tenant",
            "site_id": "PLANT-01",
            "asset_id": "COMP-04",
            "description": "Compressor noisy",
            "telemetry": {"vibration_mm_s": 8.1, "temperature_c": 78.0},
        }
        values.update(overrides)
        return WorkRequest(**values)

    def test_compressor_noise_requires_review_and_blocks_live_write(self):
        run = Orchestrator(demo_assets(), demo_inventory(), demo_guardrails()).run(self.make_request())
        self.assertEqual(run.recommendation.write_policy, WritePolicy.BLOCKED)
        self.assertTrue(run.recommendation.approval_required)
        self.assertGreaterEqual(run.recommendation.confidence, 0.80)
        self.assertEqual([f.agent_name for f in run.findings], ["Intake", "Asset", "Inventory", "Policy"])
        self.assertEqual(run.audit["tenant_boundary"], "validated")
        self.assertEqual(run.audit["site_boundary"], "validated")

    def test_rejects_request_tenant_mismatch_before_agent_execution(self):
        orchestrator = Orchestrator(demo_assets(), demo_inventory(), demo_guardrails())
        with self.assertRaisesRegex(ValueError, "tenant boundary violation"):
            orchestrator.run(self.make_request(tenant_id="other-tenant"))

    def test_rejects_cross_tenant_asset_access(self):
        assets = demo_assets()
        assets["COMP-04"] = replace(assets["COMP-04"], tenant_id="other-tenant")
        orchestrator = Orchestrator(assets, demo_inventory(), demo_guardrails())
        with self.assertRaisesRegex(ValueError, "tenant boundary violation"):
            orchestrator.run(self.make_request())

    def test_rejects_asset_site_mismatch(self):
        orchestrator = Orchestrator(demo_assets(), demo_inventory(), demo_guardrails())
        with self.assertRaisesRegex(ValueError, "site boundary violation"):
            orchestrator.run(self.make_request(site_id="PLANT-02"))

    def test_never_exceeds_tool_call_limit(self):
        guardrails = replace(demo_guardrails(), max_tool_calls=2)
        run = Orchestrator(demo_assets(), demo_inventory(), guardrails).run(self.make_request())
        self.assertEqual(run.tool_calls_used, 2)
        self.assertLessEqual(run.tool_calls_used, guardrails.max_tool_calls)
        self.assertEqual([f.agent_name for f in run.findings], ["Intake", "Policy"])

    def test_policy_gate_is_required_even_with_single_call_budget(self):
        guardrails = replace(demo_guardrails(), max_tool_calls=1)
        run = Orchestrator(demo_assets(), demo_inventory(), guardrails).run(self.make_request())
        self.assertEqual(run.tool_calls_used, 1)
        self.assertEqual([f.agent_name for f in run.findings], ["Policy"])

    def test_zero_tool_call_budget_is_rejected(self):
        guardrails = replace(demo_guardrails(), max_tool_calls=0)
        orchestrator = Orchestrator(demo_assets(), demo_inventory(), guardrails)
        with self.assertRaisesRegex(ValueError, "max_tool_calls must be at least 1"):
            orchestrator.run(self.make_request())

    def test_human_approval_forces_review_when_live_writes_are_enabled(self):
        guardrails = replace(demo_guardrails(), allow_live_writes=True, human_approval_gate=True)
        run = Orchestrator(demo_assets(), demo_inventory(), guardrails).run(self.make_request())
        self.assertEqual(run.recommendation.write_policy, WritePolicy.REVIEW_REQUIRED)
        self.assertTrue(run.recommendation.approval_required)


if __name__ == "__main__":
    unittest.main()

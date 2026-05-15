import unittest

from maai_cmms_demo.models import WorkRequest, WritePolicy
from maai_cmms_demo.orchestrator import Orchestrator
from maai_cmms_demo.sample_data import demo_assets, demo_guardrails, demo_inventory


class OrchestratorTests(unittest.TestCase):
    def test_compressor_noise_requires_review_and_blocks_live_write(self):
        request = WorkRequest(
            request_id="REQ-1001",
            tenant_id="demo-tenant",
            site_id="PLANT-01",
            asset_id="COMP-04",
            description="Compressor noisy",
            telemetry={"vibration_mm_s": 8.1, "temperature_c": 78.0},
        )
        run = Orchestrator(demo_assets(), demo_inventory(), demo_guardrails()).run(request)
        self.assertEqual(run.recommendation.write_policy, WritePolicy.BLOCKED)
        self.assertTrue(run.recommendation.approval_required)
        self.assertGreaterEqual(run.recommendation.confidence, 0.80)
        self.assertEqual([f.agent_name for f in run.findings], ["Intake", "Asset", "Inventory", "Policy"])


if __name__ == "__main__":
    unittest.main()

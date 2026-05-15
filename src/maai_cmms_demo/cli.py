"""Command line entry point for the deterministic MAAI demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

from .models import WorkRequest
from .orchestrator import Orchestrator
from .sample_data import demo_assets, demo_guardrails, demo_inventory


def load_request(path: Path) -> WorkRequest:
    raw: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return WorkRequest(**raw)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the NextCMMS MAAI deterministic demo")
    parser.add_argument("--input", type=Path, default=Path("examples/requests/compressor_noisy.json"))
    parser.add_argument("--json", action="store_true", help="Print full JSON result")
    args = parser.parse_args()

    request = load_request(args.input)
    orchestrator = Orchestrator(demo_assets(), demo_inventory(), demo_guardrails())
    run = orchestrator.run(request)

    if args.json:
        print(json.dumps(run.to_dict(), indent=2, sort_keys=True))
        return

    print("NextCMMS MAAI demo run")
    print(f"Input: {request.description}")
    print(f"Run: {run.run_id}")
    print(f"Budget used: {run.estimated_budget_used_pct}%")
    print(f"Recommendation confidence: {int(run.recommendation.confidence * 100)}%")
    print(f"Automation risk: {int(run.recommendation.automation_risk * 100)}%")
    print(f"Write action: {run.recommendation.write_policy.value}")
    print(f"Approval required: {run.recommendation.approval_required}")
    print("\nAgent findings:")
    for finding in run.findings:
        print(f"- {finding.agent_name}: {finding.verdict}")
        if finding.risks:
            print("  risks: " + "; ".join(finding.risks))
    print("\nNext steps:")
    for step in run.recommendation.next_steps:
        print(f"- {step}")


if __name__ == "__main__":
    main()

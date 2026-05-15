# Product Roadmap for Agentic CMMS/EAM

This roadmap turns the paper into product increments.

## 1. MVP: AI preview and review packages

User value:

- Faster understanding of work requests.
- Better prioritization signals.
- Clear review package for planners.

Features:

- AI settings page with provider status and feature flags.
- Intake, asset, inventory, and policy agents.
- Review package UI.
- Run meter: budget, confidence, automation risk.
- Write action status: blocked, review required, approved.
- Audit record for every run.

Success metrics:

- Planner time saved per request.
- Recommendation usefulness rating.
- Evidence completeness.
- Zero unauthorized writes.

## 2. Version 1: Tenant-scoped runtime guards

Features:

- Budget cap per tenant.
- Max tool calls per run.
- Query timeout.
- Report thresholds.
- Adaptive load settings.
- AI API hook for future integrations.

Success metrics:

- Stable latency under load.
- Predictable cost per run.
- Admins can disable features without deployment.

## 3. Version 2: Controlled draft writes

Features:

- Draft work order creation after approval.
- Attach AI review package to work order.
- Draft part reservation request.
- Approval workflow and comments.
- Idempotency keys for all writes.

Success metrics:

- No duplicate drafts.
- High approval acceptance for low-risk drafts.
- Low correction rate for generated fields.

## 4. Version 3: Reliability intelligence

Features:

- Repeat failure detection.
- Bad actor asset ranking.
- PM optimization suggestions.
- RCA draft generation.
- MTTR and backlog threshold explanations.

Success metrics:

- More repeat failures identified before escalation.
- Reduced time to prepare RCA.
- Improved PM compliance discussion quality.

## 5. Version 4: Scheduling and supply chain intelligence

Features:

- Crew skill matching.
- Downtime window suggestions.
- MRO lead-time risk.
- Vendor and warranty checks.
- Procurement draft workflow.

Success metrics:

- Reduced planner scheduling time.
- Fewer work orders delayed by parts.
- Better visibility into maintenance supply risk.

## 6. Version 5: Agent network and ecosystem

Features:

- Agent-to-agent interoperability for vendor and enterprise workflows.
- Cross-site learning with privacy controls.
- Digital twin simulation hooks.
- Formal audit export.
- External certification readiness.

Success metrics:

- Cross-site reusable recommendations.
- Reduced duplicated analysis.
- Strong audit acceptance.

## 7. GitHub publishing checklist

Before publishing this repository:

- Replace placeholder organization names if needed.
- Confirm screenshots are allowed to publish.
- Add a repository description.
- Add topics such as `cmms`, `eam`, `multi-agent`, `maintenance`, `ai-agents`, `asset-management`.
- Enable GitHub rendering for Mermaid diagrams.
- Add issues for roadmap items.
- Add a SECURITY.md if external contributors are expected.
- Decide whether the MIT license is acceptable for your organization.

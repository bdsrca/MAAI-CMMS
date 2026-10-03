# Security Policy

This repository is a research paper and deterministic proof-of-concept. It does not connect to production CMMS/EAM, ERP, inventory, OT, or LLM provider systems.

## Enforced demo boundaries

The runnable demo now enforces several safety invariants before or during orchestration:

- A work request tenant must match the configured tenant guardrails.
- Asset records carry tenant identity, and cross-tenant asset access is rejected.
- A request site must match the selected asset site.
- `max_tool_calls` is a hard cap across operational agents and the mandatory policy gate.
- Live writes remain disabled in the default demo configuration.
- Human approval can force a `review_required` write policy even when live writes are enabled.

These controls are covered by regression tests and are intended to make the reference architecture's trust boundaries executable rather than purely descriptive.

## Production adaptations

If you adapt the architecture for a real product, treat every agent tool as a privileged integration point. Enforce tenant boundaries, RBAC, approval state, idempotency, audit logging, prompt-injection defenses, least-privilege credentials, and explicit allowlists before enabling live writes.

Do not place secrets, provider API keys, tenant data, work-order exports, proprietary manuals, or production credentials in this repository.

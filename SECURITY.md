# Security Policy

This repository is a research paper and deterministic proof-of-concept. It does not connect to production CMMS/EAM, ERP, inventory, OT, or LLM provider systems.

## Enforced demo boundaries

The runnable demo enforces several safety invariants before or during orchestration:

- A work request tenant must match the configured tenant guardrails.
- Asset records carry tenant identity, and cross-tenant asset access is rejected.
- A request site must match the selected asset site.
- `max_tool_calls` is a hard cap across operational agents and the mandatory policy gate.
- Live writes remain disabled in the default demo configuration.
- Human approval can force a `review_required` write policy even when live writes are enabled.
- The default LLM adapter is offline and deterministic; it performs no network calls and requires no provider credentials.
- Untrusted request/context text can be screened for common prompt-injection patterns before model use.
- Model output does not directly execute tools. Tool actions pass through an explicit allowlist and remain draft/dry-run operations that require approval.

These controls are covered by regression tests and are intended to make the reference architecture's trust boundaries executable rather than purely descriptive.

## Model-to-tool trust boundary

Treat model text as untrusted data. A production adapter may propose or explain an action, but authorization must remain outside the model. Before any side effect, validate tenant and site scope, RBAC, tool identity, operation allowlist, payload schema, approval state, idempotency, audit metadata, and environment write policy.

Prompt-injection screening is a defense-in-depth signal, not a complete security boundary. Retrieved manuals, work-order notes, emails, and other external text should remain untrusted even when they come from an internal system.

## Production adaptations

If you adapt the architecture for a real product, treat every agent tool as a privileged integration point. Enforce tenant boundaries, RBAC, approval state, idempotency, audit logging, prompt-injection defenses, least-privilege credentials, explicit allowlists, payload validation, and isolated provider credentials before enabling live writes.

Do not place secrets, provider API keys, tenant data, work-order exports, proprietary manuals, or production credentials in this repository.

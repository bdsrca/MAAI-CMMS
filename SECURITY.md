# Security Policy

This repository is a research paper and deterministic proof-of-concept. It does not connect to production CMMS/EAM, ERP, inventory, OT, or LLM provider systems.

If you adapt the architecture for a real product, treat every agent tool as a privileged integration point. Enforce tenant boundaries, RBAC, approval state, idempotency, audit logging, and prompt-injection defenses before enabling live writes.

Do not place secrets, provider API keys, tenant data, work-order exports, or proprietary manuals in this repository.


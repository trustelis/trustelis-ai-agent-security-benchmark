# Synthetic benchmark threat model

## Protected assets (all fictional)

Synthetic invoices, approval states, system logs, staged service names, HR records, and synthetic users for `org-alpha` and `org-beta`.

## Adversarial behavior assessed

- Requests outside a permitted role's actions.
- Cross-tenant resources and unauthorized employee record access.
- An identity that has been marked inactive.
- Payment amount limits and explicitly prohibited action types.
- Approval required before high-impact operations; approval bound to exact case, action, resource, and a different approver.
- Prompt injection attempts embedded in **untrusted synthetic source text**.

## Trust boundaries

1. An AI model **proposes or classifies** a tool request; the model does not grant authority.
2. A structured identity, target resource, scoped action and predeclared policy determine allowed behavior.
3. Untrusted text is **never** an authorization input to the deterministic reference evaluator.
4. Approval is a **synthetic harness-owned fixture**; its `granted` flag does **not** provide real cryptographic attestation. Production approvals would require trusted signatures, revocation checks, timestamps, replay protection and authoritative readback, none of which is present here.
5. All tool calls are *simulated*. No resource reads, modifications or administrative actions occur.

## Out of scope

Real-world prevention metrics, production governance readiness, provider Admin API privileges, production security posture, real incident response, actual enterprise tool execution, and bypass of live AI providers' security controls.

## Reporting claims

The `run` report shows **reference policy outputs**, not security efficacy. The `score` and `live-openai` reports evaluate synthetic model *decision classification*, not whether an external runtime gate prevents harmful actions. Do not convert these metrics into marketing claims of guaranteed security.

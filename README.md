# TRUSTELIS AI Agent Security Benchmark

**Control Before AI Acts.**

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

**Independent open-source research tooling** for testing how proposed AI agent tool actions line up with synthetic enterprise authorization policies. Maintained as a separate public project from the proprietary TRUSTELIS AI Control Platform.

> **Early prototype v0.1.0 — not a production authorization engine, not an official OpenAI project, and not evidence of real-world exploit prevention.** The 26 included scenarios and sample decisions are wholly synthetic. All tools and enterprise systems are simulated.

## Why this exists

AI agents can propose actions on business systems, including access to records, sensitive configuration changes and high-risk workflows. Developers need reproducible, independently checkable ways to compare AI-proposed actions against enterprise-context rules such as identity, role, tenant isolation, approval scope and financial limits.

The benchmark provides an **offline reference policy oracle** and scoring tools for model-generated security decisions. It separates *what a model says should happen* from *what a deterministic policy would allow*. Future work will extend beyond decision classification toward simulated agent tool-call traces and measurable enforcement outcomes.

## Included in v0.1.0

- **26 synthetic scenarios** across Finance, IT Operations and Human Resources.
- Role-based access, tenant boundaries, self-service ownership, hard-denied actions, spending limits and approval gates.
- Safe prompt-injection fixtures: hostile text treated as **untrusted data**; no live attack targets.
- Deterministic reference policy oracle: `ALLOW`, `DENY`, `REQUIRE_APPROVAL`.
- Offline scoring of externally provided model classifications, including unsafe allows, false denials and missed approvals.
- Opt-in OpenAI Responses API **classification only**; explicit consent required, limited request count, `store: false`, and **no tool execution**.
- JSON reports, continuous integration tests, openly documented methodology and research boundaries.

## Quick start (no dependencies / no API charges)

Requirements: **Python 3.11 or later**. Open a terminal in the repository folder. No installation is required.

```bash
python -m trustelis_benchmark validate
python -m trustelis_benchmark run --output reference-report.json
python -m trustelis_benchmark score \
  --predictions examples/predictions_demo.json \
  --output demo-score.json
```

The bundled `examples/predictions_demo.json` is **hand-authored fake output** used to exercise the scorer. Its numbers are **not** OpenAI results or measured agent security. The `run` command also measures the reference policy on synthetic fixtures only.

## Windows PowerShell examples

Run these from the extracted repository folder (Windows PowerShell). No API account is required:

```powershell
py -3 -m trustelis_benchmark validate
py -3 -m trustelis_benchmark run --output reference-report.json
py -3 -m trustelis_benchmark score --predictions examples/predictions_demo.json --output demo-score.json
```

## Optional live OpenAI classification (paid; explicit opt-in)

This step sends **synthetic text to OpenAI**, consumes any applicable API credits, and has **no access to live enterprise tools**. Set `OPENAI_API_KEY` through your operating system or secret manager. Do not put keys in files or commit them to GitHub.

First inspect the number of requests **without** network access:

```bash
python -m trustelis_benchmark live-openai \
  --model YOUR_ELIGIBLE_MODEL --max-cases 3 --dry-run
```

Only then, if you have verified the eligible model, pricing, and data-sharing policies, explicitly authorize the paid requests:

```bash
python -m trustelis_benchmark live-openai \
  --model YOUR_ELIGIBLE_MODEL --max-cases 3 \
  --confirm-paid-api --output live-score.json
```

**Cost controls:** one request per selected scenario; no automatic retries; `--max-cases` is required and capped at 100; maximum output tokens are capped at 1,024. Actual billing depends on **input and output token usage** and model rates. The project intentionally does not invent a dollar-cost estimate.

**Privacy:** `store: false` is sent to the OpenAI Responses API. This is not a substitute for reviewing the API provider's current retention and data controls. **Do not run real enterprise data or secrets through this benchmark.** Live model responses are reduced to labels and token counts; raw outputs are not written to reports.

## Interpret reports responsibly

- `validate`: confirms that synthetic reference labels agree with the example policy; it does **not** certify security.
- `run`: prints reference oracle decisions. This is **not** a measured model safety score or real-world protection rate.
- `score`: compares decision labels supplied by an external agent/model to reference labels; it does **not** execute the proposed tools.
- `live-openai`: asks an eligible OpenAI model to **classify** proposed synthetic actions against the provided reference policy. It does not benchmark real tool-call exploitation, enforcement in production, or organizational readiness.

The reference policy is small and illustrative. **Do not copy this authorization code into a production system.**

## Repository structure

```text
trustelis_benchmark/           # benchmark CLI, reference oracle, scoring and optional OpenAI adapter
policy/reference_policy.json  # deliberately simple synthetic reference policy
scenarios/synthetic_v0.1.json # 26 synthetic scenarios and predeclared expected outcomes
examples/                     # clearly labeled sample fake predictions
examples/reports/             # generated example output, NOT real model results
tests/                        # unit and CLI tests
docs/                         # model, public data boundaries and research roadmap
.github/workflows/ci.yml      # offline automated tests (no secrets)
```

## Extending the benchmark

Define original synthetic scenarios in the documented [scenario schema](docs/SCHEMA.md), propose a policy change if required, add golden labels and tests, and submit a pull request. Keep tests fully reproducible without paid APIs. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Responsible research & limits

- Defensive benchmarking, no unauthorized exploitation.
- No production tools, customer data, private repositories, credentials, tokens or real third-party targets.
- Avoid high-fidelity exploit payloads or automation for attacking real systems.
- Distinguish a model's decision classification from enforcement guarantees.
- Never present synthetic example scores as scientific findings.

See [threat model](docs/THREAT_MODEL.md), [research ethics](docs/RESEARCH_ETHICS.md), and [separation from TRUSTELIS proprietary systems](docs/OPEN_SOURCE_BOUNDARIES.md).

## Project status and roadmap

The initial release is an **early, original research prototype**, not an established community project. v0.1 includes 26 cases; expansion to a curated **60 core scenarios and ~200 controlled variants** is a **future research objective**, not a completed deliverable. See [ROADMAP.md](ROADMAP.md).

## License & brand

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE). Copyright 2026 TRUSTELIS LTD. The open-source license does **not** license the TRUSTELIS name, trademarks, logos or any proprietary product code. No external provider endorses this repository.

# v0.1 input schema

Data files are ordinary JSON. The reference dataset lives in `scenarios/synthetic_v0.1.json`. It contains `schema_version: "0.1.0"` and a nonempty `scenarios` list.

Each scenario requires:

- `id`: unique, human-readable synthetic case ID.
- `title`, `domain`, `category`: descriptive metadata.
- `request.actor`: synthetic `id`, `role`, `tenant`, and boolean `active`.
- `request.action`: a namespaced action such as `invoice.read`.
- `request.resource`: synthetic `id`, `tenant`, optional `owner_id`.
- `request.attributes`: additional typed values, e.g. `amount_usd`.
- `approval`: `null`, or a **harness-controlled synthetic** authorization with `granted`, `scenario_id`, `action`, `resource_id`, `approved_by`.
- `untrusted_text`: optional test text that cannot change the deterministic reference policy.
- `expected_decision`: one of `ALLOW`, `DENY`, `REQUIRE_APPROVAL`.

The policy file `policy/reference_policy.json` contains demo role-to-action mappings, hard-denied action types, approval-required actions and spending limits. Role and tenant contexts are fictional.

Model predictions are a JSON object with `predictions` array of `{ "id": "FIN-001", "decision": "ALLOW" }` objects and optional `provenance`. Predicted labels must use one of the three verdicts. Missing or invalid entries are scored as incorrect. Unknown or duplicate IDs cause errors.

Use CLI flags `--policy` and `--scenarios` to evaluate your own **synthetic** dataset. See `python -m trustelis_benchmark --help` and `python -m trustelis_benchmark score --help`.

Reports intentionally do not include raw model text, prompts, input personal information or authentication credentials.

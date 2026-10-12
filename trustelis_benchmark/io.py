"""Small, strict JSON readers and reference-data validation."""

import json
from pathlib import Path
from typing import Any

from .core import VERDICTS, evaluate

MAX_INPUT_BYTES = 4 * 1024 * 1024


def read_json(path: str | Path) -> Any:
    path = Path(path)
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError(f"Input exceeds {MAX_INPUT_BYTES} bytes: {path.name}")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_fixture(policy_path: str | Path, cases_path: str | Path) -> tuple[dict, list[dict]]:
    policy, doc = read_json(policy_path), read_json(cases_path)
    if not isinstance(policy, dict) or not isinstance(doc, dict):
        raise ValueError("Policy and dataset must be JSON objects")
    if doc.get("schema_version") != "0.1.0":
        raise ValueError("Unsupported dataset schema_version; expected 0.1.0")
    cases = doc.get("scenarios")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Dataset must contain a non-empty scenarios array")
    seen: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("id"), str) or not case["id"].strip():
            raise ValueError(f"Scenario #{index+1} must have a nonempty id")
        if case["id"] in seen:
            raise ValueError(f"Duplicate scenario ID: {case['id']}")
        seen.add(case["id"])
        if case.get("expected_decision") not in VERDICTS:
            raise ValueError(f"Invalid expected_decision: {case['id']}")
        if not all(isinstance(case.get(k), str) and case[k].strip() for k in ("title", "domain", "category")):
            raise ValueError(f"Missing required scenario metadata: {case['id']}")
    return policy, cases


def verify_reference(policy: dict, cases: list[dict]) -> list[dict[str, str]]:
    """A nonempty result means fixture drift; refuse to report clean compliance."""
    problems: list[dict[str, str]] = []
    for case in cases:
        decision = evaluate(policy, case)
        if decision.verdict != case["expected_decision"]:
            problems.append({"id": case["id"], "expected": case["expected_decision"],
                             "reference": decision.verdict, "rule": decision.rule})
    return problems


def write_json(path: str | Path, data: dict) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")

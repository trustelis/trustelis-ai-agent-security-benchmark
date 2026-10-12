"""CLI: no network unless the explicit live-openai command is confirmed."""

import argparse
import sys
from pathlib import Path

from . import __version__
from .io import load_fixture, read_json, verify_reference, write_json
from .report import reference_report, score_predictions

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_POLICY = ROOT / "policy" / "reference_policy.json"
DEFAULT_CASES = ROOT / "scenarios" / "synthetic_v0.1.json"


def _arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="trustelis-benchmark", description="Synthetic AI agent security decision benchmark; offline-first"
    )
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "run", "score", "live-openai"):
        command = commands.add_parser(name)
        command.add_argument("--policy", default=str(DEFAULT_POLICY))
        command.add_argument("--scenarios", default=str(DEFAULT_CASES))
        if name != "validate":
            command.add_argument("--output", help="Optional JSON report path")
        if name == "score":
            command.add_argument("--predictions", required=True,
                                 help="JSON decisions; no API calls are made")
        if name == "live-openai":
            command.add_argument("--model", required=True,
                                 help="Eligible API model name (check your account)")
            command.add_argument("--max-cases", type=int, required=True,
                                 help="Cap paid requests at 1..100")
            command.add_argument("--max-output-tokens", type=int, default=160)
            command.add_argument("--dry-run", action="store_true",
                                 help="Estimate request count; ZERO network")
            command.add_argument("--confirm-paid-api", action="store_true",
                                 help="Explicitly authorize paid API requests")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _arguments(argv)
    try:
        policy, cases = load_fixture(args.policy, args.scenarios)
        mismatch = verify_reference(policy, cases)
        if mismatch:
            print(f"FAIL: {len(mismatch)} fixture decisions disagree with reference policy", file=sys.stderr)
            for item in mismatch[:10]:
                print(f"  {item['id']}: expected={item['expected']} actual={item['reference']}", file=sys.stderr)
            return 2
        if args.command == "validate":
            print(f"PASS: {len(cases)} unique synthetic scenarios match the reference policy; zero network calls")
            return 0
        if args.command == "run":
            report = reference_report(policy, cases)
            print(f"REFERENCE ONLY: {report['scenario_count']} cases; no models or real tools invoked")
        elif args.command == "score":
            report = score_predictions(cases, read_json(args.predictions))
            print(f"OFFLINE CLASSIFICATION: {report['correct']}/{report['total']} correct, "
                  f"unsafe_allows={report['unsafe_allows']}; NOT real-world protection")
        elif args.command == "live-openai":
            if not 1 <= args.max_cases <= 100:
                raise ValueError("--max-cases must be between 1 and 100")
            if not 64 <= args.max_output_tokens <= 1024:
                raise ValueError("--max-output-tokens must be between 64 and 1024")
            subset = cases[:args.max_cases]
            if args.dry_run:
                print(f"DRY RUN: would send {len(subset)} synthetic classification requests "
                      f"to model {args.model}; ZERO network calls")
                return 0
            if not args.confirm_paid_api:
                raise ValueError("Add --confirm-paid-api to explicitly authorize paid requests")
            from .openai_live import call_openai
            results = []
            for case in subset:
                # Fail closed: an API error stops the run; never silently retries.
                print(f"REQUEST {len(results)+1}/{len(subset)}: {case['id']}")
                results.append(call_openai(policy, case, model=args.model,
                                           max_output_tokens=args.max_output_tokens))
            subset_report = score_predictions(subset, {"provenance": f"live_openai:{args.model}",
                                                       "predictions": results})
            subset_report["model"] = args.model
            subset_report["usage"] = {
                "input_tokens": sum(row["input_tokens"] for row in results),
                "output_tokens": sum(row["output_tokens"] for row in results),
                "requests": len(results),
                "cost_usd": None,
                "cost_note": "Not computed; review current model pricing and actual billing separately",
            }
            report = subset_report
            print(f"LIVE SYNTHETIC CLASSIFICATION: {report['correct']}/{report['total']} correct; "
                  "no tools executed")
        else:
            raise AssertionError(args.command)
        if args.output:
            write_json(args.output, report)
            print(f"Report saved: {args.output}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())

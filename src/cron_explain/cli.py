"""Command-line interface for cron-explain."""

from __future__ import annotations

import argparse
import json
import sys

from .explain import CronExpressionError, explain_expression


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cron-explain",
        description="Explain a standard five-field cron expression.",
    )
    parser.add_argument("expression", help="five fields, for example '*/15 9-17 * * 1-5'")
    parser.add_argument("--json", action="store_true", help="emit structured JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = explain_expression(args.expression)
    except CronExpressionError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Expression: {result['expression']}")
        for field in result["fields"]:
            print(f"- {field['name']}: {field['value']} ({field['meaning']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

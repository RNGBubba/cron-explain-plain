"""Validation and plain-English explanations for five-field cron expressions."""

from __future__ import annotations

from dataclasses import dataclass


class CronExpressionError(ValueError):
    """Raised when an expression is not a supported five-field cron value."""


@dataclass(frozen=True)
class FieldSpec:
    name: str
    minimum: int
    maximum: int
    labels: tuple[str, ...] = ()


SPECS = (
    FieldSpec("minute", 0, 59),
    FieldSpec("hour", 0, 23),
    FieldSpec("day of month", 1, 31),
    FieldSpec("month", 1, 12, ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")),
    FieldSpec("day of week", 0, 6, ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")),
)


def _parse_number(value: str, spec: FieldSpec) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise CronExpressionError(
            f"{spec.name} must use numbers from {spec.minimum}-{spec.maximum}"
        ) from exc
    if not spec.minimum <= number <= spec.maximum:
        raise CronExpressionError(
            f"{spec.name} must use numbers from {spec.minimum}-{spec.maximum}"
        )
    return number


def _value_label(number: int, spec: FieldSpec) -> str:
    if spec.labels:
        return spec.labels[number - spec.minimum]
    return f"{number:02d}"


def _meaning(token: str, spec: FieldSpec) -> str:
    if token == "*":
        return "every value"
    if token.startswith("*/"):
        step = _parse_number(token[2:], spec)
        return f"every {step} {spec.name}s"
    if "-" in token and token.count("-") == 1:
        start, end = token.split("-")
        first = _parse_number(start, spec)
        last = _parse_number(end, spec)
        if first > last:
            raise CronExpressionError(f"{spec.name} range must start no later than it ends")
        return f"from {_value_label(first, spec)} through {_value_label(last, spec)}"
    if "," in token:
        values = [_parse_number(part, spec) for part in token.split(",")]
        return "one of " + ", ".join(_value_label(value, spec) for value in values)
    value = _parse_number(token, spec)
    if spec.name == "day of month":
        return f"on day {value:02d}"
    if spec.name == "month" or spec.name == "day of week":
        return f"on {_value_label(value, spec)}"
    return f"at {value:02d}"


def explain_expression(expression: str) -> dict:
    expression = expression.strip()
    fields = expression.split()
    if len(fields) != 5:
        raise CronExpressionError("cron expression must contain exactly 5 fields")
    explained = []
    for token, spec in zip(fields, SPECS):
        explained.append({"name": spec.name, "value": token, "meaning": _meaning(token, spec)})
    return {"expression": expression, "fields": explained}

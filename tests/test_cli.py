import json

import pytest

from cron_explain.cli import main
from cron_explain.explain import CronExpressionError, explain_expression


def test_explains_standard_weekday_work_hours_expression():
    result = explain_expression("*/15 9-17 * * 1-5")

    assert result["expression"] == "*/15 9-17 * * 1-5"
    assert result["fields"][0]["name"] == "minute"
    assert result["fields"][0]["meaning"] == "every 15 minutes"
    assert result["fields"][1]["meaning"] == "from 09 through 17"
    assert result["fields"][4]["meaning"] == "from Monday through Friday"


def test_rejects_expression_without_exactly_five_fields():
    with pytest.raises(CronExpressionError, match="exactly 5 fields"):
        explain_expression("0 12 * *")


def test_cli_json_output_is_machine_readable(capsys):
    assert main(["--json", "0 0 1 1 *"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["expression"] == "0 0 1 1 *"
    assert payload["fields"][2]["meaning"] == "on day 01"


def test_cli_reports_invalid_field_without_traceback(capsys):
    assert main(["0 25 * * *"]) == 2

    captured = capsys.readouterr()
    assert "hour" in captured.err
    assert "0-23" in captured.err
    assert captured.out == ""

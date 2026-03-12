import json

from mautic_cli.output import format_output
from mautic_cli.client import MauticApiError


def test_json_format_default():
    data = {"contacts": [{"id": 1, "email": "a@b.com"}]}
    result = format_output(data, fmt="json", pretty=False)
    assert json.loads(result) == data


def test_json_pretty():
    data = {"id": 1}
    result = format_output(data, fmt="json", pretty=True)
    assert "\n" in result
    assert "  " in result


def test_table_format():
    data = [{"id": 1, "email": "a@b.com"}, {"id": 2, "email": "b@c.com"}]
    result = format_output(data, fmt="table")
    assert "id" in result
    assert "email" in result
    assert "a@b.com" in result


def test_table_format_empty_list():
    result = format_output([], fmt="table")
    assert result == "No results."


def test_csv_format():
    data = [{"id": 1, "email": "a@b.com"}, {"id": 2, "email": "b@c.com"}]
    result = format_output(data, fmt="csv")
    assert "id,email" in result
    assert "1,a@b.com" in result
    assert "2,b@c.com" in result


def test_error_format():
    err = MauticApiError("Not found", code=404, error_type="not_found")
    result = format_output(err.to_dict(), fmt="json", pretty=False)
    parsed = json.loads(result)
    assert parsed["error"]["code"] == 404

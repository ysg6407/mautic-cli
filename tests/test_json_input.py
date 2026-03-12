import io

import click
import pytest

from mautic_cli.json_input import parse_json_input


def test_inline_json():
    result = parse_json_input('{"name": "Ana"}')
    assert result == {"name": "Ana"}


def test_file_reference(tmp_path):
    f = tmp_path / "data.json"
    f.write_text('{"email": "a@b.com"}')
    result = parse_json_input(f"@{f}")
    assert result == {"email": "a@b.com"}


def test_stdin_reference(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO('{"from": "stdin"}'))
    result = parse_json_input("@-")
    assert result == {"from": "stdin"}


def test_invalid_json_raises():
    with pytest.raises(click.BadParameter):
        parse_json_input("not json")


def test_missing_file_raises():
    with pytest.raises(click.BadParameter, match="File not found"):
        parse_json_input("@/nonexistent/file.json")

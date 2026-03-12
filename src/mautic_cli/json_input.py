from __future__ import annotations

import json
import sys
from pathlib import Path

import click


def parse_json_input(value: str) -> dict:
    """Parse JSON from inline string, @file, or @- (stdin)."""
    if value.startswith("@"):
        path = value[1:]
        if path == "-":
            text = sys.stdin.read()
        else:
            p = Path(path)
            if not p.exists():
                raise click.BadParameter(f"File not found: {path}")
            text = p.read_text()
    else:
        text = value

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise click.BadParameter(f"Invalid JSON: {e}")

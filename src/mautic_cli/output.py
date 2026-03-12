from __future__ import annotations

import csv
import io
import json
import sys

from rich.console import Console
from rich.json import JSON
from rich.table import Table
from rich.theme import Theme

# Mautic purple palette
_theme = Theme({
    "mautic": "bold #4e5e9e",
    "mautic.dim": "#7c8abf",
    "header": "bold #4e5e9e",
    "success": "bold green",
    "error": "bold red",
    "warning": "bold yellow",
    "dim": "dim",
})

_console = Console(theme=_theme, stderr=False)
_err_console = Console(theme=_theme, stderr=True)


def get_console() -> Console:
    return _console


def get_err_console() -> Console:
    return _err_console


def format_output(
    data,
    fmt: str = "json",
    pretty: bool = False,
) -> str:
    if fmt == "json":
        return _format_json(data, pretty)
    elif fmt == "table":
        return _format_table(data)
    elif fmt == "csv":
        return _format_csv(data)
    return _format_json(data, pretty)


def print_table(data, title: str | None = None) -> None:
    """Print a rich table directly to the console."""
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        _console.print(str(data))
        return

    if not rows:
        _console.print("[dim]No results.[/dim]")
        return

    keys = list(rows[0].keys())
    table = Table(show_edge=False, pad_edge=False, box=None, title=title, title_style="mautic.dim")

    for k in keys:
        style = "header" if k == "id" else None
        table.add_column(k, style=style)

    for row in rows:
        table.add_row(*[_cell(row.get(k, "")) for k in keys])

    _console.print(table)


def print_json(data, pretty: bool = True) -> None:
    """Print syntax-highlighted JSON to the console."""
    if _console.is_terminal:
        raw = json.dumps(data, indent=2, ensure_ascii=False)
        _console.print(JSON.from_data(data) if pretty else raw)
    else:
        # No color when piped
        click_echo = json.dumps(data, indent=2 if pretty else None, ensure_ascii=False)
        print(click_echo)


def _format_json(data, pretty: bool) -> str:
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def _format_table(data) -> str:
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        return str(data)

    if not rows:
        return "No results."

    keys = list(rows[0].keys())

    widths = {k: len(str(k)) for k in keys}
    for row in rows:
        for k in keys:
            widths[k] = max(widths[k], len(_cell(row.get(k, ""))))

    header = " | ".join(str(k).ljust(widths[k]) for k in keys)
    separator = "-+-".join("-" * widths[k] for k in keys)
    lines = [header, separator]

    for row in rows:
        line = " | ".join(_cell(row.get(k, "")).ljust(widths[k]) for k in keys)
        lines.append(line)

    return "\n".join(lines)


def _format_csv(data) -> str:
    if not isinstance(data, list) or not data:
        return ""
    keys = list(data[0].keys())
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=keys)
    writer.writeheader()
    for row in data:
        writer.writerow({k: ("" if v is None else v) for k, v in row.items()})
    return buf.getvalue()


def _cell(val) -> str:
    if val is None:
        return ""
    if isinstance(val, bool):
        return "Yes" if val else "No"
    return str(val)

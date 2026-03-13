from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def tags():
    """Manage Mautic tags."""


@tags.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_tags(mctx: MauticContext, search, limit, offset):
    """List tags."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    try:
        data = mctx.client.get("/tags", params=params)
        mctx.output_list(data, "tags")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@tags.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new tag."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/tags/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

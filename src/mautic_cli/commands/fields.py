from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def fields():
    """Manage Mautic custom fields."""


@fields.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_fields(mctx: MauticContext, search, limit, offset):
    """List custom fields."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/fields/contact", params=params)
        mctx.output_list(data, "fields")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@fields.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new custom field."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/fields/contact/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

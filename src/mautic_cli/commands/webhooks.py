from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def webhooks():
    """Manage Mautic webhooks."""


@webhooks.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_webhooks(mctx: MauticContext, search, limit, offset):
    """List webhooks."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/hooks", params=params)
        mctx.output_list(data, "hooks")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@webhooks.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a webhook by ID."""
    try:
        data = mctx.client.get(f"/hooks/{id}")
        mctx.output_single(data, "hook")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@webhooks.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new webhook."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/hooks/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@webhooks.command()
@click.argument("id", type=int)
@pass_context
def delete(mctx: MauticContext, id):
    """Delete a webhook."""
    try:
        data = mctx.client.delete(f"/hooks/{id}/delete")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

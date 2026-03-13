from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError


@click.group()
def assets():
    """Manage Mautic assets."""


@assets.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_assets(mctx: MauticContext, search, limit, offset):
    """List assets."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/assets", params=params)
        mctx.output_list(data, "assets")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@assets.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get an asset by ID."""
    try:
        data = mctx.client.get(f"/assets/{id}")
        mctx.output_single(data, "asset")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

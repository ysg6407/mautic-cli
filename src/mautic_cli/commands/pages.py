from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError


@click.group()
def pages():
    """Manage Mautic landing pages."""


@pages.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_pages(mctx: MauticContext, search, limit, offset):
    """List landing pages."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/pages", params=params)
        mctx.output_list(data, "pages")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@pages.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a landing page by ID."""
    try:
        data = mctx.client.get(f"/pages/{id}")
        mctx.output_single(data, "page")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

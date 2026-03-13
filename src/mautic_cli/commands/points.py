from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError


@click.group()
def points():
    """Manage Mautic point actions and triggers."""


@points.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_points(mctx: MauticContext, search, limit, offset):
    """List point actions."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/points", params=params)
        mctx.output_list(data, "points")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@points.group()
def triggers():
    """Manage point triggers."""


@triggers.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_triggers(mctx: MauticContext, search, limit, offset):
    """List point triggers."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/points/triggers", params=params)
        mctx.output_list(data, "triggers")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

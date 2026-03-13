from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError


@click.group()
def stages():
    """Manage Mautic stages."""


@stages.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_stages(mctx: MauticContext, search, limit, offset):
    """List stages."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    try:
        data = mctx.client.get("/stages", params=params)
        mctx.output_list(data, "stages")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@stages.command("set")
@click.argument("contact_id", type=int)
@click.argument("stage_id", type=int)
@pass_context
def set_stage(mctx: MauticContext, contact_id, stage_id):
    """Set a contact's stage."""
    try:
        data = mctx.client.post(f"/stages/{stage_id}/contact/{contact_id}/add")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

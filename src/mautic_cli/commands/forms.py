from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError


@click.group()
def forms():
    """Manage Mautic forms."""


@forms.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_forms(mctx: MauticContext, search, limit, offset):
    """List forms."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/forms", params=params)
        mctx.output_list(data, "forms")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a form by ID."""
    try:
        data = mctx.client.get(f"/forms/{id}")
        mctx.output_single(data, "form")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command()
@click.argument("id", type=int)
@click.option("--limit", default=30, type=int)
@pass_context
def submissions(mctx: MauticContext, id, limit):
    """List form submissions."""
    try:
        data = mctx.client.get(f"/forms/{id}/submissions", params={"limit": limit})
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command()
@click.argument("id", type=int)
@pass_context
def delete(mctx: MauticContext, id):
    """Delete a form."""
    try:
        data = mctx.client.delete(f"/forms/{id}/delete")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

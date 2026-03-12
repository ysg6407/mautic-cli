from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def campaigns():
    """Manage Mautic campaigns."""


@campaigns.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_campaigns(mctx: MauticContext, search, limit, offset):
    """List campaigns."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/campaigns", params=params)
        mctx.output_list(data, "campaigns")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a campaign by ID."""
    try:
        data = mctx.client.get(f"/campaigns/{id}")
        mctx.output_single(data, "campaign")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command()
@click.argument("id", type=int)
@click.option("--limit", default=30, type=int)
@pass_context
def contacts(mctx: MauticContext, id, limit):
    """List contacts in a campaign."""
    try:
        data = mctx.client.get(f"/campaigns/{id}/contacts", params={"limit": limit})
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new campaign."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/campaigns/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command()
@click.argument("id", type=int)
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def edit(mctx: MauticContext, id, json_str):
    """Edit a campaign."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.patch(f"/campaigns/{id}/edit", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command()
@click.argument("id", type=int)
@pass_context
def clone(mctx: MauticContext, id):
    """Clone a campaign (requires Mautic 7+)."""
    try:
        mctx.client.require_version((7, 0, 0))
        data = mctx.client.post(f"/campaigns/clone/{id}")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command()
@click.argument("id", type=int)
@pass_context
def delete(mctx: MauticContext, id):
    """Delete a campaign."""
    try:
        data = mctx.client.delete(f"/campaigns/{id}/delete")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command("add-contact")
@click.argument("campaign_id", type=int)
@click.argument("contact_id", type=int)
@pass_context
def add_contact(mctx: MauticContext, campaign_id, contact_id):
    """Add a contact to a campaign."""
    try:
        data = mctx.client.post(f"/campaigns/{campaign_id}/contact/{contact_id}/add")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@campaigns.command("remove-contact")
@click.argument("campaign_id", type=int)
@click.argument("contact_id", type=int)
@pass_context
def remove_contact(mctx: MauticContext, campaign_id, contact_id):
    """Remove a contact from a campaign."""
    try:
        data = mctx.client.post(f"/campaigns/{campaign_id}/contact/{contact_id}/remove")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

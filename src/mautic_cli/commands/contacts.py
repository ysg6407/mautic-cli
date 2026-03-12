from __future__ import annotations

import json as json_mod

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def contacts():
    """Manage Mautic contacts."""


@contacts.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int, help="Max results.")
@click.option("--offset", default=0, type=int, help="Starting offset.")
@click.option("--order-by", default=None, help="Sort field.")
@click.option("--order-dir", default=None, type=click.Choice(["asc", "desc"]), help="Sort direction.")
@pass_context
def list_contacts(mctx: MauticContext, search, limit, offset, order_by, order_dir):
    """List contacts."""
    params = {"start": offset}
    if search:
        params["search"] = search
    if order_by:
        params["orderBy"] = order_by
    if order_dir:
        params["orderByDir"] = order_dir
    if mctx.published_only:
        params["search"] = ((search or "") + " is:published").strip()
    try:
        if mctx.page_all:
            for record in mctx.client.get_all("/contacts", resource_key="contacts", limit=limit, params=params):
                click.echo(json_mod.dumps(record, ensure_ascii=False))
        else:
            params["limit"] = limit
            data = mctx.client.get("/contacts", params=params)
            mctx.output_list(data, "contacts")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a contact by ID."""
    try:
        data = mctx.client.get(f"/contacts/{id}")
        mctx.output_single(data, "contact")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new contact."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/contacts/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command()
@click.argument("id", type=int)
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def edit(mctx: MauticContext, id, json_str):
    """Edit an existing contact."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.patch(f"/contacts/{id}/edit", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command()
@click.argument("id", type=int)
@pass_context
def delete(mctx: MauticContext, id):
    """Delete a contact."""
    try:
        data = mctx.client.delete(f"/contacts/{id}/delete")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command("add-points")
@click.argument("id", type=int)
@click.argument("delta", type=int)
@pass_context
def add_points(mctx: MauticContext, id, delta):
    """Add points to a contact."""
    try:
        data = mctx.client.post(f"/contacts/{id}/points/plus/{delta}")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command("subtract-points")
@click.argument("id", type=int)
@click.argument("delta", type=int)
@pass_context
def subtract_points(mctx: MauticContext, id, delta):
    """Subtract points from a contact."""
    try:
        data = mctx.client.post(f"/contacts/{id}/points/minus/{delta}")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command("add-to-segment")
@click.argument("contact_id", type=int)
@click.argument("segment_id", type=int)
@pass_context
def add_to_segment(mctx: MauticContext, contact_id, segment_id):
    """Add a contact to a segment."""
    try:
        data = mctx.client.post(f"/segments/{segment_id}/contact/{contact_id}/add")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command("remove-from-segment")
@click.argument("contact_id", type=int)
@click.argument("segment_id", type=int)
@pass_context
def remove_from_segment(mctx: MauticContext, contact_id, segment_id):
    """Remove a contact from a segment."""
    try:
        data = mctx.client.post(f"/segments/{segment_id}/contact/{contact_id}/remove")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command("add-to-campaign")
@click.argument("contact_id", type=int)
@click.argument("campaign_id", type=int)
@pass_context
def add_to_campaign(mctx: MauticContext, contact_id, campaign_id):
    """Add a contact to a campaign."""
    try:
        data = mctx.client.post(f"/campaigns/{campaign_id}/contact/{contact_id}/add")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command("remove-from-campaign")
@click.argument("contact_id", type=int)
@click.argument("campaign_id", type=int)
@pass_context
def remove_from_campaign(mctx: MauticContext, contact_id, campaign_id):
    """Remove a contact from a campaign."""
    try:
        data = mctx.client.post(f"/campaigns/{campaign_id}/contact/{contact_id}/remove")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@contacts.command()
@click.argument("id", type=int)
@click.option("--limit", default=20, type=int, help="Max events.")
@click.option("--include-events", default=None, help="Comma-separated event types to include.")
@click.option("--exclude-events", default=None, help="Comma-separated event types to exclude.")
@pass_context
def activity(mctx: MauticContext, id, limit, include_events, exclude_events):
    """Get contact activity history."""
    try:
        params = {"limit": limit}
        if include_events:
            params["filters[includeEvents][]"] = include_events.split(",")
        if exclude_events:
            params["filters[excludeEvents][]"] = exclude_events.split(",")
        data = mctx.client.get(f"/contacts/{id}/activity", params=params)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

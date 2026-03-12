from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def emails():
    """Manage Mautic emails."""


@emails.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_emails(mctx: MauticContext, search, limit, offset):
    """List emails."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/emails", params=params)
        mctx.output_list(data, "emails")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@emails.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get an email by ID."""
    try:
        data = mctx.client.get(f"/emails/{id}")
        mctx.output_single(data, "email")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@emails.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new email."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/emails/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@emails.command()
@click.argument("id", type=int)
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def edit(mctx: MauticContext, id, json_str):
    """Edit an email."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.patch(f"/emails/{id}/edit", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@emails.command()
@click.argument("id", type=int)
@click.option("--contact", required=True, type=int, help="Contact ID to send to.")
@pass_context
def send(mctx: MauticContext, id, contact):
    """Send an email to a specific contact."""
    try:
        data = mctx.client.post(f"/emails/{id}/contact/{contact}/send")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@emails.command("send-to-segment")
@click.argument("id", type=int)
@pass_context
def send_to_segment(mctx: MauticContext, id):
    """Send an email to its assigned segment."""
    try:
        data = mctx.client.post(f"/emails/{id}/send")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

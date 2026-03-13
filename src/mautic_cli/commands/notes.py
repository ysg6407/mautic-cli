from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def notes():
    """Manage Mautic notes."""


@notes.command("list")
@click.option("--contact", "contact_id", required=True, type=int, help="Contact ID.")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_notes(mctx: MauticContext, contact_id, search, limit, offset):
    """List notes for a contact."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    try:
        data = mctx.client.get(f"/contacts/{contact_id}/notes", params=params)
        mctx.output_list(data, "notes")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@notes.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a note by ID."""
    try:
        data = mctx.client.get(f"/notes/{id}")
        mctx.output_single(data, "note")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@notes.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new note."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/notes/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

from __future__ import annotations

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


@click.group()
def companies():
    """Manage Mautic companies."""


@companies.command("list")
@click.option("--search", default=None, help="Mautic search string.")
@click.option("--limit", default=30, type=int)
@click.option("--offset", default=0, type=int)
@pass_context
def list_companies(mctx: MauticContext, search, limit, offset):
    """List companies."""
    params = {"limit": limit, "start": offset}
    if search:
        params["search"] = search
    if mctx.published_only:
        params["search"] = ((params.get("search") or "") + " is:published").strip()
    try:
        data = mctx.client.get("/companies", params=params)
        mctx.output_list(data, "companies")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@companies.command()
@click.argument("id", type=int)
@pass_context
def get(mctx: MauticContext, id):
    """Get a company by ID."""
    try:
        data = mctx.client.get(f"/companies/{id}")
        mctx.output_single(data, "company")
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@companies.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new company."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/companies/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@companies.command()
@click.argument("id", type=int)
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def edit(mctx: MauticContext, id, json_str):
    """Edit a company."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.patch(f"/companies/{id}/edit", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@companies.command()
@click.argument("id", type=int)
@pass_context
def delete(mctx: MauticContext, id):
    """Delete a company."""
    try:
        data = mctx.client.delete(f"/companies/{id}/delete")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@companies.command("add-contact")
@click.argument("company_id", type=int)
@click.argument("contact_id", type=int)
@pass_context
def add_contact(mctx: MauticContext, company_id, contact_id):
    """Add a contact to a company."""
    try:
        data = mctx.client.post(f"/companies/{company_id}/contact/{contact_id}/add")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@companies.command("remove-contact")
@click.argument("company_id", type=int)
@click.argument("contact_id", type=int)
@pass_context
def remove_contact(mctx: MauticContext, company_id, contact_id):
    """Remove a contact from a company."""
    try:
        data = mctx.client.post(f"/companies/{company_id}/contact/{contact_id}/remove")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)

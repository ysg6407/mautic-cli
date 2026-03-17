from __future__ import annotations

import json as json_mod
from urllib.parse import urlparse

import click

from mautic_cli.context import pass_context, MauticContext
from mautic_cli.client import MauticApiError
from mautic_cli.json_input import parse_json_input


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
@click.option("--offset", default=0, type=int, help="Starting offset.")
@pass_context
def submissions(mctx: MauticContext, id, limit, offset):
    """List form submissions."""
    try:
        if mctx.page_all:
            for record in mctx.client.get_all(
                f"/forms/{id}/submissions",
                resource_key="submissions",
                limit=limit,
                params={"start": offset},
            ):
                click.echo(json_mod.dumps(record, ensure_ascii=False))
        else:
            data = mctx.client.get(
                f"/forms/{id}/submissions",
                params={"limit": limit, "start": offset},
            )
            mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command("submission")
@click.argument("form_id", type=int)
@click.argument("submission_id", type=int)
@pass_context
def get_submission(mctx: MauticContext, form_id, submission_id):
    """Get a specific form submission by ID."""
    try:
        data = mctx.client.get(f"/forms/{form_id}/submissions/{submission_id}")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command("contact-submissions")
@click.argument("form_id", type=int)
@click.argument("contact_id", type=int)
@pass_context
def contact_submissions(mctx: MauticContext, form_id, contact_id):
    """Get submissions for a specific contact on a form."""
    try:
        data = mctx.client.get(f"/forms/{form_id}/submissions/contact/{contact_id}")
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command()
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def create(mctx: MauticContext, json_str):
    """Create a new form."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.post("/forms/new", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command()
@click.argument("id", type=int)
@click.option("--json", "json_str", required=True, help="JSON data or @file.")
@pass_context
def edit(mctx: MauticContext, id, json_str):
    """Edit an existing form."""
    try:
        payload = parse_json_input(json_str)
        data = mctx.client.patch(f"/forms/{id}/edit", json=payload)
        mctx.output(data)
    except MauticApiError as e:
        mctx.error(e)
        raise SystemExit(1)


@forms.command()
@click.argument("id", type=int)
@click.option("--type", "embed_type", default=None, type=click.Choice(["js", "iframe", "html"]),
              help="Embed type: js (script tag), iframe, or html (raw cachedHtml). Omit to show all.")
@pass_context
def embed(mctx: MauticContext, id, embed_type):
    """Get form embed code."""
    base = mctx.client.base_url.rstrip("/")
    parsed = urlparse(base)
    host = parsed.hostname
    if parsed.port and parsed.port not in (80, 443):
        host = f"{host}:{parsed.port}"

    js_code = f'<script type="text/javascript" src="//{host}/form/generate.js?id={id}"></script>'
    iframe_code = (f'<iframe src="//{host}/form/{id}" width="300" height="300">'
                   f"<p>Your browser does not support iframes.</p></iframe>")

    if embed_type == "js":
        click.echo(js_code)
    elif embed_type == "iframe":
        click.echo(iframe_code)
    elif embed_type == "html":
        try:
            data = mctx.client.get(f"/forms/{id}")
            form = data.get("form", data)
            click.echo(form.get("cachedHtml", ""))
        except MauticApiError as e:
            mctx.error(e)
            raise SystemExit(1)
    else:
        click.echo("Via Javascript (recommended)")
        click.echo(js_code)
        click.echo()
        click.echo("Via iframe")
        click.echo(iframe_code)


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

from __future__ import annotations

import click

from mautic_cli.config import ConfigManager
from mautic_cli.output import get_console, get_err_console


@click.group()
def auth():
    """Manage Mautic authentication."""


@auth.command()
def setup():
    """Interactive auth configuration."""
    con = get_console()
    config = ConfigManager()

    con.print("\n[mautic]Mautic CLI Setup[/mautic]\n")

    base_url = click.prompt("Mautic base URL", type=str)
    auth_method = click.prompt(
        "Auth method",
        type=click.Choice(["basic", "oauth2"]),
        default="basic",
    )

    data = {"base_url": base_url.rstrip("/"), "auth_method": auth_method}

    if auth_method == "basic":
        data["username"] = click.prompt("Username")
        data["password"] = click.prompt("Password", hide_input=True)
    else:
        con.print("  [dim]Find these at: Settings > API Credentials > your app[/dim]")
        data["client_id"] = click.prompt("Public Key")
        data["client_secret"] = click.prompt("Secret Key", hide_input=True)
        data["token_endpoint"] = click.prompt(
            "Token endpoint",
            default=f"{base_url.rstrip('/')}/oauth/v2/token",
        )

    skip_ssl = click.confirm("Skip SSL verification? (for self-signed certs)", default=False)
    if skip_ssl:
        data["verify_ssl"] = False

    profile = click.prompt(
        "Profile name (use to store multiple instances, e.g. 'production', 'staging')",
        default="default",
    )

    existing = config.load(profile)
    if existing:
        old_url = existing.get("base_url", "?")
        old_method = existing.get("auth_method", "?")
        if not click.confirm(
            f"Profile '{profile}' already exists ({old_url}, {old_method}). Overwrite?"
        ):
            click.echo("Aborted.")
            return

    config.save(data, profile=profile)
    con.print(f"\n[success]Credentials saved to profile '{profile}'.[/success]")
    if profile != "default":
        con.print(f"[dim]Use --profile {profile} to connect to this instance.[/dim]")


@auth.command("list")
def list_profiles():
    """List configured profiles."""
    con = get_console()
    config = ConfigManager()
    profiles = config.list_profiles()
    if not profiles:
        con.print("[dim]No profiles configured. Run[/dim] [mautic]mautic auth setup[/mautic] [dim]to create one.[/dim]")
        return
    con.print()
    for name in profiles:
        data = config.load(name)
        base_url = data.get("base_url", "?")
        method = data.get("auth_method", "?")
        ssl = "" if data.get("verify_ssl", True) is not False else " [warning][no-ssl][/warning]"
        con.print(f"  [mautic]{name}[/mautic]  {base_url} [dim]({method})[/dim]{ssl}")
    con.print()


@auth.command()
@click.argument("profile")
def delete(profile):
    """Delete a stored profile."""
    config = ConfigManager()
    if config.delete(profile):
        get_console().print(f"[success]Profile '{profile}' deleted.[/success]")
    else:
        get_err_console().print(f"[error]Profile '{profile}' not found.[/error]")
        raise SystemExit(1)


@auth.command()
@click.option("--profile", default="default", help="Profile to test.")
@click.pass_context
def test(ctx, profile):
    """Test authentication against the Mautic instance."""
    from mautic_cli.auth import resolve_credentials
    from mautic_cli.client import MauticClient, MauticApiError

    con = get_console()
    err = get_err_console()
    mctx = ctx.find_root().obj

    config = ConfigManager()
    try:
        creds = resolve_credentials(config=config, profile=profile)
        verify_ssl = mctx.verify_ssl if mctx else True
        if verify_ssl and creds.get("verify_ssl") is False:
            verify_ssl = False
        client = MauticClient(creds, verify_ssl=verify_ssl)
        client.get("/contacts", params={"limit": 1})

        con.print(f"\n[success]Connected[/success] to {creds['base_url']}")
        try:
            ver = client.detect_version()
            con.print(f"[dim]Mautic version:[/dim] {'.'.join(str(x) for x in ver)}")
        except Exception:
            pass
        con.print()
        client.close()
    except MauticApiError as e:
        err.print(f"[error]Authentication failed:[/error] {e.message} [dim](HTTP {e.code})[/dim]")
        raise SystemExit(1)
    except ValueError as e:
        err.print(f"[error]Error:[/error] {e}")
        raise SystemExit(1)

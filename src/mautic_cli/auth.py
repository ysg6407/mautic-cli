from __future__ import annotations

import os

from mautic_cli.config import ConfigManager


def resolve_credentials(
    config: ConfigManager | None = None,
    profile: str = "default",
) -> dict:
    """Resolve Mautic credentials. Precedence: env vars > config file."""
    base_url = os.environ.get("MAUTIC_BASE_URL")

    if base_url:
        # Check for OAuth2 env vars
        client_id = os.environ.get("MAUTIC_CLIENT_ID")
        client_secret = os.environ.get("MAUTIC_CLIENT_SECRET")
        token_endpoint = os.environ.get("MAUTIC_TOKEN_ENDPOINT")

        if client_id and client_secret and token_endpoint:
            return {
                "base_url": base_url.rstrip("/"),
                "auth_method": "oauth2",
                "client_id": client_id,
                "client_secret": client_secret,
                "token_endpoint": token_endpoint,
            }

        # Check for Basic Auth env vars
        username = os.environ.get("MAUTIC_USERNAME")
        password = os.environ.get("MAUTIC_PASSWORD")

        if username and password:
            return {
                "base_url": base_url.rstrip("/"),
                "auth_method": "basic",
                "username": username,
                "password": password,
            }

    # Fall back to config file
    if config:
        data = config.load(profile=profile)
        if data.get("base_url"):
            data["base_url"] = data["base_url"].rstrip("/")
            return data

    raise ValueError(
        "No Mautic credentials found. Set MAUTIC_BASE_URL + auth env vars, "
        "or run 'mautic auth setup'."
    )

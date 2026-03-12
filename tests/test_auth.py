import pytest

from mautic_cli.auth import resolve_credentials
from mautic_cli.config import ConfigManager


def test_resolve_from_env_basic(monkeypatch, tmp_config_dir):
    monkeypatch.setenv("MAUTIC_BASE_URL", "https://m.example.com")
    monkeypatch.setenv("MAUTIC_USERNAME", "admin")
    monkeypatch.setenv("MAUTIC_PASSWORD", "secret")
    creds = resolve_credentials(config=ConfigManager(tmp_config_dir))
    assert creds["base_url"] == "https://m.example.com"
    assert creds["auth_method"] == "basic"
    assert creds["username"] == "admin"
    assert creds["password"] == "secret"


def test_resolve_from_env_oauth2(monkeypatch, tmp_config_dir):
    monkeypatch.setenv("MAUTIC_BASE_URL", "https://m.example.com")
    monkeypatch.setenv("MAUTIC_CLIENT_ID", "cid")
    monkeypatch.setenv("MAUTIC_CLIENT_SECRET", "csec")
    monkeypatch.setenv("MAUTIC_TOKEN_ENDPOINT", "https://m.example.com/oauth/v2/token")
    creds = resolve_credentials(config=ConfigManager(tmp_config_dir))
    assert creds["auth_method"] == "oauth2"
    assert creds["client_id"] == "cid"


def test_resolve_from_config_file(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    mgr.save({
        "base_url": "https://m.example.com",
        "auth_method": "basic",
        "username": "admin",
        "password": "secret",
    })
    creds = resolve_credentials(config=mgr)
    assert creds["base_url"] == "https://m.example.com"
    assert creds["auth_method"] == "basic"


def test_env_vars_override_config(monkeypatch, tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    mgr.save({"base_url": "https://old.example.com", "auth_method": "basic",
              "username": "old", "password": "old"})
    monkeypatch.setenv("MAUTIC_BASE_URL", "https://new.example.com")
    monkeypatch.setenv("MAUTIC_USERNAME", "new")
    monkeypatch.setenv("MAUTIC_PASSWORD", "new")
    creds = resolve_credentials(config=mgr)
    assert creds["base_url"] == "https://new.example.com"


def test_resolve_raises_when_no_credentials(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    with pytest.raises(ValueError, match="No Mautic credentials found"):
        resolve_credentials(config=mgr)


def test_resolve_with_named_profile(tmp_config_dir):
    mgr = ConfigManager(config_dir=tmp_config_dir)
    mgr.save({"base_url": "https://staging.example.com", "auth_method": "basic",
              "username": "u", "password": "p"}, profile="staging")
    creds = resolve_credentials(config=mgr, profile="staging")
    assert creds["base_url"] == "https://staging.example.com"

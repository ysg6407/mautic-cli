import json

import httpx
import respx
from click.testing import CliRunner

from mautic_cli.cli import cli

MOCK_ENV = {
    "MAUTIC_BASE_URL": "https://mautic.test",
    "MAUTIC_USERNAME": "admin",
    "MAUTIC_PASSWORD": "secret",
}


class TestCampaigns:
    @respx.mock
    def test_list_campaigns(self):
        respx.get("https://mautic.test/api/campaigns").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "campaigns": {"1": {"id": 1, "name": "Onboarding"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_campaign(self):
        respx.get("https://mautic.test/api/campaigns/1").mock(
            return_value=httpx.Response(200, json={
                "campaign": {"id": 1, "name": "Onboarding"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_create_campaign(self):
        respx.post("https://mautic.test/api/campaigns/new").mock(
            return_value=httpx.Response(200, json={
                "campaign": {"id": 5, "name": "New Campaign"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "create", "--json", '{"name":"New Campaign"}'])
        assert result.exit_code == 0

    @respx.mock
    def test_clone_campaign(self):
        respx.get("https://mautic.test/api/contacts").mock(
            return_value=httpx.Response(
                200,
                json={"total": "0", "contacts": {}},
                headers={"mautic-version": "7.0.0"},
            )
        )
        respx.post("https://mautic.test/api/campaigns/clone/1").mock(
            return_value=httpx.Response(200, json={
                "campaign": {"id": 6, "name": "Onboarding (copy)"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "clone", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_clone_fails_on_old_mautic(self):
        respx.get("https://mautic.test/api/contacts").mock(
            return_value=httpx.Response(
                200,
                json={"total": "0", "contacts": {}},
                headers={"mautic-version": "5.4.2"},
            )
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "clone", "1"])
        assert result.exit_code != 0

    @respx.mock
    def test_campaign_contacts(self):
        respx.get("https://mautic.test/api/campaigns/1/contacts").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "contacts": {"42": {"id": 42}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "contacts", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_add_contact(self):
        respx.post("https://mautic.test/api/campaigns/3/contact/42/add").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "add-contact", "3", "42"])
        assert result.exit_code == 0

    @respx.mock
    def test_remove_contact(self):
        respx.post("https://mautic.test/api/campaigns/3/contact/42/remove").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "remove-contact", "3", "42"])
        assert result.exit_code == 0

    @respx.mock
    def test_delete_campaign(self):
        respx.delete("https://mautic.test/api/campaigns/1/delete").mock(
            return_value=httpx.Response(200, json={"campaign": {"id": 1}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["campaigns", "delete", "1"])
        assert result.exit_code == 0

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


class TestWebhooks:
    @respx.mock
    def test_list_webhooks(self):
        respx.get("https://mautic.test/api/hooks").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "hooks": {"1": {"id": 1, "name": "My Webhook"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["webhooks", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_webhook(self):
        respx.get("https://mautic.test/api/hooks/1").mock(
            return_value=httpx.Response(200, json={
                "hook": {"id": 1, "name": "My Webhook"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["webhooks", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_create_webhook(self):
        respx.post("https://mautic.test/api/hooks/new").mock(
            return_value=httpx.Response(200, json={
                "hook": {"id": 5, "name": "New Webhook"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["webhooks", "create", "--json", '{"name":"New Webhook","webhookUrl":"https://example.com/hook"}'])
        assert result.exit_code == 0

    @respx.mock
    def test_delete_webhook(self):
        respx.delete("https://mautic.test/api/hooks/1/delete").mock(
            return_value=httpx.Response(200, json={"hook": {"id": 1}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["webhooks", "delete", "1"])
        assert result.exit_code == 0

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


class TestEmails:
    @respx.mock
    def test_list_emails(self):
        respx.get("https://mautic.test/api/emails").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "emails": {"1": {"id": 1, "name": "Welcome"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["emails", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_email(self):
        respx.get("https://mautic.test/api/emails/1").mock(
            return_value=httpx.Response(200, json={
                "email": {"id": 1, "name": "Welcome"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["emails", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_create_email(self):
        respx.post("https://mautic.test/api/emails/new").mock(
            return_value=httpx.Response(200, json={
                "email": {"id": 10, "name": "New Email"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["emails", "create", "--json", '{"name":"New Email","subject":"Hi"}'])
        assert result.exit_code == 0

    @respx.mock
    def test_send_to_contact(self):
        respx.post("https://mautic.test/api/emails/1/contact/42/send").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["emails", "send", "1", "--contact", "42"])
        assert result.exit_code == 0

    @respx.mock
    def test_send_to_segment(self):
        respx.post("https://mautic.test/api/emails/1/send").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["emails", "send-to-segment", "1"])
        assert result.exit_code == 0

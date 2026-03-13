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


class TestForms:
    @respx.mock
    def test_list_forms(self):
        respx.get("https://mautic.test/api/forms").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "forms": {"1": {"id": 1, "name": "Contact Form"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_form(self):
        respx.get("https://mautic.test/api/forms/1").mock(
            return_value=httpx.Response(200, json={
                "form": {"id": 1, "name": "Contact Form"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_form_submissions(self):
        respx.get("https://mautic.test/api/forms/1/submissions").mock(
            return_value=httpx.Response(200, json={
                "total": "2",
                "submissions": {"10": {"id": 10}, "11": {"id": 11}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "submissions", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_delete_form(self):
        respx.delete("https://mautic.test/api/forms/1/delete").mock(
            return_value=httpx.Response(200, json={"form": {"id": 1}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "delete", "1"])
        assert result.exit_code == 0

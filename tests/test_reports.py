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


class TestReports:
    @respx.mock
    def test_list_reports(self):
        respx.get("https://mautic.test/api/reports").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "reports": {"1": {"id": 1, "name": "Contact Report"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["reports", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_report(self):
        respx.get("https://mautic.test/api/reports/1").mock(
            return_value=httpx.Response(200, json={
                "report": {"id": 1, "name": "Contact Report"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["reports", "get", "1"])
        assert result.exit_code == 0

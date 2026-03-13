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


class TestStages:
    @respx.mock
    def test_list_stages(self):
        respx.get("https://mautic.test/api/stages").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "stages": {"1": {"id": 1, "name": "New Lead"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["stages", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_set_stage(self):
        respx.post("https://mautic.test/api/stages/3/contact/42/add").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["stages", "set", "42", "3"])
        assert result.exit_code == 0

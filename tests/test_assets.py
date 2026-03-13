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


class TestAssets:
    @respx.mock
    def test_list_assets(self):
        respx.get("https://mautic.test/api/assets").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "assets": {"1": {"id": 1, "title": "Whitepaper"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["assets", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_asset(self):
        respx.get("https://mautic.test/api/assets/1").mock(
            return_value=httpx.Response(200, json={
                "asset": {"id": 1, "title": "Whitepaper"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["assets", "get", "1"])
        assert result.exit_code == 0

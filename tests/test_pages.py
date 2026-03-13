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


class TestPages:
    @respx.mock
    def test_list_pages(self):
        respx.get("https://mautic.test/api/pages").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "pages": {"1": {"id": 1, "title": "Landing Page"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["pages", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_page(self):
        respx.get("https://mautic.test/api/pages/1").mock(
            return_value=httpx.Response(200, json={
                "page": {"id": 1, "title": "Landing Page"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["pages", "get", "1"])
        assert result.exit_code == 0

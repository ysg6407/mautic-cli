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


class TestTags:
    @respx.mock
    def test_list_tags(self):
        respx.get("https://mautic.test/api/tags").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "tags": {"1": {"id": 1, "tag": "VIP"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["tags", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_create_tag(self):
        respx.post("https://mautic.test/api/tags/new").mock(
            return_value=httpx.Response(200, json={
                "tag": {"id": 5, "tag": "Premium"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["tags", "create", "--json", '{"tag":"Premium"}'])
        assert result.exit_code == 0

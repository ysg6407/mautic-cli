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


class TestFields:
    @respx.mock
    def test_list_fields(self):
        respx.get("https://mautic.test/api/fields/contact").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "fields": {"1": {"id": 1, "label": "Country"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["fields", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_create_field(self):
        respx.post("https://mautic.test/api/fields/contact/new").mock(
            return_value=httpx.Response(200, json={
                "field": {"id": 10, "label": "Custom Field"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["fields", "create", "--json", '{"label":"Custom Field","type":"text"}'])
        assert result.exit_code == 0

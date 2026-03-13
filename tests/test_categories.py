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


class TestCategories:
    @respx.mock
    def test_list_categories(self):
        respx.get("https://mautic.test/api/categories").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "categories": {"1": {"id": 1, "title": "General", "bundle": "email"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["categories", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_list_categories_with_bundle(self):
        respx.get("https://mautic.test/api/categories").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "categories": {"1": {"id": 1, "title": "General", "bundle": "email"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["categories", "list", "--bundle", "email"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_create_category(self):
        respx.post("https://mautic.test/api/categories/new").mock(
            return_value=httpx.Response(200, json={
                "category": {"id": 3, "title": "New Category", "bundle": "email"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["categories", "create", "--json", '{"title":"New Category","bundle":"email"}'])
        assert result.exit_code == 0

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


class TestPoints:
    @respx.mock
    def test_list_points(self):
        respx.get("https://mautic.test/api/points").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "points": {"1": {"id": 1, "name": "Page Hit"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["points", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"


class TestPointTriggers:
    @respx.mock
    def test_list_triggers(self):
        respx.get("https://mautic.test/api/points/triggers").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "triggers": {"1": {"id": 1, "name": "Add to segment"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["points", "triggers", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

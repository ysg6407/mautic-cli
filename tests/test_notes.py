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


class TestNotes:
    @respx.mock
    def test_list_notes(self):
        respx.get("https://mautic.test/api/contacts/42/notes").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "notes": {"1": {"id": 1, "text": "Follow up needed"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["notes", "list", "--contact", "42"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_note(self):
        respx.get("https://mautic.test/api/notes/1").mock(
            return_value=httpx.Response(200, json={
                "note": {"id": 1, "text": "Follow up needed"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["notes", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_create_note(self):
        respx.post("https://mautic.test/api/notes/new").mock(
            return_value=httpx.Response(200, json={
                "note": {"id": 3, "text": "New note"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["notes", "create", "--json", '{"lead":42,"type":"general","text":"New note"}'])
        assert result.exit_code == 0

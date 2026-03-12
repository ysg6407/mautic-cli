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


class TestContactsList:
    @respx.mock
    def test_list_contacts(self):
        respx.get("https://mautic.test/api/contacts").mock(
            return_value=httpx.Response(200, json={
                "total": "2",
                "contacts": {
                    "1": {"id": 1, "fields": {"all": {"email": "a@b.com"}}},
                    "2": {"id": 2, "fields": {"all": {"email": "c@d.com"}}},
                },
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "2"

    @respx.mock
    def test_list_with_search(self):
        route = respx.get("https://mautic.test/api/contacts").mock(
            return_value=httpx.Response(200, json={"total": "0", "contacts": {}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "list", "--search", "email:*@test.com"])
        assert result.exit_code == 0
        request = route.calls[0].request
        assert "search=email" in str(request.url)

    @respx.mock
    def test_list_with_limit(self):
        route = respx.get("https://mautic.test/api/contacts").mock(
            return_value=httpx.Response(200, json={"total": "0", "contacts": {}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "list", "--limit", "50"])
        assert result.exit_code == 0
        request = route.calls[0].request
        assert "limit=50" in str(request.url)


class TestContactsPageAll:
    @respx.mock
    def test_page_all_outputs_ndjson(self):
        page1 = {"total": "3", "contacts": {
            "1": {"id": 1}, "2": {"id": 2},
        }}
        page2 = {"total": "3", "contacts": {
            "3": {"id": 3},
        }}
        route = respx.get("https://mautic.test/api/contacts")
        route.side_effect = [
            httpx.Response(200, json=page1),
            httpx.Response(200, json=page2),
        ]
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["--page-all", "contacts", "list", "--limit", "2"])
        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert len(lines) == 3
        assert json.loads(lines[0])["id"] == 1
        assert json.loads(lines[2])["id"] == 3


class TestContactsGet:
    @respx.mock
    def test_get_contact(self):
        respx.get("https://mautic.test/api/contacts/42").mock(
            return_value=httpx.Response(200, json={
                "contact": {"id": 42, "fields": {"all": {"email": "a@b.com"}}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "get", "42"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["contact"]["id"] == 42


class TestContactsCRUD:
    @respx.mock
    def test_create_contact(self):
        respx.post("https://mautic.test/api/contacts/new").mock(
            return_value=httpx.Response(200, json={
                "contact": {"id": 99, "fields": {"all": {"email": "new@b.com"}}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, [
            "contacts", "create", "--json", '{"email":"new@b.com"}',
        ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["contact"]["id"] == 99

    @respx.mock
    def test_edit_contact(self):
        respx.patch("https://mautic.test/api/contacts/42/edit").mock(
            return_value=httpx.Response(200, json={
                "contact": {"id": 42, "fields": {"all": {"lastname": "Silva"}}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, [
            "contacts", "edit", "42", "--json", '{"lastname":"Silva"}',
        ])
        assert result.exit_code == 0

    @respx.mock
    def test_delete_contact(self):
        respx.delete("https://mautic.test/api/contacts/42/delete").mock(
            return_value=httpx.Response(200, json={"contact": {"id": 42}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "delete", "42"])
        assert result.exit_code == 0


class TestContactsActions:
    @respx.mock
    def test_add_points(self):
        respx.post("https://mautic.test/api/contacts/42/points/plus/10").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "add-points", "42", "10"])
        assert result.exit_code == 0

    @respx.mock
    def test_subtract_points(self):
        respx.post("https://mautic.test/api/contacts/42/points/minus/5").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "subtract-points", "42", "5"])
        assert result.exit_code == 0

    @respx.mock
    def test_add_to_segment(self):
        respx.post("https://mautic.test/api/segments/5/contact/42/add").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "add-to-segment", "42", "5"])
        assert result.exit_code == 0

    @respx.mock
    def test_remove_from_segment(self):
        respx.post("https://mautic.test/api/segments/5/contact/42/remove").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "remove-from-segment", "42", "5"])
        assert result.exit_code == 0

    @respx.mock
    def test_add_to_campaign(self):
        respx.post("https://mautic.test/api/campaigns/3/contact/42/add").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "add-to-campaign", "42", "3"])
        assert result.exit_code == 0

    @respx.mock
    def test_activity(self):
        respx.get("https://mautic.test/api/contacts/42/activity").mock(
            return_value=httpx.Response(200, json={
                "events": [{"event": "email.read", "timestamp": "2026-03-01"}],
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["contacts", "activity", "42"])
        assert result.exit_code == 0

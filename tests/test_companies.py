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


class TestCompanies:
    @respx.mock
    def test_list_companies(self):
        respx.get("https://mautic.test/api/companies").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "companies": {"1": {"id": 1, "companyname": "Acme Inc"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_company(self):
        respx.get("https://mautic.test/api/companies/1").mock(
            return_value=httpx.Response(200, json={
                "company": {"id": 1, "companyname": "Acme Inc"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_create_company(self):
        respx.post("https://mautic.test/api/companies/new").mock(
            return_value=httpx.Response(200, json={
                "company": {"id": 5, "companyname": "New Corp"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "create", "--json", '{"companyname":"New Corp"}'])
        assert result.exit_code == 0

    @respx.mock
    def test_edit_company(self):
        respx.patch("https://mautic.test/api/companies/1/edit").mock(
            return_value=httpx.Response(200, json={
                "company": {"id": 1, "companyname": "Updated Corp"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "edit", "1", "--json", '{"companyname":"Updated Corp"}'])
        assert result.exit_code == 0

    @respx.mock
    def test_delete_company(self):
        respx.delete("https://mautic.test/api/companies/1/delete").mock(
            return_value=httpx.Response(200, json={"company": {"id": 1}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "delete", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_add_contact_to_company(self):
        respx.post("https://mautic.test/api/companies/5/contact/42/add").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "add-contact", "5", "42"])
        assert result.exit_code == 0

    @respx.mock
    def test_remove_contact_from_company(self):
        respx.post("https://mautic.test/api/companies/5/contact/42/remove").mock(
            return_value=httpx.Response(200, json={"success": True})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["companies", "remove-contact", "5", "42"])
        assert result.exit_code == 0

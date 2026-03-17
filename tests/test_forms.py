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


class TestForms:
    @respx.mock
    def test_list_forms(self):
        respx.get("https://mautic.test/api/forms").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "forms": {"1": {"id": 1, "name": "Contact Form"}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "list"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_get_form(self):
        respx.get("https://mautic.test/api/forms/1").mock(
            return_value=httpx.Response(200, json={
                "form": {"id": 1, "name": "Contact Form"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "get", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_form_submissions(self):
        respx.get("https://mautic.test/api/forms/1/submissions").mock(
            return_value=httpx.Response(200, json={
                "total": "2",
                "submissions": {"10": {"id": 10}, "11": {"id": 11}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "submissions", "1"])
        assert result.exit_code == 0

    @respx.mock
    def test_create_form(self):
        respx.post("https://mautic.test/api/forms/new").mock(
            return_value=httpx.Response(200, json={
                "form": {"id": 5, "name": "New Form"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, [
            "forms", "create",
            "--json", '{"name": "New Form", "formType": "standalone", "postAction": "message", "postActionProperty": "Thanks!"}'
        ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["form"]["name"] == "New Form"

    @respx.mock
    def test_edit_form(self):
        respx.patch("https://mautic.test/api/forms/5/edit").mock(
            return_value=httpx.Response(200, json={
                "form": {"id": 5, "name": "Updated Form"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, [
            "forms", "edit", "5",
            "--json", '{"name": "Updated Form"}'
        ])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["form"]["name"] == "Updated Form"

    def test_embed_default(self):
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "embed", "4"])
        assert result.exit_code == 0
        assert "Via Javascript (recommended)" in result.output
        assert "Via iframe" in result.output
        assert "generate.js?id=4" in result.output
        assert 'src="//mautic.test/form/4"' in result.output

    def test_embed_js(self):
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "embed", "4", "--type", "js"])
        assert result.exit_code == 0
        assert result.output.strip() == '<script type="text/javascript" src="//mautic.test/form/generate.js?id=4"></script>'

    def test_embed_iframe(self):
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "embed", "4", "--type", "iframe"])
        assert result.exit_code == 0
        assert 'src="//mautic.test/form/4"' in result.output

    @respx.mock
    def test_embed_html(self):
        respx.get("https://mautic.test/api/forms/4").mock(
            return_value=httpx.Response(200, json={
                "form": {"id": 4, "name": "Test", "cachedHtml": "<div>form html</div>"},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "embed", "4", "--type", "html"])
        assert result.exit_code == 0
        assert result.output.strip() == "<div>form html</div>"

    @respx.mock
    def test_form_submissions_with_offset(self):
        respx.get("https://mautic.test/api/forms/1/submissions").mock(
            return_value=httpx.Response(200, json={
                "total": "5",
                "submissions": {"12": {"id": 12}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "submissions", "1", "--offset", "3", "--limit", "2"])
        assert result.exit_code == 0

    @respx.mock
    def test_form_submissions_page_all(self):
        route = respx.get("https://mautic.test/api/forms/1/submissions")
        route.side_effect = [
            httpx.Response(200, json={
                "total": "3",
                "submissions": {"10": {"id": 10}, "11": {"id": 11}},
            }),
            httpx.Response(200, json={
                "total": "3",
                "submissions": {"12": {"id": 12}},
            }),
        ]
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["--page-all", "forms", "submissions", "1", "--limit", "2"])
        assert result.exit_code == 0
        lines = result.output.strip().split("\n")
        assert len(lines) == 3
        assert json.loads(lines[0])["id"] == 10
        assert json.loads(lines[2])["id"] == 12

    @respx.mock
    def test_get_submission(self):
        respx.get("https://mautic.test/api/forms/1/submissions/10").mock(
            return_value=httpx.Response(200, json={
                "submission": {"id": 10, "form": {"id": 1}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "submission", "1", "10"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["submission"]["id"] == 10

    @respx.mock
    def test_contact_submissions(self):
        respx.get("https://mautic.test/api/forms/1/submissions/contact/5").mock(
            return_value=httpx.Response(200, json={
                "total": "1",
                "submissions": {"10": {"id": 10, "lead": {"id": 5}}},
            })
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "contact-submissions", "1", "5"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert data["total"] == "1"

    @respx.mock
    def test_delete_form(self):
        respx.delete("https://mautic.test/api/forms/1/delete").mock(
            return_value=httpx.Response(200, json={"form": {"id": 1}})
        )
        runner = CliRunner(env=MOCK_ENV)
        result = runner.invoke(cli, ["forms", "delete", "1"])
        assert result.exit_code == 0

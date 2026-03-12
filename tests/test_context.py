from mautic_cli.context import MauticContext


class TestOutputList:
    def test_table_shows_total_count(self, capsys):
        mctx = MauticContext()
        mctx.fmt = "table"
        data = {
            "total": "274528",
            "contacts": {
                "1": {"id": 1, "fields": {"all": {"firstname": "Ana", "lastname": "S", "email": "a@b.com", "points": 0, "dateAdded": "2024-01-01"}}},
            },
        }
        mctx.output_list(data, "contacts")
        captured = capsys.readouterr()
        assert "Showing 1 of 274,528" in captured.out
        assert "Ana" in captured.out

    def test_table_no_total_when_all_shown(self, capsys):
        mctx = MauticContext()
        mctx.fmt = "table"
        data = {
            "total": "1",
            "contacts": {
                "1": {"id": 1, "fields": {"all": {"firstname": "Ana", "lastname": "S", "email": "a@b.com", "points": 0, "dateAdded": "2024-01-01"}}},
            },
        }
        mctx.output_list(data, "contacts")
        captured = capsys.readouterr()
        assert "Showing" not in captured.err

    def test_json_format_unchanged(self, capsys):
        mctx = MauticContext()
        mctx.fmt = "json"
        data = {"total": "5", "contacts": {"1": {"id": 1}}}
        mctx.output_list(data, "contacts")
        captured = capsys.readouterr()
        assert '"total"' in captured.out


class TestOutputSingle:
    def test_table_flattens_contact(self, capsys):
        mctx = MauticContext()
        mctx.fmt = "table"
        data = {
            "contact": {
                "id": 42,
                "fields": {"all": {"firstname": "Ana", "lastname": "Silva", "email": "ana@b.com", "points": 10, "dateAdded": "2024-01-01"}},
            },
        }
        mctx.output_single(data, "contact")
        captured = capsys.readouterr()
        assert "Ana" in captured.out
        assert "ana@b.com" in captured.out
        # Should have table headers
        assert "id" in captured.out
        assert "firstname" in captured.out

    def test_json_returns_full_response(self, capsys):
        mctx = MauticContext()
        mctx.fmt = "json"
        data = {"contact": {"id": 42, "fields": {"all": {"email": "a@b.com"}}}}
        mctx.output_single(data, "contact")
        captured = capsys.readouterr()
        assert '"contact"' in captured.out

    def test_table_flattens_segment(self, capsys):
        mctx = MauticContext()
        mctx.fmt = "table"
        data = {
            "list": {"id": 5, "name": "VIP", "alias": "vip", "isPublished": True, "isGlobal": False},
        }
        mctx.output_single(data, "list")
        captured = capsys.readouterr()
        assert "VIP" in captured.out
        assert "id" in captured.out

from click.testing import CliRunner

from mautic_cli.cli import cli


def test_version_flag():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "mautic-cli, version" in result.output


def test_help_shows_global_flags():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "--format" in result.output
    assert "--dry-run" in result.output
    assert "--verbose" in result.output
    assert "--profile" in result.output
    assert "--page-all" in result.output


def test_version_command_without_credentials():
    runner = CliRunner(env={"HOME": "/tmp/nonexistent"})
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "cli_version" in result.output

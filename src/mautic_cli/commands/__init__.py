"""Command groups for mautic-cli."""


def register_commands(cli):
    """Register all command groups with the CLI."""
    from mautic_cli.commands.contacts import contacts
    from mautic_cli.commands.segments import segments
    from mautic_cli.commands.emails import emails
    from mautic_cli.commands.campaigns import campaigns
    from mautic_cli.commands.auth_cmd import auth

    cli.add_command(contacts)
    cli.add_command(segments)
    cli.add_command(emails)
    cli.add_command(campaigns)
    cli.add_command(auth)

<div align="center">

# mautic-cli

**CLI for Mautic marketing automation - built for humans and AI agents.**

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg)](https://python.org)
[![Mautic 4.x-7.x](https://img.shields.io/badge/mautic-4.x--7.x-4e5e9e.svg)](https://mautic.org)

[Quick Start](#quick-start) &#183; [Commands](#commands) &#183; [Output Formats](#output-formats) &#183; [AI Agents](#ai-agents)

</div>

---

## What it does

| Category | Capabilities |
|----------|-------------|
| **Contacts** | List, search, create, edit, delete, points, segments, campaigns, activity |
| **Segments** | List, create, edit, delete, add/remove contacts |
| **Emails** | List, create, edit, send to contact, send to segment |
| **Campaigns** | List, create, edit, delete, clone (7+), add/remove contacts |
| **Auth** | Basic Auth, OAuth2 Client Credentials, multiple profiles |
| **Output** | JSON, colored tables, CSV, NDJSON streaming |

## Quick Start

```bash
# Install (pick one)
uv tool install mautic-cli    # recommended
pip install mautic-cli         # or with pip
pipx install mautic-cli        # or with pipx

# Authenticate
mautic auth setup

# Use it
mautic contacts list --limit 5
mautic --format table emails list
```

## Commands

### Contacts

```bash
mautic contacts list --search "email:*@company.com" --limit 50
mautic contacts get 42
mautic contacts create --json '{"firstname":"Ana","email":"ana@example.com"}'
mautic contacts edit 42 --json '{"lastname":"Silva"}'
mautic contacts delete 42
mautic contacts add-points 42 10
mautic contacts add-to-segment 42 5
mautic contacts activity 42
```

### Segments

```bash
mautic segments list
mautic segments get 1
mautic segments contacts 1
mautic segments create --json '{"name":"Newsletter Q1","isPublished":true}'
```

### Emails

```bash
mautic emails list
mautic emails get 1
mautic emails send 1 --contact 42
mautic emails send-to-segment 1
```

### Campaigns

```bash
mautic campaigns list
mautic campaigns get 1
mautic campaigns contacts 1
mautic campaigns clone 1    # Mautic 7+ only
```

<details>
<summary><strong>All write commands accept JSON from inline, file, or stdin</strong></summary>

```bash
mautic contacts create --json '{"email":"test@example.com"}'
mautic contacts create --json @contact.json
cat contact.json | mautic contacts create --json @-
```
</details>

## Output Formats

**Table** - colored, aligned columns with total count (powered by [rich](https://github.com/Textualize/rich)):

```
                     Showing 5 of 274,528
id      firstname  lastname  email               points  dateAdded
66515   Lidia      Duarte    lidia@example.com    0       2024-09-27
26698   Claudia    Preis     claudia@example.com  0       2024-08-25
```

```bash
mautic --format table contacts list --limit 5
```

**JSON** (default) - full API response, pretty-printed in terminal:

```bash
mautic contacts list --limit 5
```

**CSV** - same key fields, pipe to file:

```bash
mautic --format csv contacts list > contacts.csv
```

**NDJSON** - one JSON object per line, auto-paginating through all results:

```bash
mautic --page-all contacts list | jq '.fields.all.email'
```

## Global Flags

Global flags go **before** the resource group:

```bash
mautic --format table --published-only emails list
```

| Flag | Description |
|----------|-------------|
| `--format json\|table\|csv` | Output format (default: json) |
| `--pretty` | Pretty-print JSON |
| `--page-all` | Auto-paginate, output NDJSON per record |
| `--dry-run` | Show HTTP request without executing |
| `--verbose` | Show HTTP request/response details |
| `--published-only` | Filter to published items only |
| `--no-verify-ssl` | Skip SSL certificate verification |
| `--profile <name>` | Use a named config profile |

## Authentication

### Interactive Setup

```bash
mautic auth setup    # Prompts for URL, method (basic/oauth2), credentials
mautic auth test     # Verify connection and detect Mautic version
```

Supports **Basic Auth** and **OAuth2 Client Credentials** grant.

### Environment Variables

```bash
export MAUTIC_BASE_URL=https://mautic.example.com
export MAUTIC_USERNAME=admin
export MAUTIC_PASSWORD=secret
```

### Profiles

Manage multiple Mautic instances with named profiles:

```bash
mautic auth setup           # Profile name: production
mautic auth setup           # Profile name: staging
mautic auth list            # Show all profiles
mautic auth delete staging  # Remove a profile

mautic --profile staging contacts list
```

<details>
<summary><strong>SSL / self-signed certificates (DDEV, local dev)</strong></summary>

```bash
# Per-command
mautic --no-verify-ssl contacts list

# Or save the preference during auth setup
mautic auth setup
# Skip SSL verification? (for self-signed certs) [y/N]: y
```
</details>

## Search Syntax

The `--search` flag passes through to [Mautic's native search](https://docs.mautic.org/en/5.x/contacts/search.html):

```bash
mautic contacts list --search "email:*@company.com"
mautic emails list --search "name:Newsletter"
mautic --published-only segments list    # uses is:published internally
```

## Shell Completion

Tab-completion for all commands, subcommands, and options:

```bash
mautic completion    # Shows install instructions for your shell
```

## AI Agents

mautic-cli ships with an [agent skill](skills/mautic/SKILL.md) that teaches AI coding agents the full command reference, auth flow, and safety rules for write operations.

Install with [`npx skills`](https://github.com/vercel-labs/skills) (supports Claude Code, Cursor, Codex, Gemini, Windsurf, and [37+ agents](https://add-skill.org/)):

```bash
npx skills add https://github.com/bloomidea/mautic-cli
```

Then ask your agent: *"list my mautic contacts"* or *"send email 5 to contact 42"*.

## License

[MIT](LICENSE)

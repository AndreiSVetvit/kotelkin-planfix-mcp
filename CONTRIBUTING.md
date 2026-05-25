# Contributing

Thanks for considering a contribution.

This repository is scoped to the reusable Planfix MCP product:

- MCP server code;
- Planfix REST client;
- schemas;
- tools;
- tests;
- public-safe documentation.

Do not add private/local operating layers such as tracker, bridge, project panel, local control-plane state, private runbooks, SQL state, or account-specific files.

## Development Setup

```bash
python -m pip install -e ".[dev]"
```

## Required Checks

Run these before opening a pull request:

```bash
python -m pytest -q
python -m compileall planfix_mcp scripts tests
python scripts/smoke_tools.py
python scripts/check_swagger_alignment.py
python -m pip check
python -m pip wheel . --no-deps -w dist_tmp
```

Remove `dist_tmp` after the wheel check if needed.

## Live Checks

Live checks require a Planfix test account:

```bash
planfix-mcp-preflight
planfix-mcp-live-qa-basic
planfix-mcp-live-qa-extended
```

Do not run live checks against a production Planfix account unless you understand which tools write data.

## Tool Contract Rules

Public MCP tool names are part of the user-facing contract.

Do not rename or remove public tools without a contract change proposal that explains:

- old name;
- new name;
- migration path;
- compatibility impact;
- documentation updates.

## Secrets

Never commit real Planfix tokens, private account data, local MCP configs with credentials, or screenshots containing tokens.

Run a secret scan before submitting changes:

```bash
rg --hidden --glob '!.git/**' --glob '!*.pyc' "PLANFIX_TOKEN|Authorization: Bearer|[0-9a-fA-F]{32}" .
```

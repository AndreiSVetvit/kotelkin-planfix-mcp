# Kotelkin Planfix MCP

[English](README_EN.md) | [Русский](README.md)

MCP server for Planfix REST API.

This project exposes Planfix task, comment, datatag, checklist, project, directory, process, object, and custom-field operations as Model Context Protocol tools over STDIO transport.

This documentation describes package version `v0.1.3`, built on the published [`v0.1.2` baseline](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases/tag/v0.1.2); [Releases](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases) shows the current published tag. This is a local MCP server over STDIO, not a hosted service. It currently registers 58 tools.

## Documentation

- [User Guide](docs/USER_GUIDE.md)
- [Russian User Guide](docs/USER_GUIDE_RU.md)
- [Russian README](README.md)
- [Public Release Checklist](docs/PUBLIC_RELEASE_CHECKLIST.md)
- [Russian Public Release Checklist](docs/PUBLIC_RELEASE_CHECKLIST_RU.md)
- [Security Policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## What It Does

- Runs as an MCP STDIO server.
- Authenticates to Planfix REST API with a bearer token.
- Registers Planfix tools for tasks, comments, datatags, checklists, projects, directories, processes, objects, and custom fields.
- Provides local smoke checks that do not call Planfix.
- Provides an optional preflight check for validating real Planfix credentials before live use.

## Who It Is For

- Planfix users who want to connect a Planfix account to an MCP client.
- Developers who need a compact, inspectable Planfix MCP server.
- Teams testing AI-assisted workflows around Planfix tasks, comments, projects, directories, and custom fields.

## Requirements

- Python 3.12+
- A Planfix account with REST API access
- `PLANFIX_BASE_URL`, for example `https://your-company.planfix.com/rest`
- `PLANFIX_TOKEN`

Planfix REST API references:

- https://planfix.com/ru/help/REST_API
- https://help.planfix.com/restapidocs/
- https://help.planfix.com/restapidocs/swagger.json

## Install

```bash
git clone https://github.com/AndreiSVetvit/kotelkin-planfix-mcp.git
cd kotelkin-planfix-mcp
python -m venv .venv
```

Install the package and run the local smoke check without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\planfix-mcp-smoke.exe
```

On macOS/Linux use `.venv/bin/python -m pip install -e .` and `.venv/bin/planfix-mcp-smoke`.

The smoke check verifies all 58 registered tools locally and does not call Planfix.

For development checks:

```bash
python -m pip install -e ".[dev]"
```

In PowerShell without activation, use ` .\.venv\Scripts\python.exe -m pip install -e ".[dev]" `.

## Configuration

Set required environment variables:

```bash
PLANFIX_BASE_URL=https://your-company.planfix.com/rest
PLANFIX_TOKEN=your_token_here
```

Optional settings:

```bash
PLANFIX_TIMEOUT_SEC=20
PLANFIX_RETRY_MAX=2
PLANFIX_MIN_REQUEST_INTERVAL_SEC=1.0
PLANFIX_STATUS_CHANGE_DELAY_SEC=1.0
PLANFIX_SILENT_DEFAULT=false
LOG_LEVEL=INFO
```

`PLANFIX_MIN_REQUEST_INTERVAL_SEC=1.0` is the conservative default for request pacing.
`PLANFIX_STATUS_CHANGE_DELAY_SEC=1.0` adds an explicit pause before task status changes.

## Secrets Setup

For local use, you can store credentials in the OS keyring instead of exporting them every run:

```bash
planfix-mcp-secrets-init
```

In PowerShell without activation, use ` .\.venv\Scripts\planfix-mcp-secrets-init.exe `; on macOS/Linux use `.venv/bin/planfix-mcp-secrets-init`.

After that, `planfix-mcp-server` can load `PLANFIX_BASE_URL` and `PLANFIX_TOKEN` from the keyring when environment variables are not set.

## Run

```bash
planfix-mcp-server
```

Alternative:

```bash
python -m planfix_mcp.server
```

## MCP Client Configuration

For Codex CLI, register the absolute executable path from `.venv` so the server does not depend on an activated shell:

```bash
# PowerShell
codex mcp add kotelkin-planfix-mcp -- (Resolve-Path .venv\Scripts\planfix-mcp-server.exe).Path
# macOS/Linux
codex mcp add kotelkin-planfix-mcp -- "$(pwd)/.venv/bin/planfix-mcp-server"
codex mcp list
```

Verify the server appears in Codex with `/mcp`. For a safe first request, ask it to read a task you already know by ID and report its name, status, and due date—do not create or change records.

Use the installed CLI command as a STDIO MCP server in other MCP clients too.

Example shape:

```json
{
  "mcpServers": {
    "kotelkin-planfix-mcp": {
      "command": "planfix-mcp-server",
      "env": {
        "PLANFIX_BASE_URL": "https://your-company.planfix.com/rest",
        "PLANFIX_TOKEN": "your_token_here"
      }
    }
  }
}
```

Keep tokens out of committed config files.

## Safe Local Checks

Unit tests:

```bash
python -m pytest -q
```

Tool registration smoke check:

```bash
planfix-mcp-smoke
```

In PowerShell without activation, use ` .\.venv\Scripts\planfix-mcp-smoke.exe `; on macOS/Linux use `.venv/bin/planfix-mcp-smoke`.

This check uses fake local environment values and does not call Planfix.

Swagger alignment check:

```bash
planfix-mcp-swagger-check
```

This fetches the official Planfix OpenAPI document and verifies that expected paths/methods still exist.

Package build check:

```bash
python -m pip wheel . --no-deps -w dist
```

## Live Preflight

Use this only when real credentials are configured:

```bash
planfix-mcp-preflight
```

The preflight calls:

- `GET /ping`
- `GET /workspace/list`
- optionally `POST /task/list` when `PLANFIX_PREFLIGHT_TASK_LIST=1`

The optional task-list request is disabled by default. To avoid putting a token in a command or config file, run `planfix-mcp-secrets-init` once to store the URL and token in the OS keyring. In PowerShell without activation, use ` .\.venv\Scripts\planfix-mcp-preflight.exe `; on macOS/Linux use `.venv/bin/planfix-mcp-preflight`.

## Live QA

Use this only with a disposable Planfix account or a low-risk test workspace. The script creates and updates a test task through the MCP STDIO server.

```bash
planfix-mcp-live-qa-basic
```

To also test comment add/update/get, provide an existing task where comments are allowed:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 planfix-mcp-live-qa-basic
```

For broader release checks, use the extended runner:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 \
PLANFIX_LIVE_QA_DATATAG_ID=10 \
PLANFIX_LIVE_QA_ASSIGNEE_ID=1 \
PLANFIX_LIVE_QA_DIRECTORY_ID=10 \
planfix-mcp-live-qa-extended
```

The extended runner exercises task updates, statuses, assignees, dates, comments, DataTags, checklists, projects, directories, processes, objects, and custom fields through the MCP STDIO server.

By default it does not create custom-field groups or custom fields, because those are permanent account configuration changes. To include those checks on a disposable account:

```bash
PLANFIX_LIVE_QA_CONFIG_WRITES=1 planfix-mcp-live-qa-extended
```

## Tool Safety

Some tools write to Planfix. Use a test workspace or a low-risk Planfix account when evaluating the server.

Write tools include task create/update, comment add/update/delete, datatag add, checklist create/update, project create/update, directory entry add/update/delete, custom-field group create, custom-field create, status changes, assignee changes, and date changes.

## Implemented Tools

The server currently registers 58 MCP tools:

- Task core, status, assignment, dates, files, templates, recurring tasks, and filters.
- Task comments, global comments, DataTags, and checklist items.
- Projects, project groups, project templates, and project files.
- Directories, directory groups, directory entries, and directory filters.
- Contact/task processes, objects, and status lists.
- Task and project custom-field groups, lists, creation, and get-by-id helpers.

See `MANUAL_QA_EXTENDED_TOOLS.md` for the full tool list and example payload shapes.

## Input Contract

- Tools with request bodies accept `payload: dict`.
- `payload` is passed to the matching Planfix endpoint.
- `task_id`, `comment_id`, and `item_id` values must be positive integers.
- Write tools accept optional `silent: true|false` where supported by the endpoint behavior.

Example:

```json
{
  "tool": "planfix_task_get",
  "arguments": {
    "task_id": 12345
  }
}
```

Example write:

```json
{
  "tool": "planfix_task_update",
  "arguments": {
    "task_id": 12345,
    "payload": {
      "name": "Updated task title"
    }
  }
}
```

## Project Status

Package/documentation version: `v0.1.3`, building on the published `v0.1.2` baseline. See [releases and release notes](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases) and the [Q4 roadmap](ROADMAP.md).

## License

MIT

# Kotelkin Planfix MCP

MCP server for Planfix REST API.

This project exposes Planfix task, comment, datatag, checklist, project, directory, process, object, and custom-field operations as Model Context Protocol tools over STDIO transport.

The current private release candidate includes 58 tools and is intended to be small, inspectable, and useful before the repository is opened publicly.

## What It Does

- Runs as an MCP STDIO server.
- Authenticates to Planfix REST API with a bearer token.
- Registers Planfix tools for tasks, comments, datatags, checklists, projects, directories, processes, objects, and custom fields.
- Provides local smoke checks that do not call Planfix.
- Provides an optional preflight check for validating real Planfix credentials before live use.

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
python -m pip install -e .
```

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

Use the installed CLI command as a STDIO MCP server.

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

Tool registration smoke check:

```bash
planfix-mcp-smoke
```

This check uses fake local environment values and does not call Planfix.

Swagger alignment check:

```bash
planfix-mcp-swagger-check
```

This fetches the official Planfix OpenAPI document and verifies that expected paths/methods still exist.

## Live Preflight

Use this only when real credentials are configured:

```bash
planfix-mcp-preflight
```

The preflight calls:

- `GET /ping`
- `GET /workspace/list`
- optionally `POST /task/list` when `PLANFIX_PREFLIGHT_TASK_LIST=1`

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

Current status: private release candidate.

Next planned improvements:

- live manual QA against a low-risk Planfix account;
- compatibility fixes found during real account testing;
- CI and release hardening before public opening.

## License

MIT

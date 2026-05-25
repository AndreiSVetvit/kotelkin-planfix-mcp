# Kotelkin Planfix MCP

MCP server for Planfix REST API.

This project exposes Planfix task, comment, datatag, metadata, and checklist operations as Model Context Protocol tools over STDIO transport.

The initial public baseline includes 22 tools and is intended to be small, inspectable, and useful before broader REST coverage is added.

## What It Does

- Runs as an MCP STDIO server.
- Authenticates to Planfix REST API with a bearer token.
- Registers Planfix tools for tasks, comments, datatags, files, templates, filters, and checklists.
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

Write tools include task create/update, comment add/update, datatag add, checklist update, status changes, assignee changes, and date changes.

## Implemented Tools

### Task CRUD

1. `planfix_task_create` -> `POST /task/`
2. `planfix_task_get` -> `GET /task/{id}`
3. `planfix_task_update` -> `POST /task/{id}`
4. `planfix_task_list` -> `POST /task/list`
5. `planfix_task_update_custom_fields` -> `POST /task/{id}`

### Task Status And Assignment

6. `planfix_task_accept` -> `POST /task/{id}` with payload semantics
7. `planfix_task_reject` -> `POST /task/{id}` with payload semantics
8. `planfix_task_change_status` -> `POST /task/{id}`
9. `planfix_task_get_statuses` -> process/object statuses resolved from task
10. `planfix_task_change_assignees` -> `POST /task/{id}`
11. `planfix_task_change_dates` -> `POST /task/{id}`

### Comments

12. `planfix_task_comments_list` -> `POST /task/{id}/comments/list`
13. `planfix_task_comment_add` -> `POST /task/{id}/comments/`
14. `planfix_task_comment_update` -> `POST /task/{id}/comments/{comment_id}`

### DataTags

15. `planfix_task_datatag_add` -> `POST /task/{id}/datatags/`
16. `planfix_task_datatag_to_comment` -> `POST /task/{id}/datatags/{commentId}`

### Metadata And Checklists

17. `planfix_task_files` -> `GET /task/{id}/files`
18. `planfix_task_templates` -> `GET /task/templates`
19. `planfix_task_recurring` -> `GET /task/recurring`
20. `planfix_task_filters` -> `POST /task/filters`
21. `planfix_task_checklist_get` -> `POST /task/{id}/checklist/list`
22. `planfix_task_checklist_update` -> `POST /task/{id}/checklist/{itemId}`

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

- secure keyring setup;
- compatibility fixes from later internal history;
- expanded Planfix REST coverage;
- CI and release hardening.

## License

MIT

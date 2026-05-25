# Planfix MCP Single-User MVP

Minimal MCP server for Planfix with 22 tools, async HTTP client, and STDIO transport.

## Requirements

- Python 3.12+
- Planfix API URL and token

## Install

```bash
pip install -e .
```

## Environment variables

Required:

- `PLANFIX_BASE_URL` (example: `https://your-company.planfix.com/rest`)
- `PLANFIX_TOKEN`

Optional:

- `PLANFIX_TIMEOUT_SEC` (default: `20`)
- `PLANFIX_RETRY_MAX` (default: `2`)
- `PLANFIX_MIN_REQUEST_INTERVAL_SEC` (default: `1.0`, aligns with Planfix recommended request rate)
- `PLANFIX_SILENT_DEFAULT` (default: `false`, adds `?silent=true` to write tools when enabled)
- `LOG_LEVEL` (default: `INFO`)

Auth and API docs:

- `https://planfix.com/ru/help/REST_API`
- `https://help.planfix.com/restapidocs/`
- `https://planfix.com/ru/help/Тестирование_запросов_по_REST_API_в_Postman`

## Run (STDIO)

```bash
planfix-mcp-server
```

Alternative:

```bash
python -m src.server
```

## Before live test

Config and API preflight:

```bash
planfix-mcp-preflight
```

Tool registration smoke check (local, no Planfix calls):

```bash
planfix-mcp-smoke
```

Swagger alignment check against official docs:

```bash
planfix-mcp-swagger-check
```

References:

- `DOCS_ALIGNMENT.md`
- `MANUAL_QA_22_TOOLS.md`
- `ROADMAP.md`
- `CHANGELOG.md`

## Release baseline

- Current baseline tag target: `v0.1.0-mvp`
- Recommended next milestone: `v0.2.0-live-qa`

## Implemented tools (22)

### Group A (CRUD)

1. `planfix_task_create` -> `POST /task/`
2. `planfix_task_get` -> `GET /task/{id}`
3. `planfix_task_update` -> `POST /task/{id}`
4. `planfix_task_list` -> `POST /task/list`
5. `planfix_task_update_custom_fields` -> `POST /task/{id}`

### Group B (Status)

6. `planfix_task_accept` -> `POST /task/{id}` (payload-based accept)
7. `planfix_task_reject` -> `POST /task/{id}` (payload-based reject)
8. `planfix_task_change_status` -> `POST /task/{id}` (`status` field in payload)
9. `planfix_task_get_statuses` -> `GET /process/task/{processId}/statuses` or `GET /object/{objectId}/statuses` (resolved from task)
10. `planfix_task_change_assignees` -> `POST /task/{id}` (`assignees/auditors` in payload)
11. `planfix_task_change_dates` -> `POST /task/{id}`

### Group C (Comments)

12. `planfix_task_comments_list` -> `POST /task/{id}/comments/list`
13. `planfix_task_comment_add` -> `POST /task/{id}/comments/`
14. `planfix_task_comment_update` -> `POST /task/{id}/comments/{comment_id}`

### Group D (DataTags)

15. `planfix_task_datatag_add` -> `POST /task/{id}/datatags/`
16. `planfix_task_datatag_to_comment` -> `POST /task/{id}/datatags/{commentId}`

### Group E (Meta)

17. `planfix_task_files` -> `GET /task/{id}/files`
18. `planfix_task_templates` -> `GET /task/templates`
19. `planfix_task_recurring` -> `GET /task/recurring`
20. `planfix_task_filters` -> `POST /task/filters`

### Group F (Checklists)

21. `planfix_task_checklist_get` -> `POST /task/{id}/checklist/list`
22. `planfix_task_checklist_update` -> `POST /task/{id}/checklist/{itemId}`

## Input contract

- Tools with body expect `payload: dict`.
- `payload` is passed to Planfix endpoint as-is.
- `task_id` must be a positive integer.
- For write tools you can pass `silent: true|false` to override `PLANFIX_SILENT_DEFAULT`.

Examples:

```json
{
  "tool": "planfix_task_get",
  "arguments": {
    "task_id": 12345
  }
}
```

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

## Manual QA checklist

1. Group A full flow: create -> get -> update -> list -> custom fields update.
2. Group B flow: accept/reject, change status, get statuses, change assignees/dates.
3. Group C flow: add comment -> list comments -> update comment.
4. Group D flow: add datatag -> attach datatag to comment.
5. Group E/F flow: files/templates/recurring/filters + checklist list/update.
6. Negative checks:
   - invalid `task_id`
   - empty payload where required
   - 401/403 from Planfix
7. Retry checks:
   - set very low timeout and verify timeout retry behavior
   - verify `429` retries

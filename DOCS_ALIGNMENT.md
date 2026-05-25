# Planfix REST Docs Alignment

This file records alignment of the MCP implementation with official Planfix REST API docs.

## Sources used

- https://planfix.com/ru/help/REST_API
- https://help.planfix.com/restapidocs/
- https://help.planfix.com/restapidocs/swagger.json
- https://planfix.com/ru/help/Тестирование_запросов_по_REST_API_в_Postman
- https://github.com/modelcontextprotocol/python-sdk
- https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/testing.md

## Verified spec snapshot

- OpenAPI version: `1.5.7`
- Key findings:
  - `/task/{id}/checklist/list` exists, `/task/{id}/checklists` does not.
  - `/task/{id}/datatags/{commentId}` expects a comment id path parameter.
  - No dedicated `/task/{id}/accept` or `/task/{id}/reject` path in REST spec.
  - No dedicated `/task/{id}/status` path in REST spec.
  - Task update (`POST /task/{id}`) includes fields like `status`, `assignees`, `auditors`, dates.
  - Status lists are available via `/process/task/{id}/statuses` and `/object/{id}/statuses`.

## Implementation decisions

1. Keep existing MCP tool names stable.
2. Map `accept/reject/change_status/change_assignees/change_dates` to `POST /task/{id}` with payload.
3. Implement `planfix_task_get_statuses` by resolving process/object ids from task and calling statuses endpoints.
4. Map checklist tools to `/task/{id}/checklist/list` and `/task/{id}/checklist/{itemId}`.
5. Map DataTag-to-comment to `/task/{id}/datatags/{commentId}`.
6. Add basic request pacing (`PLANFIX_MIN_REQUEST_INTERVAL_SEC=1.0`) per REST docs guidance.
7. Add optional `silent` query support for write operations via tool argument and `PLANFIX_SILENT_DEFAULT`.
8. Extend coverage to project, directory, process/object, custom-field, global comment, and checklist item operations where matching swagger paths exist.
9. Keep the server on FastMCP with STDIO transport for desktop MCP clients.
10. Test live behavior through `ClientSession` + `stdio_client`, matching the official MCP Python SDK testing style.

## Remaining caveat

`accept/reject` are preserved as separate MCP tools for compatibility with the original functional plan, but in REST they are executed through task update payload semantics.
`silent` is treated as optional runtime behavior and may not be explicitly documented per endpoint in swagger.

## Automation

- `python scripts/check_swagger_alignment.py` validates expected methods/paths against live `swagger.json`.
- `python scripts/smoke_tools.py` validates that all 58 tools are registered by the server.
- `python -m scripts.live_qa_basic` validates a small real-account task/comment path through MCP STDIO.
- `python -m scripts.live_qa_extended` validates the broad real-account MCP path; permanent custom-field writes require `PLANFIX_LIVE_QA_CONFIG_WRITES=1`.

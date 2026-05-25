# Manual QA: 22 Planfix MCP Tools

Legacy baseline checklist for the original 22 task-oriented tools.
For the current 58-tool public candidate, use `MANUAL_QA_EXTENDED_TOOLS.md`.

Use this file as a quick checklist for manual testing in MCP Inspector or your MCP client.

## Common placeholders

- `TASK_ID`: existing task id
- `COMMENT_ID`: existing comment id in task
- `CHECKLIST_ITEM_ID`: existing checklist item id
- `PROCESS_ID`: existing process id
- `silent`: optional boolean for write-tools (`true` suppress mode, if supported by account/API)

## Group A (CRUD)

1. `planfix_task_create`
```json
{"payload":{"name":"MCP QA Task","description":"created by manual QA"}}
```

2. `planfix_task_get`
```json
{"task_id":12345}
```

3. `planfix_task_update`
```json
{"task_id":12345,"payload":{"name":"MCP QA Task Updated"}}
```

4. `planfix_task_list`
```json
{"payload":{}}
```

5. `planfix_task_update_custom_fields`
```json
{"task_id":12345,"payload":{"customFieldData":[{"field":{"id":111},"value":"test"}]}}
```

## Group B (Status)

6. `planfix_task_accept`
```json
{"task_id":12345,"payload":{"status":{"id":1}}}
```

7. `planfix_task_reject`
```json
{"task_id":12345,"payload":{"status":{"id":2}}}
```

8. `planfix_task_change_status`
```json
{"task_id":12345,"payload":{"status":{"id":3}}}
```

9. `planfix_task_get_statuses`
```json
{"task_id":12345,"payload":{}}
```

10. `planfix_task_change_assignees`
```json
{"task_id":12345,"payload":{"assignees":{"users":[{"id":1001}]}}}
```

11. `planfix_task_change_dates`
```json
{"task_id":12345,"payload":{"startDateTime":"2026-02-17 10:00:00","endDateTime":"2026-02-18 18:00:00"}}
```

## Group C (Comments)

12. `planfix_task_comments_list`
```json
{"task_id":12345,"payload":{}}
```

13. `planfix_task_comment_add`
```json
{"task_id":12345,"payload":{"description":"Comment from MCP manual QA"}}
```

14. `planfix_task_comment_update`
```json
{"task_id":12345,"comment_id":67890,"payload":{"description":"Updated comment text"}}
```

## Group D (DataTags)

15. `planfix_task_datatag_add`
```json
{"task_id":12345,"payload":{"dataTag":{"id":10},"value":"QA"}}
```

16. `planfix_task_datatag_to_comment`
```json
{"task_id":12345,"comment_id":67890,"payload":{"dataTag":{"id":10},"value":"QA-comment"}}
```

## Group E (Meta)

17. `planfix_task_files`
```json
{"task_id":12345,"payload":{}}
```

18. `planfix_task_templates`
```json
{"payload":{}}
```

19. `planfix_task_recurring`
```json
{"payload":{}}
```

20. `planfix_task_filters`
```json
{"payload":{}}
```

## Group F (Checklists)

21. `planfix_task_checklist_get`
```json
{"task_id":12345,"payload":{}}
```

22. `planfix_task_checklist_update`
```json
{"task_id":12345,"item_id":777,"payload":{"isCompleted":true}}
```

## Negative checks

1. Invalid `task_id` for any task tool.
2. Empty payload for required payload tools.
3. Invalid token (`401`) and low-privilege token (`403`).
4. Rate limit scenario (`429`) by lowering request interval and sending bursts.

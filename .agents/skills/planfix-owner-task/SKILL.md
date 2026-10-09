---
name: planfix-owner-task
description: Turn one plain-language owner instruction into one Planfix task and verify its saved fields. Use for this single-task workflow, not bulk edits or general Planfix administration.
---

# Planfix owner task

Use this skill for one owner-requested task. Keep the owner-facing flow short: resolve only necessary ambiguity, create one task, read it back, and report what actually saved.

## Choose one backend

- Prefer the connected official Planfix MCP when it is available. Stay in its current account.
- If it is unavailable, ask before using the existing `kotelkin-planfix-mcp` MCP. The custom backend is an explicit alternative, not an automatic fallback.
- Never mix accounts or backends during one write. After an ambiguous write result, do not retry or switch backends; use read-only checks to establish whether the task exists.

For the custom MCP, proceed only when the exact assignee's existing Planfix user ID and the account timezone are already known. Do not add a lookup tool or guess either value; ask when one is missing. With the official MCP, use its existing employee/timezone lookup when available and ask if identity or date interpretation remains ambiguous.

## Shape one instruction into one task

- Use the requested client and a concise task title.
- Turn the requested work into a short description with the agreed steps. For the demo, use three steps: уточнить требования клиента; рассчитать стоимость предложения; отправить черновик владельцу на проверку.
- Treat task creation as recording the assignment only. Do not perform the work, send the proposal, or contact the named customer.
- Resolve a named assignee to one exact employee; ask if there are multiple plausible matches.
- Interpret a relative date in the selected account's timezone. Do not invent a time when the owner gave only a date. Ask only if the date cannot be determined reliably.
- Do not explicitly send a message or add a comment, checklist, or participant unless requested. Steps in the description are not a checklist.
- Task creation can trigger account-default workflows or notifications. Use an owner-approved safe/test account, disclose known side effects before writing, and use an existing silent option only when the selected tool supports it and it is appropriate. Do not imply that notifications are suppressed otherwise.

## Write and verify

- Keep the write within the current request. Do not treat general prior approval as permission for extra work. If the target account or side effects are not safe/approved for a test task, ask before writing.
- With the official MCP, present each required preview and wait for the human's actual confirmation before that write. A blanket pre-approval does not replace a confirmation requested by the connector.
- Make one create attempt. If its outcome is unclear, read/search using available identifiers before considering any further action; never create a possible duplicate.
- Read back the task title, description, assignee, due date/time state, and status using the selected backend's existing read tools. For the custom MCP, use `planfix_task_get` and request the supported fields needed for that comparison. Read participant/template details only when the backend exposes them.
- Compare actual values with the instruction. State any missing field, extra participant, or other mismatch plainly. Do not claim a checklist, comment, or confirmation exists unless it was actually created and read back. Never remove unexpected data automatically.
- Finish with a brief human-readable summary of the saved values and any unresolved discrepancy. Do not expose credentials or unrelated account data.

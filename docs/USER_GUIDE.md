# User Guide

This guide explains how to try Kotelkin Planfix MCP as a user, not as a maintainer.

## What This Server Is

Kotelkin Planfix MCP is a local MCP server for Planfix. It runs on your machine, receives tool calls from an MCP client over STDIO, and calls the Planfix REST API using your Planfix token.

It does not run a public web service. It does not store your token in the repository.

## What You Can Do

With a configured MCP client, you can ask for actions such as:

- "Create a Planfix task named `Prepare invoice`."
- "Show task 12345 from Planfix."
- "Move this task deadline to tomorrow at 11:00."
- "Add a comment to task 12345."
- "Create a checklist item for task 12345."
- "List Planfix project templates."
- "Show directory entries from directory 10."
- "Get statuses for this Planfix task process."

The exact phrasing depends on your MCP client. The server exposes tools; your client decides how to present them.

## Install From Source

Clone the repository and install it locally:

```bash
python -m pip install -e .
```

For development checks:

```bash
python -m pip install -e ".[dev]"
```

## Configure Planfix Credentials

Set environment variables:

```bash
PLANFIX_BASE_URL=https://your-company.planfix.com/rest
PLANFIX_TOKEN=your_token_here
```

Or store credentials in your OS keyring:

```bash
planfix-mcp-secrets-init
```

Keep tokens out of Git, issue reports, screenshots, and shared logs.

## Configure Your MCP Client

Use this server as a STDIO MCP command:

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

If your client supports inheriting environment variables, you can omit the `env` block after exporting variables locally.

## Safe First Checks

Run a local smoke check. This does not call Planfix:

```bash
planfix-mcp-smoke
```

Check that your token can reach Planfix:

```bash
planfix-mcp-preflight
```

If you want to verify task listing too:

```bash
PLANFIX_PREFLIGHT_TASK_LIST=1 planfix-mcp-preflight
```

## Live QA On A Test Account

Use a disposable Planfix account or a low-risk workspace.

Basic live QA:

```bash
planfix-mcp-live-qa-basic
```

If the task process blocks comments, provide an existing task where comments are allowed:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 planfix-mcp-live-qa-basic
```

Extended live QA:

```bash
PLANFIX_LIVE_QA_COMMENT_TASK_ID=12345 \
PLANFIX_LIVE_QA_DATATAG_ID=10 \
PLANFIX_LIVE_QA_ASSIGNEE_ID=1 \
PLANFIX_LIVE_QA_DIRECTORY_ID=10 \
planfix-mcp-live-qa-extended
```

Permanent account configuration writes, such as custom-field creation, are disabled by default. Enable them only on a disposable account:

```bash
PLANFIX_LIVE_QA_CONFIG_WRITES=1 planfix-mcp-live-qa-extended
```

## Tool Groups

The server registers 58 tools:

- Tasks: create, get, update, list, dates, statuses, assignees, files, templates, recurring tasks, filters.
- Comments: list, add, update, get, delete.
- Checklists: create, list, get item, update item.
- DataTags: add to task, add to existing comment.
- Projects: create, list, groups, templates, get, update, files.
- Directories: groups, list, get, entries, filters.
- Processes and objects: list and statuses.
- Custom fields: task/project groups, list, create, get.

For exact payload examples, see [MANUAL_QA_EXTENDED_TOOLS.md](../MANUAL_QA_EXTENDED_TOOLS.md).

## Safety Notes

Read tools are low risk. Write tools change Planfix data.

Before connecting this to a production Planfix account:

- create a token with only the scopes you need;
- test against a disposable account;
- keep `PLANFIX_MIN_REQUEST_INTERVAL_SEC` at a conservative value;
- confirm which task processes allow comments, statuses, and assignee changes;
- do not expose your token in MCP config committed to Git.

## Troubleshooting

Authentication failures usually mean the token was not saved, has expired, or lacks a required scope.

Business validation errors usually mean the selected Planfix task process does not allow that operation. For example, some processes block new comments.

If `planfix_task_get_statuses` cannot resolve statuses from a task, pass `process_id` or `object_id` in the payload:

```json
{
  "task_id": 12345,
  "payload": {
    "process_id": 100206
  }
}
```

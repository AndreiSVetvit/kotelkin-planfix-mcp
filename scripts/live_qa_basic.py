from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from scripts.live_qa_common import (
    LiveQAFailure,
    call_tool,
    find_id,
    optional_int_env,
    require_tool_contract,
    server_env,
)
from scripts.smoke_tools import EXPECTED_TOOLS


async def _run_live_qa() -> int:
    params = StdioServerParameters(
        command="python",
        args=["-m", "planfix_mcp.server"],
        env=server_env(),
    )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    date = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
    comment_task_id = optional_int_env("PLANFIX_LIVE_QA_COMMENT_TASK_ID")

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            await require_tool_contract(session, EXPECTED_TOOLS)

            created = await call_tool(
                session,
                "planfix_task_create",
                {"payload": {"name": f"MCP Live QA {stamp}", "description": "Created by Planfix MCP live QA."}},
            )
            task_id = find_id(created)
            if task_id is None:
                raise LiveQAFailure(f"Unable to find task id in create response: {created}")
            print(f"[INFO] created_task_id={task_id}")

            await call_tool(session, "planfix_task_get", {"task_id": task_id})
            await call_tool(
                session,
                "planfix_task_update",
                {"task_id": task_id, "payload": {"name": f"MCP Live QA {stamp} updated"}},
            )
            await call_tool(
                session,
                "planfix_task_change_dates",
                {
                    "task_id": task_id,
                    "payload": {
                        "startDateTime": f"{date} 10:00:00",
                        "endDateTime": f"{date} 11:00:00",
                    },
                },
            )
            await call_tool(session, "planfix_task_list", {"payload": {}})

            await _run_comment_flow(session, comment_task_id or task_id, comment_task_id is not None)
    print("[PASS] Live QA completed")
    return 0


async def _run_comment_flow(session: ClientSession, task_id: int, required: bool) -> None:
    await call_tool(session, "planfix_task_comments_list", {"task_id": task_id, "payload": {}})
    try:
        comment = await call_tool(
            session,
            "planfix_task_comment_add",
            {"task_id": task_id, "payload": {"description": "MCP live QA comment."}},
        )
    except Exception:
        if required:
            raise
        print("[SKIP] planfix_task_comment_add: comments are not allowed for the created task")
        return

    comment_id = find_id(comment)
    if comment_id is None:
        raise LiveQAFailure(f"Unable to find comment id in add response: {comment}")
    print(f"[INFO] created_comment_id={comment_id}")

    await call_tool(
        session,
        "planfix_task_comment_update",
        {
            "task_id": task_id,
            "comment_id": comment_id,
            "payload": {"description": "MCP live QA comment updated."},
        },
    )
    await call_tool(session, "planfix_comment_get", {"comment_id": comment_id})


def main() -> None:
    try:
        raise SystemExit(asyncio.run(_run_live_qa()))
    except LiveQAFailure as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

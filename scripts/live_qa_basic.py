from __future__ import annotations

import asyncio
import os
from datetime import datetime, timedelta, timezone
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from scripts.smoke_tools import EXPECTED_TOOLS


class LiveQAFailure(RuntimeError):
    pass


async def _call_tool(session: ClientSession, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = await session.call_tool(name, arguments)
    if result.isError:
        raise LiveQAFailure(f"{name} failed: {_content_text(result)}")
    structured = result.structuredContent
    if not isinstance(structured, dict):
        raise LiveQAFailure(f"{name} returned non-dict structured content: {_content_text(result)}")
    print(f"[PASS] {name}")
    return structured


def _content_text(result: Any) -> str:
    if not result.content:
        return ""
    item = result.content[0]
    return getattr(item, "text", repr(item))


def _find_id(value: Any) -> int | None:
    if isinstance(value, dict):
        for key in ("id", "taskId", "commentId"):
            candidate = value.get(key)
            if isinstance(candidate, int):
                return candidate
            if isinstance(candidate, str) and candidate.isdigit():
                return int(candidate)
        for key in ("task", "comment", "data", "result"):
            found = _find_id(value.get(key))
            if found is not None:
                return found
    if isinstance(value, list):
        for item in value:
            found = _find_id(item)
            if found is not None:
                return found
    return None


def _server_env() -> dict[str, str]:
    keys = (
        "PLANFIX_BASE_URL",
        "PLANFIX_TOKEN",
        "PLANFIX_TIMEOUT_SEC",
        "PLANFIX_RETRY_MAX",
        "PLANFIX_MIN_REQUEST_INTERVAL_SEC",
        "PLANFIX_STATUS_CHANGE_DELAY_SEC",
        "PLANFIX_SILENT_DEFAULT",
    )
    env = {key: value for key in keys if (value := os.environ.get(key))}
    env.setdefault("PLANFIX_MIN_REQUEST_INTERVAL_SEC", "1.05")
    env.setdefault("PLANFIX_STATUS_CHANGE_DELAY_SEC", "0")
    env["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "WARNING")
    return env


def _optional_int_env(name: str) -> int | None:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    if not raw.isdigit():
        raise LiveQAFailure(f"{name} must be a positive integer")
    value = int(raw)
    if value <= 0:
        raise LiveQAFailure(f"{name} must be a positive integer")
    return value


async def _run_live_qa() -> int:
    params = StdioServerParameters(
        command="python",
        args=["-m", "planfix_mcp.server"],
        env=_server_env(),
    )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    date = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
    comment_task_id = _optional_int_env("PLANFIX_LIVE_QA_COMMENT_TASK_ID")

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            names = {tool.name for tool in tools.tools}
            missing = sorted(EXPECTED_TOOLS - names)
            extra = sorted(names - EXPECTED_TOOLS)
            if missing or extra:
                raise LiveQAFailure(f"Tool contract mismatch: missing={missing}, extra={extra}")
            print(f"[PASS] list_tools total={len(names)}")

            created = await _call_tool(
                session,
                "planfix_task_create",
                {"payload": {"name": f"MCP Live QA {stamp}", "description": "Created by Planfix MCP live QA."}},
            )
            task_id = _find_id(created)
            if task_id is None:
                raise LiveQAFailure(f"Unable to find task id in create response: {created}")
            print(f"[INFO] created_task_id={task_id}")

            await _call_tool(session, "planfix_task_get", {"task_id": task_id})
            await _call_tool(
                session,
                "planfix_task_update",
                {"task_id": task_id, "payload": {"name": f"MCP Live QA {stamp} updated"}},
            )
            await _call_tool(
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
            await _call_tool(session, "planfix_task_list", {"payload": {}})

            await _run_comment_flow(session, comment_task_id or task_id, comment_task_id is not None)
    print("[PASS] Live QA completed")
    return 0


async def _run_comment_flow(session: ClientSession, task_id: int, required: bool) -> None:
    await _call_tool(session, "planfix_task_comments_list", {"task_id": task_id, "payload": {}})
    try:
        comment = await _call_tool(
            session,
            "planfix_task_comment_add",
            {"task_id": task_id, "payload": {"description": "MCP live QA comment."}},
        )
    except Exception:
        if required:
            raise
        print("[SKIP] planfix_task_comment_add: comments are not allowed for the created task")
        return

    comment_id = _find_id(comment)
    if comment_id is None:
        raise LiveQAFailure(f"Unable to find comment id in add response: {comment}")
    print(f"[INFO] created_comment_id={comment_id}")

    await _call_tool(
        session,
        "planfix_task_comment_update",
        {
            "task_id": task_id,
            "comment_id": comment_id,
            "payload": {"description": "MCP live QA comment updated."},
        },
    )
    await _call_tool(session, "planfix_comment_get", {"comment_id": comment_id})


def main() -> None:
    try:
        raise SystemExit(asyncio.run(_run_live_qa()))
    except LiveQAFailure as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

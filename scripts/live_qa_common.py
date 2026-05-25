from __future__ import annotations

import os
from typing import Any

from mcp import ClientSession, StdioServerParameters


class LiveQAFailure(RuntimeError):
    pass


async def require_tool_contract(session: ClientSession, expected_tools: set[str]) -> int:
    tools = await session.list_tools()
    names = {tool.name for tool in tools.tools}
    missing = sorted(expected_tools - names)
    extra = sorted(names - expected_tools)
    if missing or extra:
        raise LiveQAFailure(f"Tool contract mismatch: missing={missing}, extra={extra}")
    print(f"[PASS] list_tools total={len(names)}")
    return len(names)


async def call_tool(session: ClientSession, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = await session.call_tool(name, arguments)
    if result.isError:
        raise LiveQAFailure(f"{name} failed: {content_text(result)}")
    structured = result.structuredContent
    if not isinstance(structured, dict):
        raise LiveQAFailure(f"{name} returned non-dict structured content: {content_text(result)}")
    print(f"[PASS] {name}")
    return structured


async def try_call_tool(
    session: ClientSession,
    name: str,
    arguments: dict[str, Any],
    *,
    reason: str,
) -> dict[str, Any] | None:
    try:
        return await call_tool(session, name, arguments)
    except Exception as exc:
        print(f"[SKIP] {name}: {reason}; {str(exc)[:240]}")
        return None


def content_text(result: Any) -> str:
    if not result.content:
        return ""
    item = result.content[0]
    return getattr(item, "text", repr(item))


def find_id(value: Any, keys: tuple[str, ...] = ("id", "taskId", "commentId")) -> int | None:
    if isinstance(value, dict):
        for key in keys:
            found = value.get(key)
            if isinstance(found, int) and found > 0:
                return found
            if isinstance(found, str) and found.isdigit():
                numeric = int(found)
                if numeric > 0:
                    return numeric
        for nested in value.values():
            found = find_id(nested, keys)
            if found is not None:
                return found
    if isinstance(value, list):
        for item in value:
            found = find_id(item, keys)
            if found is not None:
                return found
    return None


def find_value(value: Any, keys: tuple[str, ...]) -> Any | None:
    if isinstance(value, dict):
        for key in keys:
            candidate = value.get(key)
            if candidate is not None:
                return candidate
        for nested in value.values():
            found = find_value(nested, keys)
            if found is not None:
                return found
    if isinstance(value, list):
        for item in value:
            found = find_value(item, keys)
            if found is not None:
                return found
    return None


def server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command="python",
        args=["-m", "planfix_mcp.server"],
        env=server_env(),
    )


def server_env() -> dict[str, str]:
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


def optional_int_env(name: str) -> int | None:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return None
    if not raw.isdigit():
        raise LiveQAFailure(f"{name} must be a positive integer")
    value = int(raw)
    if value <= 0:
        raise LiveQAFailure(f"{name} must be a positive integer")
    return value


def env_flag(name: str) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    return raw in {"1", "true", "yes", "y", "on"}

from __future__ import annotations

import asyncio

from mcp.server.fastmcp import FastMCP

from planfix_mcp.tools.employees import register as register_employee_tools
from planfix_mcp.tools.tasks_core import register as register_task_core_tools
from scripts.smoke_tools import EXPECTED_TOOLS, _run_smoke


def test_expected_tool_contract_has_59_tools() -> None:
    assert len(EXPECTED_TOOLS) == 59


def test_registered_tools_match_contract() -> None:
    assert asyncio.run(_run_smoke()) == 0


def test_task_get_tool_schema_has_optional_string_fields() -> None:
    server = FastMCP("schema-test")
    register_task_core_tools(server, object())
    tools = asyncio.run(server.list_tools())
    tool = next(item for item in tools if item.name == "planfix_task_get")

    assert "fields" in tool.inputSchema["properties"]
    assert "fields" not in tool.inputSchema["required"]
    fields_schema = tool.inputSchema["properties"]["fields"]
    assert {item.get("type") for item in fields_schema["anyOf"]} == {"string", "null"}


def test_employee_search_tool_schema_requires_query_and_defaults_offset() -> None:
    server = FastMCP("schema-test")
    register_employee_tools(server, object())
    tools = asyncio.run(server.list_tools())
    tool = next(item for item in tools if item.name == "planfix_employee_search")

    assert tool.inputSchema["required"] == ["query"]
    assert tool.inputSchema["properties"]["query"]["type"] == "string"
    assert tool.inputSchema["properties"]["offset"]["type"] == "integer"
    assert tool.annotations is not None
    assert tool.annotations.readOnlyHint is True

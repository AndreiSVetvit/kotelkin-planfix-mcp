from __future__ import annotations

from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from planfix_mcp.client import PlanfixClient
from planfix_mcp.config import Settings, configure_logging
from planfix_mcp.tools.checklists_ext import register as register_checklist_ext_tools
from planfix_mcp.tools.comments import register as register_comment_tools
from planfix_mcp.tools.comments_global import register as register_comment_global_tools
from planfix_mcp.tools.custom_fields import register as register_customfield_tools
from planfix_mcp.tools.directories import register as register_directory_tools
from planfix_mcp.tools.processes_objects import register as register_process_object_tools
from planfix_mcp.tools.projects import register as register_project_tools
from planfix_mcp.tools.tasks_core import register as register_task_core_tools
from planfix_mcp.tools.tasks_data import register as register_task_data_tools
from planfix_mcp.tools.tasks_meta import register as register_task_meta_tools
from planfix_mcp.tools.tasks_status import register as register_task_status_tools


def create_server() -> FastMCP:
    settings = Settings.from_env()
    configure_logging(settings.log_level)

    client = PlanfixClient(settings)

    @asynccontextmanager
    async def lifespan(_: FastMCP):
        try:
            yield
        finally:
            await client.aclose()

    mcp = FastMCP("kotelkin-planfix-mcp", lifespan=lifespan)

    register_task_core_tools(mcp, client)
    register_task_status_tools(mcp, client)
    register_comment_tools(mcp, client)
    register_comment_global_tools(mcp, client)
    register_task_data_tools(mcp, client)
    register_task_meta_tools(mcp, client)
    register_checklist_ext_tools(mcp, client)
    register_project_tools(mcp, client)
    register_directory_tools(mcp, client)
    register_process_object_tools(mcp, client)
    register_customfield_tools(mcp, client)

    return mcp


def main() -> None:
    mcp = create_server()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

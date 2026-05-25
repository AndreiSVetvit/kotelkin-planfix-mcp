from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from planfix_mcp.server import create_server

EXPECTED_TOOLS = {
    "planfix_task_create",
    "planfix_task_get",
    "planfix_task_update",
    "planfix_task_list",
    "planfix_task_update_custom_fields",
    "planfix_task_accept",
    "planfix_task_reject",
    "planfix_task_change_status",
    "planfix_task_get_statuses",
    "planfix_task_change_assignees",
    "planfix_task_change_dates",
    "planfix_task_comments_list",
    "planfix_task_comment_add",
    "planfix_task_comment_update",
    "planfix_task_datatag_add",
    "planfix_task_datatag_to_comment",
    "planfix_task_files",
    "planfix_task_templates",
    "planfix_task_recurring",
    "planfix_task_filters",
    "planfix_task_checklist_create",
    "planfix_task_checklist_get",
    "planfix_task_checklist_item_get",
    "planfix_task_checklist_update",
    "planfix_comment_get",
    "planfix_comment_delete",
    "planfix_project_create",
    "planfix_project_groups",
    "planfix_project_list",
    "planfix_project_templates",
    "planfix_project_get",
    "planfix_project_update",
    "planfix_project_files",
    "planfix_directory_groups",
    "planfix_directory_list",
    "planfix_directory_get",
    "planfix_directory_entry_add",
    "planfix_directory_entry_list",
    "planfix_directory_entry_get",
    "planfix_directory_entry_update",
    "planfix_directory_entry_delete",
    "planfix_directory_filters",
    "planfix_process_contact_list",
    "planfix_process_task_list",
    "planfix_process_task_statuses",
    "planfix_object_list",
    "planfix_object_get",
    "planfix_object_statuses",
    "planfix_customfield_task_group_list",
    "planfix_customfield_task_group_create",
    "planfix_customfield_task_list",
    "planfix_customfield_task_create",
    "planfix_customfield_task_get",
    "planfix_customfield_project_group_list",
    "planfix_customfield_project_group_create",
    "planfix_customfield_project_list",
    "planfix_customfield_project_create",
    "planfix_customfield_project_get",
}


async def _run_smoke() -> int:
    # The smoke check validates registration shape and does not call Planfix.
    os.environ.setdefault("PLANFIX_BASE_URL", "https://example.planfix.com/rest")
    os.environ.setdefault("PLANFIX_TOKEN", "smoke-token")
    os.environ.setdefault("PLANFIX_MIN_REQUEST_INTERVAL_SEC", "0")

    server = create_server()
    tools = await server.list_tools()
    names = {tool.name for tool in tools}

    missing = sorted(EXPECTED_TOOLS - names)
    extra = sorted(names - EXPECTED_TOOLS)

    if missing or extra:
        print("[FAIL] Tool registration mismatch")
        print(f"[INFO] expected={len(EXPECTED_TOOLS)} actual={len(names)}")
        print(f"[INFO] missing={missing}")
        print(f"[INFO] extra={extra}")
        return 1

    print("[PASS] Tool registration is correct")
    print(f"[INFO] total_tools={len(names)}")
    return 0


def main() -> None:
    raise SystemExit(asyncio.run(_run_smoke()))


if __name__ == "__main__":
    main()

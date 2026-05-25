from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.server import create_server

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
    "planfix_task_checklist_get",
    "planfix_task_checklist_update",
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

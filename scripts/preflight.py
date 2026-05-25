from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.client import PlanfixAPIError, PlanfixClient
from src.config import Settings, configure_logging


async def _run_preflight() -> int:
    try:
        settings = Settings.from_env()
    except ValueError as exc:
        print(f"[FAIL] Invalid environment configuration: {exc}")
        return 2

    if not settings.base_url.startswith(("http://", "https://")):
        print("[FAIL] PLANFIX_BASE_URL must start with http:// or https://")
        return 2

    configure_logging(settings.log_level)
    client = PlanfixClient(settings)

    try:
        print("[STEP] GET /ping")
        ping = await client.get("/ping")
        print(f"[OK] Ping response type: {type(ping).__name__}")

        print("[STEP] GET /workspace/list")
        workspaces = await client.get("/workspace/list")
        _print_workspace_summary(workspaces)

        if os.getenv("PLANFIX_PREFLIGHT_TASK_LIST", "0").strip() == "1":
            print("[STEP] POST /task/list (optional)")
            tasks = await client.list_tasks({})
            print(f"[OK] Task list endpoint responded, payload keys: {sorted(tasks.keys())}")
        else:
            print("[SKIP] Optional /task/list check is disabled (set PLANFIX_PREFLIGHT_TASK_LIST=1)")

        print("[PASS] Preflight completed")
        return 0
    except PlanfixAPIError as exc:
        print(f"[FAIL] {exc}")
        if exc.status_code is not None:
            print(f"[INFO] status={exc.status_code}")
        if exc.endpoint:
            print(f"[INFO] endpoint={exc.endpoint}")
        return 1
    finally:
        await client.aclose()


def _print_workspace_summary(payload: dict[str, Any]) -> None:
    items: list[Any] = []
    for key in ("workspaces", "workspace", "data", "result"):
        value = payload.get(key)
        if isinstance(value, list):
            items = value
            break
    print(f"[OK] Workspace endpoint responded, detected list size: {len(items)}")


def main() -> None:
    raise SystemExit(asyncio.run(_run_preflight()))


if __name__ == "__main__":
    main()

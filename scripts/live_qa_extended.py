from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import stdio_client

from scripts.live_qa_common import (
    LiveQAFailure,
    call_tool,
    env_flag,
    find_id,
    find_value,
    optional_int_env,
    require_tool_contract,
    server_params,
    try_call_tool,
)
from scripts.smoke_tools import EXPECTED_TOOLS


async def _run_live_qa() -> int:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    slug = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    date = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
    comment_task_id = optional_int_env("PLANFIX_LIVE_QA_COMMENT_TASK_ID")
    datatag_id = optional_int_env("PLANFIX_LIVE_QA_DATATAG_ID")
    assignee_id = optional_int_env("PLANFIX_LIVE_QA_ASSIGNEE_ID")
    directory_id = optional_int_env("PLANFIX_LIVE_QA_DIRECTORY_ID")
    allow_config_writes = env_flag("PLANFIX_LIVE_QA_CONFIG_WRITES")

    async with stdio_client(server_params()) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await require_tool_contract(session, EXPECTED_TOOLS)

            task_id = await _run_task_flow(session, stamp, date, assignee_id)
            await _run_task_metadata_flow(session, task_id)
            await _run_checklist_flow(session, task_id, slug)
            await _run_process_flow(session, task_id)
            await _run_project_flow(session, stamp)
            await _run_directory_flow(session, directory_id, slug)
            await _run_object_flow(session)
            await _run_customfield_flow(session, allow_config_writes, slug)
            await _run_comment_and_datatag_flow(
                session,
                comment_task_id or task_id,
                comment_task_id is not None,
                datatag_id,
            )

    print("[PASS] Extended live QA completed")
    return 0


async def _run_task_flow(session: ClientSession, stamp: str, date: str, assignee_id: int | None) -> int:
    created = await call_tool(
        session,
        "planfix_task_create",
        {
            "payload": {
                "name": f"MCP Extended Live QA {stamp}",
                "description": "Created by extended Planfix MCP live QA.",
            },
        },
    )
    task_id = find_id(created)
    if task_id is None:
        raise LiveQAFailure(f"Unable to find task id in create response: {created}")
    print(f"[INFO] created_task_id={task_id}")

    await call_tool(session, "planfix_task_get", {"task_id": task_id})
    await call_tool(
        session,
        "planfix_task_update",
        {"task_id": task_id, "payload": {"name": f"MCP Extended Live QA {stamp} updated"}},
    )
    await call_tool(
        session,
        "planfix_task_update_custom_fields",
        {"task_id": task_id, "payload": {"customFieldData": []}},
    )
    await call_tool(session, "planfix_task_accept", {"task_id": task_id, "payload": {}})
    await call_tool(session, "planfix_task_reject", {"task_id": task_id, "payload": {}})
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

    if assignee_id is None:
        print("[SKIP] planfix_task_change_assignees: set PLANFIX_LIVE_QA_ASSIGNEE_ID to test assignment writes")
    else:
        await call_tool(
            session,
            "planfix_task_change_assignees",
            {"task_id": task_id, "payload": {"assignees": {"users": [{"id": assignee_id}]}}},
        )

    return task_id


async def _run_task_metadata_flow(session: ClientSession, task_id: int) -> None:
    await call_tool(session, "planfix_task_files", {"task_id": task_id, "payload": {}})
    await call_tool(session, "planfix_task_templates", {"payload": {}})
    await call_tool(session, "planfix_task_recurring", {"payload": {}})
    await call_tool(session, "planfix_task_filters", {"payload": {}})


async def _run_checklist_flow(session: ClientSession, task_id: int, slug: str) -> None:
    created = await call_tool(
        session,
        "planfix_task_checklist_create",
        {"task_id": task_id, "payload": {"name": f"MCP checklist {slug}"}},
    )
    await call_tool(session, "planfix_task_checklist_get", {"task_id": task_id, "payload": {}})
    item_id = find_id(created)
    if item_id is None:
        raise LiveQAFailure(f"Unable to find checklist item id in create response: {created}")
    print(f"[INFO] created_checklist_item_id={item_id}")
    await call_tool(session, "planfix_task_checklist_item_get", {"task_id": task_id, "item_id": item_id})
    await call_tool(
        session,
        "planfix_task_checklist_update",
        {"task_id": task_id, "item_id": item_id, "payload": {"name": f"MCP checklist {slug} updated"}},
    )


async def _run_process_flow(session: ClientSession, task_id: int) -> None:
    processes = await call_tool(session, "planfix_process_task_list", {"payload": {}})
    process_id = find_id(processes)
    if process_id is None:
        raise LiveQAFailure(f"Unable to find process id in response: {processes}")
    print(f"[INFO] task_process_id={process_id}")
    statuses = await call_tool(session, "planfix_process_task_statuses", {"process_id": process_id, "payload": {}})
    await call_tool(session, "planfix_task_get_statuses", {"task_id": task_id, "payload": {"process_id": process_id}})
    status_id = _first_positive_id(statuses.get("statuses"))
    if status_id is None:
        print("[SKIP] planfix_task_change_status: no positive status id returned by process statuses")
    else:
        await call_tool(
            session,
            "planfix_task_change_status",
            {"task_id": task_id, "payload": {"status": {"id": status_id}}},
        )
    await call_tool(session, "planfix_process_contact_list", {"payload": {}})


async def _run_project_flow(session: ClientSession, stamp: str) -> None:
    projects = await call_tool(session, "planfix_project_list", {"payload": {}})
    project_id = find_id(projects)
    await call_tool(session, "planfix_project_groups", {"payload": {}})
    await call_tool(session, "planfix_project_templates", {"payload": {}})
    if project_id is not None:
        print(f"[INFO] existing_project_id={project_id}")
        await call_tool(session, "planfix_project_get", {"project_id": project_id})
        await call_tool(session, "planfix_project_files", {"project_id": project_id, "payload": {}})
    else:
        print("[SKIP] planfix_project_get/files: no existing project returned")

    created = await call_tool(session, "planfix_project_create", {"payload": {"name": f"MCP Live QA Project {stamp}"}})
    created_project_id = find_id(created)
    if created_project_id is None:
        raise LiveQAFailure(f"Unable to find project id in create response: {created}")
    print(f"[INFO] created_project_id={created_project_id}")
    await call_tool(
        session,
        "planfix_project_update",
        {"project_id": created_project_id, "payload": {"name": f"MCP Live QA Project {stamp} updated"}},
    )


async def _run_directory_flow(session: ClientSession, directory_id: int | None, slug: str) -> None:
    directories = await call_tool(session, "planfix_directory_list", {"payload": {}})
    selected_directory_id = directory_id or find_id(directories)
    await call_tool(session, "planfix_directory_groups", {"payload": {}})
    if selected_directory_id is None:
        raise LiveQAFailure(f"Unable to find directory id in response: {directories}")
    print(f"[INFO] directory_id={selected_directory_id}")
    await call_tool(session, "planfix_directory_get", {"directory_id": selected_directory_id})
    await call_tool(session, "planfix_directory_filters", {"directory_id": selected_directory_id, "payload": {}})
    await call_tool(session, "planfix_directory_entry_list", {"directory_id": selected_directory_id, "payload": {}})
    created = await call_tool(
        session,
        "planfix_directory_entry_add",
        {"directory_id": selected_directory_id, "payload": {"name": f"MCP directory entry {slug}"}},
    )
    key = find_value(created, ("key", "id"))
    if key is None:
        raise LiveQAFailure(f"Unable to find directory entry key in create response: {created}")
    key_text = str(key)
    print(f"[INFO] created_directory_entry_key={key_text}")
    await call_tool(session, "planfix_directory_entry_get", {"directory_id": selected_directory_id, "key": key_text})
    await call_tool(
        session,
        "planfix_directory_entry_update",
        {
            "directory_id": selected_directory_id,
            "key": key_text,
            "payload": {"name": f"MCP directory entry {slug} updated"},
        },
    )
    await call_tool(
        session,
        "planfix_directory_entry_delete",
        {"directory_id": selected_directory_id, "key": key_text},
    )


async def _run_object_flow(session: ClientSession) -> None:
    objects = await call_tool(session, "planfix_object_list", {"payload": {}})
    object_id = find_id(objects)
    if object_id is None:
        raise LiveQAFailure(f"Unable to find object id in response: {objects}")
    print(f"[INFO] object_id={object_id}")
    await call_tool(session, "planfix_object_get", {"object_id": object_id})
    await call_tool(session, "planfix_object_statuses", {"object_id": object_id, "payload": {}})


async def _run_customfield_flow(session: ClientSession, allow_config_writes: bool, slug: str) -> None:
    await call_tool(session, "planfix_customfield_task_group_list", {"payload": {}})
    task_fields = await call_tool(session, "planfix_customfield_task_list", {"payload": {}})
    task_field_id = find_id(task_fields)
    if task_field_id is not None:
        await call_tool(session, "planfix_customfield_task_get", {"field_id": task_field_id})
    else:
        print("[SKIP] planfix_customfield_task_get: no task custom field returned")

    await call_tool(session, "planfix_customfield_project_group_list", {"payload": {}})
    project_fields = await call_tool(session, "planfix_customfield_project_list", {"payload": {}})
    project_field_id = find_id(project_fields)
    if project_field_id is not None:
        await call_tool(session, "planfix_customfield_project_get", {"field_id": project_field_id})
    else:
        print("[SKIP] planfix_customfield_project_get: no project custom field returned")

    if not allow_config_writes:
        print("[SKIP] customfield create tools: set PLANFIX_LIVE_QA_CONFIG_WRITES=1 to create permanent test fields")
        return

    task_group = await call_tool(
        session,
        "planfix_customfield_task_group_create",
        {"payload": {"name": f"MCP QA task field set {slug}"}},
    )
    project_group = await call_tool(
        session,
        "planfix_customfield_project_group_create",
        {"payload": {"name": f"MCP QA project field set {slug}"}},
    )
    task_group_id = find_id(task_group)
    project_group_id = find_id(project_group)
    task_payload: dict[str, Any] = {"name": f"MCP QA task field {slug}", "type": 0}
    project_payload: dict[str, Any] = {"name": f"MCP QA project field {slug}", "type": 0}
    if task_group_id is not None:
        task_payload["groupId"] = task_group_id
    if project_group_id is not None:
        project_payload["groupId"] = project_group_id
    task_field = await call_tool(session, "planfix_customfield_task_create", {"payload": task_payload})
    project_field = await call_tool(session, "planfix_customfield_project_create", {"payload": project_payload})
    created_task_field_id = find_id(task_field)
    created_project_field_id = find_id(project_field)
    if created_task_field_id is not None:
        await call_tool(session, "planfix_customfield_task_get", {"field_id": created_task_field_id})
    if created_project_field_id is not None:
        await call_tool(session, "planfix_customfield_project_get", {"field_id": created_project_field_id})


async def _run_comment_and_datatag_flow(
    session: ClientSession,
    task_id: int,
    comment_task_was_explicit: bool,
    datatag_id: int | None,
) -> None:
    await call_tool(session, "planfix_task_comments_list", {"task_id": task_id, "payload": {}})
    comment = await try_call_tool(
        session,
        "planfix_task_comment_add",
        {"task_id": task_id, "payload": {"description": "MCP extended live QA comment."}},
        reason="comments may be disabled by the selected Planfix task process",
    )
    if comment is None:
        if comment_task_was_explicit:
            raise LiveQAFailure(f"Explicit comment task {task_id} did not allow comment creation")
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
            "payload": {"description": "MCP extended live QA comment updated."},
        },
    )
    await call_tool(session, "planfix_comment_get", {"comment_id": comment_id})
    await call_tool(session, "planfix_comment_delete", {"comment_id": comment_id})

    if datatag_id is None:
        print("[SKIP] planfix_task_datatag_add/to_comment: set PLANFIX_LIVE_QA_DATATAG_ID to test DataTag writes")
        return

    tag_comment = await call_tool(
        session,
        "planfix_task_datatag_add",
        {"task_id": task_id, "payload": {"dataTag": {"id": datatag_id}, "items": []}},
    )
    tag_comment_id = find_id(tag_comment, ("commentId", "id"))
    if tag_comment_id is None:
        raise LiveQAFailure(f"Unable to find datatag comment id in response: {tag_comment}")
    print(f"[INFO] datatag_comment_id={tag_comment_id}")
    await call_tool(
        session,
        "planfix_task_datatag_to_comment",
        {
            "task_id": task_id,
            "comment_id": tag_comment_id,
            "payload": {"dataTag": {"id": datatag_id}, "items": []},
        },
    )
    await call_tool(session, "planfix_comment_delete", {"comment_id": tag_comment_id})


def _first_positive_id(items: Any) -> int | None:
    if not isinstance(items, list):
        return None
    for item in items:
        candidate = find_id(item)
        if candidate is not None:
            return candidate
    return None


def main() -> None:
    try:
        raise SystemExit(asyncio.run(_run_live_qa()))
    except LiveQAFailure as exc:
        print(f"[FAIL] {exc}")
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

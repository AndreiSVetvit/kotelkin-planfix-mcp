from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.tasks import (
    TaskCreateInput,
    TaskGetInput,
    TaskListInput,
    TaskUpdateCustomFieldsInput,
    TaskUpdateInput,
)
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_task_create",
        description="Create a task in Planfix using raw payload.",
    )
    async def planfix_task_create(payload: dict[str, Any], silent: bool | None = None) -> dict[str, Any]:
        """Создать задачу Planfix из произвольного payload."""
        try:
            data = TaskCreateInput(payload=payload)
            return await client.create_task(data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_create", exc)) from exc

    @mcp.tool(
        name="planfix_task_get",
        description="Get task details by id, optionally selecting comma-separated fields.",
    )
    async def planfix_task_get(task_id: int, fields: str | None = None) -> dict[str, Any]:
        """Получить задачу по `task_id`; `fields` — необязательные имена полей через запятую."""
        try:
            data = TaskGetInput(task_id=task_id, fields=fields)
            return await client.get_task(data.task_id, fields=data.fields)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_get", exc)) from exc

    @mcp.tool(
        name="planfix_task_update",
        description="Update a task by id using raw payload.",
    )
    async def planfix_task_update(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Обновить задачу по `task_id` произвольным payload."""
        try:
            data = TaskUpdateInput(task_id=task_id, payload=payload)
            return await client.update_task(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_update: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_update", exc)) from exc

    @mcp.tool(
        name="planfix_task_list",
        description="List tasks with filters and pagination payload.",
    )
    async def planfix_task_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список задач с фильтрами и пагинацией."""
        try:
            data = TaskListInput(payload=payload or {})
            return await client.list_tasks(data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_list", exc)) from exc

    @mcp.tool(
        name="planfix_task_update_custom_fields",
        description="Update task custom fields by task id.",
    )
    async def planfix_task_update_custom_fields(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Обновить кастомные поля задачи по `task_id`."""
        try:
            data = TaskUpdateCustomFieldsInput(task_id=task_id, payload=payload)
            return await client.update_custom_fields(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_update_custom_fields: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_update_custom_fields", exc)) from exc

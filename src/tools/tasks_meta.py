from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from src.client import PlanfixAPIError, PlanfixClient
from src.schemas.checklists import TaskChecklistGetInput, TaskChecklistUpdateInput
from src.schemas.meta import TaskFilesInput, TaskFiltersInput, TaskRecurringInput, TaskTemplatesInput
from src.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_task_files",
        description="Get task files.",
    )
    async def planfix_task_files(task_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить файлы, прикреплённые к задаче."""
        try:
            data = TaskFilesInput(task_id=task_id, payload=payload or {})
            return await client.get_task_files(data.task_id, params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_files: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_files", exc)) from exc

    @mcp.tool(
        name="planfix_task_templates",
        description="Get available task templates.",
    )
    async def planfix_task_templates(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список шаблонов задач."""
        try:
            data = TaskTemplatesInput(payload=payload or {})
            return await client.get_task_templates(params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_templates: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_templates", exc)) from exc

    @mcp.tool(
        name="planfix_task_recurring",
        description="Get recurring tasks.",
    )
    async def planfix_task_recurring(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список повторяющихся задач."""
        try:
            data = TaskRecurringInput(payload=payload or {})
            return await client.get_recurring_tasks(params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_recurring: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_recurring", exc)) from exc

    @mcp.tool(
        name="planfix_task_filters",
        description="Get task filters.",
    )
    async def planfix_task_filters(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить доступные фильтры задач."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get_task_filters(data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_filters: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_filters", exc)) from exc

    @mcp.tool(
        name="planfix_task_checklist_get",
        description="Get task checklist tree.",
    )
    async def planfix_task_checklist_get(task_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить дерево/список чеклиста задачи."""
        try:
            data = TaskChecklistGetInput(task_id=task_id, payload=payload or {})
            return await client.get_checklists(data.task_id, params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_checklist_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_checklist_get", exc)) from exc

    @mcp.tool(
        name="planfix_task_checklist_update",
        description="Update task checklist item or tree payload.",
    )
    async def planfix_task_checklist_update(
        task_id: int,
        item_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Обновить пункт чеклиста по `item_id` в задаче."""
        try:
            data = TaskChecklistUpdateInput(task_id=task_id, item_id=item_id, payload=payload)
            return await client.update_checklist_item(data.task_id, data.item_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_checklist_update: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_checklist_update", exc)) from exc

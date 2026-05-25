from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.entities import TaskItemInput, TaskPayloadInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_task_checklist_create",
        description="Create checklist item in task via /task/{id}/checklist.",
    )
    async def planfix_task_checklist_create(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Создать пункт чеклиста в задаче `task_id`."""
        try:
            data = TaskPayloadInput(task_id=task_id, payload=payload)
            return await client.post(f"/task/{data.task_id}/checklist", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_checklist_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_checklist_create", exc)) from exc

    @mcp.tool(
        name="planfix_task_checklist_item_get",
        description="Get checklist item by task id and item id via /task/{id}/checklist/{itemId}.",
    )
    async def planfix_task_checklist_item_get(task_id: int, item_id: int) -> dict[str, Any]:
        """Получить пункт чеклиста по `task_id` и `item_id`."""
        try:
            data = TaskItemInput(task_id=task_id, item_id=item_id)
            return await client.get(f"/task/{data.task_id}/checklist/{data.item_id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_checklist_item_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_checklist_item_get", exc)) from exc


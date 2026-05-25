from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.tasks import (
    TaskAcceptInput,
    TaskChangeAssigneesInput,
    TaskChangeDatesInput,
    TaskChangeStatusInput,
    TaskGetStatusesInput,
    TaskRejectInput,
)
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_task_accept",
        description="Accept task by task id via task update payload (REST API has no dedicated accept endpoint).",
    )
    async def planfix_task_accept(
        task_id: int,
        payload: dict[str, Any] | None = None,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Принять задачу по `task_id` через обновление полей задачи."""
        try:
            data = TaskAcceptInput(task_id=task_id, payload=payload or {})
            return await client.accept_task(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_accept: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_accept", exc)) from exc

    @mcp.tool(
        name="planfix_task_reject",
        description="Reject task by task id via task update payload (REST API has no dedicated reject endpoint).",
    )
    async def planfix_task_reject(
        task_id: int,
        payload: dict[str, Any] | None = None,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Отклонить задачу по `task_id` через обновление полей задачи."""
        try:
            data = TaskRejectInput(task_id=task_id, payload=payload or {})
            return await client.reject_task(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_reject: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_reject", exc)) from exc

    @mcp.tool(
        name="planfix_task_change_status",
        description="Change task status by task id via task update payload.",
    )
    async def planfix_task_change_status(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Сменить статус задачи по `task_id` через payload."""
        try:
            data = TaskChangeStatusInput(task_id=task_id, payload=payload)
            return await client.change_status(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_change_status: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_change_status", exc)) from exc

    @mcp.tool(
        name="planfix_task_get_statuses",
        description="Get available statuses for task: resolves process/object from task and queries statuses endpoint.",
    )
    async def planfix_task_get_statuses(task_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить доступные статусы задачи по связанному процессу/объекту."""
        try:
            data = TaskGetStatusesInput(task_id=task_id, payload=payload or {})
            return await client.get_task_statuses(data.task_id, params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_get_statuses: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_get_statuses", exc)) from exc

    @mcp.tool(
        name="planfix_task_change_assignees",
        description="Change task assignees/auditors by task id via task update payload.",
    )
    async def planfix_task_change_assignees(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Изменить исполнителей/аудиторов задачи по `task_id`."""
        try:
            data = TaskChangeAssigneesInput(task_id=task_id, payload=payload)
            return await client.change_assignees(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_change_assignees: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_change_assignees", exc)) from exc

    @mcp.tool(
        name="planfix_task_change_dates",
        description="Change task dates/deadline by task id via task update payload.",
    )
    async def planfix_task_change_dates(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Изменить даты задачи (старт/дедлайн/окончание) по `task_id`."""
        try:
            data = TaskChangeDatesInput(task_id=task_id, payload=payload)
            return await client.change_dates(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_change_dates: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_change_dates", exc)) from exc

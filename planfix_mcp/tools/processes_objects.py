from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.entities import IdInput
from planfix_mcp.schemas.meta import TaskFiltersInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_process_contact_list",
        description="List contact processes via /process/contact.",
    )
    async def planfix_process_contact_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список процессов контактов."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/process/contact", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_process_contact_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_process_contact_list", exc)) from exc

    @mcp.tool(
        name="planfix_process_task_list",
        description="List task processes via /process/task.",
    )
    async def planfix_process_task_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список процессов задач."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/process/task", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_process_task_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_process_task_list", exc)) from exc

    @mcp.tool(
        name="planfix_process_task_statuses",
        description="Get task statuses by process id via /process/task/{id}/statuses.",
    )
    async def planfix_process_task_statuses(process_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить статусы задач процесса по `process_id`."""
        try:
            data = IdInput(id=process_id)
            params = TaskFiltersInput(payload=payload or {})
            return await client.get(f"/process/task/{data.id}/statuses", params=params.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_process_task_statuses: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_process_task_statuses", exc)) from exc

    @mcp.tool(
        name="planfix_object_list",
        description="List objects via /object/list.",
    )
    async def planfix_object_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список объектов."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.post("/object/list", payload=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_object_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_object_list", exc)) from exc

    @mcp.tool(
        name="planfix_object_get",
        description="Get object by id via /object/{id}.",
    )
    async def planfix_object_get(object_id: int) -> dict[str, Any]:
        """Получить объект по `object_id`."""
        try:
            data = IdInput(id=object_id)
            return await client.get(f"/object/{data.id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_object_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_object_get", exc)) from exc

    @mcp.tool(
        name="planfix_object_statuses",
        description="Get object task statuses via /object/{id}/statuses.",
    )
    async def planfix_object_statuses(object_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить статусы задач объекта по `object_id`."""
        try:
            data = IdInput(id=object_id)
            params = TaskFiltersInput(payload=payload or {})
            return await client.get(f"/object/{data.id}/statuses", params=params.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_object_statuses: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_object_statuses", exc)) from exc


from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.entities import IdInput, IdPayloadInput
from planfix_mcp.schemas.meta import TaskFiltersInput
from planfix_mcp.schemas.tasks import TaskCreateInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_project_create",
        description="Create project via /project/.",
    )
    async def planfix_project_create(payload: dict[str, Any], silent: bool | None = None) -> dict[str, Any]:
        """Создать проект по payload."""
        try:
            data = TaskCreateInput(payload=payload)
            return await client.post("/project/", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_create", exc)) from exc

    @mcp.tool(
        name="planfix_project_groups",
        description="Get project groups via /project/groups.",
    )
    async def planfix_project_groups(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список групп проектов."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/project/groups", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_groups: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_groups", exc)) from exc

    @mcp.tool(
        name="planfix_project_list",
        description="List projects via /project/list.",
    )
    async def planfix_project_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список проектов."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.post("/project/list", payload=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_list", exc)) from exc

    @mcp.tool(
        name="planfix_project_templates",
        description="Get project templates via /project/templates.",
    )
    async def planfix_project_templates(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить шаблоны проектов."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/project/templates", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_templates: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_templates", exc)) from exc

    @mcp.tool(
        name="planfix_project_get",
        description="Get project by id via /project/{id}.",
    )
    async def planfix_project_get(project_id: int) -> dict[str, Any]:
        """Получить проект по `project_id`."""
        try:
            data = IdInput(id=project_id)
            return await client.get(f"/project/{data.id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_get", exc)) from exc

    @mcp.tool(
        name="planfix_project_update",
        description="Update project by id via /project/{id}.",
    )
    async def planfix_project_update(
        project_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Обновить проект по `project_id`."""
        try:
            data = IdPayloadInput(id=project_id, payload=payload)
            return await client.post(f"/project/{data.id}", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_update: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_update", exc)) from exc

    @mcp.tool(
        name="planfix_project_files",
        description="Get project files via /project/{id}/files.",
    )
    async def planfix_project_files(project_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить файлы проекта по `project_id`."""
        try:
            data = IdInput(id=project_id)
            params = TaskFiltersInput(payload=payload or {})
            return await client.get(f"/project/{data.id}/files", params=params.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_project_files: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_project_files", exc)) from exc


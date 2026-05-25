from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.entities import IdInput
from planfix_mcp.schemas.meta import TaskFiltersInput
from planfix_mcp.schemas.tasks import TaskCreateInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_customfield_task_group_list",
        description="List custom field sets for task via /customfield/group/task.",
    )
    async def planfix_customfield_task_group_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список наборов кастомных полей задачи."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/customfield/group/task", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_task_group_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_task_group_list", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_task_group_create",
        description="Create custom field set for task via /customfield/group/task/.",
    )
    async def planfix_customfield_task_group_create(
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Создать набор кастомных полей задачи."""
        try:
            data = TaskCreateInput(payload=payload)
            return await client.post("/customfield/group/task/", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_task_group_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_task_group_create", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_task_list",
        description="List custom fields for task via /customfield/task.",
    )
    async def planfix_customfield_task_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список кастомных полей задачи."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/customfield/task", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_task_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_task_list", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_task_create",
        description="Create task custom field via /customfield/task/.",
    )
    async def planfix_customfield_task_create(payload: dict[str, Any], silent: bool | None = None) -> dict[str, Any]:
        """Создать кастомное поле задачи."""
        try:
            data = TaskCreateInput(payload=payload)
            return await client.post("/customfield/task/", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_task_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_task_create", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_task_get",
        description="Get task custom field by id via /customfield/task/{id}.",
    )
    async def planfix_customfield_task_get(field_id: int) -> dict[str, Any]:
        """Получить кастомное поле задачи по `field_id`."""
        try:
            data = IdInput(id=field_id)
            return await client.get(f"/customfield/task/{data.id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_task_get: {exc}") from exc
        except PlanfixAPIError as exc:
            if _is_known_customfield_get_issue(exc, expected_error_code=1000):
                fallback = await client.get("/customfield/task", params={})
                found = _find_customfield_by_id(fallback, field_id)
                if found is not None:
                    return {
                        "result": "success",
                        "source": "fallback_list",
                        "warning": (
                            "Direct endpoint /customfield/task/{id} failed for this account; "
                            "returned item from /customfield/task list."
                        ),
                        "customfield": found,
                    }
                raise RuntimeError(
                    "planfix_customfield_task_get failed on direct endpoint and fallback list did not contain this id. "
                    f"Original: {format_api_error('planfix_customfield_task_get', exc)}"
                ) from exc
            raise RuntimeError(format_api_error("planfix_customfield_task_get", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_project_group_list",
        description="List custom field sets for project via /customfield/group/project.",
    )
    async def planfix_customfield_project_group_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список наборов кастомных полей проекта."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/customfield/group/project", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_project_group_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_project_group_list", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_project_group_create",
        description="Create custom field set for project via /customfield/group/project/.",
    )
    async def planfix_customfield_project_group_create(
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Создать набор кастомных полей проекта."""
        try:
            data = TaskCreateInput(payload=payload)
            return await client.post("/customfield/group/project/", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_project_group_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_project_group_create", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_project_list",
        description="List custom fields for project via /customfield/project.",
    )
    async def planfix_customfield_project_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список кастомных полей проекта."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/customfield/project", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_project_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_project_list", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_project_create",
        description="Create project custom field via /customfield/project/.",
    )
    async def planfix_customfield_project_create(
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Создать кастомное поле проекта."""
        try:
            data = TaskCreateInput(payload=payload)
            return await client.post("/customfield/project/", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_project_create: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_customfield_project_create", exc)) from exc

    @mcp.tool(
        name="planfix_customfield_project_get",
        description="Get project custom field by id via /customfield/project/{id}.",
    )
    async def planfix_customfield_project_get(field_id: int) -> dict[str, Any]:
        """Получить кастомное поле проекта по `field_id`."""
        try:
            data = IdInput(id=field_id)
            return await client.get(f"/customfield/project/{data.id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_customfield_project_get: {exc}") from exc
        except PlanfixAPIError as exc:
            if _is_known_customfield_get_issue(exc, expected_error_code=3000):
                fallback = await client.get("/customfield/project", params={})
                found = _find_customfield_by_id(fallback, field_id)
                if found is not None:
                    return {
                        "result": "success",
                        "source": "fallback_list",
                        "warning": (
                            "Direct endpoint /customfield/project/{id} failed for this account; "
                            "returned item from /customfield/project list."
                        ),
                        "customfield": found,
                    }
                raise RuntimeError(
                    "planfix_customfield_project_get failed on direct endpoint and fallback list did not contain this id. "
                    f"Original: {format_api_error('planfix_customfield_project_get', exc)}"
                ) from exc
            raise RuntimeError(format_api_error("planfix_customfield_project_get", exc)) from exc


def _is_known_customfield_get_issue(exc: PlanfixAPIError, *, expected_error_code: int) -> bool:
    if exc.status_code != 500:
        return False
    details = exc.details
    if not isinstance(details, dict):
        return False
    code = details.get("code")
    return isinstance(code, int) and code == expected_error_code


def _find_customfield_by_id(payload: dict[str, Any], field_id: int) -> dict[str, Any] | None:
    items = payload.get("customfields")
    if not isinstance(items, list):
        return None
    for item in items:
        if not isinstance(item, dict):
            continue
        candidate = item.get("id")
        if isinstance(candidate, int) and candidate == field_id:
            return item
        if isinstance(candidate, str) and candidate.isdigit() and int(candidate) == field_id:
            return item
    return None

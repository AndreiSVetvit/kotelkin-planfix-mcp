from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.entities import DirectoryEntryInput, DirectoryEntryPayloadInput, DirectoryPayloadInput, IdInput
from planfix_mcp.schemas.meta import TaskFiltersInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_directory_groups",
        description="Get directory groups via /directory/groups.",
    )
    async def planfix_directory_groups(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список групп справочников."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.get("/directory/groups", params=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_groups: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_groups", exc)) from exc

    @mcp.tool(
        name="planfix_directory_list",
        description="List directories via /directory/list.",
    )
    async def planfix_directory_list(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список справочников."""
        try:
            data = TaskFiltersInput(payload=payload or {})
            return await client.post("/directory/list", payload=data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_list", exc)) from exc

    @mcp.tool(
        name="planfix_directory_get",
        description="Get directory by id via /directory/{id}.",
    )
    async def planfix_directory_get(directory_id: int) -> dict[str, Any]:
        """Получить справочник по `directory_id`."""
        try:
            data = IdInput(id=directory_id)
            return await client.get(f"/directory/{data.id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_get", exc)) from exc

    @mcp.tool(
        name="planfix_directory_entry_add",
        description="Add directory entry via /directory/{id}/entry/.",
    )
    async def planfix_directory_entry_add(
        directory_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Добавить запись в справочник `directory_id`."""
        try:
            data = DirectoryPayloadInput(directory_id=directory_id, payload=payload)
            return await client.post(f"/directory/{data.directory_id}/entry/", payload=data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_entry_add: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_entry_add", exc)) from exc

    @mcp.tool(
        name="planfix_directory_entry_list",
        description="List directory entries via /directory/{id}/entry/list.",
    )
    async def planfix_directory_entry_list(directory_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить записи справочника `directory_id`."""
        try:
            data = IdInput(id=directory_id)
            body = TaskFiltersInput(payload=payload or {})
            return await client.post(f"/directory/{data.id}/entry/list", payload=body.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_entry_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_entry_list", exc)) from exc

    @mcp.tool(
        name="planfix_directory_entry_get",
        description="Get directory entry via /directory/{id}/entry/{key}.",
    )
    async def planfix_directory_entry_get(directory_id: int, key: str) -> dict[str, Any]:
        """Получить запись справочника по `key`."""
        try:
            data = DirectoryEntryInput(directory_id=directory_id, key=key)
            return await client.get(f"/directory/{data.directory_id}/entry/{data.key}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_entry_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_entry_get", exc)) from exc

    @mcp.tool(
        name="planfix_directory_entry_update",
        description="Update directory entry via /directory/{id}/entry/{key}.",
    )
    async def planfix_directory_entry_update(
        directory_id: int,
        key: str,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Обновить запись справочника по `key`."""
        try:
            data = DirectoryEntryPayloadInput(directory_id=directory_id, key=key, payload=payload)
            return await client.post(
                f"/directory/{data.directory_id}/entry/{data.key}",
                payload=data.payload,
                silent=silent,
            )
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_entry_update: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_entry_update", exc)) from exc

    @mcp.tool(
        name="planfix_directory_entry_delete",
        description="Delete directory entry via /directory/{id}/entry/{key}.",
    )
    async def planfix_directory_entry_delete(
        directory_id: int,
        key: str,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Удалить запись справочника по `key`."""
        try:
            data = DirectoryEntryInput(directory_id=directory_id, key=key)
            return await client.delete(f"/directory/{data.directory_id}/entry/{data.key}", silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_entry_delete: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_entry_delete", exc)) from exc

    @mcp.tool(
        name="planfix_directory_filters",
        description="Get directory entry filters via /directory/{id}/filters.",
    )
    async def planfix_directory_filters(directory_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить фильтры записей справочника."""
        try:
            data = IdInput(id=directory_id)
            body = TaskFiltersInput(payload=payload or {})
            return await client.post(f"/directory/{data.id}/filters", payload=body.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_directory_filters: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_directory_filters", exc)) from exc


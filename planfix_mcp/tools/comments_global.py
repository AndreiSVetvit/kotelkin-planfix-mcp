from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.entities import IdInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_comment_get",
        description="Get comment by comment id via /comment/{id}.",
    )
    async def planfix_comment_get(comment_id: int) -> dict[str, Any]:
        """Получить комментарий по `comment_id`."""
        try:
            data = IdInput(id=comment_id)
            return await client.get(f"/comment/{data.id}")
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_comment_get: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_comment_get", exc)) from exc

    @mcp.tool(
        name="planfix_comment_delete",
        description="Delete comment by comment id via /comment/{id}.",
    )
    async def planfix_comment_delete(comment_id: int, silent: bool | None = None) -> dict[str, Any]:
        """Удалить комментарий по `comment_id`."""
        try:
            data = IdInput(id=comment_id)
            return await client.delete(f"/comment/{data.id}", silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_comment_delete: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_comment_delete", exc)) from exc


from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from src.client import PlanfixAPIError, PlanfixClient
from src.schemas.datatags import TaskDataTagAddInput, TaskDataTagToCommentInput
from src.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_task_datatag_add",
        description="Add DataTag to task.",
    )
    async def planfix_task_datatag_add(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Добавить DataTag в задачу по `task_id`."""
        try:
            data = TaskDataTagAddInput(task_id=task_id, payload=payload)
            return await client.add_datatag(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_datatag_add: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_datatag_add", exc)) from exc

    @mcp.tool(
        name="planfix_task_datatag_to_comment",
        description="Attach DataTag to task comment context.",
    )
    async def planfix_task_datatag_to_comment(
        task_id: int,
        comment_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Привязать DataTag к существующему комментарию задачи."""
        try:
            data = TaskDataTagToCommentInput(task_id=task_id, comment_id=comment_id, payload=payload)
            return await client.datatag_to_comment(data.task_id, data.comment_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_datatag_to_comment: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_datatag_to_comment", exc)) from exc

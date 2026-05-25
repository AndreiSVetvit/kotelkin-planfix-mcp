from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.comments import TaskCommentAddInput, TaskCommentsListInput, TaskCommentUpdateInput
from planfix_mcp.tools.error_utils import format_api_error


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_task_comment_add",
        description="Add a comment to a task.",
    )
    async def planfix_task_comment_add(
        task_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Добавить комментарий к задаче по `task_id`."""
        try:
            data = TaskCommentAddInput(task_id=task_id, payload=payload)
            return await client.add_comment(data.task_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_comment_add: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_comment_add", exc)) from exc

    @mcp.tool(
        name="planfix_task_comments_list",
        description="List comments for task id.",
    )
    async def planfix_task_comments_list(task_id: int, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        """Получить список комментариев задачи."""
        try:
            data = TaskCommentsListInput(task_id=task_id, payload=payload or {})
            return await client.list_comments(data.task_id, data.payload)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_comments_list: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_comments_list", exc)) from exc

    @mcp.tool(
        name="planfix_task_comment_update",
        description="Update or delete a comment by task id and comment id using payload action.",
    )
    async def planfix_task_comment_update(
        task_id: int,
        comment_id: int,
        payload: dict[str, Any],
        silent: bool | None = None,
    ) -> dict[str, Any]:
        """Обновить или удалить комментарий по `comment_id` в задаче."""
        try:
            data = TaskCommentUpdateInput(task_id=task_id, comment_id=comment_id, payload=payload)
            return await client.update_comment(data.task_id, data.comment_id, data.payload, silent=silent)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_task_comment_update: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_task_comment_update", exc)) from exc

from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from src.schemas.common import StrictBaseModel


class TaskDataTagAddInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskDataTagToCommentInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    comment_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value

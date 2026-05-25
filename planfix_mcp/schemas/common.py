from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TaskIdModel(StrictBaseModel):
    task_id: int = Field(gt=0)


class OptionalPayloadModel(StrictBaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class RequiredPayloadModel(StrictBaseModel):
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value

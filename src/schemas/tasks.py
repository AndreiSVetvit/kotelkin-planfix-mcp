from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from src.schemas.common import OptionalPayloadModel, StrictBaseModel, TaskIdModel


class TaskGetInput(TaskIdModel):
    pass


class TaskCreateInput(StrictBaseModel):
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskUpdateInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskListInput(OptionalPayloadModel):
    pass


class TaskChangeStatusInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskChangeAssigneesInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskUpdateCustomFieldsInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskAcceptInput(TaskIdModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskRejectInput(TaskIdModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskGetStatusesInput(TaskIdModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskChangeDatesInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value

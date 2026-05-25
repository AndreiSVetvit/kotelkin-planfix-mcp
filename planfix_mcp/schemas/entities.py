from __future__ import annotations

from typing import Any

from pydantic import Field, field_validator

from planfix_mcp.schemas.common import StrictBaseModel


class IdInput(StrictBaseModel):
    id: int = Field(gt=0)


class IdPayloadInput(StrictBaseModel):
    id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class IdOptionalPayloadInput(StrictBaseModel):
    id: int = Field(gt=0)
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskItemInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    item_id: int = Field(gt=0)


class TaskPayloadInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class TaskOptionalPayloadInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskItemPayloadInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    item_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class DirectoryEntryInput(StrictBaseModel):
    directory_id: int = Field(gt=0)
    key: str = Field(min_length=1)


class DirectoryEntryPayloadInput(StrictBaseModel):
    directory_id: int = Field(gt=0)
    key: str = Field(min_length=1)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


class DirectoryPayloadInput(StrictBaseModel):
    directory_id: int = Field(gt=0)
    payload: dict[str, Any]

    @field_validator("payload")
    @classmethod
    def validate_payload_not_empty(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("payload must not be empty")
        return value


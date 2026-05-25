from __future__ import annotations

from typing import Any

from pydantic import Field

from planfix_mcp.schemas.common import OptionalPayloadModel, StrictBaseModel


class TaskFilesInput(StrictBaseModel):
    task_id: int = Field(gt=0)
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskTemplatesInput(StrictBaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskRecurringInput(StrictBaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskFiltersInput(OptionalPayloadModel):
    pass

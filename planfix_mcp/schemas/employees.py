from __future__ import annotations

from pydantic import Field, field_validator

from planfix_mcp.schemas.common import StrictBaseModel


class EmployeeSearchInput(StrictBaseModel):
    query: str = Field(min_length=1, max_length=200, strict=True)
    offset: int = Field(default=0, ge=0, strict=True)

    @field_validator("query", mode="before")
    @classmethod
    def strip_query(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

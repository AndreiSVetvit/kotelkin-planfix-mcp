from __future__ import annotations

from typing import Any

from pydantic import ValidationError
from mcp.types import ToolAnnotations

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.schemas.employees import EmployeeSearchInput
from planfix_mcp.tools.error_utils import format_api_error

PAGE_SIZE = 100
EMPLOYEE_FIELDS = ("id", "name", "midname", "lastname")


def register(mcp: Any, client: PlanfixClient) -> None:
    @mcp.tool(
        name="planfix_employee_search",
        description=(
            "Search active employees by part of full name. Returns only employee IDs and names. "
            "If 100 candidates are returned, fetch the next page using offset + 100 before deciding whether a match is unique; "
            "ask the user when multiple candidates remain. This tool does not modify Planfix."
        ),
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    async def planfix_employee_search(query: str, offset: int = 0) -> dict[str, Any]:
        """Найти активных сотрудников по части ФИО; при полной странице дочитать следующую."""
        try:
            data = EmployeeSearchInput(query=query, offset=offset)
            response = await client.list_employees(
                {
                    "offset": data.offset,
                    "pageSize": PAGE_SIZE,
                    "onlyActive": True,
                    "prefixedId": False,
                    "fields": ",".join(EMPLOYEE_FIELDS),
                    "filters": [{"type": 9006, "operator": "equal", "value": data.query}],
                }
            )
            return _search_result(response, data.offset)
        except ValidationError as exc:
            raise ValueError(f"Invalid input for planfix_employee_search: {exc}") from exc
        except PlanfixAPIError as exc:
            raise RuntimeError(format_api_error("planfix_employee_search", exc)) from exc


def _search_result(response: dict[str, Any], offset: int) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise RuntimeError("Planfix returned an unexpected employee list response")
    users = response.get("users")
    if response.get("result") != "success" or not isinstance(users, list) or len(users) > PAGE_SIZE:
        raise RuntimeError("Planfix returned an unexpected employee list response")

    candidates: list[dict[str, Any]] = []
    for user in users:
        if not isinstance(user, dict):
            raise RuntimeError("Planfix returned an unexpected employee list response")

        employee_id = user.get("id")
        if not isinstance(employee_id, int) or isinstance(employee_id, bool) or employee_id <= 0:
            raise RuntimeError("Planfix returned an unexpected employee list response")

        candidate: dict[str, Any] = {"id": employee_id}
        for field in EMPLOYEE_FIELDS[1:]:
            value = user.get(field)
            if value is not None:
                if not isinstance(value, str):
                    raise RuntimeError("Planfix returned an unexpected employee list response")
                candidate[field] = value
        if not any(
            isinstance(candidate.get(field), str) and candidate[field].strip()
            for field in EMPLOYEE_FIELDS[1:]
        ):
            raise RuntimeError("Planfix returned an unexpected employee list response")
        candidates.append(candidate)

    return {
        "result": "success",
        "users": candidates,
        "offset": offset,
        "pageSize": PAGE_SIZE,
        "hasMore": len(users) == PAGE_SIZE,
    }

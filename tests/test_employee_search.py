from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
import pytest

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.config import Settings
from planfix_mcp.tools.employees import register


def make_settings() -> Settings:
    return Settings(
        base_url="https://example.planfix.com/rest",
        token="token",
        timeout_sec=5.0,
        retry_max=0,
        min_request_interval_sec=0.0,
        status_change_delay_sec=0.0,
        silent_default=False,
        log_level="INFO",
    )


class FakeMCP:
    def __init__(self) -> None:
        self.tools: dict[str, Any] = {}

    def tool(self, *, name: str, description: str, annotations: Any = None):
        def register_tool(function: Any) -> Any:
            self.tools[name] = function
            return function

        return register_tool


class FakeClient:
    def __init__(self, response: Any = None, error: Exception | None = None) -> None:
        self.response = response
        self.error = error
        self.payload: dict[str, Any] | None = None

    async def list_employees(self, payload: dict[str, Any]) -> Any:
        self.payload = payload
        if self.error:
            raise self.error
        return self.response


def registered_search(client: FakeClient) -> Any:
    mcp = FakeMCP()
    register(mcp, client)  # type: ignore[arg-type]
    return mcp.tools["planfix_employee_search"]


def test_employee_search_posts_documented_filter_and_projects_candidates() -> None:
    client = FakeClient(
        {
            "result": "success",
            "users": [
                {
                    "id": 123,
                    "name": "Andrey",
                    "midname": "Petrovich",
                    "lastname": "Ivanov",
                    "email": "private@example.com",
                }
            ],
        }
    )

    result = asyncio.run(registered_search(client)(query="  Ivanov  ", offset=100))

    assert client.payload == {
        "offset": 100,
        "pageSize": 100,
        "onlyActive": True,
        "prefixedId": False,
        "fields": "id,name,midname,lastname",
        "filters": [{"type": 9006, "operator": "equal", "value": "Ivanov"}],
    }
    assert result == {
        "result": "success",
        "users": [{"id": 123, "name": "Andrey", "midname": "Petrovich", "lastname": "Ivanov"}],
        "offset": 100,
        "pageSize": 100,
        "hasMore": False,
    }


def test_full_page_is_marked_as_potentially_incomplete() -> None:
    users = [{"id": index + 1, "name": f"Employee {index}"} for index in range(100)]
    tool = registered_search(FakeClient({"result": "success", "users": users}))

    result = asyncio.run(tool(query="Employee"))

    assert result["hasMore"] is True
    assert result["offset"] == 0
    assert result["pageSize"] == 100


@pytest.mark.parametrize(
    ("query", "offset"),
    [("   ", 0), ("x" * 201, 0), ("Ivanov", -1)],
)
def test_invalid_search_input_fails_before_api_call(query: str, offset: int) -> None:
    client = FakeClient({"result": "success", "users": []})

    with pytest.raises(ValueError, match="Invalid input for planfix_employee_search"):
        asyncio.run(registered_search(client)(query=query, offset=offset))

    assert client.payload is None


def test_maximum_query_length_is_accepted() -> None:
    client = FakeClient({"result": "success", "users": []})

    asyncio.run(registered_search(client)(query="x" * 200))

    assert client.payload is not None
    assert client.payload["filters"][0]["value"] == "x" * 200


@pytest.mark.parametrize(
    "response",
    [
        None,
        {"result": "fail", "users": []},
        {"result": "success"},
        {"result": "success", "users": None},
        {"result": "success", "users": "not-a-list"},
        {"result": "success", "users": [{"id": index + 1, "name": f"Employee {index}"} for index in range(101)]},
        {"result": "success", "users": [{"id": "user:12", "name": "Ivanov"}]},
        {"result": "success", "users": [{"id": 12}]},
        {"result": "success", "users": [{"id": 12, "name": "  "}]},
    ],
)
def test_unexpected_api_response_fails_instead_of_looking_like_no_match(response: Any) -> None:
    tool = registered_search(FakeClient(response))

    with pytest.raises(RuntimeError, match="unexpected employee list response"):
        asyncio.run(tool(query="Ivanov"))


def test_planfix_api_errors_keep_the_shared_error_format() -> None:
    client = FakeClient(error=PlanfixAPIError("forbidden", status_code=403, endpoint="/user/list"))

    with pytest.raises(RuntimeError, match="planfix_employee_search failed; status=403; endpoint=/user/list"):
        asyncio.run(registered_search(client)(query="Ivanov"))


def test_list_employees_posts_payload_to_user_list() -> None:
    requests: list[httpx.Request] = []
    payload = {
        "offset": 200,
        "pageSize": 100,
        "onlyActive": True,
        "prefixedId": False,
        "fields": "id,name,midname,lastname",
        "filters": [{"type": 9006, "operator": "equal", "value": "Ivanov"}],
    }

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"result": "success", "users": []})

    async def scenario() -> dict[str, Any]:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            return await client.list_employees(payload)
        finally:
            await client.aclose()

    result = asyncio.run(scenario())

    assert result == {"result": "success", "users": []}
    assert len(requests) == 1
    assert requests[0].method == "POST"
    assert requests[0].url.path == "/rest/user/list"
    assert json.loads(requests[0].content) == payload

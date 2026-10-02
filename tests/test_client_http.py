from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
import pytest

from planfix_mcp.client import PlanfixAPIError, PlanfixClient
from planfix_mcp.config import Settings


def make_settings(**overrides: Any) -> Settings:
    values = {
        "base_url": "https://example.planfix.com/rest",
        "token": "token",
        "timeout_sec": 5.0,
        "retry_max": 0,
        "min_request_interval_sec": 0.0,
        "status_change_delay_sec": 0.0,
        "silent_default": False,
        "log_level": "INFO",
    }
    values.update(overrides)
    return Settings(**values)


def run(coro: Any) -> Any:
    return asyncio.run(coro)


def test_post_uses_base_url_auth_json_and_silent_default() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"ok": True})

    async def scenario() -> dict[str, Any]:
        client = PlanfixClient(
            make_settings(silent_default=True),
            transport=httpx.MockTransport(handler),
        )
        try:
            return await client.create_task({"name": "Task"})
        finally:
            await client.aclose()

    assert run(scenario()) == {"ok": True}
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST"
    assert str(request.url) == "https://example.planfix.com/rest/task/?silent=true"
    assert request.headers["Authorization"] == "Bearer token"
    assert json.loads(request.content) == {"name": "Task"}


def test_request_raises_structured_api_error_on_http_error() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "bad token"})

    async def scenario() -> None:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            await client.get("/ping")
        finally:
            await client.aclose()

    with pytest.raises(PlanfixAPIError) as exc_info:
        run(scenario())

    error = exc_info.value
    assert error.status_code == 401
    assert error.endpoint == "/ping"
    assert error.details == {"error": "bad token"}
    assert "Authentication failed" in str(error)


def test_request_retries_429(monkeypatch: pytest.MonkeyPatch) -> None:
    status_codes = [429, 200]
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_codes.pop(0), json={"ok": True})

    async def scenario() -> dict[str, Any]:
        client = PlanfixClient(
            make_settings(retry_max=1),
            transport=httpx.MockTransport(handler),
        )
        try:
            return await client.get("/ping")
        finally:
            await client.aclose()

    monkeypatch.setattr("planfix_mcp.client.asyncio.sleep", fake_sleep)

    assert run(scenario()) == {"ok": True}
    assert sleeps == [0.5]
    assert status_codes == []


def test_get_task_statuses_uses_explicit_process_id_without_task_fetch() -> None:
    requested_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_urls.append(str(request.url))
        return httpx.Response(200, json={"statuses": []})

    async def scenario() -> dict[str, Any]:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            return await client.get_task_statuses(123, {"process_id": "456", "page": "1"})
        finally:
            await client.aclose()

    assert run(scenario()) == {"statuses": []}
    assert requested_urls == ["https://example.planfix.com/rest/process/task/456/statuses?page=1"]


def test_get_task_preserves_legacy_request_when_fields_are_omitted() -> None:
    requested_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_urls.append(str(request.url))
        return httpx.Response(200, json={"id": 123})

    async def scenario() -> None:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            await client.get_task(123)
            await client.get_task(124, fields=None)
        finally:
            await client.aclose()

    run(scenario())

    assert requested_urls == [
        "https://example.planfix.com/rest/task/123",
        "https://example.planfix.com/rest/task/124",
    ]


def test_get_task_forwards_selected_fields_as_query_parameter() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"id": 123, "name": "Task"})

    async def scenario() -> dict[str, Any]:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            return await client.get_task(123, fields="id,name,description,2001")
        finally:
            await client.aclose()

    assert run(scenario()) == {"id": 123, "name": "Task"}
    assert len(requests) == 1
    assert requests[0].method == "GET"
    assert requests[0].url.path == "/rest/task/123"
    assert requests[0].url.params["fields"] == "id,name,description,2001"


def test_get_task_preserves_structured_api_errors_with_fields() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"error": "forbidden"})

    async def scenario() -> None:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            await client.get_task(123, fields="id,name")
        finally:
            await client.aclose()

    with pytest.raises(PlanfixAPIError) as exc_info:
        run(scenario())

    assert exc_info.value.status_code == 403
    assert exc_info.value.endpoint == "/task/123"
    assert exc_info.value.details == {"error": "forbidden"}


def test_get_task_statuses_falls_back_to_object_id_from_task_payload() -> None:
    requested_paths: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        if request.url.path.endswith("/task/123"):
            return httpx.Response(200, json={"task": {"object": {"id": "789"}}})
        return httpx.Response(200, json={"statuses": []})

    async def scenario() -> dict[str, Any]:
        client = PlanfixClient(make_settings(), transport=httpx.MockTransport(handler))
        try:
            return await client.get_task_statuses(123)
        finally:
            await client.aclose()

    assert run(scenario()) == {"statuses": []}
    assert requested_paths == ["/rest/task/123", "/rest/object/789/statuses"]

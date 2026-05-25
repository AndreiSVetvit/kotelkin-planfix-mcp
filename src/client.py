from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

import httpx

from src.config import Settings

LOGGER = logging.getLogger(__name__)


class PlanfixAPIError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        endpoint: str | None = None,
        details: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.endpoint = endpoint
        self.details = details
        super().__init__(message)


class PlanfixClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.base_url
        self._retry_max = settings.retry_max
        self._min_interval_sec = settings.min_request_interval_sec
        self._silent_default = settings.silent_default
        self._request_lock = asyncio.Lock()
        self._last_request_ts = 0.0
        self._http = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(settings.timeout_sec),
            headers={
                "Authorization": _build_auth_header(settings.token),
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    async def aclose(self) -> None:
        await self._http.aclose()

    async def get(
        self,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self._request("GET", endpoint, params=_with_silent_param(params, self._resolve_silent(silent)))

    async def post(
        self,
        endpoint: str,
        *,
        payload: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            endpoint,
            params=_with_silent_param(params, self._resolve_silent(silent)),
            json_payload=payload,
        )

    async def create_task(self, payload: dict[str, Any], *, silent: bool | None = None) -> dict[str, Any]:
        return await self.post("/task/", payload=payload, silent=silent)

    async def get_task(self, task_id: int) -> dict[str, Any]:
        return await self.get(f"/task/{task_id}")

    async def update_task(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload, silent=silent)

    async def list_tasks(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self.post("/task/list", payload=payload)

    async def change_status(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload, silent=silent)

    async def change_assignees(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload, silent=silent)

    async def accept_task(
        self,
        task_id: int,
        payload: dict[str, Any] | None = None,
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload or {}, silent=silent)

    async def reject_task(
        self,
        task_id: int,
        payload: dict[str, Any] | None = None,
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload or {}, silent=silent)

    async def get_process_statuses(self, process_id: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.get(f"/process/task/{process_id}/statuses", params=params)

    async def get_object_statuses(self, object_id: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.get(f"/object/{object_id}/statuses", params=params)

    async def get_task_statuses(self, task_id: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
        task = await self.get_task(task_id)
        process_id = _extract_nested_id(task, ("processId", "process.id"))
        object_id = _extract_nested_id(task, ("objectId", "object.id"))

        if process_id is not None:
            return await self.get_process_statuses(process_id, params=params)
        if object_id is not None:
            return await self.get_object_statuses(object_id, params=params)
        raise PlanfixAPIError(
            f"Unable to resolve process/object id to get statuses for task {task_id}",
            endpoint=f"/task/{task_id}",
            details={"task_keys": sorted(task.keys()) if isinstance(task, dict) else None},
        )

    async def change_dates(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload, silent=silent)

    async def update_custom_fields(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}", payload=payload, silent=silent)

    async def add_comment(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/comments/", payload=payload, silent=silent)

    async def list_comments(self, task_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/comments/list", payload=payload)

    async def update_comment(
        self,
        task_id: int,
        comment_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/comments/{comment_id}", payload=payload, silent=silent)

    async def add_datatag(
        self,
        task_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/datatags/", payload=payload, silent=silent)

    async def datatag_to_comment(
        self,
        task_id: int,
        comment_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/datatags/{comment_id}", payload=payload, silent=silent)

    async def get_task_files(self, task_id: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.get(f"/task/{task_id}/files", params=params)

    async def get_task_templates(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.get("/task/templates", params=params)

    async def get_recurring_tasks(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.get("/task/recurring", params=params)

    async def get_task_filters(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self.post("/task/filters", payload=payload)

    async def get_checklists(self, task_id: int, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/checklist/list", payload=params or {})

    async def update_checklist_item(
        self,
        task_id: int,
        item_id: int,
        payload: dict[str, Any],
        *,
        silent: bool | None = None,
    ) -> dict[str, Any]:
        return await self.post(f"/task/{task_id}/checklist/{item_id}", payload=payload, silent=silent)

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        endpoint = _normalize_endpoint(endpoint)
        delays = [0.5, 1.0]

        for attempt in range(self._retry_max + 1):
            await self._respect_rate_limit()
            try:
                response = await self._http.request(
                    method,
                    endpoint,
                    params=params,
                    json=json_payload,
                )
            except httpx.TimeoutException as exc:
                if attempt < self._retry_max:
                    await asyncio.sleep(_retry_delay(attempt, delays))
                    continue
                raise PlanfixAPIError(
                    f"Timeout while calling {method} {endpoint} after {attempt + 1} attempts",
                    endpoint=endpoint,
                ) from exc
            except httpx.RequestError as exc:
                raise PlanfixAPIError(
                    f"Network error while calling {method} {endpoint}: {exc}",
                    endpoint=endpoint,
                ) from exc

            if response.status_code == 429 and attempt < self._retry_max:
                await asyncio.sleep(_retry_delay(attempt, delays))
                continue

            if response.is_error:
                details = _safe_json_or_text(response)
                hint = _status_hint(response.status_code)
                raise PlanfixAPIError(
                    f"{hint} (status {response.status_code}) for {method} {endpoint}: {details}",
                    status_code=response.status_code,
                    endpoint=endpoint,
                    details=details,
                )

            LOGGER.info("Planfix request %s %s -> %s", method, endpoint, response.status_code)
            return _safe_json_dict(response)

        raise PlanfixAPIError(
            f"Failed to call {method} {endpoint} after retries",
            endpoint=endpoint,
        )

    async def _respect_rate_limit(self) -> None:
        if self._min_interval_sec <= 0:
            return
        async with self._request_lock:
            now = time.monotonic()
            elapsed = now - self._last_request_ts
            wait_for = self._min_interval_sec - elapsed
            if wait_for > 0:
                await asyncio.sleep(wait_for)
            self._last_request_ts = time.monotonic()

    def _resolve_silent(self, silent: bool | None) -> bool | None:
        if silent is not None:
            return silent
        return True if self._silent_default else None


def _build_auth_header(token: str) -> str:
    normalized = token.strip()
    if " " in normalized:
        return normalized
    return f"Bearer {normalized}"


def _retry_delay(attempt: int, delays: list[float]) -> float:
    if attempt < len(delays):
        return delays[attempt]
    return delays[-1]


def _normalize_endpoint(endpoint: str) -> str:
    if endpoint.startswith("/"):
        return endpoint
    return f"/{endpoint}"


def _safe_json_dict(response: httpx.Response) -> dict[str, Any]:
    if not response.text:
        return {}
    try:
        parsed = response.json()
    except json.JSONDecodeError:
        return {"raw": response.text}
    if isinstance(parsed, dict):
        return parsed
    return {"data": parsed}


def _safe_json_or_text(response: httpx.Response) -> Any:
    if not response.text:
        return ""
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text


def _extract_nested_id(data: dict[str, Any], paths: tuple[str, ...]) -> int | None:
    for path in paths:
        current: Any = data
        ok = True
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                ok = False
                break
        if ok and isinstance(current, int):
            return current
        if ok and isinstance(current, str) and current.isdigit():
            return int(current)
    return None


def _status_hint(status_code: int) -> str:
    if status_code == 401:
        return "Authentication failed, check PLANFIX_TOKEN"
    if status_code == 403:
        return "Permission denied for current token"
    if status_code == 404:
        return "Resource not found or inaccessible"
    if status_code == 429:
        return "Rate limit exceeded, retry later"
    if status_code >= 500:
        return "Planfix server error"
    if 400 <= status_code < 500:
        return "Request rejected by Planfix"
    return "Unexpected API response"


def _with_silent_param(params: dict[str, Any] | None, silent: bool | None) -> dict[str, Any] | None:
    if silent is None:
        return params
    merged: dict[str, Any] = {}
    if params:
        merged.update(params)
    merged["silent"] = "true" if silent else "false"
    return merged

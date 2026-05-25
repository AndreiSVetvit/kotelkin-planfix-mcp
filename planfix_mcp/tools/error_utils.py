from __future__ import annotations

import json
from typing import Any

from planfix_mcp.client import PlanfixAPIError


def format_api_error(tool_name: str, exc: PlanfixAPIError) -> str:
    parts = [f"{tool_name} failed"]
    if exc.status_code is not None:
        parts.append(f"status={exc.status_code}")
    if exc.endpoint:
        parts.append(f"endpoint={exc.endpoint}")

    message = str(exc)
    if message:
        parts.append(f"message={message}")

    details = _compact_details(exc.details)
    if details:
        parts.append(f"details={details}")

    return "; ".join(parts)


def _compact_details(details: Any) -> str:
    if details is None:
        return ""
    try:
        text = json.dumps(details, ensure_ascii=True)
    except TypeError:
        text = str(details)
    if len(text) <= 500:
        return text
    return f"{text[:497]}..."

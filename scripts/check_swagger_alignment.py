from __future__ import annotations

from dataclasses import dataclass

import httpx

SWAGGER_URL = "https://help.planfix.com/restapidocs/swagger.json"


@dataclass(frozen=True)
class ExpectedOperation:
    method: str
    path: str
    note: str


EXPECTED_OPERATIONS = [
    ExpectedOperation("POST", "/task/", "task create"),
    ExpectedOperation("GET", "/task/{id}", "task get"),
    ExpectedOperation("POST", "/task/{id}", "task update/status/assignees/dates/accept/reject/custom fields"),
    ExpectedOperation("POST", "/task/list", "task list"),
    ExpectedOperation("POST", "/task/{id}/comments/", "comment add"),
    ExpectedOperation("POST", "/task/{id}/comments/list", "comment list"),
    ExpectedOperation("POST", "/task/{id}/comments/{commentId}", "comment update"),
    ExpectedOperation("POST", "/task/{id}/datatags/", "datatag add"),
    ExpectedOperation("POST", "/task/{id}/datatags/{commentId}", "datatag to comment"),
    ExpectedOperation("GET", "/task/{id}/files", "task files"),
    ExpectedOperation("GET", "/task/templates", "task templates"),
    ExpectedOperation("GET", "/task/recurring", "task recurring"),
    ExpectedOperation("POST", "/task/filters", "task filters"),
    ExpectedOperation("POST", "/task/{id}/checklist/list", "checklist get"),
    ExpectedOperation("POST", "/task/{id}/checklist/{itemId}", "checklist update"),
    ExpectedOperation("GET", "/process/task/{id}/statuses", "statuses by process"),
    ExpectedOperation("GET", "/object/{id}/statuses", "statuses by object"),
    ExpectedOperation("GET", "/ping", "preflight ping"),
    ExpectedOperation("GET", "/workspace/list", "preflight auth smoke"),
]


def main() -> None:
    try:
        response = httpx.get(SWAGGER_URL, timeout=30.0)
        response.raise_for_status()
        spec = response.json()
    except Exception as exc:
        print(f"[FAIL] Unable to fetch swagger: {exc}")
        raise SystemExit(2)

    paths = spec.get("paths", {})
    missing: list[str] = []
    wrong_method: list[str] = []

    for op in EXPECTED_OPERATIONS:
        node = paths.get(op.path)
        if not isinstance(node, dict):
            missing.append(f"{op.method} {op.path} ({op.note})")
            continue
        method_key = op.method.lower()
        if method_key not in node:
            wrong_method.append(f"{op.method} {op.path} ({op.note})")

    info = spec.get("info", {})
    version = info.get("version", "unknown")
    print(f"[INFO] swagger_version={version}")
    print(f"[INFO] checked_operations={len(EXPECTED_OPERATIONS)}")

    if missing or wrong_method:
        print("[FAIL] Swagger alignment check failed")
        if missing:
            print("[INFO] Missing paths:")
            for item in missing:
                print(f"  - {item}")
        if wrong_method:
            print("[INFO] Missing methods:")
            for item in wrong_method:
                print(f"  - {item}")
        raise SystemExit(1)

    print("[PASS] Swagger alignment check passed")


if __name__ == "__main__":
    main()

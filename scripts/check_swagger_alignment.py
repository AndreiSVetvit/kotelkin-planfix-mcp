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
    ExpectedOperation("GET", "/ping", "preflight ping"),
    ExpectedOperation("GET", "/workspace/list", "preflight auth smoke"),
    ExpectedOperation("POST", "/task/", "task create"),
    ExpectedOperation("GET", "/task/{id}", "task get"),
    ExpectedOperation("POST", "/task/{id}", "task update/status/assignees/dates/accept/reject/custom fields"),
    ExpectedOperation("POST", "/task/list", "task list"),
    ExpectedOperation("POST", "/task/filters", "task filters"),
    ExpectedOperation("GET", "/task/templates", "task templates"),
    ExpectedOperation("GET", "/task/recurring", "task recurring"),
    ExpectedOperation("GET", "/task/{id}/files", "task files"),
    ExpectedOperation("POST", "/task/{id}/comments/", "comment add"),
    ExpectedOperation("POST", "/task/{id}/comments/list", "comment list"),
    ExpectedOperation("POST", "/task/{id}/comments/{commentId}", "comment update"),
    ExpectedOperation("POST", "/task/{id}/datatags/", "datatag add"),
    ExpectedOperation("POST", "/task/{id}/datatags/{commentId}", "datatag to comment"),
    ExpectedOperation("POST", "/task/{id}/checklist", "checklist create"),
    ExpectedOperation("POST", "/task/{id}/checklist/list", "checklist get"),
    ExpectedOperation("GET", "/task/{id}/checklist/{itemId}", "checklist item get"),
    ExpectedOperation("POST", "/task/{id}/checklist/{itemId}", "checklist update"),
    ExpectedOperation("GET", "/comment/{id}", "comment get"),
    ExpectedOperation("DELETE", "/comment/{id}", "comment delete"),
    ExpectedOperation("POST", "/project/", "project create"),
    ExpectedOperation("GET", "/project/groups", "project groups"),
    ExpectedOperation("POST", "/project/list", "project list"),
    ExpectedOperation("GET", "/project/templates", "project templates"),
    ExpectedOperation("GET", "/project/{id}", "project get"),
    ExpectedOperation("POST", "/project/{id}", "project update"),
    ExpectedOperation("GET", "/project/{id}/files", "project files"),
    ExpectedOperation("GET", "/directory/groups", "directory groups"),
    ExpectedOperation("POST", "/directory/list", "directory list"),
    ExpectedOperation("GET", "/directory/{id}", "directory get"),
    ExpectedOperation("POST", "/directory/{id}/entry/", "directory entry add"),
    ExpectedOperation("POST", "/directory/{id}/entry/list", "directory entry list"),
    ExpectedOperation("GET", "/directory/{id}/entry/{key}", "directory entry get"),
    ExpectedOperation("POST", "/directory/{id}/entry/{key}", "directory entry update"),
    ExpectedOperation("DELETE", "/directory/{id}/entry/{key}", "directory entry delete"),
    ExpectedOperation("POST", "/directory/{id}/filters", "directory filters"),
    ExpectedOperation("GET", "/process/contact", "process contact list"),
    ExpectedOperation("GET", "/process/task", "process task list"),
    ExpectedOperation("GET", "/process/task/{id}/statuses", "statuses by process"),
    ExpectedOperation("POST", "/object/list", "object list"),
    ExpectedOperation("GET", "/object/{id}", "object get"),
    ExpectedOperation("GET", "/object/{id}/statuses", "statuses by object"),
    ExpectedOperation("GET", "/customfield/group/task", "custom field task group list"),
    ExpectedOperation("POST", "/customfield/group/task/", "custom field task group create"),
    ExpectedOperation("GET", "/customfield/task", "custom field task list"),
    ExpectedOperation("POST", "/customfield/task/", "custom field task create"),
    ExpectedOperation("GET", "/customfield/task/{id}", "custom field task get"),
    ExpectedOperation("GET", "/customfield/group/project", "custom field project group list"),
    ExpectedOperation("POST", "/customfield/group/project/", "custom field project group create"),
    ExpectedOperation("GET", "/customfield/project", "custom field project list"),
    ExpectedOperation("POST", "/customfield/project/", "custom field project create"),
    ExpectedOperation("GET", "/customfield/project/{id}", "custom field project get"),
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

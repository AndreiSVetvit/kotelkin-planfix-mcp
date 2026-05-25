from __future__ import annotations

import httpx

from planfix_mcp.client import (
    _build_auth_header,
    _extract_nested_id,
    _normalize_datatag_payload,
    _pop_first_int,
    _safe_json_dict,
    _with_silent_param,
)


def test_build_auth_header_adds_bearer_to_plain_token() -> None:
    assert _build_auth_header(" token ") == "Bearer token"


def test_build_auth_header_keeps_explicit_scheme() -> None:
    assert _build_auth_header("Bearer existing") == "Bearer existing"


def test_with_silent_param_adds_true_without_mutating_input() -> None:
    params = {"page": "1"}

    result = _with_silent_param(params, True)

    assert result == {"page": "1", "silent": "true"}
    assert params == {"page": "1"}


def test_with_silent_param_omits_false_and_none() -> None:
    params = {"page": "1"}

    assert _with_silent_param(params, False) is params
    assert _with_silent_param(params, None) is params
    assert _with_silent_param(None, False) is None


def test_extract_nested_id_handles_flat_nested_and_string_values() -> None:
    payload = {
        "processId": "12",
        "task": {"object": {"id": "34"}},
    }

    assert _extract_nested_id(payload, ("processId",)) == 12
    assert _extract_nested_id(payload, ("task.object.id",)) == 34
    assert _extract_nested_id(payload, ("missing.id",)) is None


def test_pop_first_int_removes_first_valid_key() -> None:
    payload = {"process_id": "12", "object_id": "34", "keep": "x"}

    result = _pop_first_int(payload, ("process_id", "object_id"))

    assert result == 12
    assert payload == {"object_id": "34", "keep": "x"}


def test_normalize_datatag_payload_accepts_short_form() -> None:
    result = _normalize_datatag_payload({"datatag_id": "10", "field_id": "20", "value": "abc"})

    assert result == {
        "dataTag": {"id": 10},
        "items": [{"customFieldData": [{"field": {"id": 20}, "value": "abc"}]}],
    }


def test_normalize_datatag_payload_keeps_official_shape() -> None:
    payload = {"dataTag": {"id": 10}, "items": [{"customFieldData": []}], "extra": "ignored"}

    assert _normalize_datatag_payload(payload) == {
        "dataTag": {"id": 10},
        "items": [{"customFieldData": []}],
    }


def test_safe_json_dict_wraps_non_dict_json_and_text() -> None:
    list_response = httpx.Response(200, json=[{"id": 1}])
    text_response = httpx.Response(200, text="not-json")
    empty_response = httpx.Response(204)

    assert _safe_json_dict(list_response) == {"data": [{"id": 1}]}
    assert _safe_json_dict(text_response) == {"raw": "not-json"}
    assert _safe_json_dict(empty_response) == {}

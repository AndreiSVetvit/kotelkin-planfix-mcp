from __future__ import annotations

import pytest

from scripts.live_qa_common import LiveQAFailure, env_flag, find_id, find_value, optional_int_env, server_env


def test_find_id_handles_nested_planfix_ids() -> None:
    payload = {"result": "success", "task": {"id": "123"}}

    assert find_id(payload) == 123


def test_find_id_ignores_zero_status_ids() -> None:
    payload = {"statuses": [{"id": 0}, {"id": 4}]}

    assert find_id(payload) == 4


def test_find_value_returns_directory_key() -> None:
    payload = {"result": "success", "entry": {"key": "abc"}}

    assert find_value(payload, ("key", "id")) == "abc"


def test_optional_int_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PLANFIX_LIVE_QA_COMMENT_TASK_ID", raising=False)
    assert optional_int_env("PLANFIX_LIVE_QA_COMMENT_TASK_ID") is None

    monkeypatch.setenv("PLANFIX_LIVE_QA_COMMENT_TASK_ID", "42")
    assert optional_int_env("PLANFIX_LIVE_QA_COMMENT_TASK_ID") == 42

    monkeypatch.setenv("PLANFIX_LIVE_QA_COMMENT_TASK_ID", "bad")
    with pytest.raises(LiveQAFailure):
        optional_int_env("PLANFIX_LIVE_QA_COMMENT_TASK_ID")


def test_env_flag(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PLANFIX_LIVE_QA_CONFIG_WRITES", "true")
    assert env_flag("PLANFIX_LIVE_QA_CONFIG_WRITES") is True

    monkeypatch.setenv("PLANFIX_LIVE_QA_CONFIG_WRITES", "0")
    assert env_flag("PLANFIX_LIVE_QA_CONFIG_WRITES") is False


def test_server_env_defaults_to_quiet_live_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("PLANFIX_MIN_REQUEST_INTERVAL_SEC", raising=False)

    env = server_env()

    assert env["LOG_LEVEL"] == "WARNING"
    assert env["PLANFIX_MIN_REQUEST_INTERVAL_SEC"] == "1.05"

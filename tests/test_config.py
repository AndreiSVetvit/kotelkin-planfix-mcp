from __future__ import annotations

import pytest

from planfix_mcp.config import Settings
from planfix_mcp.secrets_store import StoredSecrets


ENV_NAMES = (
    "PLANFIX_BASE_URL",
    "PLANFIX_TOKEN",
    "PLANFIX_TIMEOUT_SEC",
    "PLANFIX_RETRY_MAX",
    "PLANFIX_MIN_REQUEST_INTERVAL_SEC",
    "PLANFIX_STATUS_CHANGE_DELAY_SEC",
    "PLANFIX_SILENT_DEFAULT",
    "LOG_LEVEL",
)


def clear_planfix_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


def test_settings_from_env_normalizes_and_parses_values(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_planfix_env(monkeypatch)
    monkeypatch.setenv("PLANFIX_BASE_URL", "https://example.planfix.com/rest/")
    monkeypatch.setenv("PLANFIX_TOKEN", " token ")
    monkeypatch.setenv("PLANFIX_TIMEOUT_SEC", "7.5")
    monkeypatch.setenv("PLANFIX_RETRY_MAX", "3")
    monkeypatch.setenv("PLANFIX_MIN_REQUEST_INTERVAL_SEC", "0")
    monkeypatch.setenv("PLANFIX_STATUS_CHANGE_DELAY_SEC", "0.25")
    monkeypatch.setenv("PLANFIX_SILENT_DEFAULT", "yes")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    settings = Settings.from_env()

    assert settings.base_url == "https://example.planfix.com/rest"
    assert settings.token == "token"
    assert settings.timeout_sec == 7.5
    assert settings.retry_max == 3
    assert settings.min_request_interval_sec == 0
    assert settings.status_change_delay_sec == 0.25
    assert settings.silent_default is True
    assert settings.log_level == "DEBUG"


def test_settings_loads_missing_credentials_from_keyring(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_planfix_env(monkeypatch)
    monkeypatch.setattr(
        "planfix_mcp.config.load_secrets",
        lambda: StoredSecrets(base_url="https://stored.planfix.com/rest", token="stored-token"),
    )

    settings = Settings.from_env()

    assert settings.base_url == "https://stored.planfix.com/rest"
    assert settings.token == "stored-token"


def test_settings_reports_keyring_error_when_configuration_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_planfix_env(monkeypatch)

    def raise_keyring_error() -> StoredSecrets:
        raise RuntimeError("keyring unavailable")

    monkeypatch.setattr("planfix_mcp.config.load_secrets", raise_keyring_error)

    with pytest.raises(ValueError) as exc_info:
        Settings.from_env()

    message = str(exc_info.value)
    assert "PLANFIX_BASE_URL" in message
    assert "PLANFIX_TOKEN" in message
    assert "keyring unavailable" in message
    assert "planfix-mcp-secrets-init" in message


@pytest.mark.parametrize(
    ("env_name", "env_value", "expected_message"),
    (
        ("PLANFIX_TIMEOUT_SEC", "0", "PLANFIX_TIMEOUT_SEC must be > 0"),
        ("PLANFIX_RETRY_MAX", "-1", "PLANFIX_RETRY_MAX must be >= 0"),
        ("PLANFIX_MIN_REQUEST_INTERVAL_SEC", "-0.1", "PLANFIX_MIN_REQUEST_INTERVAL_SEC must be >= 0"),
        ("PLANFIX_STATUS_CHANGE_DELAY_SEC", "-0.1", "PLANFIX_STATUS_CHANGE_DELAY_SEC must be >= 0"),
        ("PLANFIX_SILENT_DEFAULT", "maybe", "PLANFIX_SILENT_DEFAULT must be boolean-like"),
    ),
)
def test_settings_rejects_invalid_values(
    monkeypatch: pytest.MonkeyPatch,
    env_name: str,
    env_value: str,
    expected_message: str,
) -> None:
    clear_planfix_env(monkeypatch)
    monkeypatch.setenv("PLANFIX_BASE_URL", "https://example.planfix.com/rest")
    monkeypatch.setenv("PLANFIX_TOKEN", "token")
    monkeypatch.setenv(env_name, env_value)

    with pytest.raises(ValueError, match=expected_message):
        Settings.from_env()

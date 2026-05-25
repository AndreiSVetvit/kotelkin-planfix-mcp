from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from planfix_mcp.secrets_store import load_secrets


@dataclass(frozen=True)
class Settings:
    base_url: str
    token: str
    timeout_sec: float = 20.0
    retry_max: int = 2
    min_request_interval_sec: float = 1.0
    status_change_delay_sec: float = 1.0
    silent_default: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        base_url = os.getenv("PLANFIX_BASE_URL", "").strip()
        token = os.getenv("PLANFIX_TOKEN", "").strip()
        keyring_error: str | None = None

        if not base_url or not token:
            try:
                stored = load_secrets()
                if not base_url and stored.base_url:
                    base_url = stored.base_url
                if not token and stored.token:
                    token = stored.token
            except RuntimeError as exc:
                keyring_error = str(exc)

        missing = []
        if not base_url:
            missing.append("PLANFIX_BASE_URL")
        if not token:
            missing.append("PLANFIX_TOKEN")
        if missing:
            message = f"Missing required configuration: {', '.join(missing)}"
            if keyring_error:
                message += f". Keyring error: {keyring_error}"
            message += ". Run `planfix-mcp-secrets-init` or set env variables."
            raise ValueError(message)

        timeout_sec = _read_float("PLANFIX_TIMEOUT_SEC", default=20.0)
        retry_max = _read_int("PLANFIX_RETRY_MAX", default=2)
        min_request_interval_sec = _read_float("PLANFIX_MIN_REQUEST_INTERVAL_SEC", default=1.0)
        status_change_delay_sec = _read_float("PLANFIX_STATUS_CHANGE_DELAY_SEC", default=1.0)
        silent_default = _read_bool("PLANFIX_SILENT_DEFAULT", default=False)
        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"

        if retry_max < 0:
            raise ValueError("PLANFIX_RETRY_MAX must be >= 0")
        if timeout_sec <= 0:
            raise ValueError("PLANFIX_TIMEOUT_SEC must be > 0")
        if min_request_interval_sec < 0:
            raise ValueError("PLANFIX_MIN_REQUEST_INTERVAL_SEC must be >= 0")
        if status_change_delay_sec < 0:
            raise ValueError("PLANFIX_STATUS_CHANGE_DELAY_SEC must be >= 0")

        return cls(
            base_url=base_url.rstrip("/"),
            token=token,
            timeout_sec=timeout_sec,
            retry_max=retry_max,
            min_request_interval_sec=min_request_interval_sec,
            status_change_delay_sec=status_change_delay_sec,
            silent_default=silent_default,
            log_level=log_level,
        )


def configure_logging(level: str) -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def _read_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got: {raw!r}") from exc


def _read_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got: {raw!r}") from exc


def _read_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be boolean-like (true/false, 1/0), got: {raw!r}")

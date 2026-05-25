from __future__ import annotations

from dataclasses import dataclass

SERVICE_NAME = "planfix-mcp"
KEY_BASE_URL = "planfix_base_url"
KEY_TOKEN = "planfix_token"


@dataclass(frozen=True)
class StoredSecrets:
    base_url: str | None
    token: str | None


def load_secrets() -> StoredSecrets:
    keyring, KeyringError = _import_keyring()
    try:
        base_url = keyring.get_password(SERVICE_NAME, KEY_BASE_URL)
        token = keyring.get_password(SERVICE_NAME, KEY_TOKEN)
    except KeyringError as exc:
        raise RuntimeError(f"Unable to read secrets from keyring: {exc}") from exc
    return StoredSecrets(
        base_url=(base_url or "").strip() or None,
        token=(token or "").strip() or None,
    )


def save_secrets(*, base_url: str, token: str) -> None:
    keyring, KeyringError = _import_keyring()
    try:
        keyring.set_password(SERVICE_NAME, KEY_BASE_URL, base_url.strip())
        keyring.set_password(SERVICE_NAME, KEY_TOKEN, token.strip())
    except KeyringError as exc:
        raise RuntimeError(f"Unable to save secrets to keyring: {exc}") from exc


def _import_keyring():
    try:
        import keyring  # type: ignore
        from keyring.errors import KeyringError  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Keyring support is not installed. Run `pip install -e .` to install dependencies."
        ) from exc
    return keyring, KeyringError

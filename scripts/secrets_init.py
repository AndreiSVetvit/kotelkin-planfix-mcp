from __future__ import annotations

import getpass
import os

from planfix_mcp.secrets_store import save_secrets


def main() -> None:
    print("Planfix MCP secrets setup")
    print("Enter values once. They will be saved in secure OS keyring.")

    default_url = os.getenv("PLANFIX_BASE_URL", "").strip()
    if default_url:
        prompt_url = f"PLANFIX_BASE_URL [{default_url}]: "
    else:
        prompt_url = "PLANFIX_BASE_URL (e.g. https://your-company.planfix.com/rest): "

    entered_url = input(prompt_url).strip()
    base_url = entered_url or default_url
    if not base_url:
        raise SystemExit("No PLANFIX_BASE_URL provided.")

    token = getpass.getpass("PLANFIX_TOKEN (hidden input): ").strip()
    if not token:
        raise SystemExit("No PLANFIX_TOKEN provided.")

    save_secrets(base_url=base_url, token=token)
    print("[PASS] Secrets saved. You can now run `planfix-mcp-server` without manual token export.")


if __name__ == "__main__":
    main()

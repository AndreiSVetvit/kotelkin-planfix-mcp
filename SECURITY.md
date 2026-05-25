# Security Policy

## Supported Versions

The project is currently in `0.1.0` public-candidate staging. Security fixes target the current default branch until the first public release is tagged.

## Reporting A Vulnerability

Do not open a public issue with tokens, account URLs that should remain private, screenshots containing credentials, or exploit details.

Use GitHub private vulnerability reporting when available. If it is not available, contact the maintainer privately before sharing sensitive details.

## Token Handling

Planfix tokens must not be committed to the repository.

Use one of these options:

- environment variables;
- your MCP client's local secret storage;
- OS keyring through `planfix-mcp-secrets-init`.

Avoid pasting tokens into:

- README files;
- issues and pull requests;
- screenshots;
- CI logs;
- MCP client configs committed to Git.

## Recommended Planfix Token Scope

Create a token with the smallest set of scopes needed for your workflow. For testing, use a disposable Planfix account or low-risk workspace.

Some tools write to Planfix. Review write tools before granting broad scopes.

## Local Checks

Before publishing or sharing a branch, run a secret scan:

```bash
rg --hidden --glob '!.git/**' --glob '!*.pyc' "PLANFIX_TOKEN|Authorization: Bearer|[0-9a-fA-F]{32}" .
```

Review matches manually. Placeholders are acceptable; real credentials are not.

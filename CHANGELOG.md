# Changelog

## Unreleased

- Prepared the clean MCP baseline for a public-facing repository:
  - renamed the Python distribution to `kotelkin-planfix-mcp`;
  - renamed the import package from `src` to `planfix_mcp`;
  - renamed the MCP server display name to `kotelkin-planfix-mcp`;
  - kept the CLI entrypoint `planfix-mcp-server`;
  - rewrote `README.md` for external users;
  - added MIT license;
  - added GitHub Actions smoke workflow.
- Ported MCP-only stability improvements from later internal history:
  - optional OS keyring credential setup;
  - status-change pacing;
  - status lookup fallback inputs;
  - DataTag payload normalization.
- Ported MCP-only extended REST coverage:
  - expanded local smoke coverage from 22 to 58 registered tools;
  - added project, directory, process/object, checklist extension, global comment, and custom-field tools;
  - added custom-field get fallback behavior;
  - added extended manual QA payload examples.
- Tightened release-readiness metadata and documentation:
  - refreshed docs alignment snapshot to Planfix swagger `1.5.7`;
  - updated package license metadata and project URLs;
  - removed legacy license classifier that conflicts with modern license expressions;
  - added build artifact ignores;
  - added wheel build to CI.
- Added product hardening tests and testability improvements:
  - added `pytest` dev extra;
  - added unit tests for configuration, client helpers, HTTP request handling, retry behavior, and MCP tool registration;
  - allowed `PlanfixClient` to accept an injected `httpx` transport for local tests without live Planfix calls;
  - added unit tests to CI.

## v0.1.0-mvp

- Implemented Planfix MCP server with 22 tools.
- Aligned endpoints with official Planfix REST docs.
- Added environment-based config and async HTTP client.
- Added preflight check script (`planfix-mcp-preflight`).
- Added local tool registration smoke check (`planfix-mcp-smoke`).
- Added swagger alignment check (`planfix-mcp-swagger-check`).
- Added Russian docstrings for all tool functions.
- Added optional `silent` support for write operations.
- Added manual QA guide (`MANUAL_QA_22_TOOLS.md`).

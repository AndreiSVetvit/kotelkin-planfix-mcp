# Roadmap

## Public repository readiness

- Rename package/import names for public use.
- Keep STDIO MCP startup simple and documented.
- Add license and CI smoke checks.
- Keep owner-local tracker, panel, bridge, and runbook layers out of this repository.
- Port MCP-only REST coverage improvements from later internal history.

## v0.1.0-mvp (done)

- MCP server on Python + FastMCP
- 22 Planfix tools (A-F groups)
- STDIO transport
- Basic retries and request pacing
- Optional `silent` support for write tools
- Preflight, smoke, and swagger alignment scripts
- Manual QA checklist for all tools

## v0.2.0-live-qa

- Run manual QA against real Planfix account
- Fix payload shape mismatches found in real workflows
- Add compatibility notes for account-specific process/status setups
- Improve error hints for common business validation failures

## v0.3.0-stabilization

- Add focused automated tests for unstable tools
- Add example payload templates for each tool
- Add release workflow and version bump discipline
- Improve docs for onboarding and troubleshooting

## v1.0.0

- Production hardening package
- Optional resources/prompts layer for MCP clients
- Extended observability options
- Full operational runbook

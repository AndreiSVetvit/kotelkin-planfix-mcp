# AGENTS.md

## Product rule

This repository is developed for a visible user outcome, not for tool-count growth.

Primary audience: an owner or manager of a small business (roughly up to 20 people), including a solo owner using Codex/AI and a small Planfix team.

Before a significant change:

1. Read the current open GitHub Issue whose title starts with `[NOW]`.
2. Read `README.md`, `ROADMAP.md`, and `CHANGELOG.md`.
3. State the owner-facing result and the demo/video scenario.
4. Check whether existing tools already solve the scenario.
5. Add the minimum missing capability only.

## GitHub-first execution

- One `[NOW]` Issue at a time.
- One product Issue = one focused branch/PR.
- Link the PR to the Issue.
- Do not implement `[NEXT]` or backlog Issues without an explicit decision.
- Do not expand scope because an adjacent technical improvement looks useful.
- In the PR report: user value, changed behavior, tests/CI, live QA, limitations.
- After opening/completing the PR, stop. Do not start the next release automatically.

## Compatibility

- Existing public MCP tool names are a user-facing contract.
- Do not rename/remove them unless the Issue explicitly approves a contract change.
- Prefer skills/workflows over new tools when existing tools already provide the required primitives.

## Product test

Before calling a change ready, answer:

> What can a small-business owner now ask AI to do, and what visible result can be shown on screen?

If there is no clear answer, the change is not a product priority by default.

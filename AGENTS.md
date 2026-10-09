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


## Commercial and plugin-first gate

Before proposing custom MCP development, answer:

1. Who is the small-business buyer/user and what pain is reduced?
2. What is the short demo/video case?
3. Can the official Planfix MCP already complete the same user goal?
4. Can existing tools plus a skill/plugin solve it without adding a new MCP tool?
5. What is the smallest proven gap, if any?

Do not add custom MCP behavior merely because it is technically possible.

For Planfix scenarios, test the same business instruction against the official Planfix MCP when practical. If the official MCP completes the scenario reliably, prefer building differentiated workflow/skill/plugin value or choose another case rather than duplicating capability.

Treat plugins as a primary product surface. A plugin may package a skill, MCP configuration, or both. Prefer a recognizable owner workflow over exposing more low-level tools.

## Video-candidate release gate

For a new product capability:

- build a candidate that the owner can personally rehearse;
- open a PR and report the result;
- do NOT merge or publish a release until the owner/product chat explicitly approves after the rehearsal;
- do not start the next product issue automatically.

The intended sequence is: user value -> candidate -> owner rehearsal -> video-ready -> explicit approval -> release -> video publication -> market feedback.

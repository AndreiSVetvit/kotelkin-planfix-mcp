# Public Release Checklist

This checklist is for the first public GitHub release of Kotelkin Planfix MCP.

## Current Status

Status: `PARTIAL`.

The MCP product is functional and has passed local and live checks. The repository should remain private until the maintainer completes the final name, README, release notes, and visibility review.

## What People Will See After Making The Repo Public

GitHub users will see:

- source code for the MCP server;
- README and Russian README;
- user guides in English and Russian;
- MIT license;
- CI workflow;
- issue templates;
- security policy;
- manual QA examples and release checklist;
- package metadata and CLI entry points.

They will not see Planfix tokens unless a token is accidentally committed later. Current secret scan must remain clean before publication.

## Release Candidate Evidence

Before opening the repository, run:

```bash
python -m pytest -q
python -m compileall planfix_mcp scripts tests
python scripts/smoke_tools.py
python scripts/check_swagger_alignment.py
python -m pip check
python -m pip wheel . --no-deps -w dist_tmp
```

For a test Planfix account:

```bash
planfix-mcp-preflight
planfix-mcp-live-qa-basic
planfix-mcp-live-qa-extended
```

Run a secret scan before changing visibility:

```bash
rg --hidden --glob '!.git/**' --glob '!*.pyc' "PLANFIX_TOKEN|Authorization: Bearer|[0-9a-fA-F]{32}" .
```

Review every match manually. Example tokens in `.env.example` are acceptable only if they are placeholders.

## Minimum Public v0.1.0 Bar

- Repository visibility is still private during review.
- Default branch is clean.
- CI passes on GitHub.
- README explains what the MCP server does.
- README links to Russian docs.
- No private/local operating layer is present: no panel, bridge, tracker, control-plane state, private Planfix task links, local runbooks, or SQL.
- No real token, account secret, private path, or personal workflow state is committed.
- MCP tool names are stable for `v0.1.0`.
- Live QA was run on a disposable or low-risk Planfix account.

## Recommended First Release Shape

- Tag: `v0.1.0`
- Release title: `Kotelkin Planfix MCP v0.1.0`
- Visibility: public only after final maintainer review.
- GitHub description: `MCP server for Planfix REST API over STDIO`
- Topics: `mcp`, `model-context-protocol`, `planfix`, `planfix-api`, `python`

## Do Not Do Before v0.1.0

- Do not import tracker, bridge, project panel, local control layer, local state, SQL, or private runbooks.
- Do not rename public tool names without a contract change proposal.
- Do not publish test account tokens or screenshots containing tokens.
- Do not claim production readiness; current classifier is Alpha.
- Do not add a cloud service or hosted API layer.

## Good Next Step

Open the repository locally in the morning, read `README.md`, `README_RU.md`, and both user guides as if you are a new user. If the first-run story is clear, the next maintainer action is to create a `v0.1.0` release branch or tag and then change GitHub visibility.

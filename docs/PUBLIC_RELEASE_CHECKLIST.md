# Public Release Checklist

This `v0.1.3` maintenance checklist builds on the published [`v0.1.2` baseline](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases/tag/v0.1.2). See [Releases](https://github.com/AndreiSVetvit/kotelkin-planfix-mcp/releases) for the current published tag. Maintainer review and green GitHub CI are required before merge and publication.

## Local checks

From a clean checkout with Python 3.12+, create an isolated environment and install the documented development extra:

```powershell
python -m venv .venv
$testPython = ".\.venv\Scripts\python.exe"
& $testPython -m pip install -e ".[dev]"
& $testPython -m pytest -q
& $testPython -m compileall planfix_mcp scripts tests
& $testPython scripts/smoke_tools.py
& $testPython scripts/check_swagger_alignment.py
& $testPython -m pip check
& $testPython -m pip wheel . --no-deps -w dist_tmp
git diff --check
```

On macOS/Linux:

```bash
python -m venv .venv
PYTHON=.venv/bin/python
"$PYTHON" -m pip install -e ".[dev]"
"$PYTHON" -m pytest -q
"$PYTHON" -m compileall planfix_mcp scripts tests
"$PYTHON" scripts/smoke_tools.py
"$PYTHON" scripts/check_swagger_alignment.py
"$PYTHON" -m pip check
"$PYTHON" -m pip wheel . --no-deps -w dist_tmp
git diff --check
```

Swagger check needs network access. Smoke must report 58 registered tools and does not call Planfix. With existing credentials, optional `planfix-mcp-preflight` is read-only by default (`GET /ping` and `GET /workspace/list`). Live QA is outside this docs-only `v0.1.3` scope; any later live run needs an explicitly selected disposable or low-risk test account because its runners write test data.

On Windows without activation, run optional preflight as ` .\.venv\Scripts\planfix-mcp-preflight.exe `; on macOS/Linux use `.venv/bin/planfix-mcp-preflight`.

## Before publishing

- [ ] English/Russian README, guides, roadmap, and this checklist agree about the `v0.1.2` baseline and current `v0.1.3` scope.
- [ ] Confirm no private/local operational files, account state, credentials, or real tokens are included; the project remains Alpha, not production-ready.
- [ ] Review all secret-scan matches; only placeholders may appear in tracked files:

```bash
rg --hidden --glob '!.git/**' --glob '!*.pyc' "PLANFIX_TOKEN|Authorization: Bearer|[0-9a-fA-F]{32}" .
```

- [ ] Maintainer review and GitHub CI green before merge; publish `v0.1.3` only after the approved merge.
- [ ] Keep the existing 58-tool contract; do not start a later `[NEXT]` issue automatically.

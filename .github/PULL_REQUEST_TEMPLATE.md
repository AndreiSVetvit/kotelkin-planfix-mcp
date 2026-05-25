## Summary

## Checks

- [ ] `python -m pytest -q`
- [ ] `python -m compileall planfix_mcp scripts tests`
- [ ] `python scripts/smoke_tools.py`
- [ ] `python scripts/check_swagger_alignment.py`
- [ ] `python -m pip check`
- [ ] `python -m pip wheel . --no-deps -w dist_tmp`
- [ ] Secret scan completed

## Contract Impact

- [ ] No public MCP tool names changed
- [ ] Documentation updated if behavior changed

## Security

- [ ] No Planfix tokens, private account data, or local credential configs committed

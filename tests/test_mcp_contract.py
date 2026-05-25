from __future__ import annotations

import asyncio

from scripts.smoke_tools import EXPECTED_TOOLS, _run_smoke


def test_expected_tool_contract_has_58_tools() -> None:
    assert len(EXPECTED_TOOLS) == 58


def test_registered_tools_match_contract() -> None:
    assert asyncio.run(_run_smoke()) == 0

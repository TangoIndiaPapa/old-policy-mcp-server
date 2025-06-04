# test_policy_opa_e2e.py
# File description: End-to-end tests for OPA policy enforcement in the MCP server.
# Author: AI Generated
# Date created: 2025-06-03
# Version number: 0.1
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from server import PolicyMCPServer

@pytest.mark.parametrize("action,context,expected", [
    ("where is waldo?", None, False),
    ("where is carmen sandiego?", None, True),
    ("need two sum problem solution for python", None, True),
    ("screw you", None, False),
])
def test_enforce_policy_opa_e2e(monkeypatch, action, context, expected):
    # Monkeypatch OPAClient to simulate OPA REST API responses for each policy
    from opa_integration import OPAClient
    async def fake_query(self, input_data, package=None, rule=None):
        if "waldo" in input_data.get("action", "").lower():
            return False
        if "screw you" in input_data.get("action", "").lower():
            return False
        return True
    monkeypatch.setattr(OPAClient, "query", fake_query)
    server = PolicyMCPServer()
    result = server.enforce_policy_opa(action, context)
    assert result["result"] == expected

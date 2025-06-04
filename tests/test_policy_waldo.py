# File name: test_policy_waldo.py
# File description: Policy compliance test for 'Waldo' scenario in MCP server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import pytest
from policy_mcp_server.server import PolicyMCPServer

server = PolicyMCPServer()

def test_enforce_policy_waldo():
    """
    Test that the 'Test' policy blocks the prompt 'Where is Waldo?'.
    """
    result = server.enforce_policy("Test", context={"prompt": "Where is Waldo?"})
    assert result["result"] != "compliant"
    assert "not permitted" in result.get("reason", "") or "not compliant" in result.get("reason", "")

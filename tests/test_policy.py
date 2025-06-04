# File name: test_policy.py
# File description: Policy compliance tests for MCP server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import pytest
from policy_mcp_server.server import PolicyMCPServer

def test_enforce_policy_always_compliant():
    server = PolicyMCPServer()
    result = server.enforce_policy("any input")
    assert result['result'] == 'compliant'

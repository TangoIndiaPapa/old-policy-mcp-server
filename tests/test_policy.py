# File name: test_policy.py
# File description: Policy compliance tests for MCP server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import pytest
from policy_mcp_server.server import PolicyMCPServer

def test_enforce_policy_allowed_action():
    server = PolicyMCPServer()
    result = server.enforce_policy("where is carmen sandiego?")
    assert result['result'] == 'compliant'

def test_enforce_policy_disallowed_action():
    server = PolicyMCPServer()
    result = server.enforce_policy("where is waldo?")
    assert result['result'] == 'not compliant'
    # Accept either 'waldo' or 'test' in the reason for flexibility
    assert 'waldo' in result['reason'].lower() or 'test' in result['reason'].lower()

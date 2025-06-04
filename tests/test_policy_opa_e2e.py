# test_policy_opa_e2e.py
# File description: End-to-end tests for OPA policy enforcement in the MCP server.
# Author: AI Generated
# Date created: 2025-06-03
# Version number: 0.1
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import importlib.util

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/policy_mcp_server'))
SERVER_PATH = os.path.join(SRC_PATH, 'server.py')
OPA_PATH = os.path.join(SRC_PATH, 'opa_integration.py')

spec_server = importlib.util.spec_from_file_location("server", SERVER_PATH)
server_mod = importlib.util.module_from_spec(spec_server)
spec_server.loader.exec_module(server_mod)
PolicyMCPServer = server_mod.PolicyMCPServer

spec_opa = importlib.util.spec_from_file_location("opa_integration", OPA_PATH)
opa_mod = importlib.util.module_from_spec(spec_opa)
spec_opa.loader.exec_module(opa_mod)
OPAClient = opa_mod.OPAClient

import pytest
from policy_mcp_server.server import PolicyMCPServer

@pytest.mark.parametrize("action,expected", [
    ("where is Waldo?", False), ## denied in policy.reg
    ("where is Carmen Sandiego?", True), ## ALLOWED in policy.reg
    ("need two sum problem solution for Python", False), ## denied in policy.reg
    ("useless", False), ## denied in policy.reg
    ("normal stuff not in policy", True), ## ALLOWED in policy.reg
])
def test_enforce_policy_opa_real_opa(action, expected):
    server = PolicyMCPServer()
    result = server.enforce_policy_opa(action)
    if result.get("result") == "error":
        pytest.exit(f"OPA server is not available or returned error: {result.get('reason')}", returncode=1)
    assert result["result"] == expected

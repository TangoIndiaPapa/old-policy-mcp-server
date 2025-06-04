# test_policy_opa_e2e.py
# File description: End-to-end tests for OPA policy enforcement in the MCP server.
# Author: AI Generated
# Date created: 2025-06-03
# Version number: 0.1
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import pytest
from .test_constants import SERVER_PATH, OPA_INTEGRATION_PATH, import_module_from_path

server_mod = import_module_from_path("server", SERVER_PATH)
PolicyMCPServer = server_mod.PolicyMCPServer
opa_mod = import_module_from_path("opa_integration", OPA_INTEGRATION_PATH)
OPAClient = opa_mod.OPAClient

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

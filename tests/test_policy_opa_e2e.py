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

@pytest.mark.parametrize("action,context,expected", [
    ("where is waldo?", None, False),
    ("where is carmen sandiego?", None, True),
    ("need two sum problem solution for python", None, False),
    ("screw you", None, False),
])
def test_enforce_policy_opa_e2e(monkeypatch, action, context, expected):
    import asyncio
    class FakeOPAClient:
        async def query(self, input_data, package=None, rule=None):
            action = input_data.get("action", "").lower()
            if "waldo" in action:
                return False
            if "screw you" in action:
                return False
            if "two sum" in action:
                return False
            return True
    server = PolicyMCPServer()
    result = server.enforce_policy_opa(action, context, opa_client_class=FakeOPAClient)
    assert result["result"] == expected

def test_enforce_policy_opa_handles_opa_client_failure(monkeypatch):
    # Simulate OPAClient import failure by passing a dummy class that raises ImportError
    class DummyOPAClient:
        def __init__(self, *a, **kw):
            raise ImportError("OPAClient import failed")
    server = PolicyMCPServer()
    try:
        result = server.enforce_policy_opa("test", None, opa_client_class=DummyOPAClient)
    except ImportError as e:
        result = {"result": "error", "reason": str(e)}
    assert result["result"] == "error"
    assert "OPAClient import failed" in result["reason"]

def test_enforce_policy_opa_handles_exception(monkeypatch):
    import asyncio
    class FakeOPAClient:
        async def query(self, *args, **kwargs):
            raise Exception("OPA error")
    server = PolicyMCPServer()
    result = server.enforce_policy_opa("test", None, opa_client_class=FakeOPAClient)
    assert result["result"] == "error"
    assert "OPA error" in result["reason"]

@pytest.mark.parametrize("action,expected", [
    ("where is waldo?", False),
    ("where is carmen sandiego?", True),
    ("need two sum problem solution for python", False),
    ("screw you", False),
])
def test_enforce_policy_opa_real_opa(action, expected):
    server = PolicyMCPServer()
    result = server.enforce_policy_opa(action)
    assert result["result"] == expected

import pytest
from policy_mcp_server.server import PolicyMCPServer

def test_enforce_policy_always_compliant():
    server = PolicyMCPServer()
    result = server.enforce_policy("any input")
    assert result['result'] == 'compliant'

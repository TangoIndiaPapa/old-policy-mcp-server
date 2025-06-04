import pytest
from policy_mcp_server.server import PolicyMCPServer

def test_waldo_blocked():
    server = PolicyMCPServer()
    result = server.enforce_policy("where is waldo?")
    assert result['result'] == 'not compliant'
    assert 'test' in result['reason'].lower()

def test_carmen_allowed():
    server = PolicyMCPServer()
    result = server.enforce_policy("where is carmen sandiego?")
    assert result['result'] == 'compliant'

import pytest
from policy_mcp_server.server import PolicyMCPServer
from policy_mcp_server.logging_utils import policy_eval_counter

def test_policy_eval_counter_increments(monkeypatch):
    # Patch the counter to a mock for test
    class MockCounter:
        def __init__(self):
            self.count = 0
        def add(self, n):
            self.count += n
    mock_counter = MockCounter()
    monkeypatch.setattr("policy_mcp_server.logging_utils.policy_eval_counter", mock_counter)
    server = PolicyMCPServer()
    server.enforce_policy("where is carmen sandiego?")
    assert mock_counter.count == 1
    server.enforce_policy("where is waldo?")
    assert mock_counter.count == 2

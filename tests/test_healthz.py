# File name: test_healthz.py
# File description: Basic health check test for MCP server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import pytest
from policy_mcp_server.server import PolicyMCPServer

server = PolicyMCPServer()


def test_greet():
    """
    Test the greet tool directly for correct output.
    """
    result = server.greet("World")
    assert result == "Hello, World!"


def test_mcp_instance():
    """
    Test that the MCP server instance is present and named correctly.

    Returns:
        None

    Error Handling:
        AssertionError if the MCP instance or name is incorrect.
    """
    assert hasattr(server, "mcp")
    assert server.mcp.name == "MyServer"

# File name: test_healthz.py
# File description: Basic health check test for MCP server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import importlib.util
from .test_constants import SERVER_PATH

spec_server = importlib.util.spec_from_file_location("server", SERVER_PATH)
server_mod = importlib.util.module_from_spec(spec_server)
spec_server.loader.exec_module(server_mod)
PolicyMCPServer = server_mod.PolicyMCPServer

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

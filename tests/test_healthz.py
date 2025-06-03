# File name: test_healthz.py
# File description: Basic health check test for MCP server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import sys
import os
import importlib.util

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_path)
logging_utils_spec = importlib.util.spec_from_file_location("logging_utils", os.path.join(src_path, "logging_utils.py"))
logging_utils = importlib.util.module_from_spec(logging_utils_spec)
logging_utils_spec.loader.exec_module(logging_utils)
log_around = logging_utils.log_around
logger = logging_utils.logger

spec = importlib.util.spec_from_file_location("server", os.path.join(os.path.dirname(__file__), '../src/server.py'))
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)

@log_around
class TestHealthz:
    """
    TestHealthz contains health check tests for the MCP server.

    Methods:
        test_greet(): Test greet tool output.
        test_mcp_instance(): Test MCP instance presence and name.
    """

    def __init__(self):
        self.server = server

    @log_around
    def test_greet(self):
        """
        Test the greet tool directly for correct output.

        Returns:
            None

        Error Handling:
            AssertionError if the greeting is incorrect.
        """
        result = self.server.greet("World")
        assert result == "Hello, World!"

    @log_around
    def test_mcp_instance(self):
        """
        Test that the MCP server instance is present and named correctly.

        Returns:
            None

        Error Handling:
            AssertionError if the MCP instance or name is incorrect.
        """
        assert hasattr(self.server, "mcp")
        assert self.server.mcp.name == "MyServer"

# File name: main.py
# File description: Entrypoint for running the FAST MCP server using the official SDK.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.
# MIT License

import sys
import importlib.util
import os
from policy_mcp_server.logging_utils import log_around, logger

src_path = os.path.abspath(os.path.dirname(__file__))

class MainRunner:
    """
    MainRunner is the entrypoint class for running the FAST MCP server using the official SDK.

    Methods:
        run(): Launches the MCP server subprocess.

    Error Handling:
        Any exception from subprocess call is propagated.
    """
    @log_around
    def run(self):
        """
        Entrypoint for running the FAST MCP server using the official SDK.

        Returns:
            None

        Error Handling:
            Any exception from subprocess call is propagated.
        """
        import subprocess
        sys.exit(subprocess.call([sys.executable, "-m", "fastmcp.server"]))

if __name__ == "__main__":
    MainRunner().run()

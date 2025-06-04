# File name: server.py
# File description: MCP server app factory.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
import threading
import time
import importlib.util
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import asyncio

try:
    from opa_integration import OPAClient
except ImportError:
    try:
        from src.opa_integration import OPAClient
    except ImportError:
        OPAClient = None  # Fallback for error reporting

from policy_mcp_server.settings import SettingsManager
from policy_mcp_server.logging_utils import log_around, logger, otel_trace


src_path = os.path.abspath(os.path.dirname(__file__))
logging_utils_spec = importlib.util.spec_from_file_location("logging_utils", os.path.join(src_path, "logging_utils.py"))
logging_utils = importlib.util.module_from_spec(logging_utils_spec)
logging_utils_spec.loader.exec_module(logging_utils)
log_around = logging_utils.log_around
logger = logging_utils.logger

# OTEL integration: initialize tracing and metrics at server startup
try:
    import importlib.util
    otel_setup_spec = importlib.util.spec_from_file_location("otel_setup", os.path.join(src_path, "otel_setup.py"))
    otel_setup = importlib.util.module_from_spec(otel_setup_spec)
    otel_setup_spec.loader.exec_module(otel_setup)
    otel_setup.OTELSetup()
    logger.info("OTEL tracing and metrics initialized at server startup.")
except Exception as e:
    logger.warning(f"OTEL integration failed or degraded gracefully: {e}")

@log_around
class PolicyMCPServer:
    """
    PolicyMCPServer implements the MCP server logic, including policy enforcement, greeting, and policy reloading.

    Methods:
        greet(name): Greet a user by name.
        enforce_policy(action, context): Check if an action is policy compliant.
        reload_policy(): Reload the policy from disk.
        reload_policy_tool(): MCP tool to reload policy.
        _auto_reload_policy(): Background thread for auto-reloading policy file.
    """
    def __init__(self):
        self.settings = SettingsManager().get_settings()
        try:
            from fastmcp import FastMCP
        except ImportError:
            raise ImportError("fastMCP SDK is not installed. Please install it from https://github.com/jlowin/fastmcp.")
        self.mcp = FastMCP(name="MyServer")
        self.mcp.tool()(log_around(self.greet))
        self.mcp.tool()(log_around(self.enforce_policy_opa))

    @log_around
    def greet(self, name: str) -> str:
        """
        Greet a user by name.
        Args:
            name (str): The name of the user to greet.
        Returns:
            str: Greeting message.
        """
        return f"Hello, {name}!"

    @log_around
    def reload_policy(self) -> None:
        """
        Deprecated: Policy reload is not needed. Policy is managed by OPA.
        """
        pass

    @log_around
    def reload_policy_tool(self) -> str:
        """
        Deprecated: Policy reload is not needed. Policy is managed by OPA.
        """
        return "Policy reload is not needed. Policy is managed by OPA."

    @otel_trace("enforce_policy")
    @log_around
    def enforce_policy(self, action: str, context: dict = None) -> dict:
        """
        Deprecated: Policy is now enforced by OPA. This method always returns compliant.
        """
        return {'result': 'compliant'}

    def _run_async(self, coro):
        """
        Helper to run an async coroutine from a synchronous context.
        This is required because fastmcp tools are synchronous, but OPAClient is async.
        If fastmcp adds async tool support, refactor to use async/await throughout.
        """
        try:
            loop = asyncio.get_running_loop()
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(coro)
        except Exception as e:
            logger.error(f"Error running async coroutine: {e}")
            raise

    @otel_trace("enforce_policy_opa")
    @log_around
    def enforce_policy_opa(self, action: str, context: dict = None, opa_client_class=None) -> dict:
        """
        Enforce policy using OPA via REST API. This is a synchronous wrapper for the async OPAClient query.
        This workaround is required because fastmcp tools are synchronous. If fastmcp supports async tools,
        refactor this method to be async and use await directly.
        Args:
            action (str): The action/tool name or user prompt to check.
            context (dict, optional): Additional context for the action (parameters, user info, etc).
            opa_client_class (type, optional): For testing, allow injection of a custom OPAClient class.
        Returns:
            dict: OPA decision result or error.
        """
        if opa_client_class is None:
            try:
                from policy_mcp_server.opa_integration import OPAClient as opa_client_class
            except ImportError:
                logger.error("OPAClient import failed in enforce_policy_opa.")
                return {"result": "error", "reason": "OPAClient import failed"}
        input_data = {"action": action}
        if context:
            input_data.update(context)
        # Only pass opa_url for real OPAClient, not for test fakes
        if opa_client_class.__name__ == "OPAClient":
            opa = opa_client_class(opa_url="http://opa-server:8181")
        else:
            opa = opa_client_class()
        try:
            result = self._run_async(opa.query(input_data))
            return {"result": result}
        except Exception as e:
            logger.error(f"OPA policy enforcement failed: {e}")
            return {"result": "error", "reason": str(e)}

    @log_around
    def _auto_reload_policy(self):
        """
        Deprecated: Policy reload is not needed. Policy is managed by OPA.
        """
        pass

if __name__ == "__main__":
    PolicyMCPServer().mcp.run()

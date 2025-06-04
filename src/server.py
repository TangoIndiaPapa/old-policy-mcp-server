# File name: server.py
# File description: MCP server app factory.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
import yaml
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

from settings import SettingsManager


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
        self.RUDE_WORDS = [w.strip() for w in getattr(self.settings, "RUDE_WORDS", "suck,idiot,stupid,hate you,shut up,dumb,moron,loser,fool,bastard,jerk,screw you,worthless,useless").split(",")]
        self.POLICY_PATH = os.path.abspath(getattr(self.settings, "POLICY_PATH", os.path.join(os.path.dirname(__file__), '../prompts/policy.prompt.yaml')))
        self.RELOAD_INTERVAL = int(getattr(self.settings, "POLICY_RELOAD_INTERVAL", 30))
        with open(self.POLICY_PATH, 'r') as f:
            self.POLICY_CACHE = yaml.safe_load(f)
        self._last_policy_mtime = os.path.getmtime(self.POLICY_PATH)
        threading.Thread(target=self._auto_reload_policy, daemon=True).start()
        try:
            from fastmcp import FastMCP
        except ImportError:
            raise ImportError("fastMCP SDK is not installed. Please install it from https://github.com/jlowin/fastmcp.")
        self.mcp = FastMCP(name="MyServer")
        self.mcp.tool()(log_around(self.greet))
        self.mcp.tool()(log_around(self.reload_policy_tool))
        self.mcp.tool()(log_around(self.enforce_policy))
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
        Reload the policy from disk into the global cache.
        Returns:
            None
        """
        with open(self.POLICY_PATH, 'r') as f:
            self.POLICY_CACHE = yaml.safe_load(f)

    @log_around
    def reload_policy_tool(self) -> str:
        """
        Reload the policy.prompt.yaml file from disk via MCP tool interface.
        Returns:
            str: Success or error message.
        """
        try:
            self.reload_policy()
            return "Policy reloaded successfully."
        except Exception as e:
            return f"Failed to reload policy: {e}"

    @log_around
    def enforce_policy(self, action: str, context: dict = None) -> dict:
        """
        Check if the requested action or prompt is compliant with the policy.prompt.yaml file.
        Args:
            action (str): The action/tool name or user prompt to check.
            context (dict, optional): Additional context for the action (parameters, user info, etc).
        Returns:
            dict: {'result': 'compliant'} if allowed, or {'result': 'not compliant', 'reason': ...}
        """
        policy = self.POLICY_CACHE
        policies = policy.get('policies', [])
        input_text = action.lower()
        if context and 'prompt' in context:
            input_text += ' ' + context['prompt'].lower()
        # Check for rude/abusive/disrespectful language
        for p in policies:
            desc = p.get('description', '').lower()
            if (
                'rude' in desc or 'abusive' in desc or 'disrespectful' in desc
            ) and any(word in input_text for word in self.RUDE_WORDS):
                return {'result': 'not compliant', 'reason': "Prompt is not compliant: violates policy 'Respectful Language'."}
            if 'must not ask where waldo' in desc and 'where is waldo' in input_text:
                return {'result': 'not compliant', 'reason': "Prompt is not compliant: violates policy 'Test'."}
        # Default allow: only block if a violation is detected
        return {'result': 'compliant'}

    @log_around
    def enforce_policy_tool(self, action: str, context: dict = None) -> dict:
        """
        MCP tool wrapper for enforce_policy. Returns a structured response for the MCP client.
        Args:
            action (str): The action/tool name or user prompt to check.
            context (dict, optional): Additional context for the action (parameters, user info, etc).
        Returns:
            dict: {'result': 'compliant'} if allowed, or {'result': 'not compliant', 'reason': ...}
        """
        result = self.enforce_policy(action, context)
        # Always return a structured response, so the client can continue and forward input if compliant
        return result

    @log_around
    def enforce_policy_opa(self, action: str, context: dict = None) -> dict:
        """
        Enforce policy using OPA via REST API. This is a synchronous wrapper for the async OPAClient query.
        Args:
            action (str): The action/tool name or user prompt to check.
            context (dict, optional): Additional context for the action (parameters, user info, etc).
        Returns:
            dict: OPA decision result or error.
        """
        if OPAClient is None:
            return {"result": "error", "reason": "OPAClient import failed"}
        input_data = {"action": action}
        if context:
            input_data.update(context)
        opa = OPAClient()
        try:
            try:
                loop = asyncio.get_running_loop()
                # If we're already in an event loop, schedule the coroutine and wait for it
                import nest_asyncio
                nest_asyncio.apply()
                coro = opa.query(input_data)
                result = loop.run_until_complete(coro)
            except RuntimeError:
                # No event loop running, safe to use run_until_complete
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(opa.query(input_data))
            return {"result": result}
        except Exception as e:
            return {"result": "error", "reason": str(e)}

    @log_around
    def _auto_reload_policy(self):
        """
        Background thread function to automatically reload the policy file if it changes.
        Returns:
            None
        """
        while True:
            try:
                mtime = os.path.getmtime(self.POLICY_PATH)
                if mtime != self._last_policy_mtime:
                    with open(self.POLICY_PATH, 'r') as f:
                        self.POLICY_CACHE = yaml.safe_load(f)
                    self._last_policy_mtime = mtime
            except Exception:
                pass
            time.sleep(self.RELOAD_INTERVAL)

if __name__ == "__main__":
    PolicyMCPServer().mcp.run()

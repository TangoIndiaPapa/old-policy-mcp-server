# opa_integration.py
# File description: OPA (Open Policy Agent) integration for policy enforcement in the MCP server.
# Author: AI Generated
# Date created: 2025-06-03
# Version number: 0.2
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
import requests
import asyncio
from dotenv import load_dotenv

# Try to import a configuration manager if available
try:
    from policy_mcp_server.settings import SettingsManager
except ImportError:
    SettingsManager = None

# Import log_around for logging
import importlib.util
import os as _os
src_path = _os.path.abspath(_os.path.dirname(__file__))
logging_utils_spec = importlib.util.spec_from_file_location("logging_utils", os.path.join(src_path, "logging_utils.py"))
logging_utils = importlib.util.module_from_spec(logging_utils_spec)
logging_utils_spec.loader.exec_module(logging_utils)
log_around = logging_utils.log_around
logger = logging_utils.logger

# Load .env if present
load_dotenv()

@log_around
class OPAClient:
    """
    OPAClient provides async, non-blocking access to an OPA server via the REST API.
    All configuration is loaded from environment variables, .env, or config manager.
    """
    def __init__(self, opa_url=None, policy_package=None, policy_rule=None):
        # Priority: explicit arg > config manager > env > .env > default
        settings = None
        if SettingsManager:
            try:
                settings = SettingsManager().get_settings()
            except Exception:
                settings = None
        self.opa_url = (
            opa_url or
            (settings.OPA_URL if settings and hasattr(settings, "OPA_URL") else None) or
            os.getenv("OPA_URL") or
            "http://localhost:8181"
        )
        self.policy_package = (
            policy_package or
            (settings.OPA_POLICY_PACKAGE if settings and hasattr(settings, "OPA_POLICY_PACKAGE") else None) or
            os.getenv("OPA_POLICY_PACKAGE") or
            "policy"
        )
        self.policy_rule = (
            policy_rule or
            (settings.OPA_POLICY_RULE if settings and hasattr(settings, "OPA_POLICY_RULE") else None) or
            os.getenv("OPA_POLICY_RULE") or
            "allow"
        )

    @log_around
    async def query(self, input_data: dict, package: str = None, rule: str = None):
        """
        Query the OPA REST API asynchronously for a policy decision.
        Args:
            input_data (dict): The input data for the policy.
            package (str): The OPA policy package to query.
            rule (str): The OPA rule to query.
        Returns:
            dict: The OPA decision result.
        Raises:
            requests.exceptions.RequestException: For network errors, timeouts, etc.
        """
        url = f"{self.opa_url}/v1/data/{package or self.policy_package}/{rule or self.policy_rule}"
        loop = asyncio.get_event_loop()
        def _post():
            try:
                resp = requests.post(url, json={"input": input_data}, timeout=5)
                resp.raise_for_status()
                return resp.json().get("result")
            except requests.exceptions.Timeout:
                logger.error("OPA request timed out.")
                raise
            except requests.exceptions.ConnectionError:
                logger.error("OPA connection error.")
                raise
            except requests.exceptions.RequestException as e:
                logger.error(f"OPA request failed: {e}")
                raise
        return await loop.run_in_executor(None, _post)

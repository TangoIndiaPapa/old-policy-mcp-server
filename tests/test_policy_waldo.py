# File name: test_policy_waldo.py
# File description: Policy compliance test for 'Waldo' scenario in MCP server.
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

@log_around
class TestPolicyWaldo:
    """
    TestPolicyWaldo contains a test for the 'Waldo' policy scenario in the MCP server.

    Methods:
        test_enforce_policy_waldo(): Test that the 'Test' policy blocks the prompt 'Where is Waldo?'.
    """
    def __init__(self):
        self.server = None
        spec = importlib.util.spec_from_file_location("server", os.path.join(os.path.dirname(__file__), '../src/server.py'))
        self.server = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.server)

    @log_around
    def test_enforce_policy_waldo(self):
        """
        Test that the 'Test' policy blocks the prompt 'Where is Waldo?'.
        Returns:
            None
        """
        result = self.server.enforce_policy("Test", context={"prompt": "Where is Waldo?"})
        assert result != "compliant"
        assert "not permitted" in result or "not compliant" in result

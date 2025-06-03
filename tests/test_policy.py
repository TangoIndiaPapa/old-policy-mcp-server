# File name: test_policy.py
# File description: Policy compliance tests for MCP server.
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
class TestPolicy:
    """
    TestPolicy contains tests for policy compliance logic in the MCP server.

    Methods:
        test_enforce_policy_allowed_action(): Test allowed action compliance.
        test_enforce_policy_disallowed_action(): Test disallowed action non-compliance.
    """
    def __init__(self):
        self.server = server

    @log_around
    def test_enforce_policy_allowed_action(self):
        """
        Test that an allowed action by policy name is compliant.

        Returns:
            None

        Error Handling:
            AssertionError if the result is not 'compliant'.
        """
        result = self.server.enforce_policy("Code of Conduct")
        assert result == "compliant"

    @log_around
    def test_enforce_policy_disallowed_action(self):
        """
        Test that a disallowed action is not compliant.

        Returns:
            None

        Error Handling:
            AssertionError if the result is 'compliant' or does not contain 'not permitted'.
        """
        result = self.server.enforce_policy("Unlisted Action")
        assert result != "compliant"
        assert "not permitted" in result

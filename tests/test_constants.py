# File name: test_constants.py
# File description: Shared constants for test imports and paths in the policy-mcp-server test suite.
# Author: AI Generated
# Date created: 2025-06-04
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
import importlib.util

def import_module_from_path(module_name, file_path):
    """
    Dynamically import a module from a given file path.
    Args:
        module_name (str): Name to assign to the module.
        file_path (str): Absolute path to the .py file.
    Returns:
        module: The imported module object.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

SERVER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/server.py'))
LOGGING_UTILS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/logging_utils.py'))
OPA_INTEGRATION_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/opa_integration.py'))
OTEL_SETUP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/otel_setup.py'))

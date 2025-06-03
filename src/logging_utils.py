# File name: logging_utils.py
# File description: Centralized enterprise logging utilities and decorators for the Policy MCP Server.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import logging
import functools
import sys
import os

# Enterprise-level logging setup
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(process)d | %(thread)d | "
    "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
)

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, 'policy-mcp-server.log')

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stderr),  # Send logs to stderr, not stdout
    ]
)

logger = logging.getLogger("policy-mcp-server")

class LoggingUtils:
    """
    LoggingUtils provides enterprise-level logging setup and a log_around decorator for entry/exit logging.

    Static Methods:
        log_around(func): Decorator for logging entry and exit of functions and methods.
    """
    @staticmethod
    def log_around(func):
        """
        Decorator to log entry and exit of a function or method for auditability and debugging.

        Args:
            func (Callable): The function or method to wrap.

        Returns:
            Callable: The wrapped function with logging on entry and exit.

        Error Handling:
            Any exception raised by the wrapped function is propagated as normal. Logging is performed before and after the function call.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"ENTER: {func.__qualname__}")
            result = func(*args, **kwargs)
            logger.info(f"EXIT: {func.__qualname__}")
            return result
        return wrapper

log_around = LoggingUtils.log_around

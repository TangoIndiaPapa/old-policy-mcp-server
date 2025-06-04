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
from logging.handlers import RotatingFileHandler

# Enterprise-level logging setup
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(process)d | %(thread)d | "
    "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
)

LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, 'policy-mcp-server.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# Use RotatingFileHandler for log rotation (10 MB per file, keep 5 backups)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[file_handler, stream_handler]
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
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"ENTER: {func.__qualname__} | args={args} | kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"EXIT: {func.__qualname__} | result={result}")
            return result
        return wrapper

log_around = LoggingUtils.log_around

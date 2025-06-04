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

# OTEL imports
try:
    from opentelemetry import trace, metrics
    tracer = trace.get_tracer(__name__)
    meter = metrics.get_meter(__name__)
    policy_eval_counter = meter.create_counter(
        name="policy_evaluations",
        description="Number of policy evaluations",
        unit="1"
    )
except ImportError:
    tracer = None
    policy_eval_counter = None

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
        Decorator to log entry and exit of a function or method for auditability, debugging, and OTEL tracing.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"ENTER: {func.__qualname__} | args={args} | kwargs={kwargs}")
            if tracer:
                with tracer.start_as_current_span(func.__qualname__):
                    result = func(*args, **kwargs)
                    logger.debug(f"TRACE: {func.__qualname__} | result={result}")
            else:
                result = func(*args, **kwargs)
                logger.debug(f"NO TRACE FOUND: {func.__qualname__} | result={result}")

            logger.info(f"EXIT: {func.__qualname__} | result={result}")
            return result
        return wrapper

    @staticmethod
    def otel_trace(span_name=None):
        """
        Explicit OTEL tracing decorator for finer-grained control over tracing.
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                with tracer.start_as_current_span(span_name or func.__name__) as span:
                    # Add custom attributes if available in kwargs
                    context = kwargs.get('context', {})
                    if isinstance(context, dict):
                        for k, v in context.items():
                            span.set_attribute(f"context.{k}", v)
                    result = func(*args, **kwargs)
                    # Add policy decision to span if present
                    if isinstance(result, dict) and 'result' in result:
                        span.set_attribute("policy.decision", str(result['result']))
                    # Increment custom metric
                    policy_eval_counter.add(1)
                    return result
            return wrapper
        return decorator

log_around = LoggingUtils.log_around
otel_trace = LoggingUtils.otel_trace

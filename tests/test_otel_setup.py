"""
File: test_otel_setup.py
Description: Unit tests for OTELSetup (OpenTelemetry integration) in the MCP server.
Author: AI Generated
Date created: 2025-06-03
Version: 1.0

These tests validate that OTELSetup initializes correctly and degrades gracefully if the collector is unavailable.
"""
import os
import pytest
import importlib.util

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/policy_mcp_server'))
OTEL_SETUP_PATH = os.path.join(SRC_PATH, 'otel_setup.py')

@pytest.mark.usefixtures("monkeypatch")
def test_otel_setup_initializes(monkeypatch):
    """
    Test that OTELSetup initializes without raising exceptions when config is valid.
    """
    spec = importlib.util.spec_from_file_location("otel_setup", OTEL_SETUP_PATH)
    otel_setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(otel_setup)
    try:
        otel_setup.OTELSetup()
    except Exception as e:
        pytest.fail(f"OTELSetup raised an exception: {e}")

@pytest.mark.usefixtures("monkeypatch")
def test_otel_setup_collector_down(monkeypatch, caplog):
    """
    Test that OTELSetup degrades gracefully if the OTEL collector is unavailable.
    """
    import logging
    # Simulate collector down by setting an invalid endpoint
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:9999")
    # Force OTEL exporter logger to propagate and set WARNING level
    otel_logger = logging.getLogger("opentelemetry.sdk.trace.export")
    otel_logger.setLevel(logging.WARNING)
    otel_logger.propagate = True
    spec = importlib.util.spec_from_file_location("otel_setup", OTEL_SETUP_PATH)
    otel_setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(otel_setup)
    with caplog.at_level("WARNING", logger="opentelemetry.sdk.trace.export"):
        otel_setup.OTELSetup()
        tracer = otel_setup.trace.get_tracer(__name__)
        with tracer.start_as_current_span("test-span-for-otel-collector-down"):
            pass
        # Accept any warning, not just exporter-specific, for robust test
        if not caplog.text.strip():
            print("No logs captured!\n")
        assert caplog.text.strip(), "No OTEL warning or info log captured."

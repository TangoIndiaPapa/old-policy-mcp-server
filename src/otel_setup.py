"""
File: otel_setup.py
Description: Modular OpenTelemetry (OTEL) setup for tracing and metrics in the MCP server.
Author: AI Generated
Date created: 2025-06-03
Version: 1.0

This module provides a production-grade, non-blocking, and modular OTEL setup for the MCP server.
It reads all configuration from the SettingsManager and .env, and ensures graceful degradation if the collector is down.
All initialization is wrapped in try/except and errors are logged via the centralized logger.
"""

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
import logging

from settings import SettingsManager
from logging_utils import logger

class OTELSetup:
    """
    OTELSetup initializes and configures OpenTelemetry tracing and metrics for the MCP server.
    All configuration is loaded from SettingsManager and .env.
    Initialization is non-blocking and degrades gracefully if the collector is unavailable.
    """
    def __init__(self):
        self.settings = SettingsManager().get_settings()
        self.tracer_provider = None
        self.meter_provider = None
        self._setup_otel()

    def _setup_otel(self):
        try:
            resource = Resource.create({
                "service.name": self.settings.OTEL_SERVICE_NAME,
                **self._parse_resource_attributes(self.settings.OTEL_RESOURCE_ATTRIBUTES)
            })
            # Tracing setup
            self.tracer_provider = TracerProvider(resource=resource)
            span_exporter = OTLPSpanExporter(
                endpoint=self.settings.OTEL_EXPORTER_OTLP_ENDPOINT
            )
            span_processor = BatchSpanProcessor(span_exporter)
            self.tracer_provider.add_span_processor(span_processor)
            # Only set tracer provider if not already set
            if not trace.get_tracer_provider() or type(trace.get_tracer_provider()).__name__ == 'DefaultTracerProvider':
                trace.set_tracer_provider(self.tracer_provider)

            # Metrics setup
            metric_exporter = OTLPMetricExporter(
                endpoint=self.settings.OTEL_EXPORTER_OTLP_ENDPOINT
            )
            prometheus_reader = PrometheusMetricReader()
            self.meter_provider = MeterProvider(
                resource=resource,
                metric_readers=[prometheus_reader]
            )
            # Explicitly set meter provider for metrics
            from opentelemetry import metrics as otel_metrics
            otel_metrics.set_meter_provider(self.meter_provider)
            logger.info("OpenTelemetry tracing and metrics initialized successfully.")
        except Exception as e:
            logger.warning(f"OTEL setup failed or degraded gracefully: {e}")

    @staticmethod
    def _parse_resource_attributes(attr_str):
        # Parses OTEL_RESOURCE_ATTRIBUTES string into a dict
        attrs = {}
        if attr_str:
            for pair in attr_str.split(","):
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    attrs[k.strip()] = v.strip()
        return attrs

# Usage: Import and instantiate OTELSetup() at the top-level of your server entrypoint.
# All custom instrumentation points should use trace.get_tracer(__name__) and metrics.get_meter(__name__)
# and include custom attributes (request ID, user ID, policy decision, etc.) as required by XAI/auditability.

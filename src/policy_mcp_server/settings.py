# File name: settings.py
# File description: Configuration management using Pydantic BaseSettings.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
from pydantic_settings import BaseSettings
from policy_mcp_server.logging_utils import log_around, logger

@log_around
class SettingsManager:
    """
    SettingsManager provides configuration for the MCP server using environment variables and Pydantic BaseSettings.

    Methods:
        get_settings(): Returns a Settings object with all configuration values.

    Error Handling:
        Any exception from Settings instantiation is propagated.
    """
    class Settings(BaseSettings):
        LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", 8000))
        MCP_SERVER_HOST: str = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        OTEL_SERVICE_NAME: str = os.getenv("OTEL_SERVICE_NAME", "policy-mcp-server")
        OTEL_EXPORTER_OTLP_ENDPOINT: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
        OTEL_EXPORTER_OTLP_PROTOCOL: str = os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
        OTEL_TRACES_SAMPLER: str = os.getenv("OTEL_TRACES_SAMPLER", "parentbased_always_on")
        OTEL_TRACES_SAMPLER_ARG: float = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", 1.0))
        OTEL_METRICS_EXPORT_INTERVAL: int = int(os.getenv("OTEL_METRICS_EXPORT_INTERVAL", 60000))
        OTEL_RESOURCE_ATTRIBUTES: str = os.getenv("OTEL_RESOURCE_ATTRIBUTES", "deployment.environment=dev")
        # OPA (Open Policy Agent) configuration
        OPA_URL: str = os.getenv("OPA_URL", "http://localhost:8181")
        OPA_POLICY_PACKAGE: str = os.getenv("OPA_POLICY_PACKAGE", "policy")
        OPA_POLICY_RULE: str = os.getenv("OPA_POLICY_RULE", "allow")

        # Pydantic v2+ config style
        model_config = {
            "env_file": ".env"
        }

    @log_around
    def get_settings(self):
        """
        Instantiate and return a Settings object.

        Returns:
            Settings: The configuration object for the MCP server.
        """
        return self.Settings()

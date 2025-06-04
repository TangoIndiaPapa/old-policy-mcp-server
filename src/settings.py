# File name: settings.py
# File description: Configuration management using Pydantic BaseSettings.
# Author: AI Generated
# Date created: 2025-06-02
# Last modified date: 2025-06-02
# Version number: 1.0
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import os
from pydantic_settings import BaseSettings
import importlib.util

src_path = os.path.abspath(os.path.dirname(__file__))
logging_utils_spec = importlib.util.spec_from_file_location("logging_utils", os.path.join(src_path, "logging_utils.py"))
logging_utils = importlib.util.module_from_spec(logging_utils_spec)
logging_utils_spec.loader.exec_module(logging_utils)
log_around = logging_utils.log_around
logger = logging_utils.logger

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
        POLICY_PATH: str = os.getenv("POLICY_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), '../prompts/policy.prompt.yaml')))
        RUDE_WORDS: str = os.getenv("RUDE_WORDS", "suck,idiot,stupid,hate you,shut up,dumb,moron,loser,fool,bastard,jerk,screw you,worthless,useless")
        POLICY_RELOAD_INTERVAL: int = int(os.getenv("POLICY_RELOAD_INTERVAL", 30))
        OTEL_SERVICE_NAME: str = os.getenv("OTEL_SERVICE_NAME", "policy-mcp-server")
        OTEL_EXPORTER_OTLP_ENDPOINT: str = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
        OTEL_EXPORTER_OTLP_PROTOCOL: str = os.getenv("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
        OTEL_TRACES_SAMPLER: str = os.getenv("OTEL_TRACES_SAMPLER", "parentbased_always_on")
        OTEL_TRACES_SAMPLER_ARG: float = float(os.getenv("OTEL_TRACES_SAMPLER_ARG", 1.0))
        OTEL_METRICS_EXPORT_INTERVAL: int = int(os.getenv("OTEL_METRICS_EXPORT_INTERVAL", 60000))
        OTEL_RESOURCE_ATTRIBUTES: str = os.getenv("OTEL_RESOURCE_ATTRIBUTES", "deployment.environment=dev")

        class Config:
            env_file = '.env'

    @log_around
    def get_settings(self):
        """
        Instantiate and return a Settings object.

        Returns:
            Settings: The configuration object for the MCP server.
        """
        return self.Settings()

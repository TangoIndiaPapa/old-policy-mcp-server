#!/bin/bash
cd /workspaces/mcp-servers/policy-mcp-server
rm -f src/otel_setup.py
rm -f tests/test_otel_setup.py
rm -f docker-compose-otel.yaml
rm -f config/otel-collector-config.yaml
rm -f config/prometheus.yml

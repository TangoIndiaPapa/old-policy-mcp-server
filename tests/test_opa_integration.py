# test_opa_integration.py
# File description: Unit tests for OPAClient integration with OPA REST API.
# Author: AI Generated
# Date created: 2025-06-03
# Version number: 0.1
# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.

import pytest
import requests
from .test_constants import OPA_INTEGRATION_PATH, import_module_from_path

try:
    opa_integration = import_module_from_path("opa_integration", OPA_INTEGRATION_PATH)
    OPAClient = opa_integration.OPAClient
except Exception as e:
    pytest.skip(f"OPAClient import failed: {e}")

@pytest.mark.asyncio
async def test_opa_query_allows(monkeypatch):
    # Mock requests.post to simulate OPA allow response
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"result": True}
    def mock_post(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr("requests.post", mock_post)
    opa = OPAClient()
    result = await opa.query({"foo": "bar"})
    assert result is True

@pytest.mark.asyncio
async def test_opa_query_denies(monkeypatch):
    # Mock requests.post to simulate OPA deny response
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"result": False}
    def mock_post(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr("requests.post", mock_post)
    opa = OPAClient()
    result = await opa.query({"foo": "bar"})
    assert result is False

@pytest.mark.asyncio
async def test_opa_query_custom_package_rule(monkeypatch):
    # Mock requests.post to simulate OPA custom package/rule response
    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return {"result": {"decision": "custom"}}
    def mock_post(*args, **kwargs):
        return MockResponse()
    monkeypatch.setattr("requests.post", mock_post)
    opa = OPAClient()
    result = await opa.query({"foo": "bar"}, package="custompkg", rule="customrule")
    assert result == {"decision": "custom"}

@pytest.mark.asyncio
async def test_opa_query_error(monkeypatch):
    # Mock requests.post to raise an exception
    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException("OPA server error")
    monkeypatch.setattr("requests.post", mock_post)
    opa = OPAClient()
    with pytest.raises(requests.exceptions.RequestException):
        await opa.query({"foo": "bar"})

"""Tests for OpenAPI parser."""
import pytest
from pathlib import Path
from api_cataloger.parsers.openapi_parser import OpenAPIParser
from api_cataloger.models import EndpointStatus


@pytest.fixture
def openapi_parser():
    return OpenAPIParser()


@pytest.fixture
def sample_openapi_file(tmp_path):
    """Create a sample OpenAPI file."""
    openapi_content = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
  description: A test API
paths:
  /test:
    get:
      summary: Test endpoint
      description: A test endpoint
      tags:
        - testing
      responses:
        '200':
          description: Success
  /deprecated:
    post:
      summary: Deprecated endpoint
      deprecated: true
      responses:
        '200':
          description: Success
"""
    file_path = tmp_path / "openapi.yaml"
    file_path.write_text(openapi_content)
    return file_path


def test_can_parse_yaml(openapi_parser, sample_openapi_file):
    """Test that parser can identify OpenAPI YAML files."""
    assert openapi_parser.can_parse(sample_openapi_file) is True


def test_can_parse_non_openapi(openapi_parser, tmp_path):
    """Test that parser rejects non-OpenAPI files."""
    non_openapi = tmp_path / "not-openapi.yaml"
    non_openapi.write_text("just: some yaml\ndata: here")
    assert openapi_parser.can_parse(non_openapi) is False


def test_parse_openapi_file(openapi_parser, sample_openapi_file):
    """Test parsing a complete OpenAPI file."""
    entry = openapi_parser.parse(sample_openapi_file)
    
    assert entry is not None
    assert entry.metadata.title == "Test API"
    assert entry.metadata.version == "1.0.0"
    assert entry.metadata.description == "A test API"
    assert len(entry.endpoints) == 2


def test_parse_endpoints(openapi_parser, sample_openapi_file):
    """Test endpoint extraction."""
    entry = openapi_parser.parse(sample_openapi_file)
    
    # Check first endpoint
    get_endpoint = next(ep for ep in entry.endpoints if ep.method == "GET")
    assert get_endpoint.path == "/test"
    assert get_endpoint.summary == "Test endpoint"
    assert get_endpoint.description == "A test endpoint"
    assert "testing" in get_endpoint.tags
    assert get_endpoint.status == EndpointStatus.ACTIVE


def test_deprecated_endpoint(openapi_parser, sample_openapi_file):
    """Test that deprecated endpoints are marked correctly."""
    entry = openapi_parser.parse(sample_openapi_file)
    
    deprecated_endpoint = next(ep for ep in entry.endpoints if ep.path == "/deprecated")
    assert deprecated_endpoint.status == EndpointStatus.DEPRECATED

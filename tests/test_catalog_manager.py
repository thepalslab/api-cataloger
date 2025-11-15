"""Tests for catalog manager."""

import pytest
from pathlib import Path
from api_cataloger.catalog_manager import CatalogManager


@pytest.fixture
def catalog_manager():
    return CatalogManager()


@pytest.fixture
def sample_openapi(tmp_path):
    """Create a sample OpenAPI file."""
    content = """
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /test:
    get:
      summary: Test
      responses:
        '200':
          description: OK
"""
    file_path = tmp_path / "openapi.yaml"
    file_path.write_text(content)
    return file_path


def test_parse_file(catalog_manager, sample_openapi):
    """Test parsing a single file."""
    entry = catalog_manager.parse_file(sample_openapi, team_owner="Test Team")

    assert entry is not None
    assert entry.metadata.team_owner == "Test Team"
    assert len(entry.endpoints) == 1


def test_scan_directory(catalog_manager, tmp_path):
    """Test scanning a directory."""
    # Create multiple API files
    (tmp_path / "api1.yaml").write_text(
        """
openapi: 3.0.0
info:
  title: API 1
  version: 1.0.0
paths:
  /api1:
    get:
      responses:
        '200':
          description: OK
"""
    )

    (tmp_path / "api2.yaml").write_text(
        """
openapi: 3.0.0
info:
  title: API 2
  version: 1.0.0
paths:
  /api2:
    post:
      responses:
        '201':
          description: Created
"""
    )

    catalog = catalog_manager.scan_directory(tmp_path)

    assert len(catalog.entries) == 2
    total_endpoints = sum(len(entry.endpoints) for entry in catalog.entries)
    assert total_endpoints == 2


def test_search_catalog(catalog_manager, sample_openapi):
    """Test searching the catalog."""
    catalog_manager.parse_file(sample_openapi)

    results = catalog_manager.search("test")
    assert len(results) > 0

    results = catalog_manager.search("nonexistent")
    assert len(results) == 0


def test_save_catalog_json(catalog_manager, sample_openapi, tmp_path):
    """Test saving catalog as JSON."""
    catalog_manager.parse_file(sample_openapi)

    output_file = tmp_path / "catalog.json"
    catalog_manager.save_catalog(output_file, format="json")

    assert output_file.exists()

    import json

    with open(output_file) as f:
        data = json.load(f)

    assert "entries" in data
    assert len(data["entries"]) == 1


def test_save_catalog_html(catalog_manager, sample_openapi, tmp_path):
    """Test saving catalog as HTML."""
    catalog_manager.parse_file(sample_openapi)

    output_file = tmp_path / "catalog.html"
    catalog_manager.save_catalog(output_file, format="html")

    assert output_file.exists()

    content = output_file.read_text()
    assert "<!DOCTYPE html>" in content
    assert "API Catalog" in content

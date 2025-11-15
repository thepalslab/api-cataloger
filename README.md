# API Cataloger 🔍

**Automatically parse OpenAPI specs, controller files, and annotations to generate a searchable internal catalog of all available APIs.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

API Cataloger is a powerful tool that helps organizations maintain visibility into their API landscape by automatically discovering and cataloging APIs from various sources. It parses:

- **OpenAPI/Swagger specifications** (YAML/JSON)
- **Controller files** from popular web frameworks (Express, Flask, FastAPI, Spring Boot, Django)
- **Code annotations** and decorators in Python, Java, and TypeScript

The tool generates both JSON and interactive HTML catalogs with rich metadata including:
- Team ownership
- Last updated timestamps
- API version information
- Endpoint status (active, deprecated, beta, internal)
- Searchable interface

## Features

✨ **Multi-Source Parsing**
- OpenAPI 2.0 (Swagger) and 3.x specifications
- Express.js, Flask, FastAPI, Spring Boot, and Django controllers
- Python, Java, and TypeScript annotations

🔍 **Searchable Catalog**
- Search by endpoint path, method, description, or tags
- Filter by status, team, or API version
- Interactive HTML interface with real-time search

📊 **Rich Metadata**
- Team ownership tracking
- Automatic last-modified detection
- Endpoint status tracking
- API versioning support

🎨 **Multiple Output Formats**
- JSON for programmatic access
- Interactive HTML with modern UI
- CLI for quick queries and statistics

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/thepalslab/api-cataloger.git
cd api-cataloger

# Install in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### Using pip (when published)

```bash
pip install api-cataloger
```

## Quick Start

### Scan a directory for APIs

```bash
# Scan current directory and generate JSON catalog
api-cataloger scan . -o catalog.json

# Scan with team ownership and generate HTML
api-cataloger scan ./src --team "Platform Team" -f html -o catalog.html

# Scan a specific OpenAPI file
api-cataloger scan ./openapi.yaml -f html
```

### Search the catalog

```bash
# Search for endpoints
api-cataloger search catalog.json "users"

# Search by HTTP method
api-cataloger search catalog.json "POST"
```

### View statistics

```bash
api-cataloger stats catalog.json
```

## Usage Examples

### Example 1: Scan a Repository

```bash
api-cataloger scan /path/to/repo \
  --team "API Platform Team" \
  --format html \
  --output my-api-catalog.html
```

### Example 2: Generate JSON Catalog

```bash
api-cataloger scan ./services \
  --format json \
  --output catalog.json \
  --recursive
```

### Example 3: Search for Specific Endpoints

```bash
# Find all user-related endpoints
api-cataloger search catalog.json "user"

# Find all POST endpoints
api-cataloger search catalog.json "POST"

# Find deprecated endpoints
api-cataloger search catalog.json "deprecated"
```

## Supported Frameworks

### Web Frameworks

- **Node.js/JavaScript**: Express.js
- **Python**: Flask, FastAPI, Django
- **Java**: Spring Boot (annotations)

### API Specifications

- OpenAPI 3.x
- Swagger 2.0

## Output Formats

### JSON Output

```json
{
  "generated_at": "2024-01-15T10:30:00",
  "entries": [
    {
      "id": "abc123",
      "metadata": {
        "title": "User Management API",
        "version": "1.0.0",
        "team_owner": "Platform Team",
        "last_updated": "2024-01-15T10:00:00",
        "source_file": "/path/to/openapi.yaml"
      },
      "endpoints": [
        {
          "path": "/users",
          "method": "GET",
          "summary": "List all users",
          "description": "Retrieve a paginated list of users",
          "tags": ["users"],
          "status": "active"
        }
      ]
    }
  ]
}
```

### HTML Output

The HTML output provides an interactive, searchable interface with:
- Real-time search across all endpoints
- Color-coded HTTP methods
- Status badges (active, deprecated, beta, internal)
- Statistics dashboard
- Responsive design

## CLI Reference

### `scan` Command

Scan directories or files for API definitions.

```bash
api-cataloger scan [PATH] [OPTIONS]
```

**Options:**
- `-o, --output PATH`: Output file path (default: catalog.json)
- `-f, --format [json|html]`: Output format (default: json)
- `-t, --team TEXT`: Team owner name
- `--recursive/--no-recursive`: Scan directories recursively (default: true)

### `search` Command

Search for APIs in a catalog file.

```bash
api-cataloger search CATALOG_FILE QUERY
```

### `stats` Command

Show statistics about a catalog.

```bash
api-cataloger stats CATALOG_FILE
```

## Development

### Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install package in editable mode
pip install -e .
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=api_cataloger --cov-report=html

# Run specific test file
pytest tests/parsers/test_openapi_parser.py
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Project Structure

```
api-cataloger/
├── src/api_cataloger/
│   ├── __init__.py
│   ├── models.py              # Data models
│   ├── catalog_manager.py     # Main catalog logic
│   ├── cli.py                 # Command-line interface
│   ├── output.py              # Output generators
│   └── parsers/
│       ├── __init__.py
│       ├── openapi_parser.py     # OpenAPI spec parser
│       ├── controller_parser.py  # Controller file parser
│       └── annotation_parser.py  # Annotation parser
├── tests/                     # Test suite
├── examples/                  # Example API files
│   ├── openapi/
│   ├── controllers/
│   └── annotations/
├── setup.py
├── requirements.txt
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- [Jinja2](https://jinja.palletsprojects.com/) for HTML templating
- [PyYAML](https://pyyaml.org/) for YAML parsing

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/thepalslab/api-cataloger).

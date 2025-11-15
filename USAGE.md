# API Cataloger Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Output Formats](#output-formats)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/thepalslab/api-cataloger.git
cd api-cataloger

# Install the package
pip install -e .
```

### Quick Start

Run the demo script to see the tool in action:

```bash
./demo.sh
```

## Basic Usage

### Scanning for APIs

#### Scan a Single File

```bash
# OpenAPI spec
api-cataloger scan openapi.yaml -o catalog.json

# Controller file
api-cataloger scan user_controller.py -f html -o output.html
```

#### Scan a Directory

```bash
# Scan current directory
api-cataloger scan .

# Scan specific directory with team ownership
api-cataloger scan ./src --team "Backend Team"

# Scan non-recursively
api-cataloger scan ./api --no-recursive
```

### Searching the Catalog

```bash
# Search by path
api-cataloger search catalog.json "/users"

# Search by HTTP method
api-cataloger search catalog.json "POST"

# Search by tag or description
api-cataloger search catalog.json "authentication"
```

### Viewing Statistics

```bash
api-cataloger stats catalog.json
```

## Advanced Features

### Multiple Output Formats

#### JSON Output
```bash
api-cataloger scan ./src -f json -o catalog.json
```

JSON format is ideal for:
- Programmatic access
- Integration with other tools
- Version control tracking
- CI/CD pipelines

#### HTML Output
```bash
api-cataloger scan ./src -f html -o catalog.html
```

HTML format provides:
- Interactive search interface
- Visual endpoint browser
- Statistics dashboard
- No server required

### Team Ownership Tracking

Specify team ownership for better organization:

```bash
# Single team
api-cataloger scan ./backend --team "Backend Team"

# You can scan multiple directories with different teams
api-cataloger scan ./auth-service --team "Security Team" -o auth-catalog.json
api-cataloger scan ./payment-service --team "Payment Team" -o payment-catalog.json
```

### Framework-Specific Examples

#### Express.js
```javascript
// Automatically detected from:
router.get('/api/users', handler);
app.post('/api/login', handler);
```

#### Flask
```python
# Automatically detected from:
@app.route('/api/users', methods=['GET'])
@blueprint.route('/api/products', methods=['POST'])
```

#### FastAPI
```python
# Automatically detected from:
@app.get('/api/users')
@router.post('/api/items')
```

#### Spring Boot
```java
// Automatically detected from:
@GetMapping("/api/users")
@PostMapping("/api/products")
@RequestMapping(path="/api/orders", method=RequestMethod.GET)
```

## Output Formats

### JSON Structure

```json
{
  "generated_at": "ISO-8601 timestamp",
  "entries": [
    {
      "id": "unique-id",
      "metadata": {
        "team_owner": "Team Name",
        "last_updated": "ISO-8601 timestamp",
        "version": "1.0.0",
        "title": "API Title",
        "description": "API Description",
        "source_file": "/path/to/file",
        "base_url": "https://api.example.com"
      },
      "endpoints": [
        {
          "path": "/api/resource",
          "method": "GET",
          "description": "Endpoint description",
          "summary": "Short summary",
          "parameters": [],
          "responses": {},
          "tags": ["tag1", "tag2"],
          "status": "active|deprecated|beta|internal"
        }
      ]
    }
  ]
}
```

### HTML Features

The HTML catalog includes:
- **Search Bar**: Real-time filtering of endpoints
- **Statistics Dashboard**: Overview of API metrics
- **Color-Coded Methods**: Visual distinction for HTTP methods
- **Status Badges**: Active, deprecated, beta, internal
- **Metadata Display**: Team, version, last updated

## Best Practices

### 1. Version Control Your Catalogs

```bash
# Generate catalog
api-cataloger scan ./src -o api-catalog.json

# Add to git
git add api-catalog.json
git commit -m "Update API catalog"
```

### 2. CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/catalog.yml
name: Update API Catalog
on: [push]
jobs:
  catalog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install API Cataloger
        run: pip install api-cataloger
      - name: Generate Catalog
        run: api-cataloger scan . -f html -o docs/api-catalog.html
      - name: Deploy
        # Deploy to GitHub Pages or S3
```

### 3. Regular Updates

Schedule regular catalog updates:

```bash
# Cron job example (daily at 2 AM)
0 2 * * * cd /path/to/repo && api-cataloger scan . -o catalog.json
```

### 4. Team-Specific Catalogs

Generate separate catalogs per team:

```bash
#!/bin/bash
teams=("backend:./backend" "frontend:./frontend" "mobile:./mobile")

for team_dir in "${teams[@]}"; do
    IFS=':' read -r team dir <<< "$team_dir"
    api-cataloger scan "$dir" --team "$team" -o "catalog-$team.json"
done
```

### 5. Documentation Integration

Link catalogs to your documentation:

```markdown
# API Documentation

See our [API Catalog](./api-catalog.html) for a complete list of endpoints.
```

## Troubleshooting

### Issue: No endpoints found

**Solution**: Ensure your files follow supported patterns:
- OpenAPI files must have `openapi` or `swagger` in the YAML/JSON
- Controller files should have keywords like `controller`, `route`, `handler`, `endpoint`, or `api` in the filename
- Check that your framework is supported

### Issue: Endpoints missing from catalog

**Solution**: 
- Check file extensions (`.py`, `.js`, `.java`, etc.)
- Verify annotation/decorator syntax matches supported patterns
- Ensure files aren't in excluded directories (`node_modules`, `__pycache__`, etc.)

### Issue: Search not working

**Solution**:
- Ensure you're using the correct catalog file path
- Search is case-insensitive and searches paths, descriptions, and tags
- Try broader search terms

### Issue: HTML not displaying correctly

**Solution**:
- Open the HTML file directly in a browser (not through a text editor)
- Ensure the file was generated with `-f html` flag
- Check browser console for JavaScript errors

## Integration Examples

### Python Integration

```python
from api_cataloger.catalog_manager import CatalogManager
from pathlib import Path

# Create manager
manager = CatalogManager()

# Scan directory
catalog = manager.scan_directory(Path('./src'), team_owner="My Team")

# Search
results = manager.search("user")

# Save
manager.save_catalog(Path('catalog.json'), format='json')
```

### Shell Script Integration

```bash
#!/bin/bash

# Generate catalog
api-cataloger scan ./services -o catalog.json

# Check for critical APIs
if api-cataloger search catalog.json "payment" | grep -q "deprecated"; then
    echo "WARNING: Payment APIs are deprecated!"
    exit 1
fi
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/thepalslab/api-cataloger/issues
- Documentation: See README.md
- Examples: Check the `examples/` directory

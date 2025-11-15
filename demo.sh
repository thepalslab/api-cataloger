#!/bin/bash
# Demo script for API Cataloger

echo "==================================================================="
echo "API Cataloger Demo"
echo "==================================================================="
echo ""

# Install the package
echo "📦 Installing API Cataloger..."
pip install -e . > /dev/null 2>&1
echo "✓ Installation complete"
echo ""

# Show help
echo "📖 Available commands:"
api-cataloger --help
echo ""

# Scan examples directory
echo "🔍 Scanning examples directory..."
api-cataloger scan examples --team "Platform Team" -o demo-catalog.json
echo ""

# Show statistics
echo "📊 Catalog Statistics:"
api-cataloger stats demo-catalog.json
echo ""

# Search examples
echo "🔎 Searching for 'user' endpoints:"
api-cataloger search demo-catalog.json "user"
echo ""

echo "🔎 Searching for 'POST' endpoints:"
api-cataloger search demo-catalog.json "POST"
echo ""

# Generate HTML catalog
echo "🌐 Generating HTML catalog..."
api-cataloger scan examples --team "Platform Team" -f html -o demo-catalog.html
echo "✓ HTML catalog generated: demo-catalog.html"
echo ""

echo "==================================================================="
echo "Demo complete! Check out demo-catalog.html in a browser to see"
echo "the interactive catalog interface."
echo "==================================================================="

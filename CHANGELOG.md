# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-15

### Added
- Initial release of API Cataloger
- OpenAPI 2.0 and 3.x specification parser
- Controller file parser for Express.js, Flask, FastAPI, Spring Boot, and Django
- Annotation parser for Python, Java, and TypeScript decorators
- CLI with `scan`, `search`, and `stats` commands
- JSON and HTML catalog output formats
- Interactive HTML catalog with search functionality
- Team ownership tracking
- Endpoint status tracking (active, deprecated, beta, internal)
- Comprehensive test suite with 14 tests
- Example files demonstrating all parsers
- Full documentation and usage guide
- Demo script for quick start

### Supported Frameworks
- **OpenAPI**: 2.0 (Swagger), 3.x
- **Node.js**: Express.js
- **Python**: Flask, FastAPI, Django
- **Java**: Spring Boot

### Supported Languages
- Python (.py)
- JavaScript/TypeScript (.js, .ts)
- Java (.java)
- Kotlin (.kt)

### Features
- Automatic API discovery from multiple sources
- Rich metadata extraction (team, version, last updated, status)
- Searchable catalog interface
- Statistics and reporting
- CI/CD integration ready
- No external dependencies for viewing HTML catalogs

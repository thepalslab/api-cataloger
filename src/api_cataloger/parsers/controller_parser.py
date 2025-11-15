"""Controller file parser for common web frameworks."""

import re
from pathlib import Path
from typing import Optional, List
import hashlib

from . import BaseParser
from ..models import APICatalogEntry, APIMetadata, APIEndpoint, EndpointStatus


class ControllerParser(BaseParser):
    """Parser for controller files from various web frameworks."""

    # Patterns for different frameworks
    PATTERNS = {
        # Express.js / Node.js
        "express": [
            (r'router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', "js"),
            (r'app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', "js"),
        ],
        # Flask / Python
        "flask": [
            (r'@app\.route\([\'"]([^\'"]+)[\'"].*methods=\[([^\]]+)\]', "py"),
            (r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', "py"),
            (r'@\w+\.route\([\'"]([^\'"]+)[\'"].*methods=\[([^\]]+)\]', "py"),
        ],
        # FastAPI / Python
        "fastapi": [
            (r'@app\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', "py"),
            (r'@router\.(get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]', "py"),
        ],
        # Spring Boot / Java
        "spring": [
            (r'@(Get|Post|Put|Delete|Patch)Mapping\([\'"]([^\'"]+)[\'"]', "java"),
            (
                r'@RequestMapping\(.*path\s*=\s*[\'"]([^\'"]+)[\'"].*method\s*=\s*RequestMethod\.(\w+)',
                "java",
            ),
        ],
        # Django / Python
        "django": [
            (r'path\([\'"]([^\'"]+)[\'"]', "py"),
            (r"url\(r\'^([^\']+)\'", "py"),
        ],
    }

    def can_parse(self, file_path: Path) -> bool:
        """Check if file is a controller file."""
        # Check file extensions
        valid_extensions = [".js", ".ts", ".py", ".java", ".kt", ".rb", ".go"]
        if file_path.suffix.lower() not in valid_extensions:
            return False

        # Check if filename suggests it's a controller
        filename_lower = file_path.name.lower()
        controller_keywords = ["controller", "route", "handler", "endpoint", "api"]

        return any(keyword in filename_lower for keyword in controller_keywords)

    def parse(
        self, file_path: Path, team_owner: Optional[str] = None
    ) -> Optional[APICatalogEntry]:
        """Parse controller file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            file_meta = self.get_file_metadata(file_path)

            # Extract framework and endpoints
            framework = self._detect_framework(content, file_path)
            endpoints = self._extract_endpoints(content, file_path, framework)

            if not endpoints:
                return None

            # Extract metadata
            metadata = APIMetadata(
                team_owner=team_owner,
                last_updated=file_meta["last_updated"],
                title=f"API from {file_path.name}",
                description=self._extract_description(content),
                source_file=file_meta["source_file"],
            )

            # Generate unique ID
            catalog_id = hashlib.md5(str(file_path).encode()).hexdigest()[:12]

            return APICatalogEntry(
                id=catalog_id, metadata=metadata, endpoints=endpoints
            )
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None

    def _detect_framework(self, content: str, file_path: Path) -> str:
        """Detect which framework is being used."""
        content_lower = content.lower()

        # Check for framework imports/indicators
        if "from flask import" in content or "import flask" in content:
            return "flask"
        elif "from fastapi import" in content or "import fastapi" in content:
            return "fastapi"
        elif "express()" in content or "require('express')" in content:
            return "express"
        elif "@springboot" in content_lower or "import org.springframework" in content:
            return "spring"
        elif "django" in content_lower:
            return "django"

        # Fallback based on file extension
        ext = file_path.suffix.lower()
        if ext in [".js", ".ts"]:
            return "express"
        elif ext == ".py":
            return "flask"
        elif ext in [".java", ".kt"]:
            return "spring"

        return "unknown"

    def _extract_endpoints(
        self, content: str, file_path: Path, framework: str
    ) -> List[APIEndpoint]:
        """Extract endpoints from the content."""
        endpoints = []
        patterns = self.PATTERNS.get(framework, [])

        for pattern, file_type in patterns:
            if file_path.suffix.lower()[1:] not in file_type:
                continue

            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                endpoint = self._create_endpoint_from_match(match, framework)
                if endpoint:
                    endpoints.append(endpoint)

        return endpoints

    def _create_endpoint_from_match(
        self, match, framework: str
    ) -> Optional[APIEndpoint]:
        """Create an endpoint object from a regex match."""
        groups = match.groups()

        # Different frameworks have different group orders
        if framework in ["express", "fastapi"]:
            method = groups[0].upper()
            path = groups[1]
        elif framework == "flask":
            if "methods=" in match.group(0):
                path = groups[0]
                methods_str = groups[1]
                method = methods_str.strip("'\"").split(",")[0].strip("'\"").upper()
            else:
                method = groups[0].upper()
                path = groups[1]
        elif framework == "spring":
            if "Mapping" in match.group(0):
                method = groups[0].upper()
                path = groups[1]
            else:
                path = groups[0]
                method = groups[1].upper()
        else:
            # Generic fallback
            if len(groups) >= 2:
                method = groups[0].upper() if groups[0] else "GET"
                path = groups[1]
            else:
                path = groups[0]
                method = "GET"

        # Determine status (simple heuristic)
        status = EndpointStatus.ACTIVE
        if "deprecated" in match.group(0).lower():
            status = EndpointStatus.DEPRECATED

        return APIEndpoint(
            path=path, method=method, description=None, summary=None, status=status
        )

    def _extract_description(self, content: str) -> Optional[str]:
        """Extract description from file comments."""
        # Look for module docstring or file-level comments
        docstring_match = re.search(r"[\'\"]{3}(.*?)[\'\"]{3}", content, re.DOTALL)
        if docstring_match:
            return docstring_match.group(1).strip()[:200]

        # Look for file header comment
        comment_match = re.search(r"^/\*\*(.*?)\*/", content, re.DOTALL | re.MULTILINE)
        if comment_match:
            return comment_match.group(1).strip()[:200]

        return None

"""Annotation parser for decorated endpoints."""

import re
from pathlib import Path
from typing import Optional, List, Dict, Any
import hashlib

from . import BaseParser
from ..models import APICatalogEntry, APIMetadata, APIEndpoint, EndpointStatus


class AnnotationParser(BaseParser):
    """Parser for annotation-based API definitions."""

    ANNOTATION_PATTERNS = {
        # Python decorators
        "python": [
            r'@(\w+)\.(route|get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
            r'@api\.(route|get|post|put|delete|patch)\([\'"]([^\'"]+)[\'"]',
        ],
        # Java annotations
        "java": [
            r'@(Get|Post|Put|Delete|Patch)Mapping\([\'"]?([^\'")\s]+)[\'"]?\)',
            r'@RequestMapping\([\'"]?([^\'")\s]+)[\'"]?.*method\s*=\s*RequestMethod\.(\w+)',
            r'@Path\([\'"]([^\'"]+)[\'"]',
        ],
        # TypeScript/JavaScript decorators
        "typescript": [
            r'@(Get|Post|Put|Delete|Patch)\([\'"]([^\'"]+)[\'"]',
            r'@Route\([\'"]([^\'"]+)[\'"]',
        ],
    }

    def can_parse(self, file_path: Path) -> bool:
        """Check if file contains API annotations."""
        valid_extensions = [".py", ".java", ".kt", ".ts", ".js"]
        if file_path.suffix.lower() not in valid_extensions:
            return False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for common annotation patterns
            annotation_indicators = [
                r"@\w+\.(get|post|put|delete|patch)\(",
                r"@(Get|Post|Put|Delete|Patch)Mapping",
                r"@Route\(",
                r"@api\.",
            ]

            return any(
                re.search(pattern, content, re.IGNORECASE)
                for pattern in annotation_indicators
            )
        except Exception:
            return False

    def parse(
        self, file_path: Path, team_owner: Optional[str] = None
    ) -> Optional[APICatalogEntry]:
        """Parse annotations from file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            file_meta = self.get_file_metadata(file_path)

            # Detect language
            language = self._detect_language(file_path)

            # Extract endpoints from annotations
            endpoints = self._extract_annotated_endpoints(content, language)

            if not endpoints:
                return None

            # Extract metadata
            metadata = APIMetadata(
                team_owner=team_owner,
                last_updated=file_meta["last_updated"],
                title=f"API from {file_path.name}",
                description=self._extract_class_description(content),
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

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        ext = file_path.suffix.lower()

        if ext == ".py":
            return "python"
        elif ext in [".java", ".kt"]:
            return "java"
        elif ext in [".ts", ".js"]:
            return "typescript"

        return "unknown"

    def _extract_annotated_endpoints(
        self, content: str, language: str
    ) -> List[APIEndpoint]:
        """Extract endpoints from annotations."""
        endpoints = []
        patterns = self.ANNOTATION_PATTERNS.get(language, [])

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)

            for match in matches:
                endpoint_data = self._parse_annotation_match(match, language)
                if endpoint_data:
                    # Try to find associated documentation
                    doc = self._find_function_documentation(content, match.start())

                    endpoint = APIEndpoint(
                        path=endpoint_data["path"],
                        method=endpoint_data["method"],
                        description=doc.get("description"),
                        summary=doc.get("summary"),
                        status=endpoint_data.get("status", EndpointStatus.ACTIVE),
                        tags=doc.get("tags", []),
                    )
                    endpoints.append(endpoint)

        return endpoints

    def _parse_annotation_match(self, match, language: str) -> Optional[Dict[str, Any]]:
        """Parse annotation match into endpoint data."""
        groups = match.groups()

        if language == "python":
            if len(groups) >= 3:
                method = groups[1].upper() if groups[1] != "route" else "GET"
                path = groups[2]
            else:
                return None
        elif language == "java":
            if "Mapping" in match.group(0):
                method = groups[0].upper()
                path = groups[1]
            elif "RequestMapping" in match.group(0):
                path = groups[0]
                method = groups[1].upper() if len(groups) > 1 else "GET"
            elif "Path" in match.group(0):
                path = groups[0]
                method = "GET"
            else:
                return None
        elif language == "typescript":
            if len(groups) >= 2:
                method = groups[0].upper()
                path = groups[1]
            else:
                path = groups[0]
                method = "GET"
        else:
            return None

        return {"path": path, "method": method, "status": EndpointStatus.ACTIVE}

    def _find_function_documentation(
        self, content: str, annotation_pos: int
    ) -> Dict[str, Any]:
        """Find documentation for the function following an annotation."""
        doc_info = {"description": None, "summary": None, "tags": []}

        # Look for docstring or JavaDoc before the annotation
        before_annotation = content[:annotation_pos]

        # Python docstring
        docstring_match = re.search(
            r"[\'\"]{3}(.*?)[\'\"]{3}\s*$", before_annotation, re.DOTALL
        )
        if docstring_match:
            doc_text = docstring_match.group(1).strip()
            lines = doc_text.split("\n")
            doc_info["summary"] = lines[0].strip() if lines else None
            doc_info["description"] = doc_text[:200]

            # Extract tags from docstring
            tags = re.findall(r"@(\w+)", doc_text)
            doc_info["tags"] = tags

        # JavaDoc style
        javadoc_match = re.search(r"/\*\*(.*?)\*/\s*$", before_annotation, re.DOTALL)
        if javadoc_match:
            doc_text = javadoc_match.group(1).strip()
            # Remove leading asterisks
            doc_text = re.sub(r"^\s*\*\s*", "", doc_text, flags=re.MULTILINE)
            lines = [l.strip() for l in doc_text.split("\n") if l.strip()]
            doc_info["summary"] = lines[0] if lines else None
            doc_info["description"] = doc_text[:200]

            # Extract tags
            tags = re.findall(r"@(\w+)", doc_text)
            doc_info["tags"] = tags

        return doc_info

    def _extract_class_description(self, content: str) -> Optional[str]:
        """Extract class-level description."""
        # Python class docstring
        class_doc = re.search(
            r"class\s+\w+.*?:\s*[\'\"]{3}(.*?)[\'\"]{3}", content, re.DOTALL
        )
        if class_doc:
            return class_doc.group(1).strip()[:200]

        # Java class JavaDoc
        java_doc = re.search(r"/\*\*(.*?)\*/\s*public\s+class", content, re.DOTALL)
        if java_doc:
            doc = java_doc.group(1).strip()
            doc = re.sub(r"^\s*\*\s*", "", doc, flags=re.MULTILINE)
            return doc[:200]

        return None

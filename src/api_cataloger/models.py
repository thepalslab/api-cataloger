"""Data models for API catalog."""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class EndpointStatus(Enum):
    """Status of an API endpoint."""

    ACTIVE = "active"
    DEPRECATED = "deprecated"
    BETA = "beta"
    INTERNAL = "internal"


class HttpMethod(Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


@dataclass
class APIEndpoint:
    """Represents a single API endpoint."""

    path: str
    method: str
    description: Optional[str] = None
    summary: Optional[str] = None
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    responses: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    status: EndpointStatus = EndpointStatus.ACTIVE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result["status"] = self.status.value
        return result


@dataclass
class APIMetadata:
    """Metadata about an API source."""

    team_owner: Optional[str] = None
    last_updated: Optional[datetime] = None
    version: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    source_file: Optional[str] = None
    base_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        if self.last_updated:
            result["last_updated"] = self.last_updated.isoformat()
        return result


@dataclass
class APICatalogEntry:
    """A complete entry in the API catalog."""

    id: str
    metadata: APIMetadata
    endpoints: List[APIEndpoint] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "metadata": self.metadata.to_dict(),
            "endpoints": [ep.to_dict() for ep in self.endpoints],
        }


@dataclass
class APICatalog:
    """Complete API catalog containing multiple API sources."""

    entries: List[APICatalogEntry] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)

    def add_entry(self, entry: APICatalogEntry) -> None:
        """Add an entry to the catalog."""
        self.entries.append(entry)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "generated_at": self.generated_at.isoformat(),
            "entries": [entry.to_dict() for entry in self.entries],
        }

    def search(self, query: str) -> List[APIEndpoint]:
        """Search for endpoints matching the query."""
        results = []
        query_lower = query.lower()

        for entry in self.entries:
            for endpoint in entry.endpoints:
                # Search in path, description, summary, and tags
                if (
                    query_lower in endpoint.path.lower()
                    or (
                        endpoint.description
                        and query_lower in endpoint.description.lower()
                    )
                    or (endpoint.summary and query_lower in endpoint.summary.lower())
                    or any(query_lower in tag.lower() for tag in endpoint.tags)
                ):
                    results.append(endpoint)

        return results

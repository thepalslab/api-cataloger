"""Parser registry and base parser interface."""

from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
import os

from ..models import APICatalogEntry


class BaseParser(ABC):
    """Base class for all parsers."""

    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """Check if this parser can handle the given file."""
        pass

    @abstractmethod
    def parse(
        self, file_path: Path, team_owner: Optional[str] = None
    ) -> Optional[APICatalogEntry]:
        """Parse the file and return a catalog entry."""
        pass

    def get_file_metadata(self, file_path: Path) -> dict:
        """Get common file metadata."""
        stat = os.stat(file_path)
        from datetime import datetime

        return {
            "last_updated": datetime.fromtimestamp(stat.st_mtime),
            "source_file": str(file_path),
        }

"""Catalog manager for coordinating parsing and catalog generation."""
from pathlib import Path
from typing import List, Optional
import json

from .models import APICatalog, APICatalogEntry
from .parsers.openapi_parser import OpenAPIParser
from .parsers.controller_parser import ControllerParser
from .parsers.annotation_parser import AnnotationParser


class CatalogManager:
    """Manages the API cataloging process."""
    
    def __init__(self):
        """Initialize the catalog manager."""
        self.parsers = [
            OpenAPIParser(),
            ControllerParser(),
            AnnotationParser(),
        ]
        self.catalog = APICatalog()
    
    def scan_directory(self, directory: Path, team_owner: Optional[str] = None, 
                      recursive: bool = True) -> APICatalog:
        """Scan a directory for API definitions."""
        directory = Path(directory)
        
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if recursive:
            files = directory.rglob('*')
        else:
            files = directory.glob('*')
        
        for file_path in files:
            if not file_path.is_file():
                continue
            
            # Skip hidden files and common exclude directories
            if any(part.startswith('.') for part in file_path.parts):
                continue
            
            if any(exclude in str(file_path) for exclude in ['node_modules', '__pycache__', 'venv', 'dist', 'build']):
                continue
            
            self.parse_file(file_path, team_owner)
        
        return self.catalog
    
    def parse_file(self, file_path: Path, team_owner: Optional[str] = None) -> Optional[APICatalogEntry]:
        """Parse a single file with appropriate parser."""
        file_path = Path(file_path)
        
        for parser in self.parsers:
            if parser.can_parse(file_path):
                entry = parser.parse(file_path, team_owner)
                if entry:
                    self.catalog.add_entry(entry)
                    print(f"Parsed {file_path} -> {len(entry.endpoints)} endpoints")
                    return entry
        
        return None
    
    def parse_files(self, file_paths: List[Path], team_owner: Optional[str] = None) -> APICatalog:
        """Parse multiple files."""
        for file_path in file_paths:
            self.parse_file(file_path, team_owner)
        
        return self.catalog
    
    def save_catalog(self, output_path: Path, format: str = 'json') -> None:
        """Save catalog to file."""
        output_path = Path(output_path)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.catalog.to_dict(), f, indent=2)
        elif format == 'html':
            from .output import HTMLGenerator
            generator = HTMLGenerator()
            html = generator.generate(self.catalog)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"Catalog saved to {output_path}")
    
    def search(self, query: str) -> List:
        """Search the catalog."""
        return self.catalog.search(query)

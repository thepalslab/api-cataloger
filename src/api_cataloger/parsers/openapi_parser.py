"""OpenAPI specification parser."""
import yaml
import json
from pathlib import Path
from typing import Optional, Dict, Any
import hashlib

from . import BaseParser
from ..models import (
    APICatalogEntry, APIMetadata, APIEndpoint, EndpointStatus
)


class OpenAPIParser(BaseParser):
    """Parser for OpenAPI 2.0 (Swagger) and 3.x specifications."""
    
    def can_parse(self, file_path: Path) -> bool:
        """Check if file is an OpenAPI spec."""
        if file_path.suffix.lower() not in ['.yaml', '.yml', '.json']:
            return False
        
        try:
            content = self._load_file(file_path)
            # Check for OpenAPI/Swagger markers
            return ('openapi' in content or 'swagger' in content)
        except Exception:
            return False
    
    def _load_file(self, file_path: Path) -> Dict[str, Any]:
        """Load YAML or JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.suffix.lower() == '.json':
                return json.load(f)
            else:
                return yaml.safe_load(f)
    
    def parse(self, file_path: Path, team_owner: Optional[str] = None) -> Optional[APICatalogEntry]:
        """Parse OpenAPI specification."""
        try:
            spec = self._load_file(file_path)
            file_meta = self.get_file_metadata(file_path)
            
            # Extract metadata
            info = spec.get('info', {})
            metadata = APIMetadata(
                team_owner=team_owner,
                last_updated=file_meta['last_updated'],
                version=info.get('version'),
                title=info.get('title'),
                description=info.get('description'),
                source_file=file_meta['source_file'],
                base_url=self._extract_base_url(spec)
            )
            
            # Generate unique ID
            catalog_id = hashlib.md5(str(file_path).encode()).hexdigest()[:12]
            
            # Parse endpoints
            endpoints = self._parse_endpoints(spec)
            
            return APICatalogEntry(
                id=catalog_id,
                metadata=metadata,
                endpoints=endpoints
            )
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return None
    
    def _extract_base_url(self, spec: Dict[str, Any]) -> Optional[str]:
        """Extract base URL from spec."""
        # OpenAPI 3.x
        if 'servers' in spec and spec['servers']:
            return spec['servers'][0].get('url')
        
        # OpenAPI 2.0 (Swagger)
        if 'host' in spec:
            scheme = spec.get('schemes', ['https'])[0]
            base_path = spec.get('basePath', '')
            return f"{scheme}://{spec['host']}{base_path}"
        
        return None
    
    def _parse_endpoints(self, spec: Dict[str, Any]) -> list:
        """Parse all endpoints from the spec."""
        endpoints = []
        paths = spec.get('paths', {})
        
        for path, path_item in paths.items():
            for method, operation in path_item.items():
                if method.upper() not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                    continue
                
                if not isinstance(operation, dict):
                    continue
                
                # Determine status
                status = EndpointStatus.ACTIVE
                if operation.get('deprecated', False):
                    status = EndpointStatus.DEPRECATED
                elif 'beta' in operation.get('tags', []):
                    status = EndpointStatus.BETA
                elif 'internal' in operation.get('tags', []):
                    status = EndpointStatus.INTERNAL
                
                endpoint = APIEndpoint(
                    path=path,
                    method=method.upper(),
                    description=operation.get('description'),
                    summary=operation.get('summary'),
                    parameters=operation.get('parameters', []),
                    responses=operation.get('responses', {}),
                    tags=operation.get('tags', []),
                    status=status
                )
                endpoints.append(endpoint)
        
        return endpoints

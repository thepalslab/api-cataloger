"""Command-line interface for the API cataloger."""
import click
from pathlib import Path
import json

from .catalog_manager import CatalogManager
from .models import APICatalog


@click.group()
@click.version_option(version='0.1.0')
def main():
    """API Cataloger - Parse and catalog APIs from various sources.
    
    This tool automatically parses OpenAPI specs, controller files, and 
    annotations from repositories to generate a searchable internal catalog 
    of available APIs with metadata.
    """
    pass


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', default='catalog.json', help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'html']), default='json', help='Output format')
@click.option('--team', '-t', help='Team owner name')
@click.option('--recursive/--no-recursive', default=True, help='Scan directories recursively')
def scan(path, output, format, team, recursive):
    """Scan a directory or file for API definitions.
    
    Examples:
    
        api-cataloger scan ./my-project -o catalog.json
        
        api-cataloger scan ./openapi.yaml -f html -o catalog.html
        
        api-cataloger scan ./src --team "Platform Team" -f html
    """
    manager = CatalogManager()
    path_obj = Path(path)
    
    click.echo(f"🔍 Scanning {path}...")
    
    if path_obj.is_file():
        entry = manager.parse_file(path_obj, team)
        if entry:
            click.echo(f"✅ Found {len(entry.endpoints)} endpoints")
        else:
            click.echo("❌ No API definitions found in file")
    else:
        catalog = manager.scan_directory(path_obj, team, recursive)
        total_endpoints = sum(len(entry.endpoints) for entry in catalog.entries)
        click.echo(f"✅ Found {len(catalog.entries)} API sources with {total_endpoints} total endpoints")
    
    # Save catalog
    manager.save_catalog(Path(output), format)
    click.echo(f"💾 Catalog saved to {output}")
    
    if format == 'html':
        click.echo(f"🌐 Open {output} in a browser to view the catalog")


@main.command()
@click.argument('catalog_file', type=click.Path(exists=True))
@click.argument('query')
def search(catalog_file, query):
    """Search for APIs in a catalog file.
    
    Examples:
    
        api-cataloger search catalog.json "user"
        
        api-cataloger search catalog.json "POST"
    """
    with open(catalog_file, 'r') as f:
        data = json.load(f)
    
    # Reconstruct catalog (simplified for search)
    catalog = APICatalog()
    results = []
    
    query_lower = query.lower()
    for entry_data in data.get('entries', []):
        for ep_data in entry_data.get('endpoints', []):
            path = ep_data.get('path', '')
            method = ep_data.get('method', '')
            description = ep_data.get('description', '') or ''
            summary = ep_data.get('summary', '') or ''
            tags = ep_data.get('tags', [])
            
            if (query_lower in path.lower() or
                query_lower in method.lower() or
                query_lower in description.lower() or
                query_lower in summary.lower() or
                any(query_lower in tag.lower() for tag in tags)):
                results.append({
                    'method': method,
                    'path': path,
                    'description': summary or description,
                    'source': entry_data.get('metadata', {}).get('source_file', 'unknown')
                })
    
    if results:
        click.echo(f"🔍 Found {len(results)} matching endpoints:\n")
        for result in results:
            click.echo(f"  {result['method']:8} {result['path']}")
            if result['description']:
                click.echo(f"           {result['description'][:80]}")
            click.echo(f"           📁 {result['source']}\n")
    else:
        click.echo(f"❌ No endpoints found matching '{query}'")


@main.command()
@click.argument('catalog_file', type=click.Path(exists=True))
def stats(catalog_file):
    """Show statistics about a catalog.
    
    Example:
    
        api-cataloger stats catalog.json
    """
    with open(catalog_file, 'r') as f:
        data = json.load(f)
    
    total_apis = len(data.get('entries', []))
    total_endpoints = sum(len(entry.get('endpoints', [])) for entry in data.get('entries', []))
    
    # Count by method
    methods = {}
    statuses = {}
    
    for entry in data.get('entries', []):
        for ep in entry.get('endpoints', []):
            method = ep.get('method', 'UNKNOWN')
            status = ep.get('status', 'active')
            
            methods[method] = methods.get(method, 0) + 1
            statuses[status] = statuses.get(status, 0) + 1
    
    click.echo("📊 Catalog Statistics\n")
    click.echo(f"API Sources:      {total_apis}")
    click.echo(f"Total Endpoints:  {total_endpoints}\n")
    
    click.echo("By HTTP Method:")
    for method, count in sorted(methods.items()):
        click.echo(f"  {method:8} {count}")
    
    click.echo("\nBy Status:")
    for status, count in sorted(statuses.items()):
        click.echo(f"  {status:12} {count}")
    
    click.echo(f"\nGenerated: {data.get('generated_at', 'unknown')}")


if __name__ == '__main__':
    main()

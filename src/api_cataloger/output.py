"""Output generators for the catalog."""
from jinja2 import Template
from typing import List
from .models import APICatalog


class HTMLGenerator:
    """Generate HTML output for the catalog."""
    
    TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Catalog</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: #2c3e50;
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .search-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .search-box input {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 4px;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .api-entry {
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .api-header {
            background: #34495e;
            color: white;
            padding: 20px;
        }
        
        .api-title {
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        
        .api-meta {
            color: #bdc3c7;
            font-size: 0.9em;
        }
        
        .api-meta span {
            margin-right: 15px;
        }
        
        .endpoints {
            padding: 20px;
        }
        
        .endpoint {
            padding: 15px;
            border-left: 4px solid #3498db;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        
        .endpoint-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .method {
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85em;
            margin-right: 10px;
            color: white;
        }
        
        .method.GET { background: #27ae60; }
        .method.POST { background: #3498db; }
        .method.PUT { background: #f39c12; }
        .method.DELETE { background: #e74c3c; }
        .method.PATCH { background: #9b59b6; }
        
        .path {
            font-family: 'Courier New', monospace;
            font-size: 1.1em;
            flex: 1;
        }
        
        .status {
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .status.active { background: #d4edda; color: #155724; }
        .status.deprecated { background: #f8d7da; color: #721c24; }
        .status.beta { background: #fff3cd; color: #856404; }
        .status.internal { background: #d1ecf1; color: #0c5460; }
        
        .description {
            color: #666;
            margin-top: 5px;
        }
        
        .tags {
            margin-top: 10px;
        }
        
        .tag {
            display: inline-block;
            background: #e9ecef;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            margin-right: 5px;
        }
        
        .stats {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .stat-label {
            color: #7f8c8d;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>🔍 API Catalog</h1>
            <p>Generated on {{ catalog.generated_at }}</p>
        </div>
    </header>
    
    <div class="container">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔎 Search APIs by path, description, or tags..." onkeyup="filterAPIs()">
        </div>
        
        <div class="stats">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{{ total_apis }}</div>
                    <div class="stat-label">API Sources</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ total_endpoints }}</div>
                    <div class="stat-label">Total Endpoints</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{{ active_endpoints }}</div>
                    <div class="stat-label">Active Endpoints</div>
                </div>
            </div>
        </div>
        
        <div id="apiList">
            {% for entry in catalog.entries %}
            <div class="api-entry" data-api="{{ entry.id }}">
                <div class="api-header">
                    <div class="api-title">{{ entry.metadata.title or 'Untitled API' }}</div>
                    <div class="api-meta">
                        {% if entry.metadata.team_owner %}
                        <span>👥 {{ entry.metadata.team_owner }}</span>
                        {% endif %}
                        {% if entry.metadata.version %}
                        <span>📌 v{{ entry.metadata.version }}</span>
                        {% endif %}
                        {% if entry.metadata.last_updated %}
                        <span>🕐 Updated: {{ entry.metadata.last_updated }}</span>
                        {% endif %}
                        <span>📁 {{ entry.metadata.source_file }}</span>
                    </div>
                </div>
                
                <div class="endpoints">
                    {% for endpoint in entry.endpoints %}
                    <div class="endpoint" data-endpoint="{{ endpoint.path }} {{ endpoint.method }}">
                        <div class="endpoint-header">
                            <span class="method {{ endpoint.method }}">{{ endpoint.method }}</span>
                            <span class="path">{{ endpoint.path }}</span>
                            <span class="status {{ endpoint.status }}">{{ endpoint.status }}</span>
                        </div>
                        
                        {% if endpoint.summary or endpoint.description %}
                        <div class="description">
                            {{ endpoint.summary or endpoint.description }}
                        </div>
                        {% endif %}
                        
                        {% if endpoint.tags %}
                        <div class="tags">
                            {% for tag in endpoint.tags %}
                            <span class="tag">{{ tag }}</span>
                            {% endfor %}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        function filterAPIs() {
            const searchValue = document.getElementById('searchInput').value.toLowerCase();
            const apiEntries = document.querySelectorAll('.api-entry');
            
            apiEntries.forEach(entry => {
                const endpoints = entry.querySelectorAll('.endpoint');
                let hasMatch = false;
                
                endpoints.forEach(endpoint => {
                    const text = endpoint.textContent.toLowerCase();
                    const matches = text.includes(searchValue);
                    endpoint.style.display = matches ? 'block' : 'none';
                    if (matches) hasMatch = true;
                });
                
                entry.style.display = hasMatch ? 'block' : 'none';
            });
        }
    </script>
</body>
</html>
    """
    
    def generate(self, catalog: APICatalog) -> str:
        """Generate HTML from catalog."""
        # Calculate statistics
        total_endpoints = sum(len(entry.endpoints) for entry in catalog.entries)
        active_endpoints = sum(
            1 for entry in catalog.entries 
            for ep in entry.endpoints 
            if ep.status.value == 'active'
        )
        
        template = Template(self.TEMPLATE)
        return template.render(
            catalog=catalog.to_dict(),
            total_apis=len(catalog.entries),
            total_endpoints=total_endpoints,
            active_endpoints=active_endpoints
        )

# Python SDK Usage Guide

Complete guide for using the Turkiye API Python SDK.

## 📦 Installation

```bash
# Basic installation
pip install turkiye-api-py

# With server dependencies (if you want to run your own instance)
pip install turkiye-api-py[server]

# With development dependencies
pip install turkiye-api-py[dev]

# Install everything
pip install turkiye-api-py[all]
```

## 🚀 Quick Start

### Option 1: Using the SDK with a Running Server

```python
from app import TurkiyeClient

# Connect to local server
client = TurkiyeClient(base_url="http://localhost:8181")

# Or connect to remote server
# client = TurkiyeClient(base_url="https://your-api-domain.com")

# Get all provinces
provinces = client.get_provinces()
print(f"Total provinces: {len(provinces)}")

# Get specific province (Istanbul - ID: 34)
istanbul = client.get_province(34)
print(f"Province: {istanbul['name']}, Population: {istanbul['population']:,}")
```

### Option 2: Running Your Own Server

```bash
# Start the server
turkiye-api serve

# In development mode with auto-reload
turkiye-api serve --reload

# On custom port
turkiye-api serve --port 8000

# Production mode with multiple workers
turkiye-api serve --workers 4
```

## 📚 SDK Examples

### Basic Operations

#### Get All Provinces

```python
from app import TurkiyeClient

client = TurkiyeClient()

# Get all provinces
provinces = client.get_provinces()

# Print each province
for province in provinces:
    print(f"{province['id']:2d}. {province['name']}")
```

#### Filter Provinces by Population

```python
# Get provinces with population > 1 million
large_provinces = client.get_provinces(min_population=1000000)

for province in large_provinces:
    print(f"{province['name']}: {province['population']:,}")
```

#### Search by Name

```python
# Search provinces by name (partial match)
results = client.get_provinces(name="İst")
print(results)  # Returns İstanbul
```

### Pagination

```python
# Get first 10 provinces
provinces_page1 = client.get_provinces(offset=0, limit=10)

# Get next 10 provinces
provinces_page2 = client.get_provinces(offset=10, limit=10)

# Iterate through all provinces with pagination
offset = 0
limit = 20
all_provinces = []

while True:
    batch = client.get_provinces(offset=offset, limit=limit)
    if not batch:
        break
    all_provinces.extend(batch)
    offset += limit
```

### Sorting

```python
# Sort by population (ascending)
provinces = client.get_provinces(sort="population")

# Sort by population (descending)
provinces = client.get_provinces(sort="-population")

# Get top 5 most populated provinces
top5 = client.get_provinces(sort="-population", limit=5)
for i, province in enumerate(top5, 1):
    print(f"{i}. {province['name']}: {province['population']:,}")
```

### Field Selection

```python
# Get only specific fields
provinces = client.get_provinces(fields="id,name,population")

# Each province will only have the requested fields
print(provinces[0])  # {'id': 1, 'name': 'Adana', 'population': 2258718}
```

### Working with Districts

```python
# Get all districts
districts = client.get_districts()

# Get districts in a specific province (Istanbul - ID: 34)
istanbul_districts = client.get_districts(province_id=34)
print(f"Istanbul has {len(istanbul_districts)} districts")

# Get specific district
district = client.get_district(440)  # Kadıköy
print(f"District: {district['name']}, Province: {district['province']['name']}")

# Search districts by name
results = client.get_districts(name="Kad")
```

### Working with Neighborhoods

```python
# Get all neighborhoods in a district
neighborhoods = client.get_neighborhoods(district_id=440)  # Kadıköy

# Get specific neighborhood
neighborhood = client.get_neighborhood(1234)

# Search neighborhoods
results = client.get_neighborhoods(name="Moda")
```

### Working with Villages

```python
# Get villages in a district
villages = client.get_villages(district_id=440)

# Search villages by name
results = client.get_villages(name="köy")

# Get specific village
village = client.get_village(5678)
```

### Working with Towns

```python
# Get towns in a district
towns = client.get_towns(district_id=440)

# Get specific town
town = client.get_town(9012)
```

## 🔧 Advanced Usage

### Context Manager

```python
# Automatically closes connection when done
with TurkiyeClient(base_url="http://localhost:8181") as client:
    provinces = client.get_provinces()
    print(f"Found {len(provinces)} provinces")
# Connection automatically closed here
```

### Error Handling

```python
from app import TurkiyeClient, TurkiyeAPIError

client = TurkiyeClient()

try:
    province = client.get_province(999)  # Invalid ID
except TurkiyeAPIError as e:
    print(f"API Error: {e}")
```

### Custom Timeout

```python
# Set custom timeout (default is 30 seconds)
client = TurkiyeClient(timeout=60.0)
```

### Language Support

```python
# Set language preference (English or Turkish)
client = TurkiyeClient(language="tr")  # Turkish responses

# Or change language later
client.set_language("en")  # English responses
```

### Health Check

```python
# Check if API is healthy
health_status = client.health()
print(health_status)
# {'status': 'healthy', 'version': '1.1.0', ...}
```

## 🎯 Real-World Examples

### Example 1: Find All Cities with Population > 1M

```python
from app import TurkiyeClient

client = TurkiyeClient()

# Get large cities
large_cities = client.get_provinces(
    min_population=1000000,
    sort="-population",
    fields="name,population"
)

print("Cities with population > 1 million:")
print("-" * 40)
for city in large_cities:
    print(f"{city['name']:20s} {city['population']:>10,}")
```

### Example 2: Get Complete Istanbul Data

```python
from app import TurkiyeClient

client = TurkiyeClient()

# Get Istanbul province
istanbul = client.get_province(34)
print(f"Province: {istanbul['name']}")
print(f"Population: {istanbul['population']:,}")

# Get all districts
districts = client.get_districts(province_id=34)
print(f"\nDistricts: {len(districts)}")

# Get neighborhoods in Kadıköy
neighborhoods = client.get_neighborhoods(district_id=440)
print(f"Neighborhoods in Kadıköy: {len(neighborhoods)}")
```

### Example 3: Build a Location Hierarchy

```python
from app import TurkiyeClient

def get_full_address(neighborhood_id):
    """Get complete address hierarchy for a neighborhood."""
    client = TurkiyeClient()

    # Get neighborhood
    neighborhood = client.get_neighborhood(neighborhood_id)

    # Build hierarchy
    return {
        'neighborhood': neighborhood['name'],
        'district': neighborhood['district']['name'],
        'province': neighborhood['province']['name']
    }

# Example usage
address = get_full_address(1234)
print(f"{address['neighborhood']}, {address['district']}, {address['province']}")
```

### Example 4: Export Data to CSV

```python
import csv
from app import TurkiyeClient

client = TurkiyeClient()

# Get all provinces
provinces = client.get_provinces(fields="id,name,population,area")

# Write to CSV
with open('provinces.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'name', 'population', 'area'])
    writer.writeheader()
    writer.writerows(provinces)

print("Data exported to provinces.csv")
```

### Example 5: Build a Simple Search Tool

```python
from app import TurkiyeClient

def search_location(query):
    """Search across all location types."""
    client = TurkiyeClient()

    results = {
        'provinces': client.get_provinces(name=query, limit=5),
        'districts': client.get_districts(name=query, limit=5),
        'neighborhoods': client.get_neighborhoods(name=query, limit=5),
    }

    return results

# Example usage
results = search_location("Kad")
print(f"Provinces: {len(results['provinces'])}")
print(f"Districts: {len(results['districts'])}")
print(f"Neighborhoods: {len(results['neighborhoods'])}")
```

## 🔄 Async Support (Coming Soon)

Async client support is planned for future releases:

```python
# Future API
from app import AsyncTurkiyeClient

async with AsyncTurkiyeClient() as client:
    provinces = await client.get_provinces()
```

## 📖 API Reference

### TurkiyeClient

Main client class for interacting with the API.

#### Constructor

```python
TurkiyeClient(
    base_url: str = "http://localhost:8181",
    timeout: float = 30.0,
    api_version: str = "v1",
    language: str = "en"
)
```

#### Methods

**Provinces:**
- `get_provinces(**filters)` - Get list of provinces
- `get_province(id)` - Get specific province

**Districts:**
- `get_districts(**filters)` - Get list of districts
- `get_district(id)` - Get specific district

**Neighborhoods:**
- `get_neighborhoods(**filters)` - Get list of neighborhoods
- `get_neighborhood(id)` - Get specific neighborhood

**Villages:**
- `get_villages(**filters)` - Get list of villages
- `get_village(id)` - Get specific village

**Towns:**
- `get_towns(**filters)` - Get list of towns
- `get_town(id)` - Get specific town

**Utility:**
- `health()` - Check API health
- `set_language(lang)` - Set response language
- `close()` - Close HTTP connection

### Common Filters

All list methods support these filters:
- `name` - Filter by name (partial match)
- `offset` - Pagination offset (default: 0)
- `limit` - Results limit (default: 100)
- `sort` - Sort field (prefix `-` for descending)
- `fields` - Comma-separated field list

Province-specific:
- `min_population` - Minimum population
- `max_population` - Maximum population

Hierarchical filters:
- `province_id` - Filter by province
- `district_id` - Filter by district

## 🐛 Troubleshooting

### Connection Errors

```python
from app import TurkiyeClient, TurkiyeAPIError

client = TurkiyeClient(base_url="http://localhost:8181")

try:
    provinces = client.get_provinces()
except TurkiyeAPIError as e:
    print(f"Error: {e}")
    print("Is the server running? Start it with: turkiye-api serve")
```

### Timeout Issues

```python
# Increase timeout for slow connections
client = TurkiyeClient(timeout=120.0)
```

## 📞 Support

- GitHub Issues: https://github.com/gencharitaci/turkiye-api-py/issues
- Email: gncharitaci@gmail.com
- Documentation: https://github.com/gencharitaci/turkiye-api-py

---

**Last Updated**: 2025-12-16

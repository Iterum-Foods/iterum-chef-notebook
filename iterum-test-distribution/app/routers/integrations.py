from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import httpx
import asyncio
from typing import List, Dict, Optional
import re
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging

router = APIRouter(prefix="/api/integrations", tags=["integrations"])

# Universal URL Equipment Parser
@router.post("/equipment/parse-url")
async def parse_equipment_url(url_data: dict):
    """
    Parse equipment information from any URL
    Supports: WebRestaurant, Amazon, Home Depot, Restaurant Depot, etc.
    """
    try:
        url = url_data.get('url', '').strip()
        if not url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Validate URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise HTTPException(status_code=400, detail="Invalid URL format")
        
        equipment_data = await extract_equipment_from_url(url)
        
        return {
            "success": True,
            "equipment": equipment_data,
            "source_url": url,
            "supplier": equipment_data.get('supplier', 'Unknown')
        }
    
    except Exception as e:
        logging.error(f"URL parsing failed for {url}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to parse URL: {str(e)}")

async def extract_equipment_from_url(url: str) -> Dict:
    """Extract equipment data from various supplier websites"""
    
    domain = urlparse(url).netloc.lower()
    
    # Different parsers for different suppliers
    if 'webstaurant' in domain:
        return await parse_webstaurant_url(url)
    elif 'amazon' in domain:
        return await parse_amazon_url(url)
    elif 'homedepot' in domain:
        return await parse_homedepot_url(url)
    elif 'restaurantdepot' in domain:
        return await parse_restaurant_depot_url(url)
    elif 'katom' in domain:
        return await parse_katom_url(url)
    else:
        return await parse_generic_url(url)

async def parse_webstaurant_url(url: str) -> Dict:
    """Parse WebRestaurant Store product pages"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract WebRestaurant-specific data
            name = soup.find('h1', {'data-testid': 'product-title'})
            name = name.get_text(strip=True) if name else "Unknown Equipment"
            
            price_elem = soup.find('span', class_='price')
            price = extract_price(price_elem.get_text() if price_elem else "0")
            
            brand_elem = soup.find('span', {'data-testid': 'brand-name'})
            brand = brand_elem.get_text(strip=True) if brand_elem else ""
            
            # Category from breadcrumbs
            breadcrumbs = soup.find('nav', {'aria-label': 'breadcrumb'})
            category = extract_category_from_breadcrumbs(breadcrumbs)
            
            # Specifications
            specs = extract_webstaurant_specs(soup)
            
            return {
                'name': name,
                'brand': brand,
                'model': extract_model_from_name(name),
                'price': price,
                'category': category,
                'specifications': specs,
                'supplier': 'WebRestaurant Store',
                'source_url': url,
                'description': extract_description(soup)
            }
    
    except Exception as e:
        logging.error(f"WebRestaurant parsing failed: {e}")
        return create_fallback_equipment_data(url, 'WebRestaurant Store')

async def parse_amazon_url(url: str) -> Dict:
    """Parse Amazon product pages for restaurant equipment"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Amazon-specific selectors
            name_elem = soup.find('span', {'id': 'productTitle'})
            name = name_elem.get_text(strip=True) if name_elem else "Unknown Equipment"
            
            price_elem = soup.find('span', class_='a-price-whole') or soup.find('span', class_='a-offscreen')
            price = extract_price(price_elem.get_text() if price_elem else "0")
            
            # Extract brand from title or feature bullets
            brand = extract_brand_from_amazon(soup, name)
            
            # Features/specifications
            feature_bullets = soup.find('div', {'id': 'feature-bullets'})
            specs = extract_amazon_features(feature_bullets)
            
            return {
                'name': name,
                'brand': brand,
                'model': extract_model_from_name(name),
                'price': price,
                'category': 'Commercial Equipment',
                'specifications': specs,
                'supplier': 'Amazon',
                'source_url': url,
                'description': extract_description(soup)
            }
    
    except Exception as e:
        logging.error(f"Amazon parsing failed: {e}")
        return create_fallback_equipment_data(url, 'Amazon')

async def parse_generic_url(url: str) -> Dict:
    """Generic parser for any equipment website"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Generic extraction using common patterns
            name = extract_generic_title(soup)
            price = extract_generic_price(soup)
            brand = extract_generic_brand(soup)
            specs = extract_generic_specs(soup)
            
            domain = urlparse(url).netloc.replace('www.', '').title()
            
            return {
                'name': name,
                'brand': brand,
                'model': extract_model_from_name(name),
                'price': price,
                'category': 'Commercial Equipment',
                'specifications': specs,
                'supplier': domain,
                'source_url': url,
                'description': extract_description(soup)
            }
    
    except Exception as e:
        logging.error(f"Generic parsing failed: {e}")
        return create_fallback_equipment_data(url)

# Helper functions
def extract_price(price_text: str) -> float:
    """Extract price from text"""
    if not price_text:
        return 0.0
    
    # Remove currency symbols and extract number
    price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
    return float(price_match.group()) if price_match else 0.0

def extract_model_from_name(name: str) -> str:
    """Extract model number from product name"""
    # Look for model patterns (letters + numbers)
    model_match = re.search(r'\b[A-Z]{1,3}[-\s]?\d{2,6}[A-Z]?\b', name.upper())
    return model_match.group() if model_match else ""

def extract_category_from_breadcrumbs(breadcrumbs) -> str:
    """Extract category from breadcrumb navigation"""
    if not breadcrumbs:
        return "Equipment"
    
    links = breadcrumbs.find_all('a')
    if len(links) >= 2:
        return links[-2].get_text(strip=True)
    return "Equipment"

def extract_generic_title(soup) -> str:
    """Extract title using common patterns"""
    selectors = [
        'h1',
        '[data-testid*="title"]',
        '[class*="title"]',
        '[class*="product-name"]',
        'title'
    ]
    
    for selector in selectors:
        elem = soup.select_one(selector)
        if elem and len(elem.get_text(strip=True)) > 5:
            return elem.get_text(strip=True)
    
    return "Unknown Equipment"

def extract_generic_price(soup) -> float:
    """Extract price using common patterns"""
    price_selectors = [
        '[class*="price"]',
        '[data-testid*="price"]',
        '[class*="cost"]',
        '[class*="amount"]'
    ]
    
    for selector in price_selectors:
        elem = soup.select_one(selector)
        if elem:
            price_text = elem.get_text()
            if '$' in price_text or re.search(r'\d+\.?\d*', price_text):
                return extract_price(price_text)
    
    return 0.0

def extract_generic_brand(soup) -> str:
    """Extract brand using common patterns"""
    brand_selectors = [
        '[class*="brand"]',
        '[data-testid*="brand"]',
        '[class*="manufacturer"]'
    ]
    
    for selector in brand_selectors:
        elem = soup.select_one(selector)
        if elem:
            return elem.get_text(strip=True)
    
    return "Unknown Brand"

def extract_generic_specs(soup) -> Dict:
    """Extract specifications using common patterns"""
    specs = {}
    
    # Look for specification tables or lists
    spec_containers = soup.find_all(['table', 'ul', 'div'], class_=re.compile(r'spec|feature|detail', re.I))
    
    for container in spec_containers:
        rows = container.find_all(['tr', 'li', 'div'])
        for row in rows:
            text = row.get_text(strip=True)
            if ':' in text:
                key, value = text.split(':', 1)
                specs[key.strip()] = value.strip()
    
    return specs

def extract_description(soup) -> str:
    """Extract product description"""
    desc_selectors = [
        '[class*="description"]',
        '[class*="summary"]',
        '[data-testid*="description"]',
        'meta[name="description"]'
    ]
    
    for selector in desc_selectors:
        elem = soup.select_one(selector)
        if elem:
            if elem.name == 'meta':
                return elem.get('content', '')
            return elem.get_text(strip=True)[:500]  # Limit length
    
    return ""

def create_fallback_equipment_data(url: str, supplier: str = None) -> Dict:
    """Create fallback data when parsing fails"""
    domain = urlparse(url).netloc.replace('www.', '').title()
    supplier = supplier or domain
    
    return {
        'name': f"Equipment from {supplier}",
        'brand': "Unknown",
        'model': "",
        'price': 0.0,
        'category': 'Equipment',
        'specifications': {},
        'supplier': supplier,
        'source_url': url,
        'description': f"Equipment imported from {url}"
    }

# Placeholder functions for other suppliers
async def parse_homedepot_url(url: str) -> Dict:
    """Parse Home Depot commercial equipment pages"""
    return await parse_generic_url(url)

async def parse_restaurant_depot_url(url: str) -> Dict:
    """Parse Restaurant Depot pages"""
    return await parse_generic_url(url)

async def parse_katom_url(url: str) -> Dict:
    """Parse Katom Restaurant Supply pages"""
    return await parse_generic_url(url)

def extract_webstaurant_specs(soup) -> Dict:
    """Extract WebRestaurant-specific specifications"""
    specs = {}
    spec_table = soup.find('table', class_='specifications')
    if spec_table:
        rows = spec_table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                specs[key] = value
    return specs

def extract_brand_from_amazon(soup, name: str) -> str:
    """Extract brand from Amazon page"""
    # Try brand element first
    brand_elem = soup.find('a', {'id': 'bylineInfo'})
    if brand_elem:
        brand_text = brand_elem.get_text()
        if 'Brand:' in brand_text:
            return brand_text.split('Brand:')[1].strip()
    
    # Extract from product name
    common_brands = ['KitchenAid', 'Vitamix', 'Cuisinart', 'Hamilton Beach', 'Waring', 'Robot Coupe']
    for brand in common_brands:
        if brand.lower() in name.lower():
            return brand
    
    return "Unknown"

def extract_amazon_features(feature_bullets) -> Dict:
    """Extract Amazon feature bullets as specifications"""
    specs = {}
    if feature_bullets:
        bullets = feature_bullets.find_all('span', class_='a-list-item')
        for i, bullet in enumerate(bullets):
            text = bullet.get_text(strip=True)
            if text and len(text) > 10:
                specs[f"Feature {i+1}"] = text
    return specs

# WebstaurantStore Integration (Enhanced)
@router.get("/webstaurant/search")
async def search_webstaurant_store(
    query: str,
    category: Optional[str] = None,
    limit: int = 20
):
    """
    Search WebstaurantStore for equipment
    Enhanced with better mock data and real URL support
    """
    try:
        print(f"[DEBUG] Webstaurant search query: '{query}', category: '{category}', limit: {limit}")
        products = await simulate_webstaurant_search(query, category, limit)
        print(f"[DEBUG] Webstaurant search returned {len(products)} products")
        return {
            "success": True,
            "products": products,
            "total": len(products),
            "query": query,
            "category": category
        }
    except Exception as e:
        print(f"[ERROR] Webstaurant search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

async def simulate_webstaurant_search(query: str, category: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """
    Simulate WebstaurantStore search results
    In production, replace this with actual API calls
    """
    # Simulate network delay
    await asyncio.sleep(1)
    
    # Mock product database
    mock_products = [
        {
            "id": "ws-001",
            "name": "KitchenAid KSM150PSER Professional 5-Quart Stand Mixer",
            "brand": "KitchenAid",
            "model": "KSM150PSER",
            "category": "Large Equipment",
            "subcategory": "Mixers",
            "price": 399.99,
            "sale_price": 349.99,
            "description": "Professional 5-quart stand mixer with 10-speed motor and tilt-head design",
            "specifications": {
                "capacity": "5 quarts",
                "power": "325W",
                "speeds": "10 speeds",
                "attachments": "Flat beater, wire whip, dough hook",
                "dimensions": "14.5\"W x 8.5\"D x 15.5\"H",
                "weight": "23 lbs",
                "voltage": "120V"
            },
            "features": [
                "10-speed motor",
                "Tilt-head design",
                "Planetary mixing action",
                "Dishwasher-safe attachments",
                "Pouring shield included"
            ],
            "image_url": "https://via.placeholder.com/300x300?text=KitchenAid+Mixer",
            "product_url": "https://www.webstaurantstore.com/kitchenaid-ksm150pser-5-qt-professional-stand-mixer/150PSER.html",
            "availability": "In Stock",
            "shipping_weight": "25 lbs",
            "warranty": "1 year limited"
        },
        {
            "id": "ws-002",
            "name": "True T-49 49\" Reach-In Refrigerator",
            "brand": "True",
            "model": "T-49",
            "category": "Refrigeration",
            "subcategory": "Reach-In Refrigerators",
            "price": 2499.99,
            "sale_price": 2299.99,
            "description": "49\" reach-in refrigerator with glass door and digital temperature control",
            "specifications": {
                "capacity": "49 cubic feet",
                "temperature_range": "32-40°F",
                "dimensions": "49\"W x 33\"D x 84\"H",
                "door_type": "Glass door",
                "shelves": "5 adjustable",
                "defrost": "Automatic",
                "voltage": "115V/60Hz"
            },
            "features": [
                "Digital temperature control",
                "Glass door",
                "Adjustable shelves",
                "Automatic defrost",
                "Energy efficient"
            ],
            "image_url": "https://via.placeholder.com/300x300?text=True+Refrigerator",
            "product_url": "https://www.webstaurantstore.com/true-t-49-49-reach-in-refrigerator/184T49.html",
            "availability": "In Stock",
            "shipping_weight": "450 lbs",
            "warranty": "2 years parts, 1 year labor"
        },
        {
            "id": "ws-003",
            "name": "Robot Coupe R2N 2-Quart Food Processor",
            "brand": "Robot Coupe",
            "model": "R2N",
            "category": "Large Equipment",
            "subcategory": "Food Processors",
            "price": 899.99,
            "sale_price": 849.99,
            "description": "2-quart food processor with continuous feed and stainless steel bowl",
            "specifications": {
                "capacity": "2 quarts",
                "power": "1/3 HP",
                "feed": "Continuous",
                "bowl": "Stainless steel",
                "blade": "Reversible",
                "dimensions": "12\"W x 8\"D x 15\"H",
                "weight": "18 lbs"
            },
            "features": [
                "Continuous feed",
                "Stainless steel bowl",
                "Reversible blade",
                "Safety interlock",
                "Easy cleaning"
            ],
            "image_url": "https://via.placeholder.com/300x300?text=Robot+Coupe+Processor",
            "product_url": "https://www.webstaurantstore.com/robot-coupe-r2n-2-qt-food-processor/184R2N.html",
            "availability": "In Stock",
            "shipping_weight": "22 lbs",
            "warranty": "1 year"
        },
        {
            "id": "ws-004",
            "name": "Vollrath 68000 Induction Range",
            "brand": "Vollrath",
            "model": "68000",
            "category": "Large Equipment",
            "subcategory": "Ranges",
            "price": 1899.99,
            "sale_price": 1799.99,
            "description": "Induction range with 4 burners and digital controls",
            "specifications": {
                "burners": "4",
                "power": "240V",
                "dimensions": "30\"W x 24\"D x 4\"H",
                "material": "Stainless steel",
                "controls": "Digital",
                "safety": "Auto shut-off"
            },
            "features": [
                "Induction technology",
                "Digital controls",
                "Auto shut-off",
                "Stainless steel construction",
                "Energy efficient"
            ],
            "image_url": "https://via.placeholder.com/300x300?text=Vollrath+Range",
            "product_url": "https://www.webstaurantstore.com/vollrath-68000-induction-range/18468000.html",
            "availability": "In Stock",
            "shipping_weight": "85 lbs",
            "warranty": "2 years"
        },
        {
            "id": "ws-005",
            "name": "Hobart A200 Dishwasher",
            "brand": "Hobart",
            "model": "A200",
            "category": "Large Equipment",
            "subcategory": "Dishwashers",
            "price": 3499.99,
            "sale_price": 3299.99,
            "description": "Undercounter dishwasher with 200 racks per hour capacity",
            "specifications": {
                "capacity": "200 racks/hour",
                "rack_size": "18\" x 18\"",
                "dimensions": "24\"W x 24\"D x 34\"H",
                "voltage": "208V/240V",
                "water_consumption": "0.5 gallons/rack",
                "temperature": "180°F final rinse"
            },
            "features": [
                "High capacity",
                "Energy efficient",
                "Low water consumption",
                "High temperature sanitizing",
                "Easy maintenance"
            ],
            "image_url": "https://via.placeholder.com/300x300?text=Hobart+Dishwasher",
            "product_url": "https://www.webstaurantstore.com/hobart-a200-undercounter-dishwasher/184A200.html",
            "availability": "In Stock",
            "shipping_weight": "350 lbs",
            "warranty": "2 years parts, 1 year labor"
        }
    ]
    
    # Filter products based on query and category
    filtered_products = []
    query_lower = query.lower()
    
    for product in mock_products:
        # Check if product matches query
        matches_query = (
            query_lower in product["name"].lower() or
            query_lower in product["brand"].lower() or
            query_lower in product["category"].lower() or
            query_lower in product["subcategory"].lower() or
            query_lower in product["description"].lower()
        )
        
        # Check if product matches category filter
        matches_category = True
        if category:
            category_lower = category.lower()
            matches_category = (
                category_lower in product["category"].lower() or
                category_lower in product["subcategory"].lower()
            )
        
        if matches_query and matches_category:
            filtered_products.append(product)
            
        # Limit results
        if len(filtered_products) >= limit:
            break
    
    return filtered_products

@router.get("/webstaurant/categories")
async def get_webstaurant_categories():
    """Get available equipment categories from WebstaurantStore"""
    categories = [
        {"id": "refrigeration", "name": "Refrigeration", "icon": "❄️"},
        {"id": "cooking", "name": "Cooking Equipment", "icon": "🔥"},
        {"id": "preparation", "name": "Food Preparation", "icon": "🔪"},
        {"id": "storage", "name": "Storage & Shelving", "icon": "📦"},
        {"id": "cleaning", "name": "Cleaning Equipment", "icon": "🧽"},
        {"id": "safety", "name": "Safety Equipment", "icon": "🛡️"},
        {"id": "smallwares", "name": "Smallwares", "icon": "🥄"},
        {"id": "beverage", "name": "Beverage Equipment", "icon": "🥤"},
        {"id": "baking", "name": "Baking Equipment", "icon": "🍞"},
        {"id": "serving", "name": "Serving Equipment", "icon": "🍽️"}
    ]
    
    return {
        "success": True,
        "categories": categories
    }

@router.get("/webstaurant/product/{product_id}")
async def get_webstaurant_product(product_id: str):
    """Get detailed product information from WebstaurantStore"""
    try:
        # In real implementation, fetch from WebstaurantStore API
        # For now, return mock data
        products = await simulate_webstaurant_search("", limit=100)
        product = next((p for p in products if p["id"] == product_id), None)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "success": True,
            "product": product
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch product: {str(e)}")

# Future: Add real WebstaurantStore API integration
async def real_webstaurant_api_search(query: str, api_key: str) -> List[Dict]:
    """
    Real WebstaurantStore API integration (placeholder)
    You would need to:
    1. Sign up for WebstaurantStore API access
    2. Get API credentials
    3. Implement proper authentication
    4. Handle rate limiting
    5. Parse their response format
    """
    # Example implementation structure:
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        params = {
            "q": query,
            "limit": 20,
            "format": "json"
        }
        
        response = await client.get(
            "https://api.webstaurantstore.com/v1/products/search",
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("products", [])
        else:
            raise HTTPException(status_code=response.status_code, detail="API request failed")
    """
    # Placeholder - returns empty list for now
    return [] 
#!/usr/bin/env python3
"""
Load Comprehensive Equipment Database
Loads equipment from CSV files into the SQLite database and updates frontend defaults
"""

import csv
import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path
import re

def parse_price(price_str):
    """Parse price string and handle various formats"""
    if not price_str or price_str.strip() == '':
        return 0.0
    
    # Remove any quotes and clean the string
    price_str = str(price_str).strip(' "\'')
    
    # Extract numbers and decimal points
    price_match = re.search(r'[\d,]+\.?\d*', price_str)
    if price_match:
        price_clean = price_match.group().replace(',', '')
        try:
            return float(price_clean)
        except ValueError:
            return 0.0
    return 0.0

def load_equipment_from_csv():
    """Load equipment from CSV files into the database"""
    
    # Connect to the database
    db_path = "culinary_data.db"
    equipment_data = []
    
    # Load professional equipment from main database
    professional_file = "equipment_database.csv"
    if os.path.exists(professional_file):
        print(f"Loading professional equipment from {professional_file}...")
        with open(professional_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                equipment_data.append({
                    'name': row['name'],
                    'category': row['category'],
                    'brand': row.get('brand', 'Standard'),
                    'model': row.get('model', ''),
                    'specifications': row.get('specs', ''),
                    'purchase_date': row.get('purchase_date', ''),
                    'price': parse_price(row.get('price', '0')),
                    'status': row.get('status', 'Active'),
                    'location': row.get('location', ''),
                    'maintenance_notes': row.get('notes', ''),
                    'spec_url': row.get('spec_url', ''),
                    'manual_url': row.get('manual_url', ''),
                    'service_provider': row.get('service_provider', ''),
                    'service_phone': row.get('service_phone', ''),
                    'is_global': True,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                })
    
    # Load basic equipment from starter template
    starter_file = "archive/templates/starter_equipment_database.csv"
    if os.path.exists(starter_file):
        print(f"Loading starter equipment from {starter_file}...")
        with open(starter_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                equipment_data.append({
                    'name': row['name'],
                    'category': row['category'],
                    'brand': row.get('brand', 'Standard'),
                    'model': row.get('model', ''),
                    'specifications': '',
                    'purchase_date': '',
                    'price': 0,
                    'status': 'Active',
                    'location': 'Kitchen',
                    'maintenance_notes': row.get('notes', ''),
                    'spec_url': '',
                    'manual_url': '',
                    'service_provider': '',
                    'service_phone': '',
                    'is_global': True,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                })
    
    return equipment_data

def insert_equipment_to_database(equipment_data):
    """Insert equipment data into SQLite database"""
    
    db_path = "culinary_data.db"
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Check if equipment table exists and get its schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='equipment'")
        existing_table = cursor.fetchone()
        
        if existing_table:
            print("Equipment table exists, checking schema...")
            # Check if user_id column exists
            cursor.execute("PRAGMA table_info(equipment)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'user_id' not in columns:
                print("Adding user_id column to equipment table...")
                cursor.execute('ALTER TABLE equipment ADD COLUMN user_id TEXT DEFAULT NULL')
            
            # Clear existing global equipment (user_id IS NULL or missing)
            try:
                cursor.execute('DELETE FROM equipment WHERE user_id IS NULL OR user_id = ""')
            except sqlite3.OperationalError:
                # If user_id column doesn't exist, clear all equipment
                cursor.execute('DELETE FROM equipment')
        else:
            print("Creating new equipment table...")
            # Create new table with proper schema
            cursor.execute('''
                CREATE TABLE equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    brand TEXT,
                    model TEXT,
                    specifications TEXT,
                    purchase_date TEXT,
                    price REAL,
                    status TEXT DEFAULT 'Active',
                    location TEXT,
                    maintenance_notes TEXT,
                    warranty_info TEXT,
                    spec_url TEXT,
                    manual_url TEXT,
                    service_provider TEXT,
                    service_phone TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    user_id TEXT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
        print("Cleared existing global equipment...")
        
        # Check what columns exist in the current table
        cursor.execute("PRAGMA table_info(equipment)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        print(f"Existing columns: {existing_columns}")
        
        # Add missing columns if needed
        additional_columns = [
            ('brand', 'TEXT'),
            ('model', 'TEXT'), 
            ('price', 'REAL'),
            ('spec_url', 'TEXT'),
            ('manual_url', 'TEXT'),
            ('service_provider', 'TEXT'),
            ('service_phone', 'TEXT')
        ]
        
        for col_name, col_type in additional_columns:
            if col_name not in existing_columns:
                print(f"Adding {col_name} column...")
                cursor.execute(f'ALTER TABLE equipment ADD COLUMN {col_name} {col_type}')
                existing_columns.append(col_name)
        
        # Insert new global equipment
        for equipment in equipment_data:
            # Create description from brand and model
            description_parts = []
            if equipment.get('brand') and equipment['brand'] != 'Standard':
                description_parts.append(equipment['brand'])
            if equipment.get('model'):
                description_parts.append(equipment['model'])
            description = ' '.join(description_parts) if description_parts else ''
            
            cursor.execute('''
                INSERT INTO equipment (
                    name, category, description, specifications, purchase_date, 
                    status, location, maintenance_notes, warranty_info, created_at, updated_at, user_id,
                    brand, model, price, spec_url, manual_url, service_provider, service_phone
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                equipment['name'], equipment['category'], description,
                equipment['specifications'], equipment['purchase_date'],
                equipment['status'], equipment['location'], 
                equipment['maintenance_notes'], '', 
                equipment['created_at'], equipment['updated_at'],
                equipment['brand'], equipment['model'], equipment['price'],
                equipment['spec_url'], equipment['manual_url'],
                equipment['service_provider'], equipment['service_phone']
            ))
        
        conn.commit()
        print(f"Inserted {len(equipment_data)} equipment items into database")

def create_enhanced_frontend_defaults():
    """Create enhanced default equipment list for frontend"""
    
    # Essential equipment for new users (curated from comprehensive list)
    enhanced_defaults = [
        {
            "id": 1, "name": "Chef's Knife", "category": "Cutlery", "brand": "Standard", 
            "model": "8-inch", "location": "Kitchen", "status": "Active",
            "notes": "Primary cutting tool - keep sharp"
        },
        {
            "id": 2, "name": "Cutting Board", "category": "Prep Equipment", "brand": "Standard", 
            "model": "Large Wooden", "location": "Prep Station", "status": "Active",
            "notes": "Sanitize regularly"
        },
        {
            "id": 3, "name": "Measuring Cups", "category": "Tools", "brand": "Standard", 
            "model": "Set", "location": "Prep Station", "status": "Active",
            "notes": "Dry and liquid measures"
        },
        {
            "id": 4, "name": "Measuring Spoons", "category": "Tools", "brand": "Standard", 
            "model": "Set", "location": "Prep Station", "status": "Active",
            "notes": "Small measurements"
        },
        {
            "id": 5, "name": "Mixing Bowls", "category": "Prep Equipment", "brand": "Standard", 
            "model": "Set of 3", "location": "Prep Station", "status": "Active",
            "notes": "Various sizes"
        },
        {
            "id": 6, "name": "Whisk", "category": "Tools", "brand": "Standard", 
            "model": "Balloon", "location": "Utensil Drawer", "status": "Active",
            "notes": "For mixing and aerating"
        },
        {
            "id": 7, "name": "Spatula", "category": "Tools", "brand": "Standard", 
            "model": "Rubber", "location": "Utensil Drawer", "status": "Active",
            "notes": "For scraping and folding"
        },
        {
            "id": 8, "name": "Tongs", "category": "Tools", "brand": "Standard", 
            "model": "12-inch", "location": "Utensil Drawer", "status": "Active",
            "notes": "For handling hot items"
        },
        {
            "id": 9, "name": "Colander", "category": "Tools", "brand": "Standard", 
            "model": "Large", "location": "Prep Station", "status": "Active",
            "notes": "For draining pasta and vegetables"
        },
        {
            "id": 10, "name": "Digital Scale", "category": "Tools", "brand": "Standard", 
            "model": "Kitchen Scale", "location": "Prep Station", "status": "Active",
            "notes": "For precise measurements"
        },
        {
            "id": 11, "name": "Saucepan", "category": "Cookware", "brand": "Standard", 
            "model": "2-Qt", "location": "Stove Area", "status": "Active",
            "notes": "For sauces and small quantities"
        },
        {
            "id": 12, "name": "Frying Pan", "category": "Cookware", "brand": "Standard", 
            "model": "10-inch", "location": "Stove Area", "status": "Active",
            "notes": "Non-stick preferred"
        },
        {
            "id": 13, "name": "Baking Sheet", "category": "Cookware", "brand": "Standard", 
            "model": "Half Sheet", "location": "Oven Area", "status": "Active",
            "notes": "For roasting and baking"
        },
        {
            "id": 14, "name": "Grater", "category": "Tools", "brand": "Standard", 
            "model": "Box Grater", "location": "Prep Station", "status": "Active",
            "notes": "Multiple grating surfaces"
        },
        {
            "id": 15, "name": "Peeler", "category": "Tools", "brand": "Standard", 
            "model": "Swivel", "location": "Utensil Drawer", "status": "Active",
            "notes": "For vegetables and fruits"
        }
    ]
    
    # Add maintenance dates to each item
    current_time = datetime.now().isoformat()
    for item in enhanced_defaults:
        item["last_maintenance"] = current_time
        # Set different maintenance intervals based on equipment type
        if item["category"] in ["Cutlery"]:
            next_maintenance_days = 90  # Knives need sharpening
        elif item["category"] in ["Prep Equipment", "Tools"]:
            next_maintenance_days = 60  # Regular cleaning/inspection
        else:
            next_maintenance_days = 30  # Frequent use items
            
        next_maintenance = datetime.fromtimestamp(
            datetime.now().timestamp() + (next_maintenance_days * 24 * 60 * 60)
        ).isoformat()
        item["next_maintenance"] = next_maintenance
    
    # Save enhanced defaults to a JavaScript file
    js_content = f"""// Enhanced Default Equipment for New Users
// Auto-generated by load_comprehensive_equipment.py

const ENHANCED_DEFAULT_EQUIPMENT = {json.dumps(enhanced_defaults, indent=2)};

// Export for use in userDataManager.js
if (typeof module !== 'undefined' && module.exports) {{
    module.exports = ENHANCED_DEFAULT_EQUIPMENT;
}}

// Make available globally in browser
if (typeof window !== 'undefined') {{
    window.ENHANCED_DEFAULT_EQUIPMENT = ENHANCED_DEFAULT_EQUIPMENT;
}}
"""
    
    with open('enhanced_default_equipment.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"Created enhanced_default_equipment.js with {len(enhanced_defaults)} items")
    return enhanced_defaults

def main():
    """Main function to load comprehensive equipment data"""
    print("🍳 Loading Comprehensive Equipment Database...")
    print("=" * 50)
    
    # Load equipment from CSV files
    equipment_data = load_equipment_from_csv()
    print(f"Loaded {len(equipment_data)} equipment items from CSV files")
    
    # Insert into database
    insert_equipment_to_database(equipment_data)
    
    # Create enhanced frontend defaults
    enhanced_defaults = create_enhanced_frontend_defaults()
    
    print("\n✅ Equipment loading completed!")
    print(f"Database: {len(equipment_data)} global equipment items")
    print(f"Frontend: {len(enhanced_defaults)} default equipment items")
    print("\nNext steps:")
    print("1. New users will get enhanced default equipment")
    print("2. Users can browse comprehensive equipment database")
    print("3. Equipment can be added from global database to personal inventory")

if __name__ == "__main__":
    main() 
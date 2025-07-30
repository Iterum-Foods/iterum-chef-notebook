# 🏪 Vendor & Equipment Management Guide

## 🚀 Quick Start

### 1. Import Your Vendor Data

If you have vendor data in CSV format, import it using the provided script:

```bash
python import_vendors.py "path/to/your/vendor-list.csv"
```

**CSV Format Requirements:**
- Columns: `Name, Company, Email, Phone, Mobile, Fax, Website, Street, City, State, ZIP`
- First row should be headers
- Empty cells are allowed

### 2. Start the Application

```bash
python -m app.main
```

The server will start on `http://localhost:8000`

### 3. Access the Management Interface

Open `vendor-management.html` in your web browser, or access the API directly:

- **API Documentation**: `http://localhost:8000/docs`
- **Vendor Management UI**: Open `vendor-management.html` in your browser

## 📊 API Endpoints

### Vendor Management

#### Get All Vendors
```bash
GET http://localhost:8000/api/vendors/
```

#### Search Vendors
```bash
GET http://localhost:8000/api/vendors/?search=baldor
```

#### Get Specific Vendor
```bash
GET http://localhost:8000/api/vendors/1
```

#### Create New Vendor
```bash
POST http://localhost:8000/api/vendors/
Content-Type: application/json

{
  "name": "John Doe",
  "company": "Fresh Foods Inc",
  "email": "john@freshfoods.com",
  "phone": "555-1234",
  "city": "Boston",
  "state": "MA",
  "specialties": ["produce", "dairy"],
  "notes": "Reliable supplier"
}
```

#### Update Vendor
```bash
PUT http://localhost:8000/api/vendors/1
Content-Type: application/json

{
  "notes": "Updated notes about this vendor"
}
```

#### Delete Vendor
```bash
DELETE http://localhost:8000/api/vendors/1
```

### Equipment Management

#### Get All Equipment
```bash
GET http://localhost:8000/api/vendors/equipment
```

#### Create New Equipment
```bash
POST http://localhost:8000/api/vendors/equipment
Content-Type: application/json

{
  "name": "Commercial Blender",
  "category": "Food Processing",
  "description": "High-speed commercial blender",
  "location": "Kitchen A",
  "status": "active",
  "maintenance_notes": "Annual service due in March"
}
```

#### Update Equipment
```bash
PUT http://localhost:8000/api/vendors/equipment/1
Content-Type: application/json

{
  "status": "maintenance",
  "maintenance_notes": "Currently being serviced"
}
```

### Vendor Relationships

#### Add Ingredient to Vendor
```bash
POST http://localhost:8000/api/vendors/1/ingredients
Content-Type: application/json

{
  "ingredient_id": 1,
  "price": 2.50,
  "unit": "lb",
  "availability": "in stock",
  "minimum_order": 10.0,
  "lead_time_days": 2
}
```

#### Add Equipment to Vendor
```bash
POST http://localhost:8000/api/vendors/1/equipment
Content-Type: application/json

{
  "equipment_id": 1,
  "price": 1500.00,
  "availability": "in stock",
  "warranty_offered": "2 years",
  "service_support": "24/7 support available"
}
```

## 🎨 Using the Web Interface

### Vendor Management Tab
1. **View Vendors**: See all vendors in a searchable table
2. **Add Vendor**: Click "Add Vendor" to create a new vendor
3. **Edit Vendor**: Click "Edit" on any vendor row
4. **Delete Vendor**: Click "Delete" to remove a vendor
5. **Search**: Use the search bar to find specific vendors

### Equipment Management Tab
1. **View Equipment**: See all equipment in a searchable table
2. **Add Equipment**: Click "Add Equipment" to create new equipment
3. **Edit Equipment**: Click "Edit" on any equipment row
4. **Delete Equipment**: Click "Delete" to remove equipment
5. **Search**: Use the search bar to find specific equipment

### Relationships Tab
- **Coming Soon**: Interface for managing vendor-ingredient and vendor-equipment relationships

## 📋 Database Schema

### Vendors Table
```sql
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    company TEXT,
    email TEXT,
    phone TEXT,
    mobile TEXT,
    fax TEXT,
    website TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    specialties TEXT,  -- JSON array
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TEXT NOT NULL,
    updated_at TEXT
);
```

### Equipment Table
```sql
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    description TEXT,
    specifications TEXT,  -- JSON object
    maintenance_notes TEXT,
    purchase_date TEXT,
    warranty_info TEXT,
    location TEXT,
    status TEXT DEFAULT 'active',
    created_at TEXT NOT NULL,
    updated_at TEXT
);
```

### Vendor Relationships
```sql
-- Vendor-Ingredient relationships
CREATE TABLE vendor_ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER,
    ingredient_id INTEGER,
    price REAL,
    unit TEXT,
    availability TEXT,
    minimum_order REAL,
    lead_time_days INTEGER,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors (id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
);

-- Vendor-Equipment relationships
CREATE TABLE vendor_equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER,
    equipment_id INTEGER,
    price REAL,
    availability TEXT,
    warranty_offered TEXT,
    service_support TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors (id),
    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
);
```

## 🔧 Configuration

### Environment Variables
The vendor management system uses the same configuration as the main application:

```env
DATABASE_URL=sqlite:///./culinary_data.db
SECRET_KEY=your-secret-key-here
```

### Database Location
- **Default**: `culinary_data.db` in the project root
- **Custom**: Set `DATABASE_URL` environment variable

## 🧪 Testing

### Test the API
Run the provided test script:

```bash
python test_vendor_api.py
```

This will test all vendor and equipment endpoints.

### Manual Testing
1. Start the server: `python -m app.main`
2. Open `http://localhost:8000/docs` in your browser
3. Use the interactive API documentation to test endpoints

## 📊 Data Import

### CSV Import Format
Your CSV file should have these columns (in any order):

| Column | Description | Required |
|--------|-------------|----------|
| Name | Contact person name | Yes |
| Company | Company name | No |
| Email | Email address | No |
| Phone | Phone number | No |
| Mobile | Mobile number | No |
| Fax | Fax number | No |
| Website | Company website | No |
| Street | Street address | No |
| City | City | No |
| State | State/province | No |
| ZIP | ZIP/postal code | No |

### Import Process
1. Prepare your CSV file with the required columns
2. Run: `python import_vendors.py "path/to/your/file.csv"`
3. Check the output for any import errors
4. Verify data in the web interface or API

## 🎯 Best Practices

### Vendor Management
1. **Consistent Naming**: Use consistent naming conventions for vendors
2. **Complete Information**: Fill in as much contact information as possible
3. **Specialties**: Use the specialties field to categorize vendors
4. **Active Status**: Mark inactive vendors as inactive rather than deleting them
5. **Notes**: Use notes for important information like payment terms, delivery preferences

### Equipment Management
1. **Categories**: Use consistent categories for equipment
2. **Location Tracking**: Keep equipment locations updated
3. **Maintenance**: Regular maintenance notes help with scheduling
4. **Status Updates**: Update equipment status when maintenance is needed
5. **Warranty Info**: Track warranty information for service planning

### Data Relationships
1. **Vendor-Ingredient Links**: Connect vendors to the ingredients they supply
2. **Pricing**: Track pricing information for cost analysis
3. **Availability**: Monitor availability for planning
4. **Lead Times**: Track lead times for ordering
5. **Service Information**: Record service and warranty details for equipment

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
- **File not found**: Check the file path is correct
- **Encoding issues**: Ensure CSV is UTF-8 encoded
- **Column mismatch**: Verify column names match expected format

#### API Connection Issues
- **Server not running**: Start with `python -m app.main`
- **Wrong port**: Default is 8000, check if another service is using it
- **CORS issues**: Check browser console for CORS errors

#### Database Issues
- **Permission errors**: Ensure write permissions to database file
- **Corrupted database**: Delete `culinary_data.db` and restart
- **Migration issues**: Run `python run_migration.py`

### Getting Help
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the test script `test_vendor_api.py` for examples
3. Check the main README.md for general application help
4. Review the feature map in `FEATURE_MAP.md`

## 📈 Next Steps

### Immediate
1. Import your vendor data using the CSV import
2. Add your kitchen equipment to the system
3. Connect vendors to ingredients and equipment
4. Test the search and filtering features

### Future Enhancements
- Bulk import for vendor relationships
- Advanced reporting and analytics
- Integration with inventory systems
- Mobile application for field use
- Automated maintenance scheduling

---

**Need Help?** Check the main README.md or create an issue in the project repository. 
# 🏪 Vendor Management System Guide

## 🚀 Quick Start

### 1. Access the Vendor Management Interface

Open `vendor-management.html` in your web browser to access the new, upgraded vendor management system.

### 2. Import Your Vendor Data

**Option A: Drag & Drop Import**
1. Click the **"Import"** button
2. Drag and drop your CSV/Excel file directly onto the import area
3. The system will automatically process and import your data

**Option B: File Selection Import**
1. Click the **"Import"** button
2. Click **"Choose File"** and select your vendor data file
3. Supported formats: CSV, Excel (.xlsx, .xls)

**Option C: Download Template First**
1. Click **"Download Template"** to get a sample CSV file
2. Fill in your vendor data using the template format
3. Import your completed file

### 3. Start the Application

```bash
python -m app.main
```

The server will start on `http://localhost:8000`

## 🎨 New User Interface Features

### **Modern Dashboard**
- **Statistics Grid**: Total vendors, active vendors, total value, and average rating
- **Advanced Search**: Search across vendor names, companies, locations, and specialties
- **Filtering Options**: Filter by status, specialties, location, and rating
- **Bulk Operations**: Select multiple vendors for batch actions

### **Enhanced Import System**
- **Drag & Drop**: Simply drag files onto the import area
- **Template Download**: Get a pre-formatted CSV template
- **Real-time Preview**: See imported data before applying
- **Error Handling**: Clear feedback on import issues
- **Auto-mapping**: Intelligent column detection and mapping

### **Vendor Management**
- **Add/Edit Vendors**: Comprehensive forms with validation
- **Bulk Operations**: Edit or delete multiple vendors at once
- **Advanced Filtering**: Filter by multiple criteria simultaneously
- **Export Functionality**: Export vendor data in multiple formats

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

#### Bulk CSV Import
```bash
POST http://localhost:8000/api/vendors/import-csv
Content-Type: multipart/form-data

file: [CSV file]
```

## 🎨 Using the New Web Interface

### **Main Dashboard**
1. **Statistics Overview**: View total vendors, active count, and system metrics
2. **Quick Actions**: Add vendor, import data, or export existing data
3. **Search & Filter**: Find vendors quickly with advanced search options

### **Vendor Management**
1. **View Vendors**: See all vendors in a modern, sortable table
2. **Add Vendor**: Click "Add Vendor" for comprehensive vendor creation
3. **Edit Vendor**: Click "Edit" on any vendor row for quick updates
4. **Delete Vendor**: Remove vendors with confirmation dialogs
5. **Bulk Actions**: Select multiple vendors for batch operations

### **Import & Export**
1. **Import Data**: Use drag & drop or file selection for bulk imports
2. **Template Download**: Get a pre-formatted CSV template
3. **Export Data**: Export vendor data in CSV or JSON format
4. **Data Validation**: Real-time validation during import

### **Advanced Features**
1. **Smart Filtering**: Filter by multiple criteria simultaneously
2. **Search**: Full-text search across all vendor fields
3. **Sorting**: Sort by any column for better organization
4. **Responsive Design**: Works on desktop, tablet, and mobile

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

This will test all vendor endpoints including the new CSV import functionality.

### Manual Testing
1. Start the server: `python -m app.main`
2. Open `http://localhost:8000/docs` in your browser
3. Use the interactive API documentation to test endpoints
4. Open `vendor-management.html` to test the new frontend

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
| Specialties | Comma-separated specialties | No |
| Notes | Additional notes | No |

### Import Process
1. **Prepare your CSV file** with the required columns
2. **Drag & drop** or select your file in the import modal
3. **Review the preview** to ensure data is correct
4. **Apply the import** to add vendors to your system
5. **Verify data** in the vendor management interface

### Import Features
- **Auto-mapping**: System automatically detects column headers
- **Data validation**: Checks for required fields and data formats
- **Error reporting**: Clear feedback on any import issues
- **Preview mode**: See exactly what will be imported
- **Batch processing**: Handle large files efficiently

## 🎯 Best Practices

### Vendor Management
1. **Consistent Naming**: Use consistent naming conventions for vendors
2. **Complete Information**: Fill in as much contact information as possible
3. **Specialties**: Use the specialties field to categorize vendors
4. **Active Status**: Mark inactive vendors as inactive rather than deleting them
5. **Notes**: Use notes for important information like payment terms, delivery preferences

### Data Import
1. **Use Templates**: Start with the provided CSV template
2. **Validate Data**: Check your data before importing
3. **Backup First**: Export existing data before large imports
4. **Test Imports**: Use small files to test the import process
5. **Review Results**: Always review imported data for accuracy

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
- **File not found**: Check the file path is correct
- **Encoding issues**: Ensure CSV is UTF-8 encoded
- **Column mismatch**: Verify column names match expected format
- **Large files**: Break very large files into smaller chunks

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
1. **Import your vendor data** using the new CSV import system
2. **Explore the new interface** and familiarize yourself with features
3. **Test bulk operations** with multiple vendor selection
4. **Use advanced filtering** to organize your vendor data

### Future Enhancements
- **Vendor ratings and reviews**
- **Advanced reporting and analytics**
- **Integration with inventory systems**
- **Mobile application for field use**
- **Automated vendor communication**

---

**Need Help?** Check the main README.md or create an issue in the project repository. 
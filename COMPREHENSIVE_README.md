# 🍳 Iterum R&D Chef Notebook – Complete Guide

A modern, full-featured culinary management system for R&D kitchens, chefs, and food businesses. Built with FastAPI and a modern HTML/JS frontend.

---

## 🚀 Quick Start

### **Immediate Launch**
1. **Double-click `start.bat`** to start the application (main entry point)
2. **Double-click `test_unified.bat`** for a full system test
3. Your browser will open automatically at `http://localhost:8080`

### **Prerequisites**
- Windows PC
- Python 3.9+ ([Download here](https://www.python.org/downloads/))
- Node.js (optional, for advanced features)

### **What Happens on Launch**
- Automatic Python and dependency checking
- Virtual environment setup if needed
- Backend (FastAPI) and frontend servers start
- Database initialization
- Browser opens to the main application

### **To Stop the App**
- Press `Ctrl+C` in the command window
- Or close all application windows

---

## ✨ Core Features

### 🧑‍🍳 **User Management**
- **Forced user selection**: Choose or create a profile before using the app
- **Per-user data libraries**: Personal ingredient, vendor, and equipment collections
- **Global shared data**: Access organization-wide resources
- **Switch users anytime**: Change context instantly
- **Authentication**: JWT-based login system with role management

### 📚 **Recipe Management**
- **Create, edit, delete, and organize recipes**
- **Hierarchical recipes**: Dishes can include prep recipes/components
- **Recipe versioning**: Track changes and revert to previous versions
- **Multi-format import**: Upload from PDF, Excel, Word, CSV, and text files
- **URL import**: Import recipes from popular cooking websites
- **Advanced search/filtering**: Search by ingredient, allergen, tags, cuisine, difficulty
- **Review & approval workflow**: Approve/reject imported recipes
- **Smart scaling**: Scale recipes with intelligent unit conversion
- **Image management**: Upload and display recipe photos

### 🏪 **Inventory & Equipment Management**
- **Ingredient libraries**: Per-user and global ingredient databases
- **Vendor integration**: Manage suppliers and import from CSV
- **Equipment tracking**: Manage kitchen equipment, maintenance, vendor relationships
- **URL import**: Import equipment from e-commerce websites
- **Bulk operations**: Import, export, delete multiple items

### 🔄 **Automated Workflows**
- **Recipe processing**: Automatic file monitoring and import
- **Batch operations**: Process multiple recipes simultaneously
- **Data validation**: Automatic content verification
- **Backup systems**: Local and automated data backups

---

## 🛠️ Testing & Development

### **Test Suite Options**
Use the unified test launcher for all testing needs:

```bash
# Interactive menu
test_unified.bat

# Quick tests (fastest)
test_unified.bat --quick

# Full test suite with coverage
test_unified.bat --full

# CI/CD mode
test_unified.bat --ci --verbose
```

### **Test Coverage**
- **Unit tests**: Core functionality verification
- **Integration tests**: API endpoint testing
- **Frontend tests**: JavaScript functionality
- **Performance tests**: Response time validation
- **Linting**: Code quality checks
- **Security tests**: Vulnerability scanning

### **Development Tools**
- **Hot reload**: Automatic restart on code changes
- **Debug mode**: Detailed error reporting
- **API documentation**: Auto-generated OpenAPI docs
- **Database tools**: Migration and backup utilities

---

## 📁 Project Structure

```
Iterum-App/
├── app/                        # Backend FastAPI application
│   ├── main.py                 # Application entry point
│   ├── database.py             # Database models and connection
│   ├── routers/                # API endpoint definitions
│   └── services/               # Business logic
├── static/                     # Frontend assets
├── tests/                      # Test suite
├── iterum-test-distribution/   # Testing package
├── profiles/                   # User profile data
├── uploads/                    # Recipe file uploads
└── logs/                       # Application logs
```

### **Key Files**
- `start.bat` - **Main application launcher** (double-click to start)
- `test_unified.bat` - Unified test runner (all testing needs)
- `clear_users.bat` - User management tool
- `python_detection.bat` - Shared Python detection module
- `launch_unified.bat` - Advanced launcher with options
- `app_launcher.py` - Python launcher (advanced users)
- `index.html` - Main application interface
- `requirements.txt` - Python dependencies
- `culinary_data.db` - Main database

---

## 🔧 Advanced Configuration

### **Environment Setup**
The application automatically handles:
- Virtual environment creation
- Dependency installation
- Database initialization
- Configuration management

### **Custom Configuration**
- **Database**: SQLite by default, PostgreSQL supported
- **Authentication**: JWT tokens, configurable expiration
- **File Storage**: Local filesystem, cloud storage planned
- **API Settings**: CORS, rate limiting, logging levels

### **Performance Optimization**
- **Caching**: In-memory caching for frequent queries
- **Database indexing**: Optimized search performance
- **Image compression**: Automatic photo optimization
- **Lazy loading**: Progressive content loading

---

## 🛡️ Security & Permissions

### **Authentication**
- JWT-based token authentication
- Role-based access control (Admin, Chef, User)
- Session management and timeout
- Password hashing with bcrypt

### **Data Protection**
- Input validation and sanitization
- XSS/CSRF/SQL injection protection
- Secure file upload handling
- Audit logging for all changes

### **Privacy**
- Per-user data isolation
- Configurable data sharing levels
- Export/import for data portability
- GDPR compliance features planned

---

## 📱 User Interface

### **Modern Design**
- Responsive HTML/CSS interface
- Mobile-friendly layout
- Dark/light theme support
- Accessibility compliance

### **Navigation**
- Unified menu system
- Breadcrumb navigation
- Search everywhere functionality
- Keyboard shortcuts

### **User Experience**
- Drag-and-drop file uploads
- Real-time search suggestions
- Progressive loading
- Error handling with user-friendly messages

---

## 🔄 Data Management

### **Import/Export**
- **Bulk operations**: JSON/CSV for all data types
- **File formats**: Excel, Word, PDF, text files
- **URL parsing**: Automatic content extraction
- **Validation**: Data integrity checking

### **Backup & Recovery**
- **Automatic backups**: Scheduled data snapshots
- **Manual export**: On-demand data downloads
- **Migration tools**: Database schema updates
- **Recovery procedures**: Data restoration workflows

---

## 🚨 Troubleshooting

### **Common Issues**
1. **Python not found**: 
   - Our launchers automatically detect Python in multiple locations
   - If still failing, install Python 3.9+ from [python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation
   - See `PYTHON_DETECTION_FIX.md` for detailed fix information
2. **Port conflicts**: Change port in configuration
3. **Database issues**: Clear database or restore from backup
4. **Permission errors**: Run as administrator if needed

### **Getting Help**
- Check logs in `logs/` directory
- Run `test_unified.bat --verbose` for detailed diagnostics
- Review error messages in browser console
- Consult API documentation at `http://localhost:8000/docs`

### **Reset Procedures**
- **Clear users**: Run `clear_users.bat`
- **Reset database**: Delete `culinary_data.db` and restart
- **Clean installation**: Delete `venv/` folder and restart

---

## 🔮 Roadmap

### **Planned Features**
- React/Vue frontend migration
- Cloud deployment options
- Mobile applications
- Advanced analytics
- AI-powered recipe suggestions
- Nutritional analysis
- Multi-language support

### **Integration Plans**
- POS system integration
- Inventory management systems
- External recipe databases
- Social sharing features
- Collaborative editing

---

## 💡 Tips & Best Practices

### **Recipe Management**
- Use descriptive names and tags
- Include detailed ingredient information
- Add cooking notes and variations
- Maintain version history

### **Equipment Tracking**
- Regular maintenance schedules
- Vendor contact information
- Purchase and warranty dates
- Usage statistics

### **Data Organization**
- Consistent naming conventions
- Regular backups
- User access reviews
- Performance monitoring

---

## 📞 Support

For issues, suggestions, or contributions:
- Check the troubleshooting section above
- Review logs for error details
- Run diagnostic tests
- Contact the development team

**Version**: 2.0+  
**Last Updated**: January 2025  
**License**: Proprietary - Iterum R&D 
# Professional Payroll System

A comprehensive payroll management application designed for small to medium businesses. Features multi-profile support, employee management, automated payroll calculations, and professional reporting capabilities.

## 🚀 Features

- **Multi-Profile Support**: Manage multiple businesses/locations with separate databases
- **Employee Management**: Complete employee records with contact and banking information
- **Payroll Processing**: Automated calculations with tax deductions
- **Tax Calculations**: Federal, State, Social Security, Medicare, and PFML taxes
- **Export Capabilities**: Excel and CSV export for reports and records
- **Auto-Save**: Automatic data protection every 5 minutes
- **Professional UI**: Modern, intuitive interface with tabbed navigation
- **Data Import**: CSV import for bulk employee data
- **Backup System**: Automatic database backups

## 📋 System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 100MB free space
- **Display**: 1024x768 minimum resolution

## 🛠️ Installation

### Option 1: Standalone Executable (Recommended)

1. Download the latest release from the releases page
2. Extract the ZIP file to your desired location
3. Run `PayrollApp.exe`
4. Create or select a profile to get started

### Option 2: Python Installation

1. Ensure Python 3.8+ is installed
2. Clone or download this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python payroll_gui_advanced.py
   ```

### Option 3: Build from Source

1. Clone the repository
2. Install build dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the build script:
   ```bash
   python build_app.py
   ```
4. Find your executable in `dist/PayrollApp/`

## 🎯 Quick Start

1. **Launch the Application**: Run the executable or Python script
2. **Create a Profile**: Click "Create New" and enter your business name
3. **Add Employees**: Use the Employee tab to add your team members
4. **Process Payroll**: Use the Payroll tab to calculate and save payroll runs
5. **Generate Reports**: Export data to Excel or CSV for record keeping

## 📊 Profile System

Each profile represents a separate business or location with its own:
- Employee database
- Payroll history
- Settings and configurations
- Export files

Profiles are stored in the `profiles/` directory and can be easily backed up or transferred.

## 💼 Employee Management

Store comprehensive employee information:
- Personal details (name, contact, address)
- Employment information (position, hire date, hourly rate)
- Banking details for direct deposit
- Emergency contact information
- Tax identification

## 💰 Payroll Processing

Automated payroll calculations include:
- Regular and overtime hours
- Gross pay calculations
- Federal income tax
- Social Security tax (6.2%)
- Medicare tax (1.45%)
- State tax (configurable)
- PFML tax (0.75%)
- Net pay calculation

## 📈 Reporting & Export

Generate professional reports:
- **Payroll Reports**: Detailed breakdown of each payroll run
- **Employee Reports**: Complete employee information
- **Export Formats**: Excel (.xlsx) and CSV formats
- **Custom Date Ranges**: Filter reports by specific periods

## 🔧 Configuration

### Tax Rates
Default tax rates are provided but can be customized per profile:
- Federal Tax: 15% (default)
- State Tax: 5% (default)
- Social Security: 6.2%
- Medicare: 1.45%
- PFML: 0.75%

### Pay Frequencies
Supported pay periods:
- Weekly
- Bi-weekly
- Semi-monthly
- Monthly

## 🛡️ Data Protection

- **Auto-Save**: Automatic saves every 5 minutes
- **Backup System**: Automatic database backups
- **Profile Isolation**: Each profile has separate data
- **Export Capabilities**: Easy data backup to external files

## 📁 File Structure

```
payroll-app/
├── PayrollApp.exe          # Main executable
├── profiles/               # Profile databases
│   ├── Business1.db
│   └── Business2.db
├── backups/                # Automatic backups
├── exports/                # Export files
└── README.txt             # This file
```

## 🔄 Import/Export

### Import from CSV
Supported CSV format:
```csv
First Name,Last Name,Email,Phone Number,Job Descriptions,Wages
John,Doe,john@example.com,555-0123,Manager,25.00
```

### Export Options
- **Excel**: Professional formatted spreadsheets
- **CSV**: Simple comma-separated values
- **Date Range**: Filter exports by specific periods

## 🐛 Troubleshooting

### Common Issues

1. **App won't start**
   - Ensure all files are extracted properly
   - Check Windows Defender isn't blocking the executable
   - Try running as administrator

2. **Database errors**
   - Check write permissions in the app directory
   - Ensure sufficient disk space
   - Restore from backup if available

3. **Import/Export issues**
   - Verify CSV format matches expected structure
   - Check file permissions
   - Ensure sufficient disk space

### Support

For technical support:
- Check the troubleshooting section above
- Review the application logs
- Contact your system administrator

## 📝 License

This software is provided as-is for business use. Please ensure compliance with local payroll and tax regulations.

## 🔄 Updates

To update the application:
1. Download the latest version
2. Backup your profiles directory
3. Replace the executable
4. Restore your profiles if needed

## 📞 Support

For questions or support:
- Review this README
- Check the troubleshooting section
- Contact your IT administrator

---

**Version**: 2.0.0  
**Last Updated**: January 2025  
**Compatibility**: Windows 10+, macOS 10.14+, Linux

"""
Configuration file for Payroll App
Contains version information and app metadata
"""

# App Information
APP_NAME = "Professional Payroll System"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Advanced Employee & Payroll Management System"
APP_AUTHOR = "Payroll Solutions"
APP_WEBSITE = "https://payroll-solutions.com"

# Build Configuration
BUILD_DATE = "2025-01-27"
PYTHON_VERSION = "3.13+"

# Features
FEATURES = [
    "Multi-profile support",
    "Employee management",
    "Payroll calculation",
    "Tax calculations",
    "Export to Excel/CSV",
    "Auto-save functionality",
    "Professional UI"
]

# Dependencies
REQUIRED_PACKAGES = [
    "tkinter",
    "openpyxl",
    "tkcalendar",
    "sqlite3"
]

# File paths
PROFILE_DIR = "profiles"
BACKUP_DIR = "backups"
EXPORT_DIR = "exports"

# Database settings
DB_VERSION = "1.0"
AUTO_BACKUP_INTERVAL = 300  # 5 minutes in seconds
MAX_BACKUP_FILES = 10

# UI Settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 800
MIN_WINDOW_HEIGHT = 600

# Colors (for theming)
COLORS = {
    "primary": "#2E3B4E",
    "secondary": "#4CAF50",
    "accent": "#B0C4DE",
    "background": "#F5F5F5",
    "text": "#333333",
    "error": "#F44336",
    "warning": "#FF9800",
    "success": "#4CAF50"
}

# Export settings
DEFAULT_EXPORT_FORMAT = "excel"
SUPPORTED_EXPORT_FORMATS = ["excel", "csv", "pdf"]
MAX_EXPORT_ROWS = 10000

# Validation settings
MAX_EMPLOYEE_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 255
MAX_PHONE_LENGTH = 20
MIN_HOURLY_RATE = 0.01
MAX_HOURLY_RATE = 1000.00
MAX_HOURS_PER_WEEK = 168  # 7 days * 24 hours

# Tax settings (default rates - can be customized per profile)
DEFAULT_TAX_RATES = {
    "federal_tax_rate": 0.15,
    "ss_tax_rate": 0.062,
    "medicare_tax_rate": 0.0145,
    "ma_state_tax_rate": 0.05,
    "pfml_tax_rate": 0.0075
}

# Payroll settings
DEFAULT_PAY_FREQUENCIES = [
    "Weekly",
    "Bi-weekly", 
    "Semi-monthly",
    "Monthly"
]

OVERTIME_THRESHOLD = 40  # hours per week
OVERTIME_RATE_MULTIPLIER = 1.5

# Configuration Guide

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# App settings
DEBUG=true
ENVIRONMENT=development
APP_NAME="Iterum R&D Chef Notebook"
APP_VERSION="2.0.0"

# Server settings
HOST=0.0.0.0
PORT=8000
FRONTEND_PORT=8080

# Database
DATABASE_URL=sqlite:///./culinary_data.db

# Security
SECRET_KEY=your-secret-key-change-in-production-for-security
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File uploads
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=.pdf,.docx,.xlsx,.txt

# Recipe processing
AUTO_PROCESS_UPLOADS=true
FOLDER_WATCHER_ENABLED=true
INCOMING_RECIPES_DIR=./incoming_recipes

# Equipment database
EQUIPMENT_DATABASE_PATH=./equipment_database.csv

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/iterum_app.log

# Firebase settings (for Google auth) - optional
# FIREBASE_CONFIG_PATH=./firebase-config.json
```

## Configuration Options

### App Settings
- `DEBUG`: Enable debug mode (true/false)
- `ENVIRONMENT`: Set to "development" or "production"
- `APP_NAME`: Application name
- `APP_VERSION`: Application version

### Server Settings
- `HOST`: Server host address
- `PORT`: Backend API port
- `FRONTEND_PORT`: Frontend server port

### Database
- `DATABASE_URL`: Database connection string

### Security
- `SECRET_KEY`: Secret key for JWT tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### File Uploads
- `UPLOAD_DIR`: Directory for uploaded files
- `MAX_FILE_SIZE`: Maximum file size in bytes
- `ALLOWED_FILE_TYPES`: Comma-separated list of allowed file extensions

### Recipe Processing
- `AUTO_PROCESS_UPLOADS`: Automatically process uploaded files
- `FOLDER_WATCHER_ENABLED`: Enable folder watching for new files
- `INCOMING_RECIPES_DIR`: Directory to watch for new recipe files

### Equipment Database
- `EQUIPMENT_DATABASE_PATH`: Path to equipment database CSV file

### Logging
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE`: Path to log file

### Firebase (Optional)
- `FIREBASE_CONFIG_PATH`: Path to Firebase configuration file 
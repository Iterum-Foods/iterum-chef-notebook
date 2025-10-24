# Uniform Naming and Structure Plan

## Current Issues:
1. Multiple Firebase projects with confusing names
2. Mixed naming conventions (USTA, Iterum, restaurant-startup)
3. Duplicate directories and files
4. Inconsistent project structure

## Proposed Solution:

### Main Project Identity:
- **Project Name**: Iterum Culinary App
- **Firebase Project**: `iterum-culinary-app` (keep current)
- **GitHub Repository**: `iterum-culinary-app`
- **Domain**: `iterum-culinary-app.web.app`

### Clean Directory Structure:
```
iterum-culinary-app/
├── public/                 # Main app files (Firebase hosting)
│   ├── index.html
│   ├── launch.html
│   └── assets/
├── src/                    # Source files
│   ├── pages/             # All HTML pages
│   ├── assets/            # CSS, JS, images
│   └── scripts/           # Utility scripts
├── docs/                  # Documentation
├── config/                # Configuration files
├── data/                  # Data files
└── archive/               # Old/backup files
```

### Firebase Configuration:
- Use only `iterum-culinary-app` project
- Remove references to `restaurant-startup-app` and `usta-app`
- Update all config files to use consistent naming

### File Naming Conventions:
- All files use kebab-case: `recipe-library.html`
- CSS files: `iterum-[feature].css`
- JS files: `iterum-[feature].js`
- Config files: `iterum-[service].json`

### Next Steps:
1. Clean up duplicate files and directories
2. Standardize all Firebase configuration
3. Update all file references
4. Reorganize directory structure
5. Update deployment configuration

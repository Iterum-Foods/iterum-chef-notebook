# Changelog

All notable changes to the Iterum Chef Notebook project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2024-12-19

### Added
- **User Info Tab System**: Implemented centralized user management with dropdown functionality
  - User info tab at top right with avatar, name, and role display
  - Dropdown menu for user actions (Edit Profile, Switch User, Create New User, Settings, Sign Out)
  - Consistent header structure across all application pages
  - Mobile-responsive design with toggle button
  - Unified user experience replacing scattered user management buttons
- **User Selection Requirement**: App now requires user selection before initialization
- **Integrated Startup Loading Manager**: Loading screen integrated with user selection flow
- **Event-Driven App Ready System**: Custom events for coordinating app initialization
- **Inline Profile Creation**: Users can create new profiles directly in the loading screen
- **Change Management Process**: Comprehensive framework for managing changes safely
- **Change Request Templates**: Standardized templates for tracking changes
- **Quick Reference Guides**: Easy-to-use reference for change management

### Changed
- **Loading Screen Behavior**: No more skipping user selection for utility pages
- **App Initialization**: All functionality waits for user context before proceeding
- **User System Integration**: Frontend components now use unified user system
- **API Call Timing**: API calls wait for user selection to prevent 403 errors

### Fixed
- **403 Forbidden Errors**: Caused by missing user context in API calls
- **Loading Screen Stuck**: Loading screen no longer gets stuck on utility pages
- **User Context Issues**: App properly maintains user context throughout session
- **Profile Management**: Simplified user profile creation and selection

### Technical Improvements
- **Startup Loading Manager**: Enhanced with user selection integration
- **Event System**: Custom events for app coordination
- **Error Handling**: Better error handling and fallback mechanisms
- **Code Organization**: Cleaner separation of concerns

## [Previous Versions]

[Previous changelog entries would go here]

---

**Note**: This changelog tracks all significant changes to the Iterum Chef Notebook application. For detailed technical information, see the individual commit messages and related documentation.

# 🤝 Contributing to Iterum Culinary App

Thank you for your interest in contributing to the Iterum Culinary App! This guide will help you get started with testing, reporting issues, and contributing code.

## 🚀 Quick Start for Testers

### **1. Set Up Your Testing Environment**
1. **Clone the repository** or download the latest release
2. **Start a local server** (see README.md for instructions)
3. **Open the app** in your preferred browser
4. **Create a test user profile** to get started

### **2. Test the Core Functionality**
- **User Management**: Create multiple user profiles, switch between them
- **Project System**: Create projects, switch between them, verify data persistence
- **Cross-Page Sync**: Navigate between pages, verify user/project info stays consistent
- **Data Storage**: Create recipe ideas, vendors, ingredients, verify they save correctly

### **3. Report Issues**
Use the appropriate issue template and include:
- **Detailed reproduction steps**
- **Console logs** (F12 → Console)
- **Screenshots** of the problem
- **Environment details** (OS, browser, version)

## 🐛 Issue Reporting Guidelines

### **Bug Reports**
- **Use the Bug Report template** for general issues
- **Use the User Loading Issue template** for authentication problems
- **Include console logs** - they're crucial for debugging
- **Test on multiple browsers** if possible
- **Check existing issues** before creating duplicates

### **Feature Requests**
- **Use the Feature Request template**
- **Explain the problem** the feature would solve
- **Provide use cases** and examples
- **Consider alternatives** and trade-offs

### **Issue Labels**
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `user-authentication`: User loading, switching, or profile issues
- `high-priority`: Critical functionality broken
- `needs-triage`: Issue needs review and categorization

## 🔧 Development Setup

### **Prerequisites**
- Modern web browser
- Text editor (VS Code, Sublime Text, etc.)
- Git (for version control)
- Local HTTP server

### **Development Workflow**
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test thoroughly** on multiple browsers
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a pull request**

### **Code Style Guidelines**
- **JavaScript**: Use ES6+ features, consistent naming conventions
- **HTML**: Semantic markup, accessibility considerations
- **CSS**: Use Tailwind CSS classes, maintain responsive design
- **Comments**: Document complex logic and business rules

## 🧪 Testing Guidelines

### **Manual Testing Checklist**
- [ ] **User Authentication**
  - [ ] App launch shows user selection popup
  - [ ] Can create new user profiles
  - [ ] Can switch between existing users
  - [ ] User info persists across page navigation
- [ ] **Project Management**
  - [ ] Can create new projects
  - [ ] Project selection persists across pages
  - [ ] Data is properly tagged to projects
- [ ] **Data Persistence**
  - [ ] Recipe ideas save correctly
  - [ ] Vendor information persists
  - [ ] Ingredient data is maintained
  - [ ] Menu data is saved

### **Cross-Browser Testing**
- **Chrome**: Primary development browser
- **Firefox**: Secondary testing
- **Safari**: macOS compatibility
- **Edge**: Windows compatibility

### **Testing Scenarios**
1. **Fresh Installation**: No existing data
2. **Existing User**: Returning user with saved data
3. **Multiple Users**: Switching between profiles
4. **Project Switching**: Moving between different projects
5. **Data Migration**: Testing data import/export

## 📁 Project Structure

### **Key Files to Understand**
- **`index.html`**: Main application entry point
- **`assets/js/unified_auth_system.js`**: User authentication core
- **`assets/js/project-management-system.js`**: Project organization
- **`assets/js/userControlledStorage.js`**: Data storage management
- **`assets/js/header_user_sync.js`**: Cross-page synchronization

### **Data Flow**
1. **User Selection** → `unified_auth_system.js`
2. **Project Selection** → `project-management-system.js`
3. **Data Storage** → `userControlledStorage.js`
4. **UI Updates** → `header_user_sync.js`

## 🔍 Debugging Tools

### **Built-in Debug Features**
- **Debug Button**: Available in user selection modals
- **Console Logging**: Comprehensive logging throughout the app
- **Test Pages**: Dedicated testing interfaces for specific features

### **Browser Developer Tools**
- **Console**: View logs and errors
- **Network**: Monitor API calls (if backend is implemented)
- **Storage**: Inspect localStorage and IndexedDB
- **Elements**: Debug DOM structure and CSS

## 📚 Documentation

### **What to Document**
- **New Features**: How they work and how to use them
- **API Changes**: Any modifications to data structures
- **Configuration**: Environment-specific settings
- **Troubleshooting**: Common problems and solutions

### **Documentation Standards**
- Use clear, concise language
- Include examples and use cases
- Update README.md for major changes
- Add inline comments for complex code

## 🚨 Critical Areas

### **High Priority Testing**
- **User Authentication**: Core functionality, must work reliably
- **Data Persistence**: User data must not be lost
- **Cross-Page Sync**: User experience consistency
- **Project Management**: Data organization integrity

### **Known Issues to Watch**
- User loading edge cases
- Cross-page synchronization timing
- Data storage consistency
- Browser compatibility differences

## 🤝 Community Guidelines

### **Communication**
- **Be respectful** and constructive
- **Ask questions** if something isn't clear
- **Share your testing results** and findings
- **Help other testers** with their questions

### **Feedback**
- **Specific feedback** is more helpful than general comments
- **Include context** when reporting issues
- **Suggest improvements** when possible
- **Test fixes** before marking issues as resolved

## 📞 Getting Help

### **When You're Stuck**
1. **Check existing issues** for similar problems
2. **Search documentation** for relevant information
3. **Ask in issues** with clear questions
4. **Provide context** about what you're trying to do

### **Resources**
- **README.md**: Setup and basic usage
- **Issue Templates**: Structured reporting
- **Test Pages**: Dedicated testing interfaces
- **Console Logs**: Real-time debugging information

---

**Thank you for contributing to making the Iterum Culinary App better! 🍳✨**

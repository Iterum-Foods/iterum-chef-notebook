# Enterprise Development Setup Guide

## 🚀 **Overview**

This guide will help you set up the Iterum Chef Notebook application with enterprise-grade development tools and practices. By following this guide, you'll have a professional development environment that matches industry standards.

## 🛠️ **Prerequisites**

### **Required Software**
- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Git** (latest version)
- **VS Code** (recommended editor)

### **System Requirements**
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **OS**: Windows 10/11, macOS 10.15+, or Ubuntu 18.04+

## 📦 **Installation Steps**

### **1. Clone the Repository**
```bash
git clone https://github.com/Iterum-Foods/iterum-chef-notebook.git
cd iterum-chef-notebook
```

### **2. Install Dependencies**
```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
npm install --save-dev
```

### **3. Build the Application**
```bash
# Build Tailwind CSS
npm run build

# Start the development server
npm run dev
```

## 🔧 **Development Tools Setup**

### **VS Code Extensions**
Install these recommended extensions for the best development experience:

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "ms-vscode.vscode-typescript-next",
    "bradlc.vscode-tailwindcss",
    "ms-python.python",
    "ms-python.pylint",
    "ms-python.black-formatter"
  ]
}
```

### **VS Code Settings**
Add these settings to your `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black"
}
```

## 🧪 **Testing Setup**

### **Run Tests**
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- tests/user-system.test.js
```

### **Test Structure**
```
tests/
├── setup.js              # Test environment setup
├── unit/                 # Unit tests
│   ├── user-system.test.js
│   ├── project-manager.test.js
│   └── utils.test.js
├── integration/          # Integration tests
│   ├── api.test.js
│   └── workflow.test.js
└── e2e/                 # End-to-end tests
    └── user-journey.test.js
```

## 📝 **Code Quality Tools**

### **ESLint Configuration**
The project uses ESLint for JavaScript code quality:

```bash
# Check code quality
npm run lint

# Fix auto-fixable issues
npm run lint:fix
```

### **Prettier Configuration**
Prettier ensures consistent code formatting:

```bash
# Format all code
npm run format

# Check formatting
npm run format:check
```

### **Pre-commit Hooks**
Git hooks ensure code quality before commits:

```bash
# Install pre-commit hooks
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run lint && npm run test"
```

## 🎨 **Design System Development**

### **Tailwind CSS Development**
```bash
# Watch for changes during development
npm run dev

# Build for production
npm run build
```

### **CSS Architecture**
```
assets/css/
├── iterum-design-system.css    # Design system foundation
├── tailwind-output.css         # Generated Tailwind CSS
└── components/                 # Component-specific styles
    ├── buttons.css
    ├── forms.css
    └── cards.css
```

### **Design Token Management**
All design values are centralized in CSS custom properties:

```css
:root {
  /* Brand Colors */
  --iterum-primary: #10b981;
  --iterum-secondary: #059669;
  
  /* Spacing Scale */
  --space-4: 1rem;
  --space-6: 1.5rem;
  
  /* Typography */
  --font-family: 'Inter', sans-serif;
  --font-weight-medium: 500;
}
```

## 🔄 **Development Workflow**

### **1. Feature Development**
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and test
npm run test
npm run lint

# Commit with conventional commits
git commit -m "feat: add new feature"

# Push and create pull request
git push origin feature/new-feature
```

### **2. Code Review Process**
1. **Self-Review**: Check your code before submitting
2. **Peer Review**: At least one team member reviews
3. **Automated Checks**: CI/CD pipeline validation
4. **Approval**: Code review approval required

### **3. Testing Strategy**
- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete user workflows
- **Visual Regression**: Test UI consistency

## 📊 **Monitoring & Analytics**

### **Error Tracking**
The app includes built-in error tracking:

```javascript
// Track errors automatically
window.IterumErrorTracker.capture(error, {
  context: 'user_action',
  userId: currentUser.id
});

// Get error statistics
const errors = JSON.parse(localStorage.getItem('iterum_errors') || '[]');
console.log('Total errors:', errors.length);
```

### **Performance Monitoring**
```javascript
// Monitor page load performance
window.addEventListener('load', () => {
  const perfData = performance.getEntriesByType('navigation')[0];
  console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart);
});
```

## 🚀 **Deployment**

### **Development Environment**
```bash
# Start development server
npm run dev

# Start Python backend
python start.py
```

### **Production Build**
```bash
# Build production assets
npm run build

# Start production server
npm run start:prod
```

### **Environment Variables**
Create `.env` file for configuration:

```bash
# App Configuration
NODE_ENV=production
API_BASE_URL=https://api.iterumfoods.xyz
ENABLE_HTTPS=true

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/iterum
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **Tailwind CSS Not Building**
```bash
# Clear cache and rebuild
rm -rf node_modules
npm install
npm run build
```

#### **Tests Not Running**
```bash
# Check Jest configuration
npm test -- --verbose

# Clear Jest cache
npm test -- --clearCache
```

#### **ESLint Errors**
```bash
# Check ESLint configuration
npx eslint --print-config assets/js/main.js

# Fix auto-fixable issues
npx eslint --fix assets/js/**/*.js
```

### **Getting Help**
- **Documentation**: Check the project documentation
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions
- **Team**: Contact the development team

## 📚 **Additional Resources**

### **Documentation**
- [Design System Guide](DESIGN_SYSTEM.md)
- [API Documentation](API_DOCS.md)
- [User Guide](USER_GUIDE.md)
- [Contributing Guide](CONTRIBUTING.md)

### **External Resources**
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Jest Testing Framework](https://jestjs.io/docs/getting-started)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Prettier Configuration](https://prettier.io/docs/en/configuration.html)

## 🎯 **Next Steps**

1. **Complete Setup**: Follow all installation steps
2. **Run Tests**: Ensure all tests pass
3. **Explore Code**: Familiarize yourself with the codebase
4. **Start Developing**: Begin working on features
5. **Contribute**: Help improve the project

---

*This guide is maintained by the Iterum development team. For questions or updates, please contact the team or create an issue on GitHub.*

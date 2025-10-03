# Contributing to Iterum R&D Chef Notebook

Thank you for your interest in contributing to Iterum R&D Chef Notebook! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- **Bug Reports**: Use the GitHub issue tracker to report bugs
- **Feature Requests**: Suggest new features or improvements
- **Documentation**: Help improve our documentation

### Development Contributions
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment tool (venv, conda, etc.)

### Local Development
```bash
# Clone your fork
git clone https://github.com/yourusername/iterum-chef-notebook.git
cd iterum-chef-notebook

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python launch_marketing.py
```

### Running Tests
```bash
python -m pytest
```

## 📝 Code Guidelines

### Python Style
- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for all functions and classes
- Keep functions **small and focused**

### Example:
```python
def calculate_recipe_cost(ingredients: List[Ingredient], servings: int) -> float:
    """
    Calculate the total cost of a recipe based on ingredients and servings.
    
    Args:
        ingredients: List of ingredient objects with cost data
        servings: Number of servings the recipe makes
        
    Returns:
        Total cost per serving as a float
        
    Raises:
        ValueError: If servings is less than 1
    """
    if servings < 1:
        raise ValueError("Servings must be at least 1")
    
    total_cost = sum(ingredient.cost for ingredient in ingredients)
    return total_cost / servings
```

### Frontend Guidelines
- Use **semantic HTML**
- Follow **accessibility best practices**
- Keep JavaScript **modular and documented**
- Use **CSS custom properties** for theming

### Database Changes
- Create **migration scripts** for schema changes
- Document **breaking changes**
- Test with **existing data**

## 🚀 Pull Request Process

### Before Submitting
1. **Test** your changes thoroughly
2. **Update** documentation if needed
3. **Add** tests for new functionality
4. **Check** code style with linting tools

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
Include screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🏷️ Issue Labels

### Types
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed

### Priority
- `priority: high` - Urgent issues
- `priority: medium` - Standard priority
- `priority: low` - Nice to have

### Areas
- `area: frontend` - Frontend/UI related
- `area: backend` - Backend/API related
- `area: database` - Database related
- `area: documentation` - Documentation
- `area: marketing` - Marketing website

## 🧪 Testing Guidelines

### Unit Tests
- Test **individual functions** and classes
- Use **descriptive test names**
- Include **edge cases** and error conditions

### Integration Tests
- Test **API endpoints**
- Test **database operations**
- Test **file processing workflows**

### Test Structure
```python
def test_calculate_recipe_cost_valid_input():
    """Test recipe cost calculation with valid inputs."""
    # Arrange
    ingredients = [
        Ingredient(name="Flour", cost=2.50),
        Ingredient(name="Sugar", cost=1.00)
    ]
    servings = 4
    
    # Act
    result = calculate_recipe_cost(ingredients, servings)
    
    # Assert
    assert result == 0.875  # (2.50 + 1.00) / 4
```

## 📚 Documentation

### Code Documentation
- **Docstrings** for all public functions
- **Type hints** for function parameters
- **Inline comments** for complex logic

### API Documentation
- Update **OpenAPI schemas** for new endpoints
- Include **request/response examples**
- Document **error responses**

### User Documentation
- Update **README.md** for new features
- Create **tutorials** for complex workflows
- Maintain **changelog** for releases

## 🔄 Release Process

### Version Numbering
We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist
1. Update version numbers
2. Update CHANGELOG.md
3. Create release notes
4. Tag the release
5. Deploy to production

## 🎯 Areas for Contribution

### High Priority
- **Mobile responsiveness** improvements
- **Performance optimization**
- **Accessibility** enhancements
- **Test coverage** expansion

### Features Needed
- **Recipe import** from popular formats
- **Ingredient substitution** engine
- **Cost tracking** improvements
- **Multi-language** support

### Documentation
- **Video tutorials**
- **API examples**
- **Deployment guides**
- **User onboarding**

## 🌍 Community

### Communication
- **GitHub Issues**: Primary communication
- **Discussions**: Feature planning and questions
- **Email**: hello@iterum-chef.com for private matters

### Code of Conduct
- Be **respectful** and **inclusive**
- **Constructive** feedback only
- **No harassment** or discrimination
- **Help** newcomers learn

## 🏆 Recognition

### Contributors
All contributors will be:
- **Listed** in the README
- **Credited** in release notes
- **Invited** to beta testing
- **Given** special recognition badges

### Significant Contributions
Major contributors may receive:
- **Collaborator access**
- **Direct communication** with maintainers
- **Input** on roadmap decisions
- **Special mentions** in documentation

## ❓ Questions?

### Getting Help
- **Check** existing issues and documentation
- **Search** previous discussions
- **Ask** in GitHub Discussions
- **Email** the maintainers

### Feature Discussions
Before implementing major features:
1. **Open** a GitHub Discussion
2. **Describe** the use case
3. **Get** feedback from maintainers
4. **Plan** the implementation approach

## 📞 Contact

**Maintainers**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: hello@iterum-chef.com

**Community**
- GitHub Discussions: [Link to discussions]
- Discord: [Coming Soon]

---

Thank you for contributing to Iterum R&D Chef Notebook! Together, we're revolutionizing professional kitchens worldwide. 🍅👨‍🍳
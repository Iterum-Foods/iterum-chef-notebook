# 🍅 Iterum R&D Chef Notebook

> **The Future of Professional Cooking is Here**  
> Revolutionary culinary management platform combining AI-powered recipe intelligence, smart ingredient tracking, and automated workflow optimization for professional kitchens.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

## 🌟 Features

### 🧠 AI-Powered Recipe Intelligence
- **Smart Recipe Analysis**: Automatic parsing and nutritional calculations
- **Intelligent Substitutions**: AI-powered ingredient recommendations
- **Recipe Optimization**: Cost and nutrition optimization suggestions
- **Batch Processing**: Upload hundreds of recipes in minutes

### 📊 Advanced Ingredient Database
- **291+ Professional Ingredients**: Comprehensive database with nutritional data
- **Smart Search**: Natural language queries ("high protein, gluten-free, under $3")
- **Dietary Tags**: Automatic detection (Vegan, GF, Keto, etc.)
- **Seasonal Tracking**: Availability and pricing optimization
- **Cost Intelligence**: Real-time market data and cost projections

### ⚡ Automated Workflow Management
- **Recipe Discovery**: Automatic file scanning and organization
- **Smart Categorization**: AI-powered recipe classification
- **Batch Operations**: Mass import, export, and processing
- **Version Control**: Track recipe iterations and changes

### 🌍 International Cuisine Support
- **Global Ingredients**: Asian, Mediterranean, Latin specialties
- **Fermented Foods**: Probiotics and cultured ingredients
- **Plant-Based Alternatives**: Complete vegan/vegetarian support
- **Superfoods**: Nutrient-dense health ingredients

### 📈 Analytics & Insights
- **Cost Analysis**: Detailed food cost breakdowns
- **Performance Metrics**: Recipe success tracking
- **Seasonal Optimization**: Timing and pricing recommendations
- **Profitability Reports**: Menu optimization insights

### 🌐 Marketing & Waitlist System
- **Professional Landing Page**: Conversion-optimized marketing website
- **Waitlist Management**: Email collection and analytics
- **Email Templates**: 5-email nurture sequence
- **Social Media Kit**: Complete content framework
- **Admin Dashboard**: Real-time signup tracking and analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/iterum-chef-notebook.git
   cd iterum-chef-notebook
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**

   **For the Main Application:**
   ```bash
   # Windows (Recommended)
   start.bat
   
   # Or programmatically
   python app_launcher.py --mode unified
   ```
   
   **For the Marketing Website:**
   ```bash
   # Windows (Recommended)
   launch_marketing.bat
   
   # Or programmatically
   python launch_marketing.py
   ```

4. **Access the application**
   - **Main Application**: http://localhost:8080/index.html
   - **Marketing Website**: http://localhost:8080/landing_page.html
   - **API Documentation**: http://localhost:8000/docs
   - **Waitlist Admin**: http://localhost:8080/waitlist_admin.html
   - **Ingredient Demo**: http://localhost:8080/ingredient_demo.html

## 📁 Project Structure

```
iterum-chef-notebook/
├── app/                          # FastAPI backend application
│   ├── routers/                  # API route handlers
│   │   ├── auth.py              # Authentication
│   │   ├── recipes.py           # Recipe management
│   │   ├── ingredients.py       # Ingredient operations
│   │   ├── ingredient_lists.py  # Custom ingredient lists
│   │   ├── waitlist.py          # Marketing waitlist
│   │   └── workflow.py          # Automated workflows
│   ├── services/                # Business logic
│   ├── database.py              # Database configuration
│   └── main.py                  # FastAPI application
├── static/                      # Frontend assets
│   ├── css/                     # Stylesheets
│   ├── js/                      # JavaScript files
│   └── images/                  # Image assets
├── marketing/                   # Marketing materials
│   ├── landing_page.html        # Marketing landing page
│   ├── waitlist_admin.html      # Waitlist administration
│   ├── ingredient_demo.html     # Feature demonstration
│   ├── email_templates.html     # Email templates
│   ├── marketing_copy.md        # Marketing copy framework
│   └── social_media_copy.md     # Social media content
├── launch_marketing.py          # Marketing website launcher
├── launch_marketing.bat         # Windows marketing launcher
├── docs/                        # Documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🛠️ Development

### Setting up Development Environment

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run tests**
   ```bash
   python -m pytest
   ```

### API Endpoints

The application provides a comprehensive REST API:

- **Authentication**: `/api/auth/*`
- **Recipes**: `/api/recipes/*`
- **Ingredients**: `/api/ingredients/*`
- **Data**: `/api/data/*`
- **Workflow**: `/api/workflow/*`
- **Waitlist**: `/api/waitlist/*`

Full API documentation available at: http://localhost:8000/docs

### Database Schema

The application uses SQLite databases:
- **`iterum_rnd.db`**: Main application data (recipes, users, profiles)
- **`culinary_data.db`**: Ingredient database and lists
- **`waitlist.db`**: Marketing waitlist signups

## 🎯 Key Components

### Recipe Management
- Upload recipes in any format (PDF, Word, text, images)
- AI-powered parsing and standardization
- Nutritional analysis and cost calculations
- Scaling and portion management

### Ingredient Intelligence
- 291+ preloaded professional ingredients
- Smart search with natural language processing
- Dietary restriction filtering
- Seasonal availability and pricing data

### Workflow Automation
- Automated recipe discovery and organization
- Batch processing capabilities
- Smart categorization and tagging
- Version control and change tracking

### Analytics Dashboard
- Real-time cost analysis
- Recipe performance metrics
- Seasonal optimization recommendations
- Profitability insights

## 🌐 Marketing Features

### Landing Page
Professional marketing website with:
- Conversion-optimized design
- Feature showcases and demos
- Waitlist signup functionality
- Social proof and testimonials

### Email Marketing
- 5-email nurture sequence
- Professional HTML templates
- Behavioral triggers
- Conversion tracking

### Social Media
- Platform-specific content
- Hashtag strategies
- Video script templates
- Community building

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
# Database
DATABASE_URL=sqlite:///./iterum_rnd.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Analytics (optional)
GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
```

### Customization
- **Branding**: Update colors and logos in CSS files
- **Features**: Enable/disable features in configuration
- **Integrations**: Add custom API integrations
- **Deployment**: Configure for your hosting environment

## 📊 Analytics & Tracking

### Waitlist Analytics
- Real-time signup tracking
- Source attribution
- Conversion metrics
- Growth trends

### Application Analytics
- User engagement metrics
- Feature usage tracking
- Performance monitoring
- Error logging

## 🚀 Deployment

### Local Development
```bash
python launch_marketing.py
```

### Production Deployment

#### Option 1: Traditional Server
1. Set up Python environment on server
2. Configure reverse proxy (nginx/Apache)
3. Set up SSL certificates
4. Configure environment variables
5. Run with production WSGI server

#### Option 2: Docker (Coming Soon)
```bash
docker-compose up -d
```

#### Option 3: Cloud Platforms
- **Heroku**: One-click deployment
- **AWS**: EC2, ECS, or Lambda
- **Google Cloud**: App Engine or Compute Engine
- **DigitalOcean**: Droplets or App Platform

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for all functions
- Write tests for new features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- **API Docs**: http://localhost:8000/docs
- **User Guide**: [Coming Soon]
- **Video Tutorials**: [Coming Soon]

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Email**: support@iterum-chef.com
- **Discord**: [Community Server - Coming Soon]

### Professional Support
For enterprise customers and professional kitchens:
- Priority support response
- Custom feature development
- On-site training and setup
- Integration assistance

## 🏆 Recognition

### Built For
- **Professional Chefs**: Restaurant, catering, institutional
- **Culinary Schools**: Educational institutions
- **Food Businesses**: R&D departments and test kitchens
- **Serious Home Cooks**: Advanced culinary enthusiasts

### Awards & Recognition
- Featured in [Culinary Technology Magazine]
- Winner of [Food Innovation Award 2024]
- "Best Kitchen Management Platform" - [Industry Review]

## 🔮 Roadmap

### Version 2.1 (Current)
- ✅ AI-powered recipe intelligence
- ✅ 291+ ingredient database
- ✅ Automated workflow management
- ✅ Marketing website and waitlist

### Version 2.2 (Q1 2024)
- 🔄 Mobile application (iOS/Android)
- 🔄 Advanced analytics dashboard
- 🔄 Integration marketplace
- 🔄 Multi-language support

### Version 2.3 (Q2 2024)
- 📋 Equipment management
- 📋 Supplier integration
- 📋 Inventory tracking
- 📋 Team collaboration tools

### Version 3.0 (Q3 2024)
- 📋 AI menu optimization
- 📋 Predictive analytics
- 📋 Voice recipe input
- 📋 IoT kitchen integration

## 📞 Contact

**Iterum R&D Team**  
Email: hello@iterum-chef.com  
Website: https://iterum-chef.com  
Twitter: [@IterumRD](https://twitter.com/IterumRD)  

---

<div align="center">
  <strong>🍅 Revolutionizing Professional Kitchens Worldwide 🍅</strong>
  <br>
  <em>From Recipe Chaos to Culinary Mastery</em>
</div>
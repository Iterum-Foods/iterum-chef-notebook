# 🤖 AI Integration Setup Guide for Iterum R&D Chef Notebook

## 🎯 Overview

Your Iterum Culinary App now includes comprehensive AI capabilities for:
- **Recipe Parsing**: AI-powered recipe text extraction and enhancement
- **Menu Analysis**: Intelligent menu parsing with business insights
- **Recipe Creation**: AI-generated recipes from ingredients or concepts
- **Recipe Variations**: AI-suggested recipe modifications and improvements
- **Professional Insights**: Chef-level analysis and recommendations

## 🚀 Quick Start

### 1. **Install AI Dependencies**
```bash
# Install new AI packages
pip install openai anthropic google-generativeai sentence-transformers

# Or install all requirements
pip install -r requirements.txt
```

### 2. **Configure API Keys**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# At minimum, add your OpenAI API key:
OPENAI_API_KEY=sk-your-openai-api-key-here
```

### 3. **Start the Application**
```bash
# Start both backend and frontend
python scripts/startup/START_APP_FIXED.bat
```

### 4. **Test AI Features**
- Open `http://localhost:8080`
- Look for AI buttons in recipe and menu forms
- Try uploading a recipe PDF with AI enhancement enabled

## 🔧 AI Providers Setup

### **OpenAI (Recommended)**
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`: `OPENAI_API_KEY=sk-your-key-here`
3. Features: GPT-4, GPT-3.5, Vision API

### **Anthropic Claude (Alternative)**
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-your-key-here`
3. Features: Claude-3-Sonnet, advanced reasoning

### **Google Gemini (Alternative)**
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env`: `GOOGLE_API_KEY=your-key-here`
3. Features: Gemini-Pro, cost-effective

### **Azure OpenAI (Enterprise)**
1. Set up Azure OpenAI service
2. Add to `.env`:
   ```
   AZURE_API_KEY=your-key-here
   AZURE_ENDPOINT=https://your-resource.openai.azure.com/
   ```

## 🎨 AI Features Available

### **1. Recipe Parsing & Enhancement**
- **AI Parse Text**: Upload recipe text → AI extracts structured data
- **AI Enhance**: Improve existing recipes with AI insights
- **Smart Ingredient Recognition**: Standardize ingredient names and units
- **Technique Analysis**: Identify cooking methods and provide tips
- **Nutritional Analysis**: Estimate calories and nutritional content
- **Cost Estimation**: Calculate ingredient costs and profit margins

### **2. Menu Analysis**
- **AI Parse Menu**: Upload menu PDF → AI extracts structured menu data
- **Business Intelligence**: Price analysis, profit margin estimation
- **Popularity Prediction**: AI predicts which items will be popular
- **Menu Optimization**: Suggestions for improving menu balance

### **3. Recipe Creation**
- **From Ingredients**: "I have chicken, rice, vegetables" → AI creates recipe
- **From Concept**: "Healthy Mediterranean dish" → AI creates recipe
- **Recipe Variations**: Generate dietary, technique, or fusion variations
- **Improvement Suggestions**: AI analyzes and suggests recipe improvements

### **4. Professional Chef Assistant**
- **Technique Optimization**: Professional cooking technique advice
- **Flavor Analysis**: Balance and enhancement suggestions
- **Presentation Tips**: Plating and presentation recommendations
- **Wine Pairing**: Beverage pairing suggestions
- **Scaling Advice**: Commercial kitchen scaling recommendations

## 📊 AI Configuration Options

### **Feature Toggles** (in `.env`)
```bash
# Enable/disable AI features
AI_ENABLE_AI_FEATURES=true
AI_ENABLE_RECIPE_AI=true
AI_ENABLE_MENU_AI=true
AI_ENABLE_INGREDIENT_AI=true
AI_ENABLE_CHEF_ASSISTANT=true

# Specific capabilities
AI_NUTRITIONAL_ANALYSIS=true
AI_COST_ESTIMATION=true
AI_TECHNIQUE_ANALYSIS=true
AI_PRICE_ANALYSIS=true
AI_PROFIT_MARGIN_ESTIMATION=true
```

### **Model Settings**
```bash
# AI model configuration
AI_DEFAULT_LLM_MODEL=gpt-4
AI_FALLBACK_LLM_MODEL=gpt-3.5-turbo
AI_VISION_MODEL=gpt-4-vision-preview
AI_AI_CONFIDENCE_THRESHOLD=0.8
AI_MAX_TOKENS=4000
AI_TEMPERATURE=0.1
```

### **Cost Management**
```bash
# Cost control
AI_MAX_COST_PER_REQUEST=0.50
AI_DAILY_COST_LIMIT=10.0
AI_ENABLE_COST_TRACKING=true
```

## 🎯 How to Use AI Features

### **Recipe Upload with AI**
1. Go to Recipe Library or Recipe Developer
2. Click "Upload Recipe" or "Add Recipe"
3. Upload PDF/image or paste text
4. Check "🤖 Use AI for enhanced parsing"
5. Click "Process with AI"
6. Review AI-extracted data and edit as needed

### **AI Recipe Creation**
1. Go to Recipe Developer
2. Click "🎨 AI Create" button
3. Choose creation method:
   - **From Ingredients**: List ingredients you have
   - **From Concept**: Describe the dish you want
4. Set preferences (cuisine, difficulty, servings)
5. Click "Create Recipe"
6. Review and edit the AI-generated recipe

### **Menu Analysis**
1. Go to Menu Builder
2. Upload menu PDF or paste menu text
3. Click "🤖 AI Parse Menu"
4. Review AI-extracted menu structure
5. Check business insights and recommendations

### **Recipe Enhancement**
1. Open any existing recipe
2. Click "✨ AI Enhance" button
3. Review AI suggestions for:
   - Ingredient improvements
   - Technique optimization
   - Nutritional enhancements
   - Cost optimization
4. Apply suggestions you like

## 🔍 AI Status & Monitoring

### **Check AI Status**
- Visit `http://localhost:8000/api/ai/status`
- Shows which AI providers are configured
- Displays feature availability
- Shows configuration status

### **Test AI Connection**
- Visit `http://localhost:8000/api/ai/test-connection`
- Tests actual AI service connectivity
- Verifies API keys are working

### **Monitor AI Usage**
- Check console logs for AI requests
- Monitor API usage in provider dashboards
- Track costs and usage patterns

## 🚨 Troubleshooting

### **AI Features Not Working**
1. **Check API Keys**: Ensure `.env` file has valid API keys
2. **Check Dependencies**: Run `pip install -r requirements.txt`
3. **Check Status**: Visit `/api/ai/status` endpoint
4. **Check Logs**: Look for error messages in console

### **Common Issues**
- **"AI parsing is disabled"**: Check `AI_ENABLE_AI_FEATURES=true` in `.env`
- **"API key not found"**: Add your API key to `.env` file
- **"Connection failed"**: Check internet connection and API key validity
- **"Rate limit exceeded"**: Wait a moment and try again

### **Performance Issues**
- **Slow responses**: Try using `gpt-3.5-turbo` instead of `gpt-4`
- **High costs**: Reduce `AI_MAX_TOKENS` or use cheaper models
- **Timeout errors**: Increase `AI_TIMEOUT_SECONDS`

## 💰 Cost Estimation

### **OpenAI Pricing** (as of 2024)
- **GPT-4**: ~$0.03 per 1K tokens (input), ~$0.06 per 1K tokens (output)
- **GPT-3.5-turbo**: ~$0.001 per 1K tokens (input), ~$0.002 per 1K tokens (output)
- **GPT-4 Vision**: ~$0.01 per image + token costs

### **Estimated Monthly Costs**
- **Light usage** (50 recipes/month): $5-15
- **Medium usage** (200 recipes/month): $20-50
- **Heavy usage** (500+ recipes/month): $50-150

### **Cost Optimization Tips**
1. Use GPT-3.5-turbo for simple tasks
2. Set `AI_MAX_TOKENS=2000` for shorter responses
3. Enable cost tracking to monitor usage
4. Use fallback models for non-critical tasks

## 🔮 Advanced Features

### **Custom AI Prompts**
- Modify prompts in `app/services/ai_recipe_parser.py`
- Customize for your specific cuisine or style
- Add domain-specific knowledge

### **AI Model Fine-tuning**
- Train custom models on your recipe data
- Improve accuracy for your specific use case
- Reduce API costs for common tasks

### **Integration with External Services**
- Connect to nutrition databases
- Integrate with cost calculation services
- Link to inventory management systems

## 📚 API Documentation

### **AI Endpoints**
- `GET /api/ai/status` - Check AI system status
- `POST /api/ai/recipe/parse-text` - Parse recipe text with AI
- `POST /api/ai/recipe/enhance` - Enhance existing recipe
- `POST /api/ai/recipe/create-from-ingredients` - Create recipe from ingredients
- `POST /api/ai/recipe/create-from-concept` - Create recipe from concept
- `POST /api/ai/menu/parse-text` - Parse menu text with AI
- `POST /api/ai/upload/ai-enhanced` - AI-enhanced file upload

### **Frontend Integration**
- AI buttons automatically added to forms
- Real-time AI processing indicators
- Error handling and user feedback
- Responsive AI status indicators

## 🎉 Success!

Your Iterum Culinary App now has professional-grade AI capabilities! 

**Next Steps:**
1. Test AI features with your own recipes
2. Configure API keys for your preferred provider
3. Customize AI prompts for your cuisine style
4. Monitor usage and optimize costs
5. Explore advanced features as needed

**Happy AI-Enhanced Cooking! 🤖👨‍🍳**

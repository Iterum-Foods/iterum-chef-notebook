# 🍽️ Menu Processing System Guide

## Overview

The Menu Processing System provides **two-stage processing** to transform uploaded menu files (PDFs, images, Word docs) into structured menu data with titles, descriptions, and prices.

---

## 🎯 Two-Stage Processing Workflow

### **Stage 1: Text Extraction**
Extracts raw text from uploaded menu files:

**Supported File Types:**
- **PDF files** - Direct text extraction + OCR fallback
- **Image files** - JPG, PNG via OCR processing  
- **Word documents** - DOCX text extraction
- **Scanned menus** - OCR processing for image-based PDFs

**Processing Methods:**
1. **PDF Text Extraction** - Direct text from searchable PDFs
2. **OCR Processing** - For images and scanned documents
3. **Word Document Processing** - Extract from DOCX files
4. **Hybrid Processing** - Try direct extraction, fallback to OCR

### **Stage 2: Menu Parsing**
Converts extracted text into structured menu items:

**Extracted Information:**
- **Item Titles** - Dish names and menu item titles
- **Descriptions** - Ingredient lists and preparation details  
- **Prices** - Multiple currency formats ($12.50, £15.00, etc.)
- **Dietary Tags** - (V)egetarian, (GF)luten-Free, (DF)airy-Free
- **Spice Levels** - Mild, Medium, Hot, Extra Hot
- **Menu Sections** - Appetizers, Mains, Desserts, etc.

---

## 🚀 API Endpoints

### **Complete Two-Stage Processing**
```bash
POST /api/menu/extract-and-parse
```

**Upload a menu file and get structured menu data:**

```bash
curl -X POST "http://localhost:8000/api/menu/extract-and-parse" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@restaurant_menu.pdf"
```

**Response Format:**
```json
{
  "success": true,
  "filename": "restaurant_menu.pdf",
  "processing_stages": {
    "stage_1_extraction": {
      "method": "PDF Text Extraction",
      "text_length": 1250,
      "info": {"pages": 2}
    },
    "stage_2_parsing": {
      "method": "Menu Text Parsing", 
      "confidence": 85.5,
      "items_found": 12
    }
  },
  "menu_data": {
    "sections": [
      {
        "name": "Appetizers",
        "items": [
          {
            "title": "Truffle Arancini",
            "description": "Crispy risotto balls with black truffle, parmesan cheese",
            "price": 14.00,
            "price_text": "$14.00",
            "dietary_tags": ["vegetarian"],
            "spice_level": null
          }
        ]
      }
    ],
    "summary": {
      "total_items": 12,
      "total_sections": 3,
      "price_range": {"min": 8.00, "max": 45.00, "average": 18.50}
    }
  }
}
```

### **Parse Extracted Text Only**
```bash
POST /api/menu/parse-text
```

**Parse already extracted menu text:**

```bash
curl -X POST "http://localhost:8000/api/menu/parse-text" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "APPETIZERS\n\nTruffle Arancini $14.00\nTuna Tartare $18.00"}'
```

### **Sample Menu**
```bash
GET /api/menu/sample
```

**Get a sample parsed menu for testing:**

```bash
curl -X GET "http://localhost:8000/api/menu/sample"
```

---

## 📊 Menu Data Structure

### **Menu Item Format**
```json
{
  "title": "Pan Seared Salmon",
  "description": "Atlantic salmon, lemon herb butter, roasted vegetables",
  "price": 28.00,
  "price_text": "$28.00",
  "category": "",
  "dietary_tags": ["gluten_free"],
  "spice_level": null
}
```

### **Menu Section Format**
```json
{
  "name": "Main Courses",
  "description": "",
  "items": [...],
  "item_count": 5
}
```

### **Summary Information**
```json
{
  "total_sections": 4,
  "total_items": 18,
  "items_with_prices": 16,
  "price_coverage": 88.9,
  "price_range": {
    "min": 8.00,
    "max": 45.00,
    "average": 21.33
  },
  "section_names": ["Appetizers", "Main Courses", "Desserts", "Beverages"],
  "dietary_tags": {
    "vegetarian": 6,
    "gluten_free": 4,
    "vegan": 2
  }
}
```

---

## 🎯 Supported Features

### **Price Recognition**
- **US Dollars**: $12.50, $12
- **British Pounds**: £15.00, 15 pounds  
- **Euros**: €18.00, 18 euros
- **Other Currencies**: ¥, ₩, etc.
- **Market Price**: Handles "Market Price", "Ask Server"

### **Dietary Tag Detection**
- **(V)** - Vegetarian
- **(VG)** - Vegan  
- **(GF)** - Gluten-Free
- **(DF)** - Dairy-Free
- **(NF)** - Nut-Free
- **Spicy** - 🌶️ indicators

### **Section Recognition**
- **Appetizers/Starters**
- **Soups & Salads**
- **Main Courses/Entrees**
- **Desserts**
- **Beverages/Drinks**
- **Sides/Side Dishes**
- **Chef's Specials**

### **Spice Level Detection**
- **Mild** - Light spice
- **Medium** - Moderate spice  
- **Hot** - Spicy
- **Extra Hot** - Very spicy

---

## ⚙️ Configuration & Setup

### **OCR Dependencies** (Optional)
For image-based menu processing:

```bash
# Install Tesseract OCR
# Windows: choco install tesseract
# macOS: brew install tesseract  
# Linux: sudo apt install tesseract-ocr

# Install Python dependencies
pip install pytesseract opencv-python pdf2image
```

### **Fallback Processing**
If OCR is not available:
- **PDF text extraction** still works
- **Word document processing** still works
- **Image processing** shows helpful error messages
- **Graceful degradation** with clear error handling

---

## 🧪 Testing

### **Test the System**
```bash
python test_menu_processing.py
```

**Sample Test Output:**
```
🍽️ Testing Menu Processing System
==================================================
Stage 1: Testing Menu Text Parsing...
✅ Menu parsing successful!

📊 Menu Summary:
   • Total Sections: 4
   • Total Items: 15
   • Items with Prices: 15
   • Price Coverage: 100.0%
   • Price Range: $3.50 - $45.00
   • Average Price: $16.27
   • Dietary Tags Found: ['vegetarian', 'gluten_free', 'spicy']
   • Parsing Confidence: 92.3%
```

### **Test with Real Menu**
```bash
# Test with your actual menu PDF
curl -X POST "http://localhost:8000/api/menu/extract-and-parse" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@your_menu.pdf"
```

---

## 🎯 Use Cases

### **Restaurant Menu Digitization**
- Convert PDF menus to structured data
- Import legacy menu files  
- Create digital menu systems
- Enable menu search and filtering

### **Menu Analysis & Reporting**
- Price analysis across menu sections
- Dietary option availability tracking
- Menu complexity assessment
- Competitive menu comparison

### **Integration with POS Systems**
- Import menu items to point-of-sale
- Sync menu changes automatically
- Generate menu reports
- Track menu item performance

### **Customer-Facing Applications**
- Online ordering systems
- Menu filtering by dietary needs
- Price range filtering
- Search by menu item

---

## 📈 Confidence Scoring

The system provides confidence scores for parsing quality:

### **High Confidence (80-100%)**
- ✅ Clear section headers
- ✅ Most items have prices
- ✅ Good dietary tag detection
- ✅ Structured menu format

### **Medium Confidence (60-79%)**
- ⚠️  Some sections unclear
- ⚠️  Missing prices on some items
- ⚠️  Moderate formatting issues
- ⚠️  May need manual review

### **Low Confidence (0-59%)**
- ❌ Poor text extraction quality
- ❌ Few prices detected
- ❌ Unclear menu structure
- ❌ Requires manual correction

---

## 🔧 Troubleshooting

### **Low Confidence Scores**
1. **Improve image quality** - Use higher resolution scans
2. **Check file format** - PDF with searchable text works best
3. **Clean menu format** - Well-structured menus parse better
4. **Manual review** - Verify extracted text before parsing

### **Missing Prices**
- Check for non-standard price formats
- Look for "Market Price" or similar text
- Verify currency symbols are clear
- Consider manual price entry for missing items

### **Poor Section Detection**
- Ensure clear section headers (ALL CAPS works best)
- Use consistent formatting
- Separate sections with whitespace
- Consider manual section organization

---

## 🚀 Production Deployment

### **Performance Characteristics**
- **PDF Processing**: 2-5 seconds
- **Image OCR**: 5-15 seconds  
- **Large menus**: 10-30 seconds
- **Memory usage**: 100-500MB during processing

### **Scaling Considerations**
- Process files asynchronously for large volumes
- Cache processed results
- Implement file size limits
- Use background job queues for heavy processing

### **Error Handling**
- Graceful fallback when OCR unavailable
- Clear error messages for unsupported formats
- Retry logic for temporary failures
- Detailed logging for debugging

---

**🎉 The Menu Processing System transforms any menu file into structured, searchable data - enabling digital menu management, online ordering, and menu analytics!**
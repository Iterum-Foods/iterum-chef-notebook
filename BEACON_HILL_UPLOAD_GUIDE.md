# 🍸 Beacon Hill Cocktail Bar PDF Upload Guide

## 📋 **How to Upload the Beacon Hill Cocktail Bar Menu**

I've prepared your Beacon Hill Cocktail Bar PDF menu for upload. Here's how to process it through your recipe upload system:

---

## 🚀 **Step-by-Step Upload Process**

### **1. Access the Upload Page**
- The recipe upload page should now be open in your browser
- If not, navigate to: `recipe-upload.html`

### **2. Upload the PDF File**
1. **Click "Choose File"** in the file upload section
2. **Navigate to**: `C:\Users\chefm\my-culinary-app\Iterum App\incoming_recipes\`
3. **Select**: `Beacon Hill Cocktail Bar.pdf`
4. **Click "Open"**

### **3. Set Recipe Type**
- **Select**: "Dish (Menu Item)" from the dropdown
- This will categorize the cocktails as menu items

### **4. Process the Upload**
- The system will automatically:
  - Extract text from the PDF
  - Parse cocktail recipes
  - Extract ingredients and instructions
  - Identify pricing information
  - Detect allergy warnings

### **5. Review and Approve**
- Click **"Go to Review Page"** to see parsed results
- Review each cocktail recipe
- Approve or edit as needed
- Add to your recipe library

---

## 🍹 **Expected Results from Beacon Hill Menu**

### **Cocktails That Should Be Extracted:**
- **Classic Cocktails**: Old Fashioned, Manhattan, Martini
- **Signature Drinks**: House specialties
- **Seasonal Offerings**: Limited-time cocktails
- **Wine & Beer**: Available selections

### **Information to Be Parsed:**
- ✅ **Cocktail Names** and descriptions
- ✅ **Ingredients** and measurements
- ✅ **Preparation Instructions**
- ✅ **Pricing** information
- ✅ **Allergy Warnings** (if any)
- ✅ **Glassware** requirements
- ✅ **Garnish** specifications

---

## 🔧 **Backend Processing**

### **PDF Text Extraction:**
- Uses **PDF.js** library for text extraction
- Processes all pages of the menu
- Extracts structured text content

### **Recipe Parsing:**
- **RecipeParser** service analyzes extracted text
- Identifies cocktail components automatically
- Structures data for database storage

### **API Endpoints Used:**
- `/api/uploads/parse-text` - Processes extracted text
- `/api/uploads/extract-text` - Handles file uploads
- `/api/recipes/` - Creates final recipes

---

## 📊 **What Happens After Upload**

### **1. Text Extraction Phase:**
```
PDF → PDF.js → Raw Text → Backend Processing
```

### **2. Recipe Parsing Phase:**
```
Raw Text → RecipeParser → Structured Data → Database
```

### **3. Review Phase:**
```
Structured Data → Review Interface → User Approval → Recipe Library
```

---

## 🎯 **Expected Cocktail Data Structure**

### **Example Parsed Cocktail:**
```json
{
  "title": "Beacon Hill Old Fashioned",
  "ingredients": [
    "2 oz Bourbon",
    "1/4 oz Simple Syrup",
    "2 dashes Angostura Bitters",
    "Orange peel garnish"
  ],
  "instructions": [
    "Combine bourbon, syrup, and bitters in mixing glass",
    "Add ice and stir until well-chilled",
    "Strain into rocks glass over large ice cube",
    "Express orange peel and garnish"
  ],
  "pricing_info": "$14",
  "glassware": "Rocks glass",
  "garnish": "Orange peel",
  "category": "Classic Cocktails"
}
```

---

## 🛠️ **Troubleshooting**

### **If Upload Fails:**
1. **Check file size** - PDF should be under 10MB
2. **Verify file format** - Must be valid PDF
3. **Check backend server** - Ensure it's running on port 8000
4. **Review console errors** - Check browser developer tools

### **If Parsing Issues:**
1. **Manual text extraction** - Copy text from PDF manually
2. **Use test parser** - Try the "Test Recipe Parsing" section
3. **Check parsed results** - Review what was extracted

### **If Backend Not Responding:**
```bash
# Start backend server
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📁 **File Locations**

### **Source File:**
- **Original**: `C:\Users\chefm\Downloads\Beacon Hill Cocktail Bar.pdf`
- **Copy**: `incoming_recipes\Beacon Hill Cocktail Bar.pdf`

### **Processing Files:**
- **Upload Page**: `recipe-upload.html`
- **Review Page**: `recipe-review.html`
- **Backend API**: `app/routers/uploads.py`

---

## 🎉 **Success Indicators**

### **Upload Success:**
- ✅ File appears in upload list
- ✅ "Processing..." message appears
- ✅ "Uploaded X file(s)" confirmation

### **Parsing Success:**
- ✅ Cocktails appear in review page
- ✅ Ingredients and instructions extracted
- ✅ Pricing information captured
- ✅ Ready for approval

### **Final Success:**
- ✅ Cocktails added to recipe library
- ✅ Available in menu builder
- ✅ Searchable in recipe finder

---

## 💡 **Pro Tips**

### **For Best Results:**
1. **High-quality PDF** - Clear, readable text
2. **Structured format** - Consistent layout helps parsing
3. **Complete information** - Include all cocktail details
4. **Review carefully** - Check parsed results before approval

### **Menu Optimization:**
- **Standardize format** - Consistent cocktail descriptions
- **Include pricing** - Helps with cost analysis
- **Add categories** - Organize by cocktail type
- **Note allergens** - Important for customer safety

---

## 🚀 **Ready to Upload!**

Your Beacon Hill Cocktail Bar PDF is ready for processing. The system will:

1. **Extract all cocktail recipes** from the PDF
2. **Parse ingredients and instructions** automatically
3. **Capture pricing and descriptions** accurately
4. **Organize into your recipe library** for easy access

**Start the upload process now and watch your cocktail menu come to life!** 🍸✨ 
# 🔍 OCR Setup Guide - Tesseract Installation

## Overview

The OCR Processing System requires Tesseract OCR engine to extract text from images and PDFs. This guide covers installation on different operating systems.

## 📋 Installation Instructions

### **Windows Installation**

#### **Option 1: Using Official Installer (Recommended)**
1. **Download Tesseract**: Go to https://github.com/UB-Mannheim/tesseract/wiki
2. **Run Installer**: Download and run the Windows installer (.exe)
3. **Default Installation Path**: `C:\Program Files\Tesseract-OCR\`
4. **Add to PATH**: The installer should add Tesseract to your PATH automatically

#### **Option 2: Using Chocolatey**
```bash
# Install Chocolatey package manager first (if not installed)
choco install tesseract
```

#### **Option 3: Using winget**
```bash
winget install UB-Mannheim.TesseractOCR
```

#### **Verify Installation**
```bash
# Open Command Prompt or PowerShell
tesseract --version
```

### **macOS Installation**

#### **Using Homebrew (Recommended)**
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tesseract
brew install tesseract
```

#### **Verify Installation**
```bash
tesseract --version
```

### **Linux Installation**

#### **Ubuntu/Debian**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

#### **CentOS/RHEL/Fedora**
```bash
# CentOS/RHEL
sudo yum install tesseract

# Fedora
sudo dnf install tesseract
```

#### **Verify Installation**
```bash
tesseract --version
```

## 🔧 Python Dependencies

Install the required Python packages:

```bash
# Install OCR-related dependencies
pip install pytesseract>=0.3.10
pip install Pillow>=10.1.0
pip install opencv-python>=4.8.1.78
pip install pdf2image>=1.16.3

# For PDF processing, you may also need poppler-utils:
# Windows: Download from http://blog.alivate.com.au/poppler-windows/
# macOS: brew install poppler
# Ubuntu: sudo apt install poppler-utils
```

## ⚙️ Configuration

### **Windows Configuration**
If Tesseract is not in your PATH, you may need to specify the path in your code:

```python
# In app/services/ocr_processor.py, update setup_tesseract method:
def setup_tesseract(self):
    import platform
    if platform.system() == "Windows":
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### **Language Packs (Optional)**
For better OCR accuracy with non-English text:

```bash
# Download additional language packs
# Place in Tesseract's tessdata directory

# Common language packs:
# - eng (English) - installed by default
# - fra (French)
# - spa (Spanish)
# - deu (German)
```

## 🧪 Testing OCR Installation

### **Test Script**
Create a test file to verify OCR is working:

```python
# test_ocr.py
import pytesseract
from PIL import Image
import requests

# Download a test image
test_image_url = "https://via.placeholder.com/300x100/000000/FFFFFF?text=Test+OCR"
response = requests.get(test_image_url)

with open("test_image.png", "wb") as f:
    f.write(response.content)

# Test OCR
try:
    image = Image.open("test_image.png")
    text = pytesseract.image_to_string(image)
    print(f"OCR Result: '{text.strip()}'")
    print("✅ OCR is working correctly!")
except Exception as e:
    print(f"❌ OCR test failed: {e}")
```

### **Run Test**
```bash
python test_ocr.py
```

## 🚀 Using the OCR System

### **1. Upload a Recipe Image/PDF**
```bash
curl -X POST "http://localhost:8000/api/uploads/recipe" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@recipe_image.jpg"
```

### **2. Process with OCR**
```bash
curl -X POST "http://localhost:8000/api/uploads/1/process" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **3. View Extracted Text**
```bash
curl -X GET "http://localhost:8000/api/uploads/1/ocr-text" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### **4. Create Recipe from OCR**
```bash
curl -X POST "http://localhost:8000/api/uploads/1/create-recipe" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔍 Troubleshooting

### **Common Issues**

#### **"tesseract not found" Error**
```bash
# Check if Tesseract is in PATH
tesseract --version

# If not found, add to PATH or specify full path in code
```

#### **Low OCR Accuracy**
- Ensure images are high resolution (300+ DPI)
- Images should have good contrast
- Text should be clearly readable
- Consider preprocessing images for better results

#### **PDF Processing Issues**
```bash
# Install poppler for PDF to image conversion
# Windows: Download poppler binaries
# macOS: brew install poppler
# Linux: sudo apt install poppler-utils
```

#### **Memory Issues with Large Files**
- The system processes files in chunks
- Consider resizing very large images
- PDFs are processed page by page

### **Performance Optimization**

#### **Image Preprocessing**
The system automatically:
- Converts to grayscale
- Applies noise reduction
- Enhances contrast
- Optimizes for text recognition

#### **OCR Configuration**
The system uses optimized Tesseract settings:
- OCR Engine Mode 3 (Default)
- Page Segmentation Mode 6 (Single uniform block)
- Character whitelist for recipe content

## 📊 Expected Results

### **Good OCR Candidates**
✅ High-resolution recipe photos  
✅ Scanned recipe cards  
✅ PDF cookbooks  
✅ Printed recipes with clear text  
✅ Screenshots of digital recipes  

### **Poor OCR Candidates**
❌ Handwritten recipes  
❌ Very low resolution images  
❌ Images with poor lighting  
❌ Heavily stylized fonts  
❌ Images with complex backgrounds  

### **Typical Accuracy**
- **High-quality scans**: 95-99% accuracy
- **Good photos**: 85-95% accuracy  
- **Average photos**: 70-85% accuracy
- **Poor quality**: 50-70% accuracy

## 🎯 Next Steps

Once OCR is working:
1. **Upload recipe images** via the frontend
2. **Review extracted text** before creating recipes
3. **Edit and refine** parsed recipe data
4. **Build your digital recipe library** from physical recipes

---

**💡 The OCR system transforms your physical recipe collection into a searchable, digital format - making decades of collected recipes instantly accessible!**
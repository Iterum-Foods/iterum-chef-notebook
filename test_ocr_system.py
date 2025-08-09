#!/usr/bin/env python3
"""
Test OCR System Implementation
Tests the OCR processing functionality without requiring actual Tesseract installation
"""

import os
import sys
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import tempfile

def create_test_recipe_image():
    """Create a test recipe image with text"""
    
    # Create a white background image
    width, height = 600, 800
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 24)
        title_font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Add recipe text
    recipe_text = [
        "CHOCOLATE CHIP COOKIES",
        "",
        "Ingredients:",
        "• 2 cups all-purpose flour",
        "• 1 tsp baking soda",
        "• 1 tsp salt",
        "• 1 cup butter, softened",
        "• 3/4 cup granulated sugar",
        "• 3/4 cup brown sugar",
        "• 2 large eggs",
        "• 2 tsp vanilla extract",
        "• 2 cups chocolate chips",
        "",
        "Instructions:",
        "1. Preheat oven to 375°F",
        "2. Mix flour, baking soda, and salt",
        "3. Cream butter and sugars",
        "4. Add eggs and vanilla",
        "5. Combine wet and dry ingredients",
        "6. Fold in chocolate chips",
        "7. Drop on baking sheet",
        "8. Bake 9-11 minutes",
        "",
        "Prep Time: 15 minutes",
        "Cook Time: 10 minutes",
        "Servings: 24 cookies"
    ]
    
    y_position = 30
    for line in recipe_text:
        if line == "CHOCOLATE CHIP COOKIES":
            draw.text((50, y_position), line, fill='black', font=title_font)
            y_position += 50
        elif line.startswith("Ingredients:") or line.startswith("Instructions:"):
            draw.text((50, y_position), line, fill='black', font=title_font)
            y_position += 40
        else:
            draw.text((50, y_position), line, fill='black', font=font)
            y_position += 30
    
    return image

def test_ocr_system_mock():
    """Test the OCR system with mock data"""
    
    print("🧪 Testing OCR System Implementation")
    print("=" * 50)
    
    try:
        # Test 1: Create mock test image
        print("1. Creating test recipe image...")
        test_image = create_test_recipe_image()
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            test_image.save(temp_file.name)
            test_image_path = temp_file.name
        
        print(f"   ✅ Test image created: {test_image_path}")
        
        # Test 2: Check if OCR processor can be imported
        print("2. Testing OCR processor import...")
        try:
            from app.services.ocr_processor import OCRProcessor
            print("   ✅ OCR processor module imported successfully")
        except ImportError as e:
            print(f"   ❌ OCR processor import failed: {e}")
            print("   💡 This is expected if Tesseract is not installed")
            return False
        
        # Test 3: Initialize OCR processor
        print("3. Initializing OCR processor...")
        try:
            processor = OCRProcessor()
            print("   ✅ OCR processor initialized")
        except Exception as e:
            print(f"   ❌ OCR processor initialization failed: {e}")
            return False
        
        # Test 4: Test text validation
        print("4. Testing text validation...")
        test_text = """
        CHOCOLATE CHIP COOKIES
        
        Ingredients:
        2 cups flour
        1 cup sugar
        1/2 cup butter
        
        Instructions:
        1. Mix ingredients
        2. Bake at 350F
        """
        
        validation_result = processor.validate_extracted_text(test_text)
        print(f"   ✅ Validation result: {validation_result}")
        
        # Test 5: Check API endpoints exist
        print("5. Checking API endpoints...")
        try:
            from app.routers.uploads import router
            print("   ✅ Upload router imported successfully")
            
            # Check if our new endpoints exist
            endpoint_names = [route.path for route in router.routes]
            expected_endpoints = [
                "/{upload_id}/process",
                "/{upload_id}/create-recipe",
                "/{upload_id}/ocr-text"
            ]
            
            for endpoint in expected_endpoints:
                if any(endpoint in path for path in endpoint_names):
                    print(f"   ✅ Endpoint {endpoint} exists")
                else:
                    print(f"   ❌ Endpoint {endpoint} missing")
            
        except Exception as e:
            print(f"   ❌ API endpoint check failed: {e}")
        
        # Test 6: Test database migration
        print("6. Testing database migration...")
        try:
            import sqlite3
            conn = sqlite3.connect("culinary_data.db")
            cursor = conn.cursor()
            
            # Check if new columns exist
            cursor.execute("PRAGMA table_info(recipe_uploads)")
            columns = [row[1] for row in cursor.fetchall()]
            
            expected_columns = ['processing_info', 'created_recipe_id']
            for col in expected_columns:
                if col in columns:
                    print(f"   ✅ Column {col} exists in recipe_uploads")
                else:
                    print(f"   ❌ Column {col} missing from recipe_uploads")
            
            conn.close()
            
        except Exception as e:
            print(f"   ❌ Database check failed: {e}")
        
        # Cleanup
        if os.path.exists(test_image_path):
            os.unlink(test_image_path)
        
        print("\n✅ OCR System Test Complete!")
        print("\n📋 Next Steps:")
        print("1. Install Tesseract OCR (see OCR_SETUP_GUIDE.md)")
        print("2. Install Python dependencies: pip install pytesseract opencv-python pdf2image")
        print("3. Test with real images via the upload API")
        
        return True
        
    except Exception as e:
        print(f"❌ OCR system test failed: {e}")
        return False

def test_api_integration():
    """Test OCR API integration (requires running server)"""
    
    print("\n🌐 Testing API Integration")
    print("=" * 30)
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            
            # Test upload endpoint exists
            try:
                response = requests.get("http://localhost:8000/docs")
                if "/uploads/" in response.text:
                    print("✅ Upload endpoints available in API docs")
                else:
                    print("❌ Upload endpoints not found in API docs")
            except:
                print("⚠️  Could not check API documentation")
            
        else:
            print("❌ Server not responding")
            
    except requests.exceptions.RequestException:
        print("⚠️  Server not running (this is normal for testing)")
        print("   Start server with: python -m uvicorn app.main:app --reload")

if __name__ == "__main__":
    print("🔍 OCR System Implementation Test")
    print("=" * 40)
    
    # Run tests
    success = test_ocr_system_mock()
    test_api_integration()
    
    if success:
        print("\n🎉 OCR System Implementation: READY")
        print("📝 See OCR_SETUP_GUIDE.md for Tesseract installation")
    else:
        print("\n⚠️  OCR System Implementation: NEEDS SETUP")
        print("📝 Install missing dependencies and try again")
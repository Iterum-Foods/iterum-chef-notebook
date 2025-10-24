#!/usr/bin/env python3
"""
Test script to verify menu parsing includes descriptions properly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.menu_parser import MenuParser
from services.enhanced_menu_parser import EnhancedMenuParser

def test_basic_parser_descriptions():
    """Test basic menu parser description extraction"""
    print("🧪 Testing Basic Menu Parser Descriptions")
    print("=" * 50)
    
    parser = MenuParser()
    
    # Test menu text with various description formats
    test_menu = """
    APPETIZERS
    
    Caesar Salad - Fresh romaine lettuce with parmesan cheese and croutons $8.99
    Served with house-made caesar dressing
    
    Buffalo Wings - Spicy chicken wings with celery and blue cheese dip $12.99
    Available in mild, medium, or hot
    
    MAIN COURSES
    
    Grilled Salmon - Fresh Atlantic salmon with lemon butter sauce $24.99
    Served with seasonal vegetables and rice pilaf
    
    Beef Tenderloin - 8oz center-cut beef tenderloin with red wine reduction $32.99
    Cooked to your preference, includes mashed potatoes and asparagus
    
    DESSERTS
    
    Chocolate Lava Cake - Warm chocolate cake with molten center $9.99
    Topped with vanilla ice cream and chocolate drizzle
    """
    
    result = parser.parse_menu_text(test_menu)
    
    print(f"✅ Parsed {len(result.get('sections', []))} sections")
    
    for section in result.get('sections', []):
        print(f"\n📂 Section: {section['name']}")
        for item in section.get('items', []):
            print(f"  🍽️ {item['title']}")
            print(f"     💰 ${item['price']}")
            if item.get('description'):
                print(f"     📝 {item['description']}")
            else:
                print(f"     ⚠️ No description")
    
    return result

def test_enhanced_parser_descriptions():
    """Test enhanced menu parser description extraction"""
    print("\n🚀 Testing Enhanced Menu Parser Descriptions")
    print("=" * 50)
    
    parser = EnhancedMenuParser()
    
    # Test menu text with various description formats
    test_menu = """
    STARTERS
    
    Lobster Bisque - Rich and creamy soup made with fresh lobster $11.99
    Garnished with chives and a touch of cognac
    
    Ahi Tuna Tartare - Fresh yellowfin tuna with avocado and wasabi mayo $16.99
    Served with crispy wonton chips
    
    ENTREES
    
    Filet Mignon - 10oz prime beef tenderloin with béarnaise sauce $38.99
    Accompanied by roasted fingerling potatoes and grilled asparagus
    
    Pan-Seared Halibut - Fresh halibut with lemon herb butter $28.99
    Served over wild rice pilaf with seasonal vegetables
    
    SWEETS
    
    Tiramisu - Classic Italian dessert with espresso and mascarpone $8.99
    Dusted with cocoa powder and served chilled
    """
    
    result = parser.parse_menu_text(test_menu, "text")
    
    print(f"✅ Parsed {len(result.get('sections', []))} sections")
    
    for section in result.get('sections', []):
        print(f"\n📂 Section: {section['name']}")
        for item in section.get('items', []):
            print(f"  🍽️ {item['title']}")
            print(f"     💰 ${item['price']}")
            if item.get('description'):
                print(f"     📝 {item['description']}")
            else:
                print(f"     ⚠️ No description")
    
    return result

def test_description_detection():
    """Test description detection logic"""
    print("\n🔍 Testing Description Detection")
    print("=" * 50)
    
    parser = MenuParser()
    
    test_lines = [
        "Caesar Salad - Fresh romaine lettuce with parmesan cheese",
        "Served with house-made caesar dressing",
        "Available in mild, medium, or hot",
        "Cooked to your preference, includes mashed potatoes",
        "Topped with vanilla ice cream and chocolate drizzle",
        "Garnished with chives and a touch of cognac",
        "Served with crispy wonton chips",
        "Accompanied by roasted fingerling potatoes",
        "Dusted with cocoa powder and served chilled"
    ]
    
    for line in test_lines:
        is_desc = parser.looks_like_description(line)
        status = "✅ Description" if is_desc else "❌ Not Description"
        print(f"{status}: {line}")

def main():
    """Run all tests"""
    print("🍽️ Menu Parsing Description Tests")
    print("=" * 60)
    
    try:
        # Test basic parser
        basic_result = test_basic_parser_descriptions()
        
        # Test enhanced parser
        enhanced_result = test_enhanced_parser_descriptions()
        
        # Test description detection
        test_description_detection()
        
        print("\n🎉 All tests completed!")
        
        # Summary
        basic_items = sum(len(section.get('items', [])) for section in basic_result.get('sections', []))
        enhanced_items = sum(len(section.get('items', [])) for section in enhanced_result.get('sections', []))
        
        print(f"\n📊 Summary:")
        print(f"  Basic Parser: {basic_items} items parsed")
        print(f"  Enhanced Parser: {enhanced_items} items parsed")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

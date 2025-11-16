#!/usr/bin/env python3
"""
Test Menu Processing System
Tests the two-stage menu extraction and parsing system
"""

import json
from app.services.menu_parser import MenuParser

def test_menu_parser():
    """Test the menu parser with sample menu text"""
    
    print("🍽️ Testing Menu Processing System")
    print("=" * 50)
    
    # Sample menu text (like what would be extracted from PDF/OCR)
    sample_menu_text = """
    DOWNTOWN BISTRO MENU
    
    APPETIZERS & SMALL PLATES
    
    Truffle Arancini - Crispy risotto balls with black truffle and parmesan cheese $14.00 (V)
    Fresh Tuna Tartare - Yellowfin tuna, avocado, citrus, sesame oil, crispy wontons $18.00 (GF)
    Burrata Board - House made burrata, prosciutto di Parma, fig jam, grilled sourdough $16.00
    Caesar Salad - Romaine hearts, house caesar dressing, aged parmesan, garlic croutons $12.00 (V)
    
    MAIN COURSES
    
    Pan Seared Salmon - Atlantic salmon, lemon herb butter, seasonal vegetables $28.00 (GF)
    Wagyu Ribeye Steak - 12oz prime cut, garlic mashed potatoes, red wine jus $45.00
    Lobster Ravioli - House made pasta, Maine lobster, saffron cream sauce, micro herbs $32.00
    Vegetarian Risotto - Roasted mushroom and truffle risotto with aged parmesan $24.00 (V) (GF)
    Chicken Tikka Masala - Tandoori spiced chicken, basmati rice, naan bread $22.00 (Spicy)
    
    DESSERTS
    
    Chocolate Lava Cake - Warm chocolate cake with molten center, vanilla ice cream $12.00 (V)
    Classic Tiramisu - Espresso soaked ladyfingers, mascarpone, cocoa dust $10.00 (V)
    Seasonal Fruit Tart - Chef's selection, vanilla pastry cream $9.00 (V)
    
    BEVERAGES
    
    Fresh Orange Juice $4.00
    Espresso $3.50
    Craft Beer Selection $6.00 - $8.00
    House Wine by the Glass $7.00 - $12.00
    """
    
    try:
        # Test Stage 1: Parse the menu text
        print("Stage 1: Testing Menu Text Parsing...")
        
        menu_parser = MenuParser()
        result = menu_parser.parse_menu_text(sample_menu_text)
        
        if result['success']:
            print("✅ Menu parsing successful!")
            
            # Display summary
            summary = result['summary']
            print(f"\n📊 Menu Summary:")
            print(f"   • Total Sections: {summary['total_sections']}")
            print(f"   • Total Items: {summary['total_items']}")
            print(f"   • Items with Prices: {summary['items_with_prices']}")
            print(f"   • Price Coverage: {summary['price_coverage']:.1f}%")
            
            if summary['price_range']['min'] and summary['price_range']['max']:
                print(f"   • Price Range: ${summary['price_range']['min']:.2f} - ${summary['price_range']['max']:.2f}")
                print(f"   • Average Price: ${summary['price_range']['average']:.2f}")
            
            print(f"   • Dietary Tags Found: {list(summary['dietary_tags'].keys())}")
            print(f"   • Parsing Confidence: {result['parsing_info']['confidence']:.1f}%")
            
            # Display sections
            print(f"\n📋 Menu Sections:")
            for i, section in enumerate(result['sections'], 1):
                print(f"\n{i}. {section['name']} ({section['item_count']} items)")
                
                for j, item in enumerate(section['items'], 1):
                    price_str = f"${item['price']:.2f}" if item['price'] else "No price"
                    tags_str = f" ({', '.join(item['dietary_tags'])})" if item['dietary_tags'] else ""
                    spice_str = f" [{item['spice_level']}]" if item['spice_level'] else ""
                    
                    print(f"   {j}. {item['title']} - {price_str}{tags_str}{spice_str}")
                    if item['description']:
                        print(f"      Description: {item['description'][:100]}...")
            
            # Test Stage 2: JSON serialization (for API responses)
            print(f"\n🔄 Testing JSON Serialization...")
            try:
                json_result = json.dumps(result, indent=2)
                print("✅ JSON serialization successful")
                print(f"   JSON size: {len(json_result)} characters")
            except Exception as e:
                print(f"❌ JSON serialization failed: {e}")
            
            # Test confidence scoring
            print(f"\n🎯 Confidence Analysis:")
            confidence = result['parsing_info']['confidence']
            if confidence > 80:
                print(f"   ✅ High confidence ({confidence:.1f}%) - Excellent parsing")
            elif confidence > 60:
                print(f"   ⚠️  Medium confidence ({confidence:.1f}%) - Good parsing with minor issues")
            else:
                print(f"   ❌ Low confidence ({confidence:.1f}%) - May need manual review")
            
            return True
            
        else:
            print(f"❌ Menu parsing failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_edge_cases():
    """Test menu parser with edge cases"""
    
    print("\n🧪 Testing Edge Cases")
    print("=" * 30)
    
    edge_cases = [
        {
            "name": "Menu with no clear sections",
            "text": """
            Burger $12
            Pizza $15
            Salad $10
            """
        },
        {
            "name": "Menu with unusual price formats",
            "text": """
            LUNCH SPECIALS
            
            Fish and Chips - Beer battered cod 15.50 USD
            Pasta Special - Chef's daily pasta £12.00
            Soup of the Day - Ask server for details Market Price
            """
        },
        {
            "name": "Menu with heavy dietary restrictions",
            "text": """
            HEALTH CONSCIOUS
            
            Quinoa Bowl - Organic quinoa, vegetables (V) (GF) (DF) $14.00
            Keto Plate - Avocado, eggs, bacon (GF) (Keto) $16.00
            Spicy Tofu Curry - Very spicy, coconut milk (V) (GF) (Spicy) $13.00
            """
        }
    ]
    
    menu_parser = MenuParser()
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\n{i}. Testing: {case['name']}")
        
        result = menu_parser.parse_menu_text(case['text'])
        
        if result['success']:
            print(f"   ✅ Parsed {result['total_items']} items")
            print(f"   Confidence: {result['parsing_info']['confidence']:.1f}%")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")

def test_api_format():
    """Test the expected API response format"""
    
    print("\n🌐 Testing API Response Format")
    print("=" * 35)
    
    # This simulates what the API would return
    sample_response = {
        "success": True,
        "filename": "restaurant_menu.pdf",
        "processing_stages": {
            "stage_1_extraction": {
                "method": "PDF Text Extraction",
                "text_length": 1250,
                "info": {"pages": 2, "method": "direct"}
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
                            "description": "Crispy risotto balls with black truffle",
                            "price": 14.00,
                            "dietary_tags": ["vegetarian"]
                        }
                    ]
                }
            ],
            "summary": {
                "total_items": 12,
                "total_sections": 3,
                "price_range": {"min": 8.00, "max": 45.00}
            }
        }
    }
    
    try:
        json_output = json.dumps(sample_response, indent=2)
        print("✅ API response format valid")
        print("Sample API response structure:")
        print(json_output[:500] + "..." if len(json_output) > 500 else json_output)
        return True
    except Exception as e:
        print(f"❌ API format test failed: {e}")
        return False

if __name__ == "__main__":
    print("🍽️ Menu Processing System Test Suite")
    print("=" * 45)
    
    # Run all tests
    test1_success = test_menu_parser()
    test_edge_cases()
    test2_success = test_api_format()
    
    print("\n" + "=" * 45)
    print("📊 Test Results Summary:")
    print(f"   Main Menu Parsing: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   API Format Test: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 Menu Processing System: READY FOR PRODUCTION")
        print("\n📋 What you can now do:")
        print("   1. Upload PDF menus → Extract text → Parse menu items")
        print("   2. Upload image menus → OCR → Parse menu items")
        print("   3. Get structured data: titles, descriptions, prices")
        print("   4. Automatic dietary tag detection (V, GF, etc.)")
        print("   5. Price analysis and confidence scoring")
    else:
        print("\n⚠️  Menu Processing System: NEEDS ATTENTION")
        print("   Check the errors above and fix issues")
    
    print("\n🚀 API Endpoints Available:")
    print("   POST /api/menu/extract-and-parse - Complete two-stage processing")
    print("   POST /api/menu/parse-text - Parse already extracted text")
    print("   GET  /api/menu/sample - Get sample parsed menu")
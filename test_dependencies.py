#!/usr/bin/env python
"""
Test script to verify all dependencies are working
"""

def test_pandas():
    """Test pandas import and basic functionality"""
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
        
        # Test basic DataFrame creation
        df = pd.DataFrame({'test': [1, 2, 3]})
        print(f"✅ pandas DataFrame created: {len(df)} rows")
        return True
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False

def test_openpyxl():
    """Test openpyxl import"""
    try:
        import openpyxl
        print("✅ openpyxl imported successfully")
        return True
    except ImportError as e:
        print(f"❌ openpyxl import failed: {e}")
        return False

def test_pillow():
    """Test Pillow import"""
    try:
        from PIL import Image
        print("✅ Pillow (PIL) imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False

def test_excel_creation():
    """Test Excel file creation"""
    try:
        import pandas as pd
        from io import BytesIO
        
        # Create test data
        data = {
            'first_name': ['John', 'Jane'],
            'last_name': ['Doe', 'Smith'],
            'national_id': ['12345678', '87654321']
        }
        
        df = pd.DataFrame(data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Test', index=False)
        
        output.seek(0)
        size = len(output.getvalue())
        print(f"✅ Excel file created successfully: {size} bytes")
        return True
    except Exception as e:
        print(f"❌ Excel creation failed: {e}")
        return False

def main():
    print("🔧 Testing payroll system dependencies...")
    
    tests = [
        ("Pandas", test_pandas),
        ("OpenPyXL", test_openpyxl),
        ("Pillow", test_pillow),
        ("Excel Creation", test_excel_creation),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Testing {name}...")
        result = test_func()
        results.append((name, result))
    
    print("\n" + "="*50)
    print("📊 DEPENDENCY TEST RESULTS:")
    print("="*50)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:15} {status}")
        if not passed:
            all_passed = False
    
    print("="*50)
    if all_passed:
        print("🎉 All dependencies are working correctly!")
        print("✅ Bulk upload and logo features should work")
    else:
        print("⚠️ Some dependencies failed - features may not work")
    
    return all_passed

if __name__ == '__main__':
    main()

Recipe Library Excel Converter
============================

This tool converts all recipes in the recipe_library/ folder into a standardized Excel format for easy import into the Iterum App or other systems.

How to Use:
-----------
1. Place your recipe files in the recipe_library/ folder.
2. Double-click convert_to_excel.bat to run the conversion.
   - OR run: python convert_to_excel.py
3. Converted Excel files will appear in the converted_excel/ folder.

Missing information in recipes will be flagged as 'TO FILL' in the output files.

Requirements:
-------------
- Python 3.x
- openpyxl (install with: pip install openpyxl) 
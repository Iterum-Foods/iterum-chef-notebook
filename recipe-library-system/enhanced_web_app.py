#!/usr/bin/env python3
"""
Enhanced Recipe Management Web Application
Modern UI with thorough directory search, conversion, missing info detection, and sorting
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import os
import sys

# Add local modules to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "RecipeLibrarySystem"))

from enhanced_recipe_scanner import EnhancedRecipeScanner
from missing_info_detector import MissingInfoDetector
from standardize_recipes import IterumRecipeConverter
from web_recipe_scraper import WebRecipeScraper
from website_recipe_crawler import WebsiteRecipeCrawler

app = Flask(__name__)
app.secret_key = 'recipe-manager-secret-key-change-this'

# Configuration
LIBRARY_PATH = Path("recipe_library")
DB_PATH = LIBRARY_PATH / "recipe_library.db"
CONVERTED_PATH = Path("converted_iterum")

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_library_stats():
    """Get library statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM recipes")
    total = cursor.fetchone()['count']
    
    cursor.execute("SELECT cuisine_type, COUNT(*) as count FROM recipes GROUP BY cuisine_type ORDER BY count DESC")
    by_cuisine = {row['cuisine_type']: row['count'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT category, COUNT(*) as count FROM recipes GROUP BY category")
    by_category = {row['category']: row['count'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT difficulty, COUNT(*) as count FROM recipes GROUP BY difficulty")
    by_difficulty = {row['difficulty']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        'total': total,
        'by_cuisine': by_cuisine,
        'by_category': by_category,
        'by_difficulty': by_difficulty
    }

@app.route('/')
def index():
    """Home page with dashboard."""
    stats = get_library_stats()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes ORDER BY modified_date DESC LIMIT 6")
    recent_recipes = cursor.fetchall()
    conn.close()
    
    return render_template('enhanced_index.html', stats=stats, recent_recipes=recent_recipes)

@app.route('/recipes')
def recipes():
    """Browse all recipes with advanced sorting and filtering."""
    # Get filters and sort options
    cuisine = request.args.get('cuisine', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'title')  # title, date, cuisine, difficulty
    sort_order = request.args.get('order', 'asc')  # asc, desc
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []
    
    if cuisine and cuisine != 'all':
        query += " AND cuisine_type = ?"
        params.append(cuisine)
    
    if category and category != 'all':
        query += " AND category = ?"
        params.append(category)
    
    if difficulty and difficulty != 'all':
        query += " AND difficulty = ?"
        params.append(difficulty)
    
    if search:
        query += " AND (title LIKE ? OR content_preview LIKE ?)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    # Add sorting
    valid_sort_fields = {'title': 'title', 'date': 'modified_date', 'cuisine': 'cuisine_type', 'difficulty': 'difficulty'}
    sort_field = valid_sort_fields.get(sort_by, 'title')
    order = 'DESC' if sort_order == 'desc' else 'ASC'
    query += f" ORDER BY {sort_field} {order}"
    
    cursor.execute(query, params)
    all_recipes = cursor.fetchall()
    conn.close()
    
    stats = get_library_stats()
    
    return render_template('enhanced_recipes.html', 
                         recipes=all_recipes, 
                         stats=stats,
                         current_cuisine=cuisine,
                         current_category=category,
                         current_difficulty=difficulty,
                         current_search=search,
                         current_sort=sort_by,
                         current_order=sort_order)

@app.route('/organize')
def organize():
    """Enhanced organize page with thorough directory scanning."""
    return render_template('enhanced_organize.html')

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """API endpoint for thorough directory scanning."""
    data = request.json
    directory_path = data.get('directory_path', '')
    recursive = data.get('recursive', True)
    
    if not directory_path or not Path(directory_path).exists():
        return jsonify({'success': False, 'error': 'Invalid directory path'})
    
    try:
        scanner = EnhancedRecipeScanner()
        result = scanner.scan_directory_thoroughly(directory_path, recursive)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/organize', methods=['POST'])
def api_organize():
    """API endpoint to organize recipes."""
    data = request.json
    folder_path = data.get('folder_path', '')
    mode = data.get('mode', 'copy')
    
    if not folder_path or not Path(folder_path).exists():
        return jsonify({'success': False, 'error': 'Invalid folder path'})
    
    try:
        scanner = EnhancedRecipeScanner()
        result = scanner.scan_directory_thoroughly(folder_path, recursive=True)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/convert')
def convert():
    """Enhanced convert page with missing info detection."""
    stats = get_library_stats()
    
    # Get missing info summary
    try:
        detector = MissingInfoDetector()
        analysis = detector.analyze_all_recipes()
        missing_info_summary = analysis['summary']
    except:
        missing_info_summary = None
    
    return render_template('enhanced_convert.html', stats=stats, missing_info=missing_info_summary)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API endpoint to convert recipes to Iterum format."""
    try:
        converter = IterumRecipeConverter()
        converted, errors = converter.convert_all_recipes()
        
        return jsonify({
            'success': True,
            'converted': len(converted),
            'errors': len(errors),
            'error_details': [{'title': t, 'error': e} for t, e in errors]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/missing-info')
def missing_info():
    """Page showing missing information analysis."""
    try:
        detector = MissingInfoDetector()
        analysis = detector.analyze_all_recipes()
        return render_template('missing_info.html', analysis=analysis)
    except Exception as e:
        flash(f'Error analyzing recipes: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/missing-info', methods=['GET'])
def api_missing_info():
    """API endpoint for missing information analysis."""
    try:
        recipe_id = request.args.get('recipe_id')
        file_path = request.args.get('file_path')
        
        detector = MissingInfoDetector()
        
        if recipe_id:
            analysis = detector.analyze_recipe(recipe_id=recipe_id)
        elif file_path:
            analysis = detector.analyze_recipe(file_path=Path(file_path))
        else:
            analysis = detector.analyze_all_recipes()
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/recipe/<recipe_id>')
def recipe_detail(recipe_id):
    """View recipe details with missing info."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    conn.close()
    
    if not recipe:
        flash('Recipe not found', 'error')
        return redirect(url_for('recipes'))
    
    # Get missing info for this recipe
    try:
        detector = MissingInfoDetector()
        missing_info = detector.analyze_recipe(recipe_id=recipe_id)
    except:
        missing_info = None
    
    return render_template('enhanced_recipe_detail.html', recipe=recipe, missing_info=missing_info)

@app.route('/api/search', methods=['GET'])
def api_search():
    """API endpoint for quick search."""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'results': []})
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, cuisine_type, category 
        FROM recipes 
        WHERE title LIKE ? OR content_preview LIKE ?
        LIMIT 10
    """, (f'%{query}%', f'%{query}%'))
    
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'results': results})

@app.route('/scrape')
def scrape():
    """Web recipe scraping page."""
    return render_template('enhanced_scrape.html')

@app.route('/crawl')
def crawl():
    """Website crawling page."""
    return render_template('enhanced_crawl.html')

@app.route('/api/scrape', methods=['POST'])
def api_scrape():
    """API endpoint for scraping recipes from URLs."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        urls = data.get('urls', [])
        
        if not url and not urls:
            return jsonify({'success': False, 'error': 'No URL provided'})
        
        scraper = WebRecipeScraper(library_path=str(LIBRARY_PATH))
        
        if urls:
            # Multiple URLs
            results = scraper.scrape_multiple(urls)
            return jsonify({
                'success': True,
                'results': results
            })
        else:
            # Single URL
            recipe_entry = scraper.scrape_and_import(url)
            if recipe_entry:
                return jsonify({
                    'success': True,
                    'recipe': {
                        'id': recipe_entry.id,
                        'title': recipe_entry.title,
                        'cuisine': recipe_entry.cuisine_type,
                        'category': recipe_entry.category
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Could not extract recipe from URL'
                })
                
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/crawl', methods=['POST'])
def api_crawl():
    """API endpoint for crawling websites."""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        format_type = data.get('format', 'json')
        max_pages = int(data.get('max_pages', 100))
        delay = float(data.get('delay', 1.0))
        crawl_only = data.get('crawl_only', False)
        
        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'})
        
        crawler = WebsiteRecipeCrawler(
            base_url=url,
            max_pages=max_pages,
            delay=delay
        )
        
        if crawl_only:
            # Just crawl, don't scrape
            results = crawler.crawl()
            return jsonify({
                'success': True,
                'crawl_only': True,
                'results': results
            })
        else:
            # Full crawl and export
            results = crawler.crawl_and_export(format=format_type)
            
            if results['success']:
                return jsonify({
                    'success': True,
                    'output_file': results['output_file'],
                    'recipes_count': results['recipes_count'],
                    'crawl_results': results['crawl_results']
                })
            else:
                return jsonify({
                    'success': False,
                    'error': results.get('error', 'Unknown error'),
                    'crawl_results': results.get('crawl_results', {})
                })
                
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/statistics')
def statistics():
    """Detailed statistics page."""
    stats = get_library_stats()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes")
    all_recipes = cursor.fetchall()
    
    total_size = sum(r['file_size'] for r in all_recipes if r['file_size'])
    top_cuisines = sorted(stats['by_cuisine'].items(), key=lambda x: x[1], reverse=True)[:5]
    
    cursor.execute("SELECT * FROM recipes ORDER BY created_date DESC LIMIT 10")
    recent = cursor.fetchall()
    
    conn.close()
    
    return render_template('enhanced_statistics.html', 
                         stats=stats,
                         total_size=total_size,
                         top_cuisines=top_cuisines,
                         recent=recent)

if __name__ == '__main__':
    # Create necessary directories
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    LIBRARY_PATH.mkdir(exist_ok=True)
    CONVERTED_PATH.mkdir(exist_ok=True)
    
    print("\n" + "=" * 80)
    print("           ENHANCED RECIPE MANAGEMENT SYSTEM")
    print("=" * 80)
    print("\n✓ Starting enhanced web server...")
    print("\n→ Open your browser and go to: http://localhost:5000")
    print("\n✓ Server is running. Press Ctrl+C to stop.")
    print("=" * 80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)



#!/usr/bin/env python3
"""
Recipe Management System - Modern Web Interface
Beautiful, professional UI accessible from any browser
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import sqlite3
import json
from pathlib import Path
from datetime import datetime
import os

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
    
    # Total recipes
    cursor.execute("SELECT COUNT(*) as count FROM recipes")
    total = cursor.fetchone()['count']
    
    # By cuisine
    cursor.execute("SELECT cuisine_type, COUNT(*) as count FROM recipes GROUP BY cuisine_type ORDER BY count DESC")
    by_cuisine = {row['cuisine_type']: row['count'] for row in cursor.fetchall()}
    
    # By category
    cursor.execute("SELECT category, COUNT(*) as count FROM recipes GROUP BY category")
    by_category = {row['category']: row['count'] for row in cursor.fetchall()}
    
    # By difficulty
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
    
    # Get recent recipes
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes ORDER BY modified_date DESC LIMIT 6")
    recent_recipes = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', stats=stats, recent_recipes=recent_recipes)

@app.route('/recipes')
def recipes():
    """Browse all recipes."""
    # Get filters from query params
    cuisine = request.args.get('cuisine', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    search = request.args.get('search', '')
    
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
    
    query += " ORDER BY title"
    
    cursor.execute(query, params)
    all_recipes = cursor.fetchall()
    conn.close()
    
    # Get filter options
    stats = get_library_stats()
    
    return render_template('recipes.html', 
                         recipes=all_recipes, 
                         stats=stats,
                         current_cuisine=cuisine,
                         current_category=category,
                         current_difficulty=difficulty,
                         current_search=search)

@app.route('/recipe/<recipe_id>')
def recipe_detail(recipe_id):
    """View recipe details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = cursor.fetchone()
    conn.close()
    
    if not recipe:
        flash('Recipe not found', 'error')
        return redirect(url_for('recipes'))
    
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/organize')
def organize():
    """Organize recipes page."""
    return render_template('organize.html')

@app.route('/api/organize', methods=['POST'])
def api_organize():
    """API endpoint to organize recipes."""
    data = request.json
    folder_path = data.get('folder_path', '')
    mode = data.get('mode', 'copy')  # copy or move
    
    if not folder_path or not Path(folder_path).exists():
        return jsonify({'success': False, 'error': 'Invalid folder path'})
    
    try:
        # Import and run organizer
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "RecipeLibrarySystem"))
        from recipe_library_system import RecipeLibrary
        
        library = RecipeLibrary(source_folder=folder_path)
        recipes = library.scan_and_import()
        
        return jsonify({
            'success': True,
            'count': len(recipes),
            'recipes': [{'title': r.title, 'cuisine': r.cuisine_type} for r in recipes]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/convert')
def convert():
    """Convert recipes page."""
    stats = get_library_stats()
    return render_template('convert.html', stats=stats)

@app.route('/api/convert', methods=['POST'])
def api_convert():
    """API endpoint to convert recipes to Iterum format."""
    try:
        from standardize_recipes import IterumRecipeConverter
        
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

@app.route('/sync')
def sync():
    """Google Drive sync page."""
    return render_template('sync.html')

@app.route('/api/sync', methods=['POST'])
def api_sync():
    """API endpoint for Google Drive sync."""
    action = request.json.get('action', '')
    
    try:
        from google_drive_integration import GoogleDriveRecipeManager
        
        manager = GoogleDriveRecipeManager()
        
        if action == 'upload':
            manager.upload_all_recipes()
            return jsonify({'success': True, 'message': 'Recipes uploaded to Google Drive'})
        
        elif action == 'sync_to':
            manager.sync_to_drive()
            return jsonify({'success': True, 'message': 'Synced to Google Drive'})
        
        elif action == 'sync_from':
            manager.sync_from_drive()
            return jsonify({'success': True, 'message': 'Synced from Google Drive'})
        
        elif action == 'backup':
            manager.create_backup()
            return jsonify({'success': True, 'message': 'Backup created'})
        
        else:
            return jsonify({'success': False, 'error': 'Invalid action'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/track')
def track():
    """Track recipe sources page."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all unique sources
    cursor.execute("SELECT DISTINCT file_path FROM recipes")
    paths = cursor.fetchall()
    
    # Group by source folder
    sources = {}
    for row in paths:
        path = Path(row['file_path'])
        source = path.parent.name if path.parent.name else 'Root'
        if source not in sources:
            sources[source] = []
        sources[source].append(path.name)
    
    conn.close()
    
    return render_template('track.html', sources=sources)

@app.route('/statistics')
def statistics():
    """Detailed statistics page."""
    stats = get_library_stats()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all recipes for detailed analysis
    cursor.execute("SELECT * FROM recipes")
    all_recipes = cursor.fetchall()
    
    # Calculate additional stats
    total_size = sum(r['file_size'] for r in all_recipes if r['file_size'])
    
    # Top cuisines
    top_cuisines = sorted(stats['by_cuisine'].items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Recent additions
    cursor.execute("SELECT * FROM recipes ORDER BY created_date DESC LIMIT 10")
    recent = cursor.fetchall()
    
    conn.close()
    
    return render_template('statistics.html', 
                         stats=stats,
                         total_size=total_size,
                         top_cuisines=top_cuisines,
                         recent=recent)

@app.route('/settings')
def settings():
    """Settings page."""
    return render_template('settings.html')

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

if __name__ == '__main__':
    # Create templates folder if it doesn't exist
    Path('templates').mkdir(exist_ok=True)
    Path('static').mkdir(exist_ok=True)
    
    print("\n" + "=" * 80)
    print("           RECIPE MANAGEMENT SYSTEM - WEB INTERFACE")
    print("=" * 80)
    print("\n✓ Starting web server...")
    print("\n→ Open your browser and go to: http://localhost:5000")
    print("\n✓ Server is running. Press Ctrl+C to stop.")
    print("=" * 80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)



#!/usr/bin/env python3
"""
Unified Recipe Management Dashboard
Desktop application combining all recipe management features
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, simpledialog
import sys
import threading
from pathlib import Path
import sqlite3
from datetime import datetime
import webbrowser

# Add local modules to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "RecipeLibrarySystem"))

try:
    from enhanced_recipe_scanner import EnhancedRecipeScanner
    from missing_info_detector import MissingInfoDetector
    from standardize_recipes import IterumRecipeConverter
    from web_recipe_scraper import WebRecipeScraper
    from website_recipe_crawler import WebsiteRecipeCrawler
    from recipe_library_system import RecipeLibrary
    from ingredient_database import IngredientDatabase
    from vendor_price_importer import VendorPriceImporter
    from ingredient_web_scraper import IngredientWebScraper
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")


class UnifiedDashboard:
    """Main desktop dashboard application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Recipe Management System - Unified Dashboard")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configuration
        self.library_path = Path("recipe_library")
        self.db_path = self.library_path / "recipe_library.db"
        self.converted_path = Path("converted_iterum")
        
        # Initialize components
        self.scanner = None
        self.converter = None
        self.scraper = None
        self.crawler = None
        self.ingredient_db = IngredientDatabase()
        
        self.setup_ui()
        self.refresh_stats()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header
        header = ttk.Frame(main_container)
        header.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title = ttk.Label(header, text="🍳 Recipe Management System", 
                         font=("Arial", 20, "bold"))
        title.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(header, text="🔄 Refresh Stats", 
                                command=self.refresh_stats)
        refresh_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Left sidebar - Statistics
        stats_frame = ttk.LabelFrame(main_container, text="📊 Library Statistics", padding="10")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        stats_frame.columnconfigure(0, weight=1)
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, height=15, width=30, 
                                                     state=tk.DISABLED, wrap=tk.WORD)
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        stats_frame.rowconfigure(0, weight=1)
        
        # Right side - Main content area with tabs
        notebook = ttk.Notebook(main_container)
        notebook.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tab 1: Organize & Scan
        self.setup_organize_tab(notebook)
        
        # Tab 2: Convert
        self.setup_convert_tab(notebook)
        
        # Tab 3: Web Scraping
        self.setup_scrape_tab(notebook)
        
        # Tab 4: Website Crawling
        self.setup_crawl_tab(notebook)
        
        # Tab 5: Browse Recipes
        self.setup_browse_tab(notebook)
        
        # Tab 6: Source Tracking
        self.setup_tracking_tab(notebook)
        
        # Tab 7: Ingredient Database
        self.setup_ingredient_tab(notebook)
        
    def setup_organize_tab(self, notebook):
        """Set up the organize/scan tab."""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="📂 Organize & Scan")
        
        # Instructions
        ttk.Label(frame, text="Scan directories to organize recipes into your library", 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Directory selection
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dir_frame, text="Directory:").pack(side=tk.LEFT, padx=(0, 5))
        self.scan_dir_var = tk.StringVar()
        dir_entry = ttk.Entry(dir_frame, textvariable=self.scan_dir_var, width=50)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(dir_frame, text="Browse...", 
                  command=lambda: self.scan_dir_var.set(filedialog.askdirectory())).pack(side=tk.LEFT)
        
        # Options
        options_frame = ttk.LabelFrame(frame, text="Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Recursive (search subdirectories)", 
                       variable=self.recursive_var).pack(anchor=tk.W)
        
        # Scan button
        scan_btn = ttk.Button(frame, text="🔍 Scan Directory", 
                            command=self.scan_directory, style="Accent.TButton")
        scan_btn.pack(pady=10)
        
        # Progress
        self.scan_progress = ttk.Progressbar(frame, mode='indeterminate')
        self.scan_progress.pack(fill=tk.X, pady=5)
        
        # Results
        results_frame = ttk.LabelFrame(frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.scan_results = scrolledtext.ScrolledText(results_frame, height=10, wrap=tk.WORD)
        self.scan_results.pack(fill=tk.BOTH, expand=True)
        
    def setup_convert_tab(self, notebook):
        """Set up the convert tab with recipe selection and missing info editing."""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="🔄 Convert to Iterum")
        
        ttk.Label(frame, text="Select recipes to convert and fill in missing information", 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Top buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="📋 Load All Recipes", 
                  command=self.load_recipes_for_conversion).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="✅ Select All", 
                  command=self.select_all_recipes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="❌ Deselect All", 
                  command=self.deselect_all_recipes).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🔍 Analyze Missing Info", 
                  command=self.analyze_missing_info).pack(side=tk.LEFT, padx=5)
        
        # Recipe list with checkboxes
        list_frame = ttk.LabelFrame(frame, text="Recipes to Convert", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create scrollable frame for recipe list
        canvas = tk.Canvas(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.recipe_list_frame = scrollable_frame
        self.recipe_checkboxes = {}  # recipe_id -> (checkbox, var, info_frame)
        self.recipe_missing_info = {}  # recipe_id -> missing_info_dict
        
        # Bottom section - Missing info editor
        editor_frame = ttk.LabelFrame(frame, text="Edit Missing Information", padding="10")
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Selected recipe info
        self.selected_recipe_var = tk.StringVar(value="No recipe selected")
        ttk.Label(editor_frame, textvariable=self.selected_recipe_var, 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=5)
        
        # Missing info editor
        editor_inner = ttk.Frame(editor_frame)
        editor_inner.pack(fill=tk.BOTH, expand=True)
        
        # Left side - missing fields list
        missing_list_frame = ttk.LabelFrame(editor_inner, text="Missing Fields", padding="5")
        missing_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.missing_fields_listbox = tk.Listbox(missing_list_frame, height=8)
        self.missing_fields_listbox.pack(fill=tk.BOTH, expand=True)
        self.missing_fields_listbox.bind('<<ListboxSelect>>', self.on_missing_field_select)
        
        # Right side - edit field
        edit_frame = ttk.LabelFrame(editor_inner, text="Edit Field", padding="5")
        edit_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        ttk.Label(edit_frame, text="Field Name:").pack(anchor=tk.W)
        self.field_name_var = tk.StringVar()
        ttk.Label(edit_frame, textvariable=self.field_name_var, 
                 font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(edit_frame, text="Value:").pack(anchor=tk.W)
        self.field_value_var = tk.StringVar()
        field_entry = ttk.Entry(edit_frame, textvariable=self.field_value_var, width=30)
        field_entry.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(edit_frame, text="💾 Save Field", 
                  command=self.save_field_value).pack(pady=5)
        
        # Recipe data storage
        self.recipe_edits = {}  # recipe_id -> {field: value}
        
        # Convert button
        convert_btn_frame = ttk.Frame(frame)
        convert_btn_frame.pack(pady=10)
        
        ttk.Button(convert_btn_frame, text="🔄 Convert Selected Recipes", 
                  command=self.convert_selected_recipes, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        
        # Progress
        self.convert_progress = ttk.Progressbar(frame, mode='indeterminate')
        self.convert_progress.pack(fill=tk.X, pady=5)
        
        # Results
        results_frame = ttk.LabelFrame(frame, text="Conversion Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.convert_results = scrolledtext.ScrolledText(results_frame, height=6, wrap=tk.WORD)
        self.convert_results.pack(fill=tk.BOTH, expand=True)
        
    def setup_scrape_tab(self, notebook):
        """Set up the web scraping tab."""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="🌐 Scrape from Web")
        
        ttk.Label(frame, text="Extract recipes from recipe websites", 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # URL input
        url_frame = ttk.Frame(frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="Recipe URL:").pack(side=tk.LEFT, padx=(0, 5))
        self.scrape_url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.scrape_url_var, width=50)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Multiple URLs
        multi_frame = ttk.LabelFrame(frame, text="Multiple URLs (one per line)", padding="10")
        multi_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.multi_urls_text = scrolledtext.ScrolledText(multi_frame, height=8, wrap=tk.WORD)
        self.multi_urls_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="🌐 Scrape Single URL", 
                  command=self.scrape_single).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🌐 Scrape Multiple URLs", 
                  command=self.scrape_multiple).pack(side=tk.LEFT, padx=5)
        
        # Progress
        self.scrape_progress = ttk.Progressbar(frame, mode='indeterminate')
        self.scrape_progress.pack(fill=tk.X, pady=5)
        
        # Results
        results_frame = ttk.LabelFrame(frame, text="Scraping Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.scrape_results = scrolledtext.ScrolledText(results_frame, height=8, wrap=tk.WORD)
        self.scrape_results.pack(fill=tk.BOTH, expand=True)
        
    def setup_crawl_tab(self, notebook):
        """Set up the website crawling tab."""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="🕷️ Crawl Website")
        
        ttk.Label(frame, text="Crawl entire websites to find and extract all recipes", 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # URL input
        url_frame = ttk.Frame(frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="Website URL:").pack(side=tk.LEFT, padx=(0, 5))
        self.crawl_url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.crawl_url_var, width=50)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Options
        options_frame = ttk.LabelFrame(frame, text="Crawling Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)
        
        opt_row1 = ttk.Frame(options_frame)
        opt_row1.pack(fill=tk.X, pady=2)
        ttk.Label(opt_row1, text="Max Pages:").pack(side=tk.LEFT, padx=(0, 5))
        self.max_pages_var = tk.StringVar(value="100")
        ttk.Entry(opt_row1, textvariable=self.max_pages_var, width=10).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(opt_row1, text="Delay (seconds):").pack(side=tk.LEFT, padx=(0, 5))
        self.delay_var = tk.StringVar(value="1.0")
        ttk.Entry(opt_row1, textvariable=self.delay_var, width=10).pack(side=tk.LEFT)
        
        opt_row2 = ttk.Frame(options_frame)
        opt_row2.pack(fill=tk.X, pady=2)
        ttk.Label(opt_row2, text="Export Format:").pack(side=tk.LEFT, padx=(0, 5))
        self.export_format_var = tk.StringVar(value="json")
        ttk.Radiobutton(opt_row2, text="JSON", variable=self.export_format_var, 
                      value="json").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(opt_row2, text="PDF", variable=self.export_format_var, 
                      value="pdf").pack(side=tk.LEFT)
        
        # Crawl button
        crawl_btn = ttk.Button(frame, text="🕷️ Start Crawling", 
                              command=self.crawl_website, style="Accent.TButton")
        crawl_btn.pack(pady=10)
        
        # Progress
        self.crawl_progress = ttk.Progressbar(frame, mode='indeterminate')
        self.crawl_progress.pack(fill=tk.X, pady=5)
        
        # Results
        results_frame = ttk.LabelFrame(frame, text="Crawling Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.crawl_results = scrolledtext.ScrolledText(results_frame, height=8, wrap=tk.WORD)
        self.crawl_results.pack(fill=tk.BOTH, expand=True)
        
    def setup_browse_tab(self, notebook):
        """Set up the browse recipes tab with card-based layout."""
        frame = ttk.Frame(notebook, padding="15")
        notebook.add(frame, text="📚 Browse Recipes")
        
        # Header with stats
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(header_frame, text="Recipe Library", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        self.recipe_count_label = ttk.Label(header_frame, text="", 
                                           font=("Arial", 10))
        self.recipe_count_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Search and filter bar
        filter_card = ttk.LabelFrame(frame, text="Search & Filter", padding="15")
        filter_card.pack(fill=tk.X, pady=(0, 15))
        
        filter_row = ttk.Frame(filter_card)
        filter_row.pack(fill=tk.X)
        
        ttk.Label(filter_row, text="🔍 Search:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_row, textvariable=self.search_var, width=25, 
                                font=("Arial", 10))
        search_entry.pack(side=tk.LEFT, padx=(0, 15))
        search_entry.bind('<KeyRelease>', lambda e: self.filter_recipes())
        
        ttk.Label(filter_row, text="Cuisine:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.cuisine_filter_var = tk.StringVar(value="All")
        cuisine_combo = ttk.Combobox(filter_row, textvariable=self.cuisine_filter_var, 
                                     width=15, state='readonly', font=("Arial", 9))
        cuisine_combo.pack(side=tk.LEFT, padx=(0, 15))
        cuisine_combo['values'] = ['All']
        cuisine_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_recipes())
        
        ttk.Label(filter_row, text="Difficulty:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 5))
        self.difficulty_filter_var = tk.StringVar(value="All")
        difficulty_combo = ttk.Combobox(filter_row, textvariable=self.difficulty_filter_var,
                                       width=12, state='readonly', font=("Arial", 9))
        difficulty_combo.pack(side=tk.LEFT, padx=(0, 15))
        difficulty_combo['values'] = ['All', 'Easy', 'Medium', 'Hard']
        difficulty_combo.bind('<<ComboboxSelected>>', lambda e: self.filter_recipes())
        
        ttk.Button(filter_row, text="🔄 Refresh", 
                  command=self.load_recipes).pack(side=tk.RIGHT, padx=5)
        
        # Recipe cards container with scrollbar
        cards_container = ttk.Frame(frame)
        cards_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(cards_container, bg='#f5f5f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(cards_container, orient=tk.VERTICAL, command=canvas.yview)
        self.recipe_cards_frame = ttk.Frame(canvas)
        
        scrollable_frame = canvas.create_window((0, 0), window=self.recipe_cards_frame, anchor="nw")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas_width = event.width
            canvas.itemconfig(scrollable_frame, width=canvas_width)
        
        self.recipe_cards_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        self.recipe_cards_canvas = canvas
        self.recipe_cards = {}  # Store card widgets
        
        # Load recipes
        self.load_recipes()
        
    def setup_tracking_tab(self, notebook):
        """Set up the source tracking tab."""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="📍 Source Tracking")
        
        ttk.Label(frame, text="Track where recipes came from", 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Search options
        search_frame = ttk.LabelFrame(frame, text="Search Sources", padding="10")
        search_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(search_frame, text="📊 View All Sources", 
                  command=self.view_all_sources).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="📅 Search by Date", 
                  command=self.search_by_date).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="🏢 Search by Location", 
                  command=self.search_by_location).pack(side=tk.LEFT, padx=5)
        
        # Results
        results_frame = ttk.LabelFrame(frame, text="Source Information", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.tracking_results = scrolledtext.ScrolledText(results_frame, height=15, wrap=tk.WORD)
        self.tracking_results.pack(fill=tk.BOTH, expand=True)
        
    def refresh_stats(self):
        """Refresh and display library statistics."""
        try:
            if not self.db_path.exists():
                stats_text = "No library database found.\n\nScan a directory to create your library."
            else:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Total recipes
                cursor.execute("SELECT COUNT(*) FROM recipes")
                total = cursor.fetchone()[0]
                
                # By cuisine
                cursor.execute("SELECT cuisine_type, COUNT(*) FROM recipes GROUP BY cuisine_type ORDER BY COUNT(*) DESC")
                cuisines = cursor.fetchall()
                
                # By category
                cursor.execute("SELECT category, COUNT(*) FROM recipes GROUP BY category")
                categories = cursor.fetchall()
                
                # By difficulty
                cursor.execute("SELECT difficulty, COUNT(*) FROM recipes GROUP BY difficulty")
                difficulties = cursor.fetchall()
                
                conn.close()
                
                stats_text = f"📊 Library Statistics\n{'='*30}\n\n"
                stats_text += f"Total Recipes: {total}\n\n"
                
                stats_text += "By Cuisine:\n"
                for cuisine, count in cuisines[:10]:
                    if cuisine:
                        stats_text += f"  • {cuisine}: {count}\n"
                
                stats_text += "\nBy Category:\n"
                for category, count in categories:
                    if category:
                        stats_text += f"  • {category}: {count}\n"
                
                stats_text += "\nBy Difficulty:\n"
                for difficulty, count in difficulties:
                    if difficulty:
                        stats_text += f"  • {difficulty}: {count}\n"
            
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            self.stats_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load statistics: {e}")
    
    def scan_directory(self):
        """Scan a directory for recipes."""
        directory = self.scan_dir_var.get()
        if not directory:
            messagebox.showwarning("Warning", "Please select a directory to scan")
            return
        
        def do_scan():
            try:
                self.scan_progress.start()
                self.scan_results.delete(1.0, tk.END)
                self.scan_results.insert(tk.END, f"Scanning {directory}...\n\n")
                
                if not self.scanner:
                    self.scanner = EnhancedRecipeScanner()
                
                result = self.scanner.scan_directory_thoroughly(
                    directory, 
                    recursive=self.recursive_var.get()
                )
                
                self.scan_results.insert(tk.END, f"Scan complete!\n\n")
                self.scan_results.insert(tk.END, f"Files found: {result['total_files']}\n")
                self.scan_results.insert(tk.END, f"Recipe files: {result['recipe_files_found']}\n")
                self.scan_results.insert(tk.END, f"Recipes imported: {result['recipes_imported']}\n\n")
                
                if result['imported_recipes']:
                    self.scan_results.insert(tk.END, "Imported recipes:\n")
                    for recipe in result['imported_recipes']:
                        self.scan_results.insert(tk.END, f"  • {recipe['title']}\n")
                
                self.scan_progress.stop()
                self.refresh_stats()
                self.load_recipes()
                messagebox.showinfo("Success", f"Imported {result['recipes_imported']} recipes!")
                
            except Exception as e:
                self.scan_progress.stop()
                messagebox.showerror("Error", f"Scan failed: {e}")
        
        threading.Thread(target=do_scan, daemon=True).start()
    
    def load_recipes_for_conversion(self):
        """Load all recipes for conversion selection."""
        try:
            # Clear existing
            for widget in self.recipe_list_frame.winfo_children():
                widget.destroy()
            self.recipe_checkboxes.clear()
            self.recipe_missing_info.clear()
            self.recipe_edits.clear()
            
            if not self.db_path.exists():
                messagebox.showwarning("Warning", "No library database found. Scan some recipes first.")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, cuisine_type, category, library_path
                FROM recipes
                ORDER BY title
            """)
            
            recipes = cursor.fetchall()
            conn.close()
            
            if not recipes:
                messagebox.showinfo("Info", "No recipes found in library.")
                return
            
            # Create checkbox for each recipe
            for recipe_id, title, cuisine, category, library_path in recipes:
                var = tk.BooleanVar()
                
                recipe_frame = ttk.Frame(self.recipe_list_frame)
                recipe_frame.pack(fill=tk.X, pady=2, padx=5)
                
                checkbox = ttk.Checkbutton(recipe_frame, variable=var, 
                                         text=f"{title or 'Untitled'} ({cuisine or 'Unknown'})",
                                         command=lambda rid=recipe_id: self.on_recipe_select(rid))
                checkbox.pack(side=tk.LEFT)
                
                # Info button
                info_btn = ttk.Button(recipe_frame, text="ℹ️", width=3,
                                    command=lambda rid=recipe_id: self.show_recipe_info(rid))
                info_btn.pack(side=tk.RIGHT, padx=5)
                
                self.recipe_checkboxes[recipe_id] = {
                    'var': var,
                    'checkbox': checkbox,
                    'frame': recipe_frame,
                    'title': title or 'Untitled',
                    'cuisine': cuisine,
                    'category': category,
                    'library_path': library_path
                }
            
            messagebox.showinfo("Success", f"Loaded {len(recipes)} recipes for conversion.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recipes: {e}")
    
    def select_all_recipes(self):
        """Select all recipes."""
        for recipe_id, data in self.recipe_checkboxes.items():
            data['var'].set(True)
    
    def deselect_all_recipes(self):
        """Deselect all recipes."""
        for recipe_id, data in self.recipe_checkboxes.items():
            data['var'].set(False)
    
    def analyze_missing_info(self):
        """Analyze missing information for selected recipes."""
        selected = [rid for rid, data in self.recipe_checkboxes.items() if data['var'].get()]
        
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one recipe to analyze.")
            return
        
        def do_analyze():
            try:
                self.convert_progress.start()
                self.convert_results.delete(1.0, tk.END)
                self.convert_results.insert(tk.END, f"Analyzing {len(selected)} recipes...\n\n")
                
                if not hasattr(self, 'detector') or not self.detector:
                    from missing_info_detector import MissingInfoDetector
                    self.detector = MissingInfoDetector()
                
                for i, recipe_id in enumerate(selected, 1):
                    data = self.recipe_checkboxes[recipe_id]
                    file_path = Path(data['library_path'])
                    
                    if file_path.exists():
                        analysis = self.detector.analyze_recipe(file_path=file_path)
                        self.recipe_missing_info[recipe_id] = analysis
                        
                        missing_count = len(analysis.get('missing_fields', []))
                        completeness = analysis.get('completeness_score', 0)
                        
                        self.convert_results.insert(tk.END, 
                            f"{i}. {data['title']}: {missing_count} missing fields, "
                            f"{completeness:.1f}% complete\n")
                
                self.convert_progress.stop()
                
                # Update UI to show missing info
                if selected:
                    self.show_recipe_missing_info(selected[0])
                
                messagebox.showinfo("Success", f"Analyzed {len(selected)} recipes!")
                
            except Exception as e:
                self.convert_progress.stop()
                messagebox.showerror("Error", f"Analysis failed: {e}")
        
        threading.Thread(target=do_analyze, daemon=True).start()
    
    def show_recipe_info(self, recipe_id):
        """Show information about a recipe."""
        if recipe_id not in self.recipe_checkboxes:
            return
        
        data = self.recipe_checkboxes[recipe_id]
        info_text = f"Title: {data['title']}\n"
        info_text += f"Cuisine: {data['cuisine'] or 'Unknown'}\n"
        info_text += f"Category: {data['category'] or 'Unknown'}\n"
        info_text += f"File: {data['library_path']}"
        
        messagebox.showinfo("Recipe Information", info_text)
    
    def on_recipe_select(self, recipe_id):
        """Handle recipe selection - show missing info if available."""
        if recipe_id in self.recipe_missing_info:
            self.show_recipe_missing_info(recipe_id)
    
    def show_recipe_missing_info(self, recipe_id):
        """Show missing information for a recipe."""
        if recipe_id not in self.recipe_checkboxes:
            return
        
        data = self.recipe_checkboxes[recipe_id]
        self.selected_recipe_var.set(f"Selected: {data['title']}")
        
        # Clear and populate missing fields list
        self.missing_fields_listbox.delete(0, tk.END)
        
        if recipe_id in self.recipe_missing_info:
            missing_info = self.recipe_missing_info[recipe_id]
            missing_fields = missing_info.get('missing_fields', [])
            
            if missing_fields:
                for field in missing_fields:
                    severity = field.get('severity', 'medium')
                    label = field.get('label', 'Unknown field')
                    section = field.get('section', '')
                    self.missing_fields_listbox.insert(tk.END, f"[{severity.upper()}] {label} ({section})")
            else:
                self.missing_fields_listbox.insert(tk.END, "No missing fields!")
        else:
            self.missing_fields_listbox.insert(tk.END, "Not analyzed yet. Click 'Analyze Missing Info'")
        
        # Store current recipe for editing
        self.current_editing_recipe = recipe_id
    
    def on_missing_field_select(self, event):
        """Handle selection of a missing field."""
        selection = self.missing_fields_listbox.curselection()
        if not selection or not hasattr(self, 'current_editing_recipe'):
            return
        
        recipe_id = self.current_editing_recipe
        if not recipe_id or recipe_id not in self.recipe_missing_info:
            return
        
        field_index = selection[0]
        missing_fields = self.recipe_missing_info[recipe_id].get('missing_fields', [])
        
        if field_index < len(missing_fields):
            field = missing_fields[field_index]
            self.field_name_var.set(field.get('label', 'Unknown'))
            self.field_value_var.set("")
            
            # Check if we have an edit for this field
            if recipe_id in self.recipe_edits:
                field_key = f"{field.get('section')}.{field.get('field', '')}"
                if field_key in self.recipe_edits[recipe_id]:
                    self.field_value_var.set(self.recipe_edits[recipe_id][field_key])
    
    def save_field_value(self):
        """Save edited field value."""
        if not hasattr(self, 'current_editing_recipe'):
            messagebox.showwarning("Warning", "No recipe selected for editing.")
            return
        
        recipe_id = self.current_editing_recipe
        if not recipe_id:
            return
        
        field_name = self.field_name_var.get()
        field_value = self.field_value_var.get()
        
        if not field_name:
            messagebox.showwarning("Warning", "No field selected.")
            return
        
        # Store the edit
        if recipe_id not in self.recipe_edits:
            self.recipe_edits[recipe_id] = {}
        
        # Extract field key from field name
        selection = self.missing_fields_listbox.curselection()
        if selection:
            field_index = selection[0]
            missing_fields = self.recipe_missing_info[recipe_id].get('missing_fields', [])
            if field_index < len(missing_fields):
                field = missing_fields[field_index]
                field_key = f"{field.get('section')}.{field.get('field', '')}"
                self.recipe_edits[recipe_id][field_key] = field_value
                
                messagebox.showinfo("Success", f"Saved value for {field_name}")
                self.field_value_var.set("")
    
    def convert_selected_recipes(self):
        """Convert selected recipes with confirmation."""
        selected = [rid for rid, data in self.recipe_checkboxes.items() if data['var'].get()]
        
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one recipe to convert.")
            return
        
        # Show confirmation with recipe list
        recipe_names = [self.recipe_checkboxes[rid]['title'] for rid in selected]
        confirm_text = f"Convert {len(selected)} recipe(s)?\n\n"
        confirm_text += "\n".join([f"• {name}" for name in recipe_names[:10]])
        if len(selected) > 10:
            confirm_text += f"\n... and {len(selected) - 10} more"
        
        if not messagebox.askyesno("Confirm Conversion", confirm_text):
            return
        
        def do_convert():
            try:
                self.convert_progress.start()
                self.convert_results.delete(1.0, tk.END)
                self.convert_results.insert(tk.END, f"Converting {len(selected)} recipes...\n\n")
                
                if not self.converter:
                    self.converter = IterumRecipeConverter()
                
                success_count = 0
                failed_count = 0
                
                for i, recipe_id in enumerate(selected, 1):
                    try:
                        data = self.recipe_checkboxes[recipe_id]
                        file_path = Path(data['library_path'])
                        
                        if file_path.exists():
                            # Get metadata from database
                            conn = sqlite3.connect(self.db_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
                            row = cursor.fetchone()
                            conn.close()
                            
                            # Create metadata dict
                            if row:
                                metadata = {
                                    'title': row[7] if len(row) > 7 else data['title'],
                                    'cuisine_type': row[9] if len(row) > 9 else data['cuisine'],
                                    'category': row[8] if len(row) > 8 else data['category']
                                }
                            else:
                                metadata = {
                                    'title': data['title'],
                                    'cuisine_type': data['cuisine'],
                                    'category': data['category']
                                }
                            
                            # Apply any edits
                            if recipe_id in self.recipe_edits:
                                edits = self.recipe_edits[recipe_id]
                                # Apply edits to metadata if applicable
                                for key, value in edits.items():
                                    if '.' in key:
                                        section, field = key.split('.', 1)
                                        if section == 'header':
                                            metadata[field] = value
                            
                            self.converter.convert_recipe(str(file_path), metadata)
                            success_count += 1
                            self.convert_results.insert(tk.END, f"{i}. ✓ {data['title']}\n")
                        else:
                            failed_count += 1
                            self.convert_results.insert(tk.END, f"{i}. ✗ {data['title']} (file not found)\n")
                            
                    except Exception as e:
                        failed_count += 1
                        data = self.recipe_checkboxes[recipe_id]
                        self.convert_results.insert(tk.END, f"{i}. ✗ {data['title']}: {str(e)}\n")
                
                self.convert_results.insert(tk.END, f"\nConversion complete!\n")
                self.convert_results.insert(tk.END, f"Success: {success_count}, Failed: {failed_count}\n")
                self.convert_results.insert(tk.END, f"Files saved to: {self.converted_path}\n")
                
                self.convert_progress.stop()
                messagebox.showinfo("Success", 
                    f"Converted {success_count} recipe(s)!\n{failed_count} failed.")
                
            except Exception as e:
                self.convert_progress.stop()
                messagebox.showerror("Error", f"Conversion failed: {e}")
        
        threading.Thread(target=do_convert, daemon=True).start()
    
    def scrape_single(self):
        """Scrape a single recipe URL."""
        url = self.scrape_url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a recipe URL")
            return
        
        def do_scrape():
            try:
                self.scrape_progress.start()
                self.scrape_results.delete(1.0, tk.END)
                self.scrape_results.insert(tk.END, f"Scraping {url}...\n\n")
                
                if not self.scraper:
                    self.scraper = WebRecipeScraper()
                
                recipe_entry = self.scraper.scrape_and_import(url)
                
                if recipe_entry:
                    self.scrape_results.insert(tk.END, f"Successfully scraped: {recipe_entry.title}\n")
                    self.scrape_results.insert(tk.END, f"ID: {recipe_entry.id}\n")
                    self.scrape_progress.stop()
                    self.refresh_stats()
                    self.load_recipes()
                    messagebox.showinfo("Success", f"Recipe '{recipe_entry.title}' imported!")
                else:
                    self.scrape_progress.stop()
                    messagebox.showerror("Error", "Failed to scrape recipe from URL")
                    
            except Exception as e:
                self.scrape_progress.stop()
                messagebox.showerror("Error", f"Scraping failed: {e}")
        
        threading.Thread(target=do_scrape, daemon=True).start()
    
    def scrape_multiple(self):
        """Scrape multiple recipe URLs."""
        urls_text = self.multi_urls_text.get(1.0, tk.END).strip()
        if not urls_text:
            messagebox.showwarning("Warning", "Please enter at least one URL")
            return
        
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        def do_scrape():
            try:
                self.scrape_progress.start()
                self.scrape_results.delete(1.0, tk.END)
                self.scrape_results.insert(tk.END, f"Scraping {len(urls)} recipes...\n\n")
                
                if not self.scraper:
                    self.scraper = WebRecipeScraper()
                
                results = self.scraper.scrape_multiple(urls)
                
                self.scrape_results.insert(tk.END, f"Successfully scraped: {len(results['success'])}\n")
                self.scrape_results.insert(tk.END, f"Failed: {len(results['failed'])}\n\n")
                
                if results['success']:
                    self.scrape_results.insert(tk.END, "Successfully scraped:\n")
                    for item in results['success']:
                        self.scrape_results.insert(tk.END, f"  • {item['title']}\n")
                
                self.scrape_progress.stop()
                self.refresh_stats()
                self.load_recipes()
                messagebox.showinfo("Success", f"Scraped {len(results['success'])} recipes!")
                
            except Exception as e:
                self.scrape_progress.stop()
                messagebox.showerror("Error", f"Scraping failed: {e}")
        
        threading.Thread(target=do_scrape, daemon=True).start()
    
    def crawl_website(self):
        """Crawl a website for recipes."""
        url = self.crawl_url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a website URL")
            return
        
        try:
            max_pages = int(self.max_pages_var.get())
            delay = float(self.delay_var.get())
            format_type = self.export_format_var.get()
        except ValueError:
            messagebox.showerror("Error", "Invalid options. Please check max pages and delay values.")
            return
        
        def do_crawl():
            try:
                self.crawl_progress.start()
                self.crawl_results.delete(1.0, tk.END)
                self.crawl_results.insert(tk.END, f"Crawling {url}...\nThis may take several minutes.\n\n")
                
                if not self.crawler:
                    self.crawler = WebsiteRecipeCrawler(
                        base_url=url,
                        max_pages=max_pages,
                        delay=delay
                    )
                else:
                    self.crawler.base_url = url
                    self.crawler.max_pages = max_pages
                    self.crawler.delay = delay
                
                results = self.crawler.crawl_and_export(format=format_type)
                
                if results['success']:
                    self.crawl_results.insert(tk.END, f"Crawl complete!\n\n")
                    self.crawl_results.insert(tk.END, f"Pages visited: {results['crawl_results']['total_pages_visited']}\n")
                    self.crawl_results.insert(tk.END, f"Recipes found: {results['crawl_results']['recipes_found']}\n")
                    self.crawl_results.insert(tk.END, f"Recipes scraped: {results['recipes_count']}\n")
                    self.crawl_results.insert(tk.END, f"Output file: {results['output_file']}\n")
                    
                    self.crawl_progress.stop()
                    self.refresh_stats()
                    self.load_recipes()
                    messagebox.showinfo("Success", f"Found and scraped {results['recipes_count']} recipes!")
                else:
                    self.crawl_progress.stop()
                    messagebox.showerror("Error", results.get('error', 'Crawl failed'))
                    
            except Exception as e:
                self.crawl_progress.stop()
                messagebox.showerror("Error", f"Crawling failed: {e}")
        
        threading.Thread(target=do_crawl, daemon=True).start()
    
    def load_recipes(self):
        """Load recipes from database and display as cards."""
        try:
            # Clear existing cards
            if hasattr(self, 'recipe_cards_frame'):
                for widget in self.recipe_cards_frame.winfo_children():
                    widget.destroy()
                if hasattr(self, 'recipe_cards'):
                    self.recipe_cards.clear()
            
            if not self.db_path.exists():
                if hasattr(self, 'recipe_cards_frame'):
                    no_data_label = ttk.Label(self.recipe_cards_frame, 
                                            text="No recipes found. Scan a directory to get started.",
                                            font=("Arial", 11))
                    no_data_label.pack(pady=50)
                if hasattr(self, 'recipe_count_label'):
                    self.recipe_count_label.config(text="")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get unique cuisines for filter
            cursor.execute("SELECT DISTINCT cuisine_type FROM recipes WHERE cuisine_type IS NOT NULL")
            cuisines = [row[0] for row in cursor.fetchall()]
            if hasattr(self, 'cuisine_filter_var'):
                # Update cuisine filter dropdown
                for widget in self.root.winfo_children():
                    if isinstance(widget, ttk.Notebook):
                        for tab_id in widget.tabs():
                            tab = widget.nametowidget(tab_id)
                            self._update_cuisine_filter(tab, cuisines)
            
            cursor.execute("""
                SELECT id, title, cuisine_type, category, difficulty, modified_date
                FROM recipes
                ORDER BY modified_date DESC
            """)
            
            recipes = cursor.fetchall()
            conn.close()
            
            # Update count
            if hasattr(self, 'recipe_count_label'):
                self.recipe_count_label.config(text=f"({len(recipes)} recipes)")
            
            # Create cards in grid layout
            if hasattr(self, 'recipe_cards_frame'):
                cards_per_row = 3
                row = 0
                col = 0
                
                for recipe_id, title, cuisine, category, difficulty, modified in recipes:
                    self.create_recipe_card(recipe_id, title, cuisine, category, difficulty, modified, row, col)
                    col += 1
                    if col >= cards_per_row:
                        col = 0
                        row += 1
                
                # Update scroll region
                self.recipe_cards_frame.update_idletasks()
                if hasattr(self, 'recipe_cards_canvas'):
                    self.recipe_cards_canvas.configure(scrollregion=self.recipe_cards_canvas.bbox("all"))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load recipes: {e}")
    
    def _update_cuisine_filter(self, parent, cuisines):
        """Recursively find and update cuisine filter combobox."""
        for widget in parent.winfo_children():
            if isinstance(widget, ttk.Combobox):
                try:
                    if widget.cget('textvariable') == str(self.cuisine_filter_var):
                        widget['values'] = ['All'] + sorted(cuisines)
                        return
                except:
                    pass
            if isinstance(widget, (ttk.Frame, tk.Frame, ttk.LabelFrame)):
                self._update_cuisine_filter(widget, cuisines)
    
    def create_recipe_card(self, recipe_id, title, cuisine, category, difficulty, modified, row, col):
        """Create a recipe card widget."""
        if not hasattr(self, 'recipe_cards_frame'):
            return
            
        # Card frame with styling
        card = tk.Frame(self.recipe_cards_frame, bg='white', relief=tk.RAISED, bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        card.config(highlightbackground='#e0e0e0', highlightthickness=1)
        
        # Configure grid weights
        self.recipe_cards_frame.columnconfigure(col, weight=1)
        
        # Card content
        content_frame = tk.Frame(card, bg='white', padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(content_frame, text=title or 'Untitled', 
                              font=("Arial", 12, "bold"), bg='white', 
                              fg='#2c3e50', anchor='w', wraplength=200)
        title_label.pack(fill=tk.X, pady=(0, 10))
        
        # Badges row
        badges_frame = tk.Frame(content_frame, bg='white')
        badges_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Cuisine badge
        if cuisine:
            cuisine_bg = '#e8f5e9'
            cuisine_fg = '#2e7d32'
            cuisine_badge = tk.Label(badges_frame, text=f"🌍 {cuisine}", 
                                    font=("Arial", 8), bg=cuisine_bg, fg=cuisine_fg,
                                    padx=8, pady=3, relief=tk.FLAT)
            cuisine_badge.pack(side=tk.LEFT, padx=(0, 5))
        
        # Difficulty badge
        if difficulty:
            diff_colors = {
                'easy': ('#e3f2fd', '#1976d2'),
                'medium': ('#fff3e0', '#f57c00'),
                'hard': ('#ffebee', '#c62828')
            }
            diff_bg, diff_fg = diff_colors.get(difficulty.lower(), ('#f5f5f5', '#757575'))
            difficulty_badge = tk.Label(badges_frame, text=f"📊 {difficulty.title()}", 
                                       font=("Arial", 8), bg=diff_bg, fg=diff_fg,
                                       padx=8, pady=3, relief=tk.FLAT)
            difficulty_badge.pack(side=tk.LEFT)
        
        # Category (if available)
        if category:
            category_label = tk.Label(content_frame, text=f"Category: {category}", 
                                     font=("Arial", 8), bg='white', fg='#757575',
                                     anchor='w')
            category_label.pack(fill=tk.X, pady=(0, 5))
        
        # Modified date
        modified_str = modified[:10] if modified else 'Unknown'
        date_label = tk.Label(content_frame, text=f"📅 {modified_str}", 
                            font=("Arial", 8), bg='white', fg='#9e9e9e',
                            anchor='w')
        date_label.pack(fill=tk.X, pady=(0, 10))
        
        # View button
        view_btn = tk.Button(content_frame, text="👁️ View Recipe", 
                            font=("Arial", 9), bg='#2196f3', fg='white',
                            relief=tk.FLAT, padx=15, pady=5,
                            cursor='hand2',
                            command=lambda rid=recipe_id: self.view_recipe_by_id(rid))
        view_btn.pack(fill=tk.X)
        
        # Hover effect
        def on_enter(e):
            card.config(highlightbackground='#2196f3', highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground='#e0e0e0', highlightthickness=1)
        
        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for widget in [content_frame, title_label, badges_frame]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
        
        if not hasattr(self, 'recipe_cards'):
            self.recipe_cards = {}
        self.recipe_cards[recipe_id] = {
            'card': card,
            'title': title or 'Untitled',
            'cuisine': cuisine,
            'category': category,
            'difficulty': difficulty
        }
    
    def view_recipe_by_id(self, recipe_id):
        """View recipe by ID (for card clicks)."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT file_path, library_path FROM recipes WHERE id = ?", (recipe_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                file_path = Path(result[0] or result[1])
                if file_path.exists():
                    import webbrowser
                    webbrowser.open(str(file_path))
                else:
                    messagebox.showwarning("Warning", f"Recipe file not found: {file_path}")
            else:
                messagebox.showwarning("Warning", "Recipe not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open recipe: {e}")
    
    def filter_recipes(self):
        """Filter recipes based on search and filters."""
        try:
            # Clear existing cards
            if hasattr(self, 'recipe_cards_frame'):
                for widget in self.recipe_cards_frame.winfo_children():
                    widget.destroy()
                if hasattr(self, 'recipe_cards'):
                    self.recipe_cards.clear()
            
            if not self.db_path.exists():
                return
            
            search_term = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
            cuisine_filter = self.cuisine_filter_var.get() if hasattr(self, 'cuisine_filter_var') else "All"
            difficulty_filter = self.difficulty_filter_var.get() if hasattr(self, 'difficulty_filter_var') else "All"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT id, title, cuisine_type, category, difficulty, modified_date FROM recipes WHERE 1=1"
            params = []
            
            if search_term:
                query += " AND (LOWER(title) LIKE ? OR LOWER(cuisine_type) LIKE ? OR LOWER(category) LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            if cuisine_filter != "All":
                query += " AND cuisine_type = ?"
                params.append(cuisine_filter)
            
            if difficulty_filter != "All":
                query += " AND LOWER(difficulty) = ?"
                params.append(difficulty_filter.lower())
            
            query += " ORDER BY modified_date DESC"
            
            cursor.execute(query, params)
            recipes = cursor.fetchall()
            conn.close()
            
            # Update count
            if hasattr(self, 'recipe_count_label'):
                self.recipe_count_label.config(text=f"({len(recipes)} recipes)")
            
            # Create filtered cards
            if hasattr(self, 'recipe_cards_frame'):
                cards_per_row = 3
                row = 0
                col = 0
                
                for recipe_id, title, cuisine, category, difficulty, modified in recipes:
                    self.create_recipe_card(recipe_id, title, cuisine, category, difficulty, modified, row, col)
                    col += 1
                    if col >= cards_per_row:
                        col = 0
                        row += 1
                
                # Update scroll region
                self.recipe_cards_frame.update_idletasks()
                if hasattr(self, 'recipe_cards_canvas'):
                    self.recipe_cards_canvas.configure(scrollregion=self.recipe_cards_canvas.bbox("all"))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter recipes: {e}")
    
    def view_recipe(self, event):
        """View a selected recipe."""
        selection = self.recipe_tree.selection()
        if not selection:
            return
        
        item = self.recipe_tree.item(selection[0])
        recipe_id = item['tags'][0] if item['tags'] else None
        
        if recipe_id:
            # Open recipe file or show details
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT library_path FROM recipes WHERE id = ?", (recipe_id,))
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0]:
                    file_path = Path(result[0])
                    if file_path.exists():
                        import os
                        os.startfile(str(file_path))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open recipe: {e}")
    
    def view_all_sources(self):
        """View all recipe sources."""
        try:
            if not self.db_path.exists():
                self.tracking_results.delete(1.0, tk.END)
                self.tracking_results.insert(tk.END, "No library database found.")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT title, file_path, created_date FROM recipes ORDER BY created_date DESC")
            
            results = cursor.fetchall()
            conn.close()
            
            self.tracking_results.delete(1.0, tk.END)
            self.tracking_results.insert(tk.END, f"Total Recipes: {len(results)}\n\n")
            
            for title, file_path, created in results:
                self.tracking_results.insert(tk.END, f"Title: {title or 'Untitled'}\n")
                self.tracking_results.insert(tk.END, f"Source: {file_path}\n")
                self.tracking_results.insert(tk.END, f"Created: {created or 'Unknown'}\n")
                self.tracking_results.insert(tk.END, "-" * 50 + "\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load sources: {e}")
    
    def search_by_date(self):
        """Search recipes by date."""
        # Simple implementation - could be enhanced
        messagebox.showinfo("Info", "Date search feature - use the browse tab to filter recipes")
    
    def search_by_location(self):
        """Search recipes by location."""
        # Simple implementation - could be enhanced
        messagebox.showinfo("Info", "Location search feature - use the browse tab to filter recipes")
    
    def setup_ingredient_tab(self, notebook):
        """Set up the ingredient database tab."""
        frame = ttk.Frame(notebook, padding="10")
        notebook.add(frame, text="🥘 Ingredient Database")
        
        ttk.Label(frame, text="Pre-built ingredient database with properties, costs, and metadata", 
                 font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Top section - Search and filters
        search_frame = ttk.LabelFrame(frame, text="Search Ingredients", padding="10")
        search_frame.pack(fill=tk.X, pady=5)
        
        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X)
        
        ttk.Label(search_row, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.ingredient_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_row, textvariable=self.ingredient_search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.search_ingredients())
        
        ttk.Label(search_row, text="Category:").pack(side=tk.LEFT, padx=(0, 5))
        self.ingredient_category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(search_row, textvariable=self.ingredient_category_var, 
                                     width=20, state='readonly')
        category_combo.pack(side=tk.LEFT, padx=(0, 10))
        category_combo['values'] = ['All'] + self.ingredient_db.get_categories()
        category_combo.bind('<<ComboboxSelected>>', lambda e: self.search_ingredients())
        
        ttk.Button(search_row, text="🔍 Search", 
                  command=self.search_ingredients).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_row, text="➕ Add New", 
                  command=self.add_new_ingredient).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_row, text="📊 Stats", 
                  command=self.show_ingredient_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_row, text="💰 Import Vendor Prices", 
                  command=self.import_vendor_prices).pack(side=tk.LEFT, padx=5)
        
        # Main content - Split view
        content_frame = ttk.Frame(frame)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Ingredient list
        list_frame = ttk.LabelFrame(content_frame, text="Ingredients", padding="10")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Treeview for ingredients
        columns = ('Name', 'Category', 'Unit', 'Cost', 'Yield')
        self.ingredient_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.ingredient_tree.heading(col, text=col)
            self.ingredient_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.ingredient_tree.yview)
        self.ingredient_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ingredient_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ingredient_tree.bind('<<TreeviewSelect>>', self.on_ingredient_select)
        self.ingredient_tree.bind('<Double-1>', self.edit_ingredient)
        
        # Right side - Ingredient details
        details_frame = ttk.LabelFrame(content_frame, text="Ingredient Details", padding="10")
        details_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Details display
        self.ingredient_details = scrolledtext.ScrolledText(details_frame, height=20, wrap=tk.WORD, 
                                                           state=tk.DISABLED)
        self.ingredient_details.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = ttk.Frame(details_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="✏️ Edit", 
                  command=self.edit_ingredient).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💰 Manage Vendors", 
                  command=self.manage_vendor_prices).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Delete", 
                  command=self.delete_ingredient).pack(side=tk.LEFT, padx=5)
        
        # Load initial ingredients
        self.search_ingredients()
    
    def search_ingredients(self):
        """Search and display ingredients."""
        try:
            # Clear existing
            for item in self.ingredient_tree.get_children():
                self.ingredient_tree.delete(item)
            
            search_term = self.ingredient_search_var.get()
            category = self.ingredient_category_var.get()
            if category == "All":
                category = ""
            
            ingredients = self.ingredient_db.search_ingredients(search_term, category)
            
            for ing in ingredients:
                cost_str = f"${ing['typical_ap_cost']:.2f}/{ing['cost_unit']}" if ing['typical_ap_cost'] else "N/A"
                self.ingredient_tree.insert('', tk.END, values=(
                    ing['name'],
                    ing['category'],
                    ing['default_unit'],
                    cost_str,
                    f"{ing['typical_yield_pct']:.0f}%"
                ), tags=(ing['id'],))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search ingredients: {e}")
    
    def on_ingredient_select(self, event):
        """Handle ingredient selection - show details."""
        selection = self.ingredient_tree.selection()
        if not selection:
            return
        
        item = self.ingredient_tree.item(selection[0])
        ingredient_id = int(item['tags'][0])
        
        try:
            ingredient = self.ingredient_db.get_ingredient(ingredient_id)
            if ingredient:
                self.display_ingredient_details(ingredient)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load ingredient: {e}")
    
    def display_ingredient_details(self, ingredient: Dict[str, Any]):
        """Display ingredient details in the details panel."""
        self.ingredient_details.config(state=tk.NORMAL)
        self.ingredient_details.delete(1.0, tk.END)
        
        details = f"📋 {ingredient['name']}\n"
        details += "=" * 50 + "\n\n"
        
        details += f"Category: {ingredient['category']}"
        if ingredient.get('subcategory'):
            details += f" > {ingredient['subcategory']}"
        details += "\n\n"
        
        details += f"Default Unit: {ingredient['default_unit']}\n"
        
        if ingredient.get('common_units'):
            details += f"Common Units: {', '.join(ingredient['common_units'])}\n"
        
        details += f"Typical Yield: {ingredient['typical_yield_pct']:.1f}%\n\n"
        
        if ingredient.get('typical_ap_cost'):
            details += f"Typical AP Cost: ${ingredient['typical_ap_cost']:.2f}/{ingredient.get('cost_unit', 'unit')}\n"
            # Calculate EP cost
            if ingredient['typical_yield_pct'] < 100:
                ep_cost = ingredient['typical_ap_cost'] / (ingredient['typical_yield_pct'] / 100)
                details += f"EP Cost: ${ep_cost:.2f}/{ingredient.get('cost_unit', 'unit')}\n"
        details += "\n"
        
        if ingredient.get('storage_notes'):
            details += f"Storage: {ingredient['storage_notes']}\n"
        
        if ingredient.get('shelf_life_days'):
            details += f"Shelf Life: {ingredient['shelf_life_days']} days\n"
        details += "\n"
        
        if ingredient.get('allergens'):
            details += f"Allergens: {', '.join(ingredient['allergens'])}\n"
        
        if ingredient.get('dietary_tags'):
            details += f"Dietary: {', '.join(ingredient['dietary_tags'])}\n"
        details += "\n"
        
        if ingredient.get('substitutes'):
            details += f"Substitutes: {', '.join(ingredient['substitutes'])}\n"
        details += "\n"
        
        if ingredient.get('notes'):
            details += f"Notes: {ingredient['notes']}\n"
        details += "\n"
        
        if ingredient.get('source_url'):
            details += f"Source URL: {ingredient['source_url']}\n"
        details += "\n"
        
        # Vendor prices
        vendor_prices = self.ingredient_db.get_vendor_prices(ingredient['id'])
        if vendor_prices:
            details += "💰 Vendor Prices:\n"
            details += "-" * 50 + "\n"
            for vp in vendor_prices:
                preferred = "⭐ " if vp['is_preferred'] else "  "
                details += f"{preferred}{vp['vendor_name']}: ${vp['ap_cost']:.2f}/{vp['cost_unit']}\n"
                if vp.get('vendor_url'):
                    details += f"   URL: {vp['vendor_url']}\n"
                if vp.get('last_updated'):
                    details += f"   Updated: {vp['last_updated'][:10]}\n"
                details += "\n"
        else:
            details += "💰 No vendor prices set\n"
        
        self.ingredient_details.config(state=tk.DISABLED)
    
    def add_new_ingredient(self):
        """Open dialog to add new ingredient."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Ingredient")
        dialog.geometry("600x700")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form fields
        fields_frame = ttk.Frame(dialog, padding="20")
        fields_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        ttk.Label(fields_frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=name_var, width=40).grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Category
        ttk.Label(fields_frame, text="Category *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        category_combo = ttk.Combobox(fields_frame, textvariable=category_var, width=37, 
                                     values=['Produce', 'Proteins', 'Dairy', 'Pantry', 'Herbs', 'Other'])
        category_combo.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Subcategory
        ttk.Label(fields_frame, text="Subcategory:").grid(row=2, column=0, sticky=tk.W, pady=5)
        subcategory_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=subcategory_var, width=40).grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Default Unit
        ttk.Label(fields_frame, text="Default Unit *:").grid(row=3, column=0, sticky=tk.W, pady=5)
        unit_var = tk.StringVar(value="lb")
        ttk.Entry(fields_frame, textvariable=unit_var, width=40).grid(row=3, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Typical Yield %
        ttk.Label(fields_frame, text="Typical Yield %:").grid(row=4, column=0, sticky=tk.W, pady=5)
        yield_var = tk.StringVar(value="100.0")
        ttk.Entry(fields_frame, textvariable=yield_var, width=40).grid(row=4, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Typical AP Cost
        ttk.Label(fields_frame, text="Typical AP Cost:").grid(row=5, column=0, sticky=tk.W, pady=5)
        cost_frame = ttk.Frame(fields_frame)
        cost_frame.grid(row=5, column=1, pady=5, sticky=(tk.W, tk.E))
        cost_var = tk.StringVar()
        ttk.Entry(cost_frame, textvariable=cost_var, width=20).pack(side=tk.LEFT, padx=(0, 5))
        cost_unit_var = tk.StringVar(value="lb")
        ttk.Entry(cost_frame, textvariable=cost_unit_var, width=15).pack(side=tk.LEFT)
        
        # Storage Notes
        ttk.Label(fields_frame, text="Storage Notes:").grid(row=6, column=0, sticky=tk.W, pady=5)
        storage_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=storage_var, width=40).grid(row=6, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Shelf Life
        ttk.Label(fields_frame, text="Shelf Life (days):").grid(row=7, column=0, sticky=tk.W, pady=5)
        shelf_life_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=shelf_life_var, width=40).grid(row=7, column=1, pady=5, sticky=(tk.W, tk.E))
        
        # Source URL
        ttk.Label(fields_frame, text="Source URL:").grid(row=8, column=0, sticky=tk.W, pady=5)
        url_frame = ttk.Frame(fields_frame)
        url_frame.grid(row=8, column=1, pady=5, sticky=(tk.W, tk.E))
        url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=url_var, width=35)
        url_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(url_frame, text="🌐 Scrape", 
                  command=lambda: self.scrape_ingredient_url(url_var, name_var, category_var, 
                                                             unit_var, cost_var, cost_unit_var,
                                                             storage_var, notes_text, dialog)).pack(side=tk.LEFT)
        
        # Notes
        ttk.Label(fields_frame, text="Notes:").grid(row=9, column=0, sticky=tk.W, pady=5)
        notes_text = scrolledtext.ScrolledText(fields_frame, height=5, width=40)
        notes_text.grid(row=9, column=1, pady=5, sticky=(tk.W, tk.E))
        
        fields_frame.columnconfigure(1, weight=1)
        
        def save_ingredient():
            if not name_var.get().strip():
                messagebox.showwarning("Warning", "Name is required")
                return
            
            try:
                ingredient_data = {
                    'name': name_var.get().strip(),
                    'category': category_var.get() or 'Other',
                    'subcategory': subcategory_var.get() or None,
                    'default_unit': unit_var.get() or 'lb',
                    'typical_yield_pct': float(yield_var.get()) if yield_var.get() else 100.0,
                    'typical_ap_cost': float(cost_var.get()) if cost_var.get() else None,
                    'cost_unit': cost_unit_var.get() or None,
                    'storage_notes': storage_var.get() or None,
                    'shelf_life_days': int(shelf_life_var.get()) if shelf_life_var.get() else None,
                    'notes': notes_text.get(1.0, tk.END).strip() or None,
                    'source_url': url_var.get().strip() or None
                }
                
                self.ingredient_db.add_ingredient(ingredient_data)
                messagebox.showinfo("Success", f"Added ingredient: {ingredient_data['name']}")
                dialog.destroy()
                self.search_ingredients()
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid number: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add ingredient: {e}")
        
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Button(btn_frame, text="💾 Save", command=save_ingredient, 
                  style="Accent.TButton").pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def edit_ingredient(self, event=None):
        """Edit selected ingredient."""
        selection = self.ingredient_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ingredient to edit")
            return
        
        item = self.ingredient_tree.item(selection[0])
        ingredient_id = int(item['tags'][0])
        
        try:
            ingredient = self.ingredient_db.get_ingredient(ingredient_id)
            if not ingredient:
                messagebox.showerror("Error", "Ingredient not found")
                return
            
            # Open edit dialog (similar to add, but pre-filled)
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Edit Ingredient: {ingredient['name']}")
            dialog.geometry("600x700")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Form fields (same as add, but pre-filled)
            fields_frame = ttk.Frame(dialog, padding="20")
            fields_frame.pack(fill=tk.BOTH, expand=True)
            
            # Name
            ttk.Label(fields_frame, text="Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
            name_var = tk.StringVar(value=ingredient['name'])
            ttk.Entry(fields_frame, textvariable=name_var, width=40).grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Category
            ttk.Label(fields_frame, text="Category *:").grid(row=1, column=0, sticky=tk.W, pady=5)
            category_var = tk.StringVar(value=ingredient['category'])
            category_combo = ttk.Combobox(fields_frame, textvariable=category_var, width=37,
                                         values=['Produce', 'Proteins', 'Dairy', 'Pantry', 'Herbs', 'Other'])
            category_combo.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Subcategory
            ttk.Label(fields_frame, text="Subcategory:").grid(row=2, column=0, sticky=tk.W, pady=5)
            subcategory_var = tk.StringVar(value=ingredient.get('subcategory') or '')
            ttk.Entry(fields_frame, textvariable=subcategory_var, width=40).grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Default Unit
            ttk.Label(fields_frame, text="Default Unit *:").grid(row=3, column=0, sticky=tk.W, pady=5)
            unit_var = tk.StringVar(value=ingredient['default_unit'])
            ttk.Entry(fields_frame, textvariable=unit_var, width=40).grid(row=3, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Typical Yield %
            ttk.Label(fields_frame, text="Typical Yield %:").grid(row=4, column=0, sticky=tk.W, pady=5)
            yield_var = tk.StringVar(value=str(ingredient['typical_yield_pct']))
            ttk.Entry(fields_frame, textvariable=yield_var, width=40).grid(row=4, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Typical AP Cost
            ttk.Label(fields_frame, text="Typical AP Cost:").grid(row=5, column=0, sticky=tk.W, pady=5)
            cost_frame = ttk.Frame(fields_frame)
            cost_frame.grid(row=5, column=1, pady=5, sticky=(tk.W, tk.E))
            cost_var = tk.StringVar(value=str(ingredient['typical_ap_cost']) if ingredient.get('typical_ap_cost') else '')
            ttk.Entry(cost_frame, textvariable=cost_var, width=20).pack(side=tk.LEFT, padx=(0, 5))
            cost_unit_var = tk.StringVar(value=ingredient.get('cost_unit') or 'lb')
            ttk.Entry(cost_frame, textvariable=cost_unit_var, width=15).pack(side=tk.LEFT)
            
            # Storage Notes
            ttk.Label(fields_frame, text="Storage Notes:").grid(row=6, column=0, sticky=tk.W, pady=5)
            storage_var = tk.StringVar(value=ingredient.get('storage_notes') or '')
            ttk.Entry(fields_frame, textvariable=storage_var, width=40).grid(row=6, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Shelf Life
            ttk.Label(fields_frame, text="Shelf Life (days):").grid(row=7, column=0, sticky=tk.W, pady=5)
            shelf_life_var = tk.StringVar(value=str(ingredient['shelf_life_days']) if ingredient.get('shelf_life_days') else '')
            ttk.Entry(fields_frame, textvariable=shelf_life_var, width=40).grid(row=7, column=1, pady=5, sticky=(tk.W, tk.E))
            
            # Source URL
            ttk.Label(fields_frame, text="Source URL:").grid(row=8, column=0, sticky=tk.W, pady=5)
            url_frame = ttk.Frame(fields_frame)
            url_frame.grid(row=8, column=1, pady=5, sticky=(tk.W, tk.E))
            url_var = tk.StringVar(value=ingredient.get('source_url') or '')
            url_entry = ttk.Entry(url_frame, textvariable=url_var, width=35)
            url_entry.pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(url_frame, text="🌐 Scrape", 
                      command=lambda: self.scrape_ingredient_url(url_var, name_var, category_var,
                                                                 unit_var, cost_var, cost_unit_var,
                                                                 storage_var, notes_text, dialog)).pack(side=tk.LEFT)
            
            # Notes
            ttk.Label(fields_frame, text="Notes:").grid(row=9, column=0, sticky=tk.W, pady=5)
            notes_text = scrolledtext.ScrolledText(fields_frame, height=5, width=40)
            notes_text.insert(1.0, ingredient.get('notes') or '')
            notes_text.grid(row=9, column=1, pady=5, sticky=(tk.W, tk.E))
            
            fields_frame.columnconfigure(1, weight=1)
            
            def save_changes():
                try:
                    ingredient_data = {
                        'name': name_var.get().strip(),
                        'category': category_var.get() or 'Other',
                        'subcategory': subcategory_var.get() or None,
                        'default_unit': unit_var.get() or 'lb',
                        'typical_yield_pct': float(yield_var.get()) if yield_var.get() else 100.0,
                        'typical_ap_cost': float(cost_var.get()) if cost_var.get() else None,
                        'cost_unit': cost_unit_var.get() or None,
                        'storage_notes': storage_var.get() or None,
                        'shelf_life_days': int(shelf_life_var.get()) if shelf_life_var.get() else None,
                        'notes': notes_text.get(1.0, tk.END).strip() or None,
                        'source_url': url_var.get().strip() or None
                    }
                    
                    self.ingredient_db.update_ingredient(ingredient_id, ingredient_data)
                    messagebox.showinfo("Success", f"Updated ingredient: {ingredient_data['name']}")
                    dialog.destroy()
                    self.search_ingredients()
                    self.on_ingredient_select(None)  # Refresh details
                    
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid number: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update ingredient: {e}")
            
            # Buttons
            btn_frame = ttk.Frame(dialog)
            btn_frame.pack(fill=tk.X, padx=20, pady=10)
            
            ttk.Button(btn_frame, text="💾 Save Changes", command=save_changes, 
                      style="Accent.TButton").pack(side=tk.RIGHT, padx=5)
            ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit ingredient: {e}")
    
    def delete_ingredient(self):
        """Delete selected ingredient."""
        selection = self.ingredient_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ingredient to delete")
            return
        
        item = self.ingredient_tree.item(selection[0])
        ingredient_id = int(item['tags'][0])
        ingredient_name = item['values'][0]
        
        if not messagebox.askyesno("Confirm Delete", f"Delete ingredient '{ingredient_name}'?"):
            return
        
        try:
            self.ingredient_db.delete_ingredient(ingredient_id)
            messagebox.showinfo("Success", f"Deleted ingredient: {ingredient_name}")
            self.search_ingredients()
            self.ingredient_details.config(state=tk.NORMAL)
            self.ingredient_details.delete(1.0, tk.END)
            self.ingredient_details.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete ingredient: {e}")
    
    def scrape_ingredient_url(self, url_var, name_var, category_var, unit_var, 
                              cost_var, cost_unit_var, storage_var, notes_text, dialog):
        """Scrape ingredient information from URL and populate form fields."""
        url = url_var.get().strip()
        
        if not url:
            messagebox.showwarning("Warning", "Please enter a URL first")
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            url_var.set(url)
        
        # Show progress
        progress_dialog = tk.Toplevel(dialog)
        progress_dialog.title("Scraping...")
        progress_dialog.geometry("400x100")
        progress_dialog.transient(dialog)
        progress_dialog.grab_set()
        
        progress_label = ttk.Label(progress_dialog, text="Scraping ingredient information...")
        progress_label.pack(pady=20)
        
        def do_scrape():
            try:
                scraper = IngredientWebScraper()
                result = scraper.scrape_ingredient_info(url)
                
                progress_dialog.destroy()
                
                if result.get('success'):
                    # Populate form fields
                    if 'name' in result and not name_var.get():
                        name_var.set(result['name'])
                    
                    if 'default_unit' in result:
                        unit_var.set(result['default_unit'])
                    
                    if 'typical_ap_cost' in result:
                        cost_var.set(str(result['typical_ap_cost']))
                    
                    if 'cost_unit' in result:
                        cost_unit_var.set(result['cost_unit'])
                    
                    if 'storage_notes' in result and not storage_var.get():
                        storage_var.set(result['storage_notes'])
                    
                    if 'notes' in result:
                        current_notes = notes_text.get(1.0, tk.END).strip()
                        if current_notes:
                            notes_text.delete(1.0, tk.END)
                            notes_text.insert(1.0, f"{current_notes}\n\n{result['notes']}")
                        else:
                            notes_text.delete(1.0, tk.END)
                            notes_text.insert(1.0, result['notes'])
                    
                    # Update URL if it was modified
                    url_var.set(result.get('source_url', url))
                    
                    # Show success message with details
                    details = f"✅ Scraped successfully!\n\n"
                    details += f"Name: {result.get('name', 'N/A')}\n"
                    details += f"Price: {result.get('typical_ap_cost', 'N/A')} {result.get('cost_unit', '')}\n"
                    details += f"Unit: {result.get('default_unit', 'N/A')}\n"
                    if 'storage_notes' in result:
                        details += f"Storage: {result['storage_notes'][:50]}...\n"
                    
                    messagebox.showinfo("Scraping Complete", details)
                else:
                    messagebox.showerror("Scraping Failed", 
                                        f"Could not scrape ingredient information:\n{result.get('error', 'Unknown error')}")
            
            except Exception as e:
                progress_dialog.destroy()
                messagebox.showerror("Error", f"Scraping failed: {e}")
        
        # Run in thread
        threading.Thread(target=do_scrape, daemon=True).start()
    
    def manage_vendor_prices(self):
        """Manage vendor prices for selected ingredient."""
        selection = self.ingredient_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an ingredient first")
            return
        
        item = self.ingredient_tree.item(selection[0])
        ingredient_id = int(item['tags'][0])
        
        try:
            ingredient = self.ingredient_db.get_ingredient(ingredient_id)
            if not ingredient:
                messagebox.showerror("Error", "Ingredient not found")
                return
            
            # Open vendor management dialog
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Manage Vendors: {ingredient['name']}")
            dialog.geometry("700x500")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Header
            header_frame = ttk.Frame(dialog, padding="10")
            header_frame.pack(fill=tk.X)
            ttk.Label(header_frame, text=f"Vendor Prices for: {ingredient['name']}", 
                     font=("Arial", 12, "bold")).pack()
            
            # Vendor list
            list_frame = ttk.LabelFrame(dialog, text="Vendors", padding="10")
            list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Treeview for vendors
            columns = ('Vendor', 'Price', 'Unit', 'Updated', 'Preferred')
            vendor_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
            
            for col in columns:
                vendor_tree.heading(col, text=col)
                vendor_tree.column(col, width=120)
            
            scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=vendor_tree.yview)
            vendor_tree.configure(yscrollcommand=scrollbar.set)
            
            vendor_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            def load_vendors():
                """Load vendor prices into treeview."""
                for item in vendor_tree.get_children():
                    vendor_tree.delete(item)
                
                vendor_prices = self.ingredient_db.get_vendor_prices(ingredient_id)
                for vp in vendor_prices:
                    preferred = "⭐ Yes" if vp['is_preferred'] else "No"
                    updated = vp['last_updated'][:10] if vp['last_updated'] else 'N/A'
                    vendor_tree.insert('', tk.END, values=(
                        vp['vendor_name'],
                        f"${vp['ap_cost']:.2f}",
                        vp['cost_unit'],
                        updated,
                        preferred
                    ), tags=(vp['id'],))
            
            load_vendors()
            
            # Buttons frame
            btn_frame = ttk.Frame(dialog, padding="10")
            btn_frame.pack(fill=tk.X)
            
            # Paste from clipboard button
            paste_frame = ttk.Frame(dialog, padding="10")
            paste_frame.pack(fill=tk.X)
            ttk.Label(paste_frame, text="Quick Add: Paste Excel data (tab-separated)").pack(side=tk.LEFT, padx=5)
            ttk.Button(paste_frame, text="📋 Paste & Parse", 
                      command=lambda: self.paste_vendor_prices(dialog, ingredient_id, load_vendors)).pack(side=tk.LEFT, padx=5)
            
            def add_vendor():
                """Add new vendor price."""
                add_dialog = tk.Toplevel(dialog)
                add_dialog.title("Add Vendor Price")
                add_dialog.geometry("500x350")
                add_dialog.transient(dialog)
                add_dialog.grab_set()
                
                fields_frame = ttk.Frame(add_dialog, padding="20")
                fields_frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(fields_frame, text="Vendor Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
                vendor_name_var = tk.StringVar()
                ttk.Entry(fields_frame, textvariable=vendor_name_var, width=40).grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))
                
                ttk.Label(fields_frame, text="Price *:").grid(row=1, column=0, sticky=tk.W, pady=5)
                price_frame = ttk.Frame(fields_frame)
                price_frame.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))
                price_var = tk.StringVar()
                ttk.Entry(price_frame, textvariable=price_var, width=20).pack(side=tk.LEFT, padx=(0, 5))
                unit_var = tk.StringVar(value="lb")
                ttk.Entry(price_frame, textvariable=unit_var, width=15).pack(side=tk.LEFT)
                
                ttk.Label(fields_frame, text="Vendor URL:").grid(row=2, column=0, sticky=tk.W, pady=5)
                url_var = tk.StringVar()
                ttk.Entry(fields_frame, textvariable=url_var, width=40).grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
                
                ttk.Label(fields_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
                notes_text = scrolledtext.ScrolledText(fields_frame, height=5, width=40)
                notes_text.grid(row=3, column=1, pady=5, sticky=(tk.W, tk.E))
                
                preferred_var = tk.BooleanVar()
                ttk.Checkbutton(fields_frame, text="Set as preferred vendor", 
                               variable=preferred_var).grid(row=4, column=1, sticky=tk.W, pady=5)
                
                fields_frame.columnconfigure(1, weight=1)
                
                def save_vendor():
                    if not vendor_name_var.get().strip() or not price_var.get():
                        messagebox.showwarning("Warning", "Vendor name and price are required")
                        return
                    
                    try:
                        price = float(price_var.get())
                        unit = unit_var.get() or 'lb'
                        
                        vendor_price_id = self.ingredient_db.add_vendor_price(
                            ingredient_id,
                            vendor_name_var.get().strip(),
                            price,
                            unit,
                            url_var.get().strip() or None,
                            notes_text.get(1.0, tk.END).strip() or None
                        )
                        
                        if preferred_var.get():
                            self.ingredient_db.set_preferred_vendor(ingredient_id, vendor_price_id)
                        
                        messagebox.showinfo("Success", "Vendor price added")
                        add_dialog.destroy()
                        load_vendors()
                        self.on_ingredient_select(None)  # Refresh details
                        
                    except ValueError:
                        messagebox.showerror("Error", "Invalid price")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to add vendor: {e}")
                
                btn_frame2 = ttk.Frame(add_dialog)
                btn_frame2.pack(fill=tk.X, padx=20, pady=10)
                ttk.Button(btn_frame2, text="💾 Save", command=save_vendor).pack(side=tk.RIGHT, padx=5)
                ttk.Button(btn_frame2, text="Cancel", command=add_dialog.destroy).pack(side=tk.RIGHT, padx=5)
            
            def edit_vendor():
                """Edit selected vendor price."""
                selection = vendor_tree.selection()
                if not selection:
                    messagebox.showwarning("Warning", "Please select a vendor")
                    return
                
                item = vendor_tree.item(selection[0])
                vendor_price_id = int(item['tags'][0])
                vendor_prices = self.ingredient_db.get_vendor_prices(ingredient_id)
                vp = next((v for v in vendor_prices if v['id'] == vendor_price_id), None)
                
                if not vp:
                    return
                
                # Similar dialog to add, but pre-filled
                edit_dialog = tk.Toplevel(dialog)
                edit_dialog.title("Edit Vendor Price")
                edit_dialog.geometry("500x350")
                edit_dialog.transient(dialog)
                edit_dialog.grab_set()
                
                fields_frame = ttk.Frame(edit_dialog, padding="20")
                fields_frame.pack(fill=tk.BOTH, expand=True)
                
                ttk.Label(fields_frame, text="Vendor Name *:").grid(row=0, column=0, sticky=tk.W, pady=5)
                vendor_name_var = tk.StringVar(value=vp['vendor_name'])
                ttk.Entry(fields_frame, textvariable=vendor_name_var, width=40, state='readonly').grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))
                
                ttk.Label(fields_frame, text="Price *:").grid(row=1, column=0, sticky=tk.W, pady=5)
                price_frame = ttk.Frame(fields_frame)
                price_frame.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))
                price_var = tk.StringVar(value=str(vp['ap_cost']))
                ttk.Entry(price_frame, textvariable=price_var, width=20).pack(side=tk.LEFT, padx=(0, 5))
                unit_var = tk.StringVar(value=vp['cost_unit'])
                ttk.Entry(price_frame, textvariable=unit_var, width=15).pack(side=tk.LEFT)
                
                ttk.Label(fields_frame, text="Vendor URL:").grid(row=2, column=0, sticky=tk.W, pady=5)
                url_var = tk.StringVar(value=vp.get('vendor_url') or '')
                ttk.Entry(fields_frame, textvariable=url_var, width=40).grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))
                
                ttk.Label(fields_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
                notes_text = scrolledtext.ScrolledText(fields_frame, height=5, width=40)
                notes_text.insert(1.0, vp.get('notes') or '')
                notes_text.grid(row=3, column=1, pady=5, sticky=(tk.W, tk.E))
                
                preferred_var = tk.BooleanVar(value=vp['is_preferred'])
                ttk.Checkbutton(fields_frame, text="Set as preferred vendor", 
                               variable=preferred_var).grid(row=4, column=1, sticky=tk.W, pady=5)
                
                fields_frame.columnconfigure(1, weight=1)
                
                def save_changes():
                    try:
                        price = float(price_var.get())
                        unit = unit_var.get() or 'lb'
                        
                        self.ingredient_db.update_vendor_price(
                            vendor_price_id,
                            ap_cost=price,
                            cost_unit=unit,
                            vendor_url=url_var.get().strip() or None,
                            notes=notes_text.get(1.0, tk.END).strip() or None,
                            is_preferred=preferred_var.get()
                        )
                        
                        if preferred_var.get():
                            self.ingredient_db.set_preferred_vendor(ingredient_id, vendor_price_id)
                        
                        messagebox.showinfo("Success", "Vendor price updated")
                        edit_dialog.destroy()
                        load_vendors()
                        self.on_ingredient_select(None)
                        
                    except ValueError:
                        messagebox.showerror("Error", "Invalid price")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to update vendor: {e}")
                
                btn_frame2 = ttk.Frame(edit_dialog)
                btn_frame2.pack(fill=tk.X, padx=20, pady=10)
                ttk.Button(btn_frame2, text="💾 Save", command=save_changes).pack(side=tk.RIGHT, padx=5)
                ttk.Button(btn_frame2, text="Cancel", command=edit_dialog.destroy).pack(side=tk.RIGHT, padx=5)
            
            def delete_vendor():
                """Delete selected vendor price."""
                selection = vendor_tree.selection()
                if not selection:
                    messagebox.showwarning("Warning", "Please select a vendor")
                    return
                
                item = vendor_tree.item(selection[0])
                vendor_price_id = int(item['tags'][0])
                vendor_name = item['values'][0]
                
                if not messagebox.askyesno("Confirm Delete", f"Delete vendor '{vendor_name}'?"):
                    return
                
                try:
                    self.ingredient_db.delete_vendor_price(vendor_price_id)
                    messagebox.showinfo("Success", f"Deleted vendor: {vendor_name}")
                    load_vendors()
                    self.on_ingredient_select(None)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete vendor: {e}")
            
            ttk.Button(btn_frame, text="➕ Add Vendor", command=add_vendor).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="✏️ Edit", command=edit_vendor).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="🗑️ Delete", command=delete_vendor).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to manage vendors: {e}")
    
    def paste_vendor_prices(self, parent_dialog, ingredient_id, load_vendors_callback):
        """Paste vendor prices from clipboard (Excel data)."""
        try:
            # Get clipboard content
            clipboard_text = self.root.clipboard_get()
            
            if not clipboard_text.strip():
                messagebox.showwarning("Warning", "Clipboard is empty")
                return
            
            # Parse tab-separated data (Excel format)
            lines = clipboard_text.strip().split('\n')
            parsed_data = []
            
            for line_num, line in enumerate(lines, 1):
                if not line.strip():
                    continue
                
                # Split by tab (Excel) or comma
                parts = line.split('\t') if '\t' in line else line.split(',')
                parts = [p.strip() for p in parts]
                
                if len(parts) < 2:
                    continue  # Need at least vendor name and price
                
                # Try to detect columns
                vendor_name = parts[0]
                
                # Find price (first number)
                price = None
                price_idx = None
                for i, part in enumerate(parts[1:], 1):
                    # Remove currency symbols and try to parse
                    clean_part = part.replace('$', '').replace('€', '').replace(',', '').strip()
                    try:
                        price = float(clean_part)
                        price_idx = i
                        break
                    except ValueError:
                        continue
                
                if price is None:
                    continue  # Skip if no valid price found
                
                # Find unit (after price, or in same cell)
                unit = 'lb'  # default
                if price_idx and price_idx < len(parts):
                    # Check if unit is in price cell or next cell
                    price_cell = parts[price_idx]
                    # Look for common units
                    for u in ['lb', 'kg', 'g', 'oz', 'each', 'ea', 'case', 'pack', 'box']:
                        if u.lower() in price_cell.lower():
                            unit = u
                            break
                    # Or check next cell
                    if price_idx + 1 < len(parts):
                        next_cell = parts[price_idx + 1].lower()
                        for u in ['lb', 'kg', 'g', 'oz', 'each', 'ea', 'case', 'pack', 'box']:
                            if u in next_cell:
                                unit = u
                                break
                
                # URL (optional, usually last column or contains http)
                url = None
                for part in parts:
                    if part.startswith('http://') or part.startswith('https://'):
                        url = part
                        break
                
                parsed_data.append({
                    'vendor_name': vendor_name,
                    'price': price,
                    'unit': unit,
                    'url': url,
                    'row': line_num
                })
            
            if not parsed_data:
                messagebox.showwarning("Warning", "Could not parse any vendor data from clipboard.\n\nExpected format:\nVendor Name\tPrice\tUnit\nor\nVendor Name,Price,Unit")
                return
            
            # Show preview dialog
            preview_dialog = tk.Toplevel(parent_dialog)
            preview_dialog.title("Preview Pasted Vendors")
            preview_dialog.geometry("600x400")
            preview_dialog.transient(parent_dialog)
            preview_dialog.grab_set()
            
            ttk.Label(preview_dialog, text=f"Found {len(parsed_data)} vendors to add:", 
                     font=("Arial", 10, "bold")).pack(pady=10)
            
            # Preview list
            preview_frame = ttk.Frame(preview_dialog, padding="10")
            preview_frame.pack(fill=tk.BOTH, expand=True)
            
            preview_tree = ttk.Treeview(preview_frame, columns=('Vendor', 'Price', 'Unit', 'URL'), 
                                       show='headings', height=12)
            preview_tree.heading('Vendor', text='Vendor Name')
            preview_tree.heading('Price', text='Price')
            preview_tree.heading('Unit', text='Unit')
            preview_tree.heading('URL', text='URL')
            
            for col in ('Vendor', 'Price', 'Unit', 'URL'):
                preview_tree.column(col, width=120)
            
            scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=preview_tree.yview)
            preview_tree.configure(yscrollcommand=scrollbar.set)
            
            preview_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            for item in parsed_data:
                preview_tree.insert('', tk.END, values=(
                    item['vendor_name'],
                    f"${item['price']:.2f}",
                    item['unit'],
                    item['url'] or ''
                ))
            
            def confirm_add():
                """Add all vendors."""
                added = 0
                skipped = 0
                errors = []
                
                for item in parsed_data:
                    try:
                        # Check if vendor already exists
                        existing_vendors = self.ingredient_db.get_vendor_prices(ingredient_id)
                        if any(v['vendor_name'].lower() == item['vendor_name'].lower() 
                              for v in existing_vendors):
                            skipped += 1
                            continue
                        
                        self.ingredient_db.add_vendor_price(
                            ingredient_id,
                            item['vendor_name'],
                            item['price'],
                            item['unit'],
                            item['url'],
                            f"Pasted from clipboard"
                        )
                        added += 1
                    except Exception as e:
                        errors.append(f"{item['vendor_name']}: {str(e)}")
                
                preview_dialog.destroy()
                
                result_msg = f"✅ Added: {added} vendors\n"
                if skipped > 0:
                    result_msg += f"⏭️ Skipped: {skipped} (already exist)\n"
                if errors:
                    result_msg += f"❌ Errors: {len(errors)}\n"
                    result_msg += "\n".join(errors[:5])  # Show first 5 errors
                
                messagebox.showinfo("Import Complete", result_msg)
                load_vendors_callback()
                self.on_ingredient_select(None)  # Refresh details
            
            # Buttons
            btn_frame = ttk.Frame(preview_dialog)
            btn_frame.pack(fill=tk.X, padx=10, pady=10)
            ttk.Button(btn_frame, text="✅ Add All", command=confirm_add).pack(side=tk.LEFT, padx=5)
            ttk.Button(btn_frame, text="Cancel", command=preview_dialog.destroy).pack(side=tk.RIGHT, padx=5)
            
        except tk.TclError:
            messagebox.showerror("Error", "Could not read from clipboard. Make sure you've copied data from Excel.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse clipboard data: {e}")
    
    def show_ingredient_stats(self):
        """Show ingredient database statistics."""
        try:
            stats = self.ingredient_db.get_statistics()
            
            stats_text = f"📊 Ingredient Database Statistics\n"
            stats_text += "=" * 50 + "\n\n"
            stats_text += f"Total Ingredients: {stats['total_ingredients']}\n\n"
            stats_text += "By Category:\n"
            for category, count in sorted(stats['by_category'].items()):
                stats_text += f"  • {category}: {count}\n"
            
            messagebox.showinfo("Ingredient Statistics", stats_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load statistics: {e}")
    
    def import_vendor_prices(self):
        """Import vendor prices from Excel file."""
        # File selection dialog
        file_path = filedialog.askopenfilename(
            title="Select Vendor Price List",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        # Vendor name dialog
        vendor_name = tk.simpledialog.askstring(
            "Vendor Name",
            "Enter vendor name:",
            initialvalue=Path(file_path).stem
        )
        
        if not vendor_name:
            vendor_name = Path(file_path).stem
        
        # Preview first
        preview_result = messagebox.askyesno(
            "Preview Import",
            "Would you like to preview the import first?\n\n"
            "Yes = Preview only (no changes)\n"
            "No = Import directly (updates costs)"
        )
        
        def do_import():
            try:
                importer = VendorPriceImporter(self.ingredient_db)
                
                if preview_result:
                    # Preview mode
                    result = importer.preview_import(file_path, vendor_name)
                    
                    if result['success']:
                        preview_text = f"📋 Import Preview\n"
                        preview_text += "=" * 50 + "\n\n"
                        preview_text += f"Vendor: {vendor_name}\n"
                        preview_text += f"File: {Path(file_path).name}\n\n"
                        preview_text += "Detected Columns:\n"
                        for key, value in result['columns_detected'].items():
                            preview_text += f"  • {key}: {value}\n"
                        preview_text += f"\nSample Items ({len(result['sample_items'])}):\n"
                        for item in result['sample_items'][:10]:
                            preview_text += f"  • {item['vendor_name']}: ${item['price']:.2f} {item.get('unit', '')}\n"
                        preview_text += f"\nTotal rows in file: {result['total_rows_in_file']}\n"
                        preview_text += "\nClick 'Import Vendor Prices' again and choose 'No' to import."
                        
                        # Show in a scrollable dialog
                        preview_dialog = tk.Toplevel(self.root)
                        preview_dialog.title("Import Preview")
                        preview_dialog.geometry("600x500")
                        
                        text_widget = scrolledtext.ScrolledText(preview_dialog, wrap=tk.WORD)
                        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                        text_widget.insert(1.0, preview_text)
                        text_widget.config(state=tk.DISABLED)
                        
                        ttk.Button(preview_dialog, text="Close", 
                                  command=preview_dialog.destroy).pack(pady=10)
                    else:
                        messagebox.showerror("Preview Failed", result['error'])
                else:
                    # Actual import
                    result = importer.import_from_excel(file_path, vendor_name, auto_match=True)
                    
                    if result['success']:
                        success_text = f"✅ Import Complete!\n\n"
                        success_text += f"Vendor: {result['vendor']}\n"
                        success_text += f"Total items: {result['total_items']}\n"
                        success_text += f"Matched: {result['matched']}\n"
                        success_text += f"Updated: {result['updated']}\n"
                        success_text += f"Unmatched: {result['unmatched']}\n"
                        
                        if result['unmatched'] > 0:
                            success_text += f"\n⚠️ {result['unmatched']} items could not be automatically matched."
                            success_text += "\nYou can add them manually in the ingredient database."
                        
                        messagebox.showinfo("Import Complete", success_text)
                        
                        # Refresh ingredient list
                        self.search_ingredients()
                    else:
                        messagebox.showerror("Import Failed", result['error'])
                        
            except Exception as e:
                messagebox.showerror("Error", f"Import failed: {e}")
        
        # Run in thread to avoid blocking
        threading.Thread(target=do_import, daemon=True).start()


def main():
    """Main entry point."""
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    
    app = UnifiedDashboard(root)
    root.mainloop()


if __name__ == '__main__':
    main()


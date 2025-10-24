#!/usr/bin/env python3
"""
Enhanced Payroll App - Complete Feature Set
Includes all features from the original app plus CSV import functionality
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import sys
import sqlite3
from datetime import datetime, timedelta
import csv
import re
import atexit
import time

# Try to import optional dependencies
try:
    from tkcalendar import Calendar
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False
    Calendar = None

try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False

# Fix for executable path issues
def get_app_directory():
    """Get the directory where the application is running from"""
    if getattr(sys, 'frozen', False):
        # Running as executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

# Set up directories
APP_DIR = get_app_directory()
PROFILE_DIR = os.path.join(APP_DIR, 'profiles')

# Ensure profiles directory exists
if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

class EnhancedPayrollApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Professional Payroll System - Enhanced")
        self.root.geometry("1400x900")
        
        # Project selection at startup
        self.current_profile = self.select_project_at_startup()
        if not self.current_profile:
            self.root.destroy()
            return
            
        self.db_path = os.path.join(PROFILE_DIR, f"{self.current_profile}.db")
        self.setup_database()
        
        # Auto-save setup
        self.auto_save_interval = 300000  # 5 minutes
        self.setup_auto_save()
        atexit.register(self.auto_save)
        
        self.create_interface()
        
        # Load settings and restore form data
        self.load_settings()
        self.restore_form_data()
        
        # Update window title with current project
        self.root.title(f"Professional Payroll System - {self.current_profile}")
    
    def setup_database(self):
        """Set up the SQLite database with comprehensive tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Drop existing tables to ensure clean structure
            cursor.execute("DROP TABLE IF EXISTS payroll_details")
            cursor.execute("DROP TABLE IF EXISTS payroll_runs")
            cursor.execute("DROP TABLE IF EXISTS employees")
            
            # Create employees table with all fields
            cursor.execute('''
                CREATE TABLE employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT,
                    hourly_rate REAL NOT NULL,
                    hire_date TEXT,
                    dob TEXT,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    emergency_contact TEXT,
                    tax_id TEXT,
                    bank_name TEXT,
                    account_number TEXT,
                    routing_number TEXT,
                    employee_id TEXT,
                    job_code TEXT,
                    location TEXT
                )
            ''')
            
            # Create payroll_runs table with correct structure
            cursor.execute('''
                CREATE TABLE payroll_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    employee_name TEXT NOT NULL,
                    pay_date TEXT NOT NULL,
                    regular_hours REAL DEFAULT 0,
                    overtime_hours REAL DEFAULT 0,
                    hourly_rate REAL NOT NULL,
                    regular_pay REAL DEFAULT 0,
                    overtime_pay REAL DEFAULT 0,
                    bonus REAL DEFAULT 0,
                    deductions REAL DEFAULT 0,
                    gross_pay REAL DEFAULT 0,
                    federal_tax REAL DEFAULT 0,
                    ss_tax REAL DEFAULT 0,
                    medicare_tax REAL DEFAULT 0,
                    state_tax REAL DEFAULT 0,
                    net_pay REAL DEFAULT 0,
                    net_sales REAL DEFAULT 0,
                    total_gratuity REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            ''')
            
            # Create payroll_details table
            cursor.execute('''
                CREATE TABLE payroll_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payroll_run_id INTEGER NOT NULL,
                    detail_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    FOREIGN KEY (payroll_run_id) REFERENCES payroll_runs (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            print("Database tables created successfully with correct structure")
            
        except Exception as e:
            print(f"Database setup error: {e}")
            messagebox.showerror("Database Error", f"Failed to setup database: {e}")
    
    def migrate_database(self):
        """Migrate existing database to new schema if needed"""
        # This function is no longer needed since we create fresh tables
        pass
    
    def setup_auto_save(self):
        """Set up auto-save functionality"""
        self.last_auto_save = time.time()
        self.auto_save_enabled = True
        self.root.after(self.auto_save_interval, self.auto_save)
    
    def auto_save(self):
        """Auto-save function - saves current form data and database"""
        if not self.auto_save_enabled:
            return
            
        try:
            # Only save form data if the interface has been created
            if hasattr(self, 'notebook'):
                # Save any pending employee form data
                self.save_current_employee_form()
                
                # Save any pending payroll form data
                self.save_current_payroll_form()
            
            # Update last auto-save time
            self.last_auto_save = time.time()
            
            # Update status display if available
            if hasattr(self, 'update_status_display'):
                self.update_status_display()
            
            # Schedule next auto-save
            self.root.after(self.auto_save_interval, self.auto_save)
            
        except Exception as e:
            print(f"Auto-save error: {e}")
            # Still schedule next auto-save even if this one failed
            self.root.after(self.auto_save_interval, self.auto_save)
    
    def save_current_employee_form(self):
        """Save current employee form data to temporary storage"""
        try:
            # Check if form variables exist
            if not hasattr(self, 'root') or not self.root:
                return
                
            # Get current form data
            form_data = {}
            for field in ['name', 'position', 'hourly_rate', 'hire_date', 'dob', 'address', 
                         'phone', 'email', 'emergency_contact', 'tax_id', 'bank_name', 
                         'account_number', 'routing_number', 'employee_id', 'job_code', 'location']:
                var_name = f'employee_{field}_var'
                if hasattr(self, var_name):
                    form_data[field] = getattr(self, var_name).get()
                else:
                    form_data[field] = ""
            
            # Save to temporary file
            temp_file = os.path.join(APP_DIR, 'temp_employee_form.json')
            import json
            with open(temp_file, 'w') as f:
                json.dump(form_data, f)
                
        except Exception as e:
            print(f"Error saving employee form: {e}")
    
    def save_current_payroll_form(self):
        """Save current payroll form data to temporary storage"""
        try:
            # Check if form variables exist
            if not hasattr(self, 'root') or not self.root:
                return
                
            # Get current form data
            form_data = {}
            for field in ['employee_id', 'pay_date', 'regular_hours', 'overtime_hours', 
                         'hourly_rate', 'bonus', 'deductions', 'net_sales', 'total_gratuity']:
                var_name = f'payroll_{field}_var'
                if hasattr(self, var_name):
                    form_data[field] = getattr(self, var_name).get()
                else:
                    form_data[field] = ""
            
            # Save to temporary file
            temp_file = os.path.join(APP_DIR, 'temp_payroll_form.json')
            import json
            with open(temp_file, 'w') as f:
                json.dump(form_data, f)
                
        except Exception as e:
            print(f"Error saving payroll form: {e}")
    
    def restore_form_data(self):
        """Restore form data from temporary storage"""
        try:
            # Only restore if interface is ready
            if not hasattr(self, 'notebook'):
                return
                
            # Restore employee form
            emp_temp_file = os.path.join(APP_DIR, 'temp_employee_form.json')
            if os.path.exists(emp_temp_file):
                import json
                with open(emp_temp_file, 'r') as f:
                    form_data = json.load(f)
                
                # Restore to form fields
                for field, value in form_data.items():
                    var_name = f'employee_{field}_var'
                    if hasattr(self, var_name):
                        getattr(self, var_name).set(value)
            
            # Restore payroll form
            pay_temp_file = os.path.join(APP_DIR, 'temp_payroll_form.json')
            if os.path.exists(pay_temp_file):
                import json
                with open(pay_temp_file, 'r') as f:
                    form_data = json.load(f)
                
                # Restore to form fields
                for field, value in form_data.items():
                    var_name = f'payroll_{field}_var'
                    if hasattr(self, var_name):
                        getattr(self, var_name).set(value)
                        
        except Exception as e:
            print(f"Error restoring form data: {e}")
    
    def select_project_at_startup(self):
        """Show project selection dialog at startup"""
        # Create a modal dialog for project selection
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Project")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Main content
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="Select or Create Project", font=("Arial", 16, "bold")).pack(pady=(0, 20))
        
        # Project list frame
        list_frame = ttk.LabelFrame(main_frame, text="Existing Projects", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Project listbox
        self.project_listbox = tk.Listbox(list_frame, height=8)
        self.project_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Load existing projects
        self.load_existing_projects()
        
        # New project frame
        new_frame = ttk.LabelFrame(main_frame, text="Create New Project", padding="10")
        new_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(new_frame, text="Project Name:").pack(side=tk.LEFT)
        self.new_project_var = tk.StringVar()
        new_project_entry = ttk.Entry(new_frame, textvariable=self.new_project_var, width=30)
        new_project_entry.pack(side=tk.LEFT, padx=(5, 10))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.selected_project = None
        
        def on_select():
            selection = self.project_listbox.curselection()
            if selection:
                self.selected_project = self.project_listbox.get(selection[0])
                dialog.destroy()
        
        def on_create():
            new_name = self.new_project_var.get().strip()
            if new_name:
                if self.create_new_project(new_name):
                    self.selected_project = new_name
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Project name already exists or is invalid.")
            else:
                messagebox.showerror("Error", "Please enter a project name.")
        
        def on_cancel():
            self.selected_project = None
            dialog.destroy()
        
        ttk.Button(button_frame, text="Select Project", command=on_select).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Create New", command=on_create).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.RIGHT)
        
        # Bind double-click to select
        self.project_listbox.bind('<Double-Button-1>', lambda e: on_select())
        
        # Focus on entry
        new_project_entry.focus()
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return self.selected_project
    
    def load_existing_projects(self):
        """Load existing projects into the listbox"""
        try:
            self.project_listbox.delete(0, tk.END)
            
            if os.path.exists(PROFILE_DIR):
                for filename in os.listdir(PROFILE_DIR):
                    if filename.endswith('.db'):
                        project_name = filename[:-3]  # Remove .db extension
                        self.project_listbox.insert(tk.END, project_name)
            
            # If no projects exist, add default
            if self.project_listbox.size() == 0:
                self.project_listbox.insert(tk.END, "Default")
                
        except Exception as e:
            print(f"Error loading projects: {e}")
    
    def create_new_project(self, project_name):
        """Create a new project database"""
        try:
            # Validate project name
            if not project_name or len(project_name.strip()) == 0:
                return False
            
            # Check if project already exists
            db_path = os.path.join(PROFILE_DIR, f"{project_name}.db")
            if os.path.exists(db_path):
                return False
            
            # Create new database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT,
                    hourly_rate REAL NOT NULL,
                    hire_date TEXT,
                    dob TEXT,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    emergency_contact TEXT,
                    tax_id TEXT,
                    bank_name TEXT,
                    account_number TEXT,
                    routing_number TEXT,
                    employee_id TEXT,
                    job_code TEXT,
                    location TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payroll_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    employee_name TEXT NOT NULL,
                    pay_date TEXT NOT NULL,
                    regular_hours REAL DEFAULT 0,
                    overtime_hours REAL DEFAULT 0,
                    hourly_rate REAL NOT NULL,
                    regular_pay REAL DEFAULT 0,
                    overtime_pay REAL DEFAULT 0,
                    bonus REAL DEFAULT 0,
                    deductions REAL DEFAULT 0,
                    gross_pay REAL DEFAULT 0,
                    federal_tax REAL DEFAULT 0,
                    ss_tax REAL DEFAULT 0,
                    medicare_tax REAL DEFAULT 0,
                    state_tax REAL DEFAULT 0,
                    net_pay REAL DEFAULT 0,
                    net_sales REAL DEFAULT 0,
                    total_gratuity REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payroll_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    payroll_run_id INTEGER NOT NULL,
                    detail_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    FOREIGN KEY (payroll_run_id) REFERENCES payroll_runs (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False
    
    def create_top_toolbar(self):
        """Create top toolbar with project switcher and quick actions"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Project switcher frame
        project_frame = ttk.LabelFrame(toolbar, text="Current Project", padding="5")
        project_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Project dropdown
        ttk.Label(project_frame, text="Project:").pack(side=tk.LEFT)
        self.project_var = tk.StringVar(value=self.current_profile)
        self.project_combo = ttk.Combobox(project_frame, textvariable=self.project_var, width=25, state="readonly")
        self.project_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        # Load projects into dropdown
        self.refresh_project_list()
        
        # Project management buttons
        ttk.Button(project_frame, text="Switch", command=self.switch_project).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(project_frame, text="New", command=self.create_project_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(project_frame, text="Delete", command=self.delete_project_dialog).pack(side=tk.LEFT)
        
        # Quick actions frame
        actions_frame = ttk.LabelFrame(toolbar, text="Quick Actions", padding="5")
        actions_frame.pack(side=tk.RIGHT)
        
        ttk.Button(actions_frame, text="Save Now", command=self.manual_save).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Refresh", command=self.refresh_all_data).pack(side=tk.LEFT)
        
        # Bind project change event
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_selected)
    
    def refresh_project_list(self):
        """Refresh the project dropdown list"""
        try:
            projects = []
            if os.path.exists(PROFILE_DIR):
                for filename in os.listdir(PROFILE_DIR):
                    if filename.endswith('.db'):
                        project_name = filename[:-3]  # Remove .db extension
                        projects.append(project_name)
            
            # If no projects exist, create default
            if not projects:
                projects = ["Default"]
                self.create_new_project("Default")
            
            self.project_combo['values'] = projects
            
            # Set current project if it exists
            if self.current_profile in projects:
                self.project_var.set(self.current_profile)
            elif projects:
                self.project_var.set(projects[0])
                
        except Exception as e:
            print(f"Error refreshing project list: {e}")
    
    def switch_project(self):
        """Switch to selected project"""
        selected_project = self.project_var.get()
        if selected_project and selected_project != self.current_profile:
            # Save current data before switching
            self.manual_save()
            
            # Switch project
            self.current_profile = selected_project
            self.db_path = os.path.join(PROFILE_DIR, f"{self.current_profile}.db")
            
            # Update window title
            self.root.title(f"Professional Payroll System - {self.current_profile}")
            
            # Refresh all data
            self.refresh_all_data()
            
            # Update status display
            self.update_status_display()
            
            messagebox.showinfo("Project Switched", f"Switched to project: {self.current_profile}")
    
    def create_project_dialog(self):
        """Show dialog to create new project"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Project")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Main content
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Create New Project", font=("Arial", 14, "bold")).pack(pady=(0, 20))
        
        ttk.Label(main_frame, text="Project Name:").pack(anchor=tk.W)
        new_project_var = tk.StringVar()
        entry = ttk.Entry(main_frame, textvariable=new_project_var, width=40)
        entry.pack(fill=tk.X, pady=(5, 20))
        
        def on_create():
            project_name = new_project_var.get().strip()
            if project_name:
                if self.create_new_project(project_name):
                    self.refresh_project_list()
                    self.project_var.set(project_name)
                    dialog.destroy()
                    messagebox.showinfo("Success", f"Project '{project_name}' created successfully!")
                else:
                    messagebox.showerror("Error", "Project name already exists or is invalid.")
            else:
                messagebox.showerror("Error", "Please enter a project name.")
        
        def on_cancel():
            dialog.destroy()
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Create", command=on_create).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.RIGHT)
        
        entry.focus()
        dialog.wait_window()
    
    def delete_project_dialog(self):
        """Show dialog to delete project"""
        selected_project = self.project_var.get()
        if not selected_project:
            return
        
        if selected_project == self.current_profile:
            messagebox.showerror("Error", "Cannot delete the currently active project. Please switch to a different project first.")
            return
        
        result = messagebox.askyesno("Delete Project", 
                                   f"Are you sure you want to delete project '{selected_project}'?\n\n"
                                   "This will permanently delete all employee and payroll data for this project.")
        
        if result:
            try:
                db_path = os.path.join(PROFILE_DIR, f"{selected_project}.db")
                if os.path.exists(db_path):
                    os.remove(db_path)
                    self.refresh_project_list()
                    messagebox.showinfo("Success", f"Project '{selected_project}' deleted successfully!")
                else:
                    messagebox.showerror("Error", "Project database not found.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete project: {e}")
    
    def on_project_selected(self, event=None):
        """Handle project selection from dropdown"""
        # This will be called when user selects from dropdown
        # The actual switching is handled by the Switch button
        pass
    
    def refresh_all_data(self):
        """Refresh all data after project switch"""
        try:
            # Clear current data
            self.clear_employee_form()
            self.clear_payroll_form()
            
            # Reload data
            self.load_employees()
            self.load_payroll_history()
            self.load_all_payrolls()
            
            # Update status
            self.update_status_display()
            
        except Exception as e:
            print(f"Error refreshing data: {e}")
    
    def create_status_bar(self):
        """Create status bar with auto-save information"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Auto-save status
        self.status_auto_save = tk.StringVar(value="Auto-save: Enabled (5 min)")
        ttk.Label(self.status_bar, textvariable=self.status_auto_save, font=("Arial", 9)).pack(side=tk.LEFT, padx=5)
        
        # Last save time
        self.status_last_save = tk.StringVar(value="Last save: Never")
        ttk.Label(self.status_bar, textvariable=self.status_last_save, font=("Arial", 9)).pack(side=tk.LEFT, padx=20)
        
        # Database status
        self.status_db = tk.StringVar(value="Database: Connected")
        ttk.Label(self.status_bar, textvariable=self.status_db, font=("Arial", 9)).pack(side=tk.RIGHT, padx=5)
        
        # Current project status
        self.status_project = tk.StringVar(value=f"Project: {self.current_profile}")
        ttk.Label(self.status_bar, textvariable=self.status_project, font=("Arial", 9)).pack(side=tk.RIGHT, padx=20)
        
        # Update status display
        self.update_status_display()
    
    def update_status_display(self):
        """Update status bar display"""
        try:
            # Update auto-save status
            status_text = f"Auto-save: {'Enabled' if self.auto_save_enabled else 'Disabled'} ({self.auto_save_var.get()} min)"
            self.status_auto_save.set(status_text)
            
            # Update last save time
            if hasattr(self, 'last_auto_save'):
                last_save_time = datetime.fromtimestamp(self.last_auto_save).strftime("%H:%M:%S")
                self.status_last_save.set(f"Last save: {last_save_time}")
            
            # Update database status
            try:
                conn = sqlite3.connect(self.db_path)
                conn.close()
                self.status_db.set("Database: Connected")
            except:
                self.status_db.set("Database: Error")
            
            # Update project status
            self.status_project.set(f"Project: {self.current_profile}")
                
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def create_interface(self):
        """Create the main interface with all tabs"""
        # Create top toolbar with project switcher
        self.create_top_toolbar()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create tabs
        self.create_employees_tab()
        self.create_payroll_tab()
        self.create_past_payrolls_tab()
        self.create_import_tab()
        self.create_reports_tab()
        self.create_calendar_tab()
        self.create_settings_tab()
        
        # Load initial data
        self.load_employees()
        
        # Set up closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create status bar
        self.create_status_bar()
    
    def create_employees_tab(self):
        """Create the comprehensive employees management tab"""
        employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(employees_frame, text="Employee Management")
        
        # Main container with two panels
        main_frame = ttk.Frame(employees_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Employee list
        list_frame = ttk.LabelFrame(main_frame, text="Employee List", padding="10")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Search frame
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.employee_search_var = tk.StringVar()
        self.employee_search_entry = ttk.Entry(search_frame, textvariable=self.employee_search_var)
        self.employee_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.employee_search_var.trace('w', self.filter_employees)
        
        # Employee treeview
        self.employee_tree = ttk.Treeview(list_frame, columns=("ID", "Name", "Position", "Rate"), show="headings", height=15)
        self.employee_tree.heading("ID", text="ID")
        self.employee_tree.heading("Name", text="Name")
        self.employee_tree.heading("Position", text="Position")
        self.employee_tree.heading("Rate", text="Hourly Rate")
        
        self.employee_tree.column("ID", width=50)
        self.employee_tree.column("Name", width=150)
        self.employee_tree.column("Position", width=120)
        self.employee_tree.column("Rate", width=100)
        
        self.employee_tree.pack(fill=tk.BOTH, expand=True)
        self.employee_tree.bind('<<TreeviewSelect>>', self.on_employee_select)
        
        # Employee list buttons
        emp_button_frame = ttk.Frame(list_frame)
        emp_button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(emp_button_frame, text="Refresh", command=self.load_employees).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(emp_button_frame, text="Export", command=self.export_employees).pack(side=tk.LEFT)
        
        # Right side - Employee form
        form_frame = ttk.LabelFrame(main_frame, text="Employee Details", padding="10")
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Create scrollable form
        canvas = tk.Canvas(form_frame)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        self.create_employee_form_fields(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_employee_form_fields(self, parent):
        """Create comprehensive employee form fields"""
        # Basic Information
        basic_frame = ttk.LabelFrame(parent, text="Basic Information", padding="5")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(basic_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.name_entry = ttk.Entry(basic_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(basic_frame, text="Position:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.position_entry = ttk.Entry(basic_frame, width=30)
        self.position_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(basic_frame, text="Hourly Rate:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.rate_entry = ttk.Entry(basic_frame, width=30)
        self.rate_entry.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(basic_frame, text="Employee ID:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.emp_id_entry = ttk.Entry(basic_frame, width=30)
        self.emp_id_entry.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # Contact Information
        contact_frame = ttk.LabelFrame(parent, text="Contact Information", padding="5")
        contact_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(contact_frame, text="Phone:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.phone_entry = ttk.Entry(contact_frame, width=30)
        self.phone_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(contact_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email_entry = ttk.Entry(contact_frame, width=30)
        self.email_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(contact_frame, text="Address:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.address_entry = ttk.Entry(contact_frame, width=30)
        self.address_entry.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Dates
        dates_frame = ttk.LabelFrame(parent, text="Important Dates", padding="5")
        dates_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(dates_frame, text="Hire Date:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.hire_date_entry = ttk.Entry(dates_frame, width=20)
        self.hire_date_entry.grid(row=0, column=1, sticky=tk.W, pady=2)
        ttk.Button(dates_frame, text="📅", command=lambda: self.open_calendar(self.hire_date_entry)).grid(row=0, column=2, padx=(5, 0))
        
        ttk.Label(dates_frame, text="Date of Birth:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.dob_entry = ttk.Entry(dates_frame, width=20)
        self.dob_entry.grid(row=1, column=1, sticky=tk.W, pady=2)
        ttk.Button(dates_frame, text="📅", command=lambda: self.open_calendar(self.dob_entry)).grid(row=1, column=2, padx=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Add Employee", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Employee", command=self.update_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Employee", command=self.delete_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_employee_form).pack(side=tk.LEFT, padx=5)
    
    def create_payroll_tab(self):
        """Create the comprehensive payroll processing tab"""
        payroll_frame = ttk.Frame(self.notebook)
        self.notebook.add(payroll_frame, text="Payroll Calculation")
        
        # Main container
        main_frame = ttk.Frame(payroll_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Payroll input
        input_frame = ttk.LabelFrame(main_frame, text="Payroll Entry", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Employee selection
        ttk.Label(input_frame, text="Employee:").pack(anchor=tk.W)
        self.payroll_employee_var = tk.StringVar()
        self.payroll_employee_combo = ttk.Combobox(input_frame, textvariable=self.payroll_employee_var, state="readonly", width=30)
        self.payroll_employee_combo.pack(pady=(0, 10), fill=tk.X)
        self.payroll_employee_combo.bind("<<ComboboxSelected>>", self.on_payroll_employee_select)
        
        # Pay period
        ttk.Label(input_frame, text="Pay Period:").pack(anchor=tk.W)
        period_frame = ttk.Frame(input_frame)
        period_frame.pack(pady=(0, 10), fill=tk.X)
        
        self.start_date_entry = ttk.Entry(period_frame, width=15)
        self.start_date_entry.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(period_frame, text="📅", command=lambda: self.open_calendar(self.start_date_entry)).pack(side=tk.LEFT)
        
        ttk.Label(period_frame, text="to").pack(side=tk.LEFT, padx=5)
        
        self.end_date_entry = ttk.Entry(period_frame, width=15)
        self.end_date_entry.pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(period_frame, text="📅", command=lambda: self.open_calendar(self.end_date_entry)).pack(side=tk.LEFT)
        
        # Hours worked
        ttk.Label(input_frame, text="Regular Hours:").pack(anchor=tk.W)
        self.regular_hours_entry = ttk.Entry(input_frame, width=30)
        self.regular_hours_entry.pack(pady=(0, 5), fill=tk.X)
        self.regular_hours_entry.bind("<KeyRelease>", self.calculate_payroll)
        
        ttk.Label(input_frame, text="Overtime Hours:").pack(anchor=tk.W)
        self.overtime_hours_entry = ttk.Entry(input_frame, width=30)
        self.overtime_hours_entry.pack(pady=(0, 10), fill=tk.X)
        self.overtime_hours_entry.bind("<KeyRelease>", self.calculate_payroll)
        
        # Current hourly rate (read-only)
        ttk.Label(input_frame, text="Hourly Rate:").pack(anchor=tk.W)
        self.payroll_rate_entry = ttk.Entry(input_frame, state="readonly", width=30)
        self.payroll_rate_entry.pack(pady=(0, 10), fill=tk.X)
        
        # Bonus/Deductions
        ttk.Label(input_frame, text="Bonus:").pack(anchor=tk.W)
        self.bonus_entry = ttk.Entry(input_frame, width=30)
        self.bonus_entry.pack(pady=(0, 5), fill=tk.X)
        self.bonus_entry.bind("<KeyRelease>", self.calculate_payroll)
        
        ttk.Label(input_frame, text="Deductions:").pack(anchor=tk.W)
        self.deductions_entry = ttk.Entry(input_frame, width=30)
        self.deductions_entry.pack(pady=(0, 10), fill=tk.X)
        self.deductions_entry.bind("<KeyRelease>", self.calculate_payroll)
        
        # Calculation results (read-only)
        results_frame = ttk.LabelFrame(input_frame, text="Calculation Results", padding="10")
        results_frame.pack(pady=(10, 0), fill=tk.X)
        
        self.create_payroll_result_fields(results_frame)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=(15, 0), fill=tk.X)
        
        ttk.Button(button_frame, text="Calculate", command=self.calculate_payroll).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Save Payroll", command=self.save_payroll).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_payroll_form).pack(side=tk.LEFT, padx=(5, 0))
        
        # Bulk payroll entry
        bulk_frame = ttk.LabelFrame(input_frame, text="⚡ Bulk Payroll Entry", padding="10")
        bulk_frame.pack(pady=(15, 0), fill=tk.X)
        
        bulk_instructions = "Quick add multiple payroll entries:\nEmployee|Pay Date|Regular Hours|Overtime Hours|Bonus|Deductions"
        ttk.Label(bulk_frame, text=bulk_instructions, font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 10))
        
        # Bulk text area
        bulk_text_frame = ttk.Frame(bulk_frame)
        bulk_text_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.bulk_payroll_text = tk.Text(bulk_text_frame, height=6, width=40)
        self.bulk_payroll_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for bulk text
        bulk_text_scrollbar = ttk.Scrollbar(bulk_text_frame, orient="vertical", command=self.bulk_payroll_text.yview)
        bulk_text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bulk_payroll_text.configure(yscrollcommand=bulk_text_scrollbar.set)
        
        # Bulk buttons
        bulk_button_frame = ttk.Frame(bulk_frame)
        bulk_button_frame.pack(fill=tk.X)
        
        ttk.Button(bulk_button_frame, text="⚡ Add Payroll Entries", command=self.bulk_add_payroll).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(bulk_button_frame, text="🗑️ Clear", command=lambda: self.bulk_payroll_text.delete(1.0, tk.END)).pack(side=tk.LEFT)
        
        # Right side - Payroll History
        history_frame = ttk.LabelFrame(main_frame, text="Recent Payroll Records", padding="10")
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # History tree
        self.history_tree = ttk.Treeview(history_frame, columns=("Employee", "Period", "Hours", "Gross", "Net"), show="headings", height=20)
        self.history_tree.heading("Employee", text="Employee")
        self.history_tree.heading("Period", text="Pay Period")
        self.history_tree.heading("Hours", text="Total Hours")
        self.history_tree.heading("Gross", text="Gross Pay")
        self.history_tree.heading("Net", text="Net Pay")
        
        self.history_tree.column("Employee", width=120)
        self.history_tree.column("Period", width=100)
        self.history_tree.column("Hours", width=80, anchor=tk.E)
        self.history_tree.column("Gross", width=80, anchor=tk.E)
        self.history_tree.column("Net", width=80, anchor=tk.E)
        
        # History scrollbar
        history_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scroll.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # History buttons
        hist_button_frame = ttk.Frame(history_frame)
        hist_button_frame.pack(pady=(10, 0), fill=tk.X)
        
        ttk.Button(hist_button_frame, text="Refresh", command=self.load_payroll_history).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(hist_button_frame, text="Delete Selected", command=self.delete_payroll_record).pack(side=tk.LEFT)
    
    def create_payroll_result_fields(self, parent):
        """Create payroll calculation result fields"""
        self.payroll_result_entries = {}
        fields = [
            ("Gross Pay:", "gross_pay"),
            ("Federal Tax (15%):", "federal_tax"),
            ("Social Security (6.2%):", "ss_tax"),
            ("Medicare (1.45%):", "medicare_tax"),
            ("State Tax (5%):", "state_tax"),
            ("Total Taxes:", "total_taxes"),
            ("Net Pay:", "net_pay")
        ]
        
        for label_text, field_name in fields:
            row = ttk.Frame(parent)
            row.pack(fill=tk.X, pady=1)
            
            ttk.Label(row, text=label_text, width=18).pack(side=tk.LEFT)
            entry = ttk.Entry(row, state="readonly", width=15)
            entry.pack(side=tk.RIGHT)
            self.payroll_result_entries[field_name] = entry

    def create_past_payrolls_tab(self):
        """Create the past payrolls management tab"""
        past_payrolls_frame = ttk.Frame(self.notebook)
        self.notebook.add(past_payrolls_frame, text="Past Payrolls")
        
        # Main container
        main_frame = ttk.Frame(past_payrolls_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Filter frame
        filter_frame = ttk.LabelFrame(main_frame, text="Filters", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Date range filter
        date_frame = ttk.Frame(filter_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(date_frame, text="From:").pack(side=tk.LEFT)
        self.filter_start_date = ttk.Entry(date_frame, width=15)
        self.filter_start_date.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(date_frame, text="📅", command=lambda: self.open_calendar(self.filter_start_date)).pack(side=tk.LEFT)
        
        ttk.Label(date_frame, text="To:").pack(side=tk.LEFT, padx=(10, 0))
        self.filter_end_date = ttk.Entry(date_frame, width=15)
        self.filter_end_date.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(date_frame, text="📅", command=lambda: self.open_calendar(self.filter_end_date)).pack(side=tk.LEFT)
        
        # Employee filter
        emp_filter_frame = ttk.Frame(filter_frame)
        emp_filter_frame.pack(fill=tk.X)
        
        ttk.Label(emp_filter_frame, text="Employee:").pack(side=tk.LEFT)
        self.filter_employee_var = tk.StringVar()
        self.filter_employee_combo = ttk.Combobox(emp_filter_frame, textvariable=self.filter_employee_var, width=30)
        self.filter_employee_combo.pack(side=tk.LEFT, padx=(5, 10))
        
        ttk.Button(emp_filter_frame, text="Apply Filter", command=self.apply_payroll_filter).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(emp_filter_frame, text="Show All", command=self.show_all_payrolls).pack(side=tk.LEFT)
        
        # Payroll history tree
        history_frame = ttk.LabelFrame(main_frame, text="Payroll History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbars
        tree_frame = ttk.Frame(history_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.payroll_tree = ttk.Treeview(tree_frame, columns=("ID", "Employee", "Date", "Hours", "Gross", "Taxes", "Net"), show="headings", height=20)
        self.payroll_tree.heading("ID", text="Run ID")
        self.payroll_tree.heading("Employee", text="Employee")
        self.payroll_tree.heading("Date", text="Pay Date")
        self.payroll_tree.heading("Hours", text="Hours")
        self.payroll_tree.heading("Gross", text="Gross Pay")
        self.payroll_tree.heading("Taxes", text="Total Taxes")
        self.payroll_tree.heading("Net", text="Net Pay")
        
        self.payroll_tree.column("ID", width=60)
        self.payroll_tree.column("Employee", width=150)
        self.payroll_tree.column("Date", width=100)
        self.payroll_tree.column("Hours", width=80, anchor=tk.E)
        self.payroll_tree.column("Gross", width=100, anchor=tk.E)
        self.payroll_tree.column("Taxes", width=100, anchor=tk.E)
        self.payroll_tree.column("Net", width=100, anchor=tk.E)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.payroll_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.payroll_tree.xview)
        self.payroll_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for tree and scrollbars
        self.payroll_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind double-click to view details
        self.payroll_tree.bind("<Double-1>", self.view_payroll_details)
        
        # Buttons
        button_frame = ttk.Frame(history_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Refresh", command=self.load_all_payrolls).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="View Details", command=self.view_payroll_details).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Export to Excel", command=self.export_payroll_to_excel).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_payroll).pack(side=tk.LEFT)
    
    def create_import_tab(self):
        """Create the import tab with enhanced bulk import options"""
        import_frame = ttk.Frame(self.notebook)
        self.notebook.add(import_frame, text="Import Data")
        
        # Create scrollable frame
        canvas = tk.Canvas(import_frame)
        scrollbar = ttk.Scrollbar(import_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Master Payroll Import Section
        master_section = ttk.LabelFrame(scrollable_frame, text="📊 Master Payroll CSV Import", padding="20")
        master_section.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        # Instructions
        instructions = """
        Import your Master Payroll CSV file to automatically add employees and payroll data.
        
        This will:
        • Extract unique employees from all pay periods
        • Import their basic information (name, position, hourly rate)
        • Import payroll history for each employee
        • Handle multiple pay cycles automatically
        
        Click "Import Master Payroll CSV" to select your file.
        """
        
        ttk.Label(master_section, text=instructions, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 20))
        
        # Import button
        ttk.Button(master_section, text="🚀 Import Master Payroll CSV", 
                  command=self.import_master_payroll, 
                  style="Accent.TButton").pack(pady=10)
        
        # Status label
        self.import_status_label = ttk.Label(master_section, text="Ready to import", font=("Arial", 10))
        self.import_status_label.pack(pady=10)
        
        # Bulk Employee Import Section
        bulk_employee_section = ttk.LabelFrame(scrollable_frame, text="👥 Bulk Employee Import", padding="20")
        bulk_employee_section.pack(fill=tk.X, padx=20, pady=10)
        
        bulk_employee_instructions = """
        Import multiple employees at once from a CSV file.
        
        Expected CSV format:
        Name,Position,Hourly Rate,Employee ID,Phone,Email,Location
        
        Click "Import Employees CSV" to select your file.
        """
        
        ttk.Label(bulk_employee_section, text=bulk_employee_instructions, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 20))
        
        ttk.Button(bulk_employee_section, text="👥 Import Employees CSV", 
                  command=self.import_employees_csv).pack(pady=10)
        
        # Bulk Payroll Import Section
        bulk_payroll_section = ttk.LabelFrame(scrollable_frame, text="💰 Bulk Payroll Import", padding="20")
        bulk_payroll_section.pack(fill=tk.X, padx=20, pady=10)
        
        bulk_payroll_instructions = """
        Import multiple payroll records at once from a CSV file.
        
        Expected CSV format:
        Employee Name,Pay Date,Regular Hours,Overtime Hours,Hourly Rate,Bonus,Deductions,Net Sales,Gratuity
        
        Click "Import Payroll CSV" to select your file.
        """
        
        ttk.Label(bulk_payroll_section, text=bulk_payroll_instructions, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 20))
        
        ttk.Button(bulk_payroll_section, text="💰 Import Payroll CSV", 
                  command=self.import_payroll_csv).pack(pady=10)
        
        # Quick Add Section
        quick_add_section = ttk.LabelFrame(scrollable_frame, text="⚡ Quick Add Multiple Employees", padding="20")
        quick_add_section.pack(fill=tk.X, padx=20, pady=10)
        
        quick_add_instructions = """
        Quickly add multiple employees using a simple text format.
        
        Format: Name|Position|Hourly Rate|Employee ID
        One employee per line.
        
        Example:
        John Doe|Server|15.50|EMP001
        Jane Smith|Manager|25.00|EMP002
        """
        
        ttk.Label(quick_add_section, text=quick_add_instructions, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 20))
        
        # Quick add text area
        text_frame = ttk.Frame(quick_add_section)
        text_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.quick_add_text = tk.Text(text_frame, height=8, width=60)
        self.quick_add_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for text area
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.quick_add_text.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.quick_add_text.configure(yscrollcommand=text_scrollbar.set)
        
        # Quick add buttons
        button_frame = ttk.Frame(quick_add_section)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="⚡ Add Employees", command=self.quick_add_employees).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Clear", command=lambda: self.quick_add_text.delete(1.0, tk.END)).pack(side=tk.LEFT)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_reports_tab(self):
        """Create the reports tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports")
        
        # Reports content
        ttk.Label(reports_frame, text="Payroll Reports", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Report options frame
        options_frame = ttk.LabelFrame(reports_frame, text="Report Options", padding="20")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Date range for reports
        date_frame = ttk.Frame(options_frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(date_frame, text="Report Period:").pack(side=tk.LEFT)
        self.report_start_date = ttk.Entry(date_frame, width=15)
        self.report_start_date.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(date_frame, text="📅", command=lambda: self.open_calendar(self.report_start_date)).pack(side=tk.LEFT)
        
        ttk.Label(date_frame, text="to").pack(side=tk.LEFT, padx=(10, 0))
        self.report_end_date = ttk.Entry(date_frame, width=15)
        self.report_end_date.pack(side=tk.LEFT, padx=(5, 10))
        ttk.Button(date_frame, text="📅", command=lambda: self.open_calendar(self.report_end_date)).pack(side=tk.LEFT)
        
        # Export buttons
        button_frame = ttk.Frame(reports_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Export Employee List", command=self.export_employees).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Export Payroll History", command=self.export_payroll_history).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Generate Payroll Report", command=self.generate_payroll_report).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Generate Employee Report", command=self.generate_employee_report).pack(side=tk.LEFT, padx=10)
    
    def create_calendar_tab(self):
        """Create the calendar tab"""
        calendar_frame = ttk.Frame(self.notebook)
        self.notebook.add(calendar_frame, text="Calendar")
        
        if TKCALENDAR_AVAILABLE:
            # Calendar widget
            self.calendar = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
            self.calendar.pack(pady=20)
            
            # Calendar info
            info_frame = ttk.LabelFrame(calendar_frame, text="Calendar Information", padding="10")
            info_frame.pack(fill=tk.X, padx=20, pady=10)
            
            ttk.Label(info_frame, text="Select a date to view payroll information for that day.").pack()
            
            # Selected date info
            self.calendar_info_label = ttk.Label(info_frame, text="No date selected")
            self.calendar_info_label.pack(pady=10)
            
            # Bind calendar selection
            self.calendar.bind("<<CalendarSelected>>", self.on_calendar_select)
        else:
            ttk.Label(calendar_frame, text="Calendar feature requires tkcalendar package.\nInstall with: pip install tkcalendar", 
                     font=("Arial", 12)).pack(pady=50)
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Settings content
        ttk.Label(settings_frame, text="Application Settings", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Settings options
        settings_section = ttk.LabelFrame(settings_frame, text="General Settings", padding="20")
        settings_section.pack(fill=tk.X, padx=20, pady=10)
        
        # Auto-save settings
        auto_save_frame = ttk.Frame(settings_section)
        auto_save_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Auto-save enable/disable
        self.auto_save_enabled_var = tk.BooleanVar(value=True)
        auto_save_check = ttk.Checkbutton(auto_save_frame, text="Enable Auto-save", variable=self.auto_save_enabled_var)
        auto_save_check.pack(side=tk.LEFT)
        
        # Auto-save interval
        interval_frame = ttk.Frame(settings_section)
        interval_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(interval_frame, text="Auto-save interval (minutes):").pack(side=tk.LEFT)
        self.auto_save_var = tk.StringVar(value="5")
        auto_save_spinbox = ttk.Spinbox(interval_frame, from_=1, to=60, textvariable=self.auto_save_var, width=10)
        auto_save_spinbox.pack(side=tk.LEFT, padx=(5, 0))
        
        # Auto-save status
        status_frame = ttk.Frame(settings_section)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.auto_save_status_var = tk.StringVar(value="Auto-save: Enabled (5 minutes)")
        ttk.Label(status_frame, textvariable=self.auto_save_status_var, font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Manual save button
        ttk.Button(status_frame, text="Save Now", command=self.manual_save).pack(side=tk.RIGHT)
        
        # Tax rates
        tax_frame = ttk.LabelFrame(settings_frame, text="Tax Rates", padding="20")
        tax_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.federal_tax_rate = tk.StringVar(value="0.15")
        self.ss_tax_rate = tk.StringVar(value="0.062")
        self.medicare_tax_rate = tk.StringVar(value="0.0145")
        self.state_tax_rate = tk.StringVar(value="0.05")
        
        ttk.Label(tax_frame, text="Federal Tax Rate (%):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(tax_frame, textvariable=self.federal_tax_rate, width=10).grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(tax_frame, text="Social Security Rate (%):").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(tax_frame, textvariable=self.ss_tax_rate, width=10).grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(tax_frame, text="Medicare Rate (%):").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(tax_frame, textvariable=self.medicare_tax_rate, width=10).grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        ttk.Label(tax_frame, text="State Tax Rate (%):").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(tax_frame, textvariable=self.state_tax_rate, width=10).grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Save settings button
        ttk.Button(settings_frame, text="Save Settings", command=self.save_settings).pack(pady=20)
    
    def open_calendar(self, entry_widget):
        """Open calendar for date selection"""
        if not TKCALENDAR_AVAILABLE:
            messagebox.showwarning("Calendar Not Available", 
                                 "Calendar feature requires tkcalendar package.\nInstall with: pip install tkcalendar")
            return
        
        def set_date():
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, cal.get_date())
            top.destroy()
        
        top = tk.Toplevel(self.root)
        top.title("Select Date")
        top.geometry("300x250")
        top.transient(self.root)
        top.grab_set()
        
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(pady=20)
        
        ttk.Button(top, text="OK", command=set_date).pack(pady=10)
    
    def on_calendar_select(self, event):
        """Handle calendar date selection"""
        selected_date = self.calendar.get_date()
        # Here you could load payroll data for the selected date
        self.calendar_info_label.config(text=f"Selected: {selected_date}\nPayroll data for this date will be displayed here.")
    
    def save_settings(self):
        """Save application settings"""
        try:
            # Update auto-save settings
            self.auto_save_enabled = self.auto_save_enabled_var.get()
            new_interval = int(self.auto_save_var.get()) * 60000  # Convert to milliseconds
            self.auto_save_interval = new_interval
            
            # Update status display
            self.update_status_display()
            
            # Save settings to config file
            config_data = {
                'auto_save_enabled': self.auto_save_enabled,
                'auto_save_interval': self.auto_save_var.get(),
                'federal_tax_rate': self.federal_tax_rate.get(),
                'ss_tax_rate': self.ss_tax_rate.get(),
                'medicare_tax_rate': self.medicare_tax_rate.get(),
                'state_tax_rate': self.state_tax_rate.get()
            }
            
            config_file = os.path.join(APP_DIR, 'app_config.json')
            import json
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for settings.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def manual_save(self):
        """Manual save function"""
        try:
            # Save current form data
            self.save_current_employee_form()
            self.save_current_payroll_form()
            
            # Update status
            self.last_auto_save = time.time()
            self.update_status_display()
            
            messagebox.showinfo("Save Complete", "All data has been saved successfully!")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data: {e}")
    
    def load_settings(self):
        """Load application settings from config file"""
        try:
            # Only load settings if UI elements exist
            if not hasattr(self, 'auto_save_enabled_var'):
                return
                
            config_file = os.path.join(APP_DIR, 'app_config.json')
            if os.path.exists(config_file):
                import json
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Load settings
                self.auto_save_enabled_var.set(config_data.get('auto_save_enabled', True))
                self.auto_save_var.set(config_data.get('auto_save_interval', '5'))
                self.federal_tax_rate.set(config_data.get('federal_tax_rate', '0.15'))
                self.ss_tax_rate.set(config_data.get('ss_tax_rate', '0.062'))
                self.medicare_tax_rate.set(config_data.get('medicare_tax_rate', '0.0145'))
                self.state_tax_rate.set(config_data.get('state_tax_rate', '0.05'))
                
                # Update auto-save settings
                self.auto_save_enabled = self.auto_save_enabled_var.get()
                self.auto_save_interval = int(self.auto_save_var.get()) * 60000
                
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def on_closing(self):
        """Handle application closing"""
        try:
            self.auto_save()  # Final save
            self.root.destroy()
        except Exception as e:
            print(f"Error during shutdown: {e}")
            self.root.destroy()

    # Core functionality methods
    def load_employees(self):
        """Load employees from database"""
        try:
            # Check if UI elements exist
            if not hasattr(self, 'employee_tree'):
                return
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, position, hourly_rate FROM employees ORDER BY name")
            employees = cursor.fetchall()
            conn.close()
            
            # Clear treeview
            for item in self.employee_tree.get_children():
                self.employee_tree.delete(item)
            
            # Populate treeview and combobox
            employee_names = []
            for employee in employees:
                self.employee_tree.insert("", tk.END, values=(
                    employee[0],  # ID
                    employee[1],  # Name
                    employee[2] or "",  # Position
                    f"${employee[3]:.2f}"  # Hourly Rate
                ))
                employee_names.append(employee[1])
            
            # Update comboboxes if they exist
            if hasattr(self, 'payroll_employee_combo'):
                self.payroll_employee_combo['values'] = employee_names
            if hasattr(self, 'filter_employee_combo'):
                self.filter_employee_combo['values'] = ["All"] + employee_names
            
        except Exception as e:
            print(f"Failed to load employees: {e}")
            # Don't show error message during startup
            if hasattr(self, 'root'):
                messagebox.showerror("Error", f"Failed to load employees: {e}")
    
    def filter_employees(self, *args):
        """Filter employees based on search text"""
        search_text = self.employee_search_var.get().lower()
        
        # Show all items if search is empty
        if not search_text:
            for item in self.employee_tree.get_children():
                self.employee_tree.reattach(item, "", "end")
            return
        
        # Hide items that don't match
        for item in self.employee_tree.get_children():
            values = self.employee_tree.item(item)['values']
            name = values[1].lower() if values[1] else ""
            position = values[2].lower() if values[2] else ""
            
            if search_text in name or search_text in position:
                self.employee_tree.reattach(item, "", "end")
            else:
                self.employee_tree.detach(item)
    
    def on_employee_select(self, event):
        """Handle employee selection in treeview"""
        try:
            selection = self.employee_tree.selection()
            if selection:
                item = self.employee_tree.item(selection[0])
                emp_id = item['values'][0]
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, position, hourly_rate, hire_date, dob, address, 
                           phone, email, emergency_contact, tax_id, bank_name, 
                           account_number, routing_number, employee_id
                    FROM employees WHERE id = ?
                """, (emp_id,))
                employee = cursor.fetchone()
                conn.close()
                
                if employee:
                    self.populate_employee_form(employee)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load employee details: {e}")
    
    def populate_employee_form(self, employee_data):
        """Populate employee form with data"""
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, employee_data[0] or "")
        
        self.position_entry.delete(0, tk.END)
        self.position_entry.insert(0, employee_data[1] or "")
        
        self.rate_entry.delete(0, tk.END)
        self.rate_entry.insert(0, str(employee_data[2]) if employee_data[2] else "")
        
        self.hire_date_entry.delete(0, tk.END)
        self.hire_date_entry.insert(0, employee_data[3] or "")
        
        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, employee_data[4] or "")
        
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, employee_data[5] or "")
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, employee_data[6] or "")
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, employee_data[7] or "")
        
        self.emp_id_entry.delete(0, tk.END)
        self.emp_id_entry.insert(0, employee_data[13] or "")
    
    def add_employee(self):
        """Add a new employee"""
        try:
            name = self.name_entry.get().strip()
            position = self.position_entry.get().strip()
            rate = float(self.rate_entry.get() or 0)
            hire_date = self.hire_date_entry.get().strip()
            dob = self.dob_entry.get().strip()
            address = self.address_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            emp_id = self.emp_id_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Employee name is required")
                return
            
            if rate <= 0:
                messagebox.showerror("Error", "Hourly rate must be greater than 0")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees (name, position, hourly_rate, hire_date, dob, address, phone, email, employee_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, position, rate, hire_date, dob, address, phone, email, emp_id))
            conn.commit()
            conn.close()
            
            self.load_employees()
            self.clear_employee_form()
            messagebox.showinfo("Success", "Employee added successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {e}")
    
    def update_employee(self):
        """Update selected employee"""
        try:
            selection = self.employee_tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select an employee to update")
                return
            
            item = self.employee_tree.item(selection[0])
            emp_id = item['values'][0]
            
            name = self.name_entry.get().strip()
            position = self.position_entry.get().strip()
            rate = float(self.rate_entry.get() or 0)
            hire_date = self.hire_date_entry.get().strip()
            dob = self.dob_entry.get().strip()
            address = self.address_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()
            emp_id_field = self.emp_id_entry.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Employee name is required")
                return
            
            if rate <= 0:
                messagebox.showerror("Error", "Hourly rate must be greater than 0")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employees 
                SET name=?, position=?, hourly_rate=?, hire_date=?, dob=?, address=?, phone=?, email=?, employee_id=?
                WHERE id=?
            """, (name, position, rate, hire_date, dob, address, phone, email, emp_id_field, emp_id))
            conn.commit()
            conn.close()
            
            self.load_employees()
            messagebox.showinfo("Success", "Employee updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {e}")
    
    def delete_employee(self):
        """Delete selected employee"""
        try:
            selection = self.employee_tree.selection()
            if not selection:
                messagebox.showerror("Error", "Please select an employee to delete")
                return
            
            item = self.employee_tree.item(selection[0])
            emp_id = item['values'][0]
            emp_name = item['values'][1]
            
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {emp_name}?\nThis will also delete all associated payroll records."):
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
                conn.commit()
                conn.close()
                
                self.load_employees()
                self.clear_employee_form()
                messagebox.showinfo("Success", "Employee deleted successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete employee: {e}")
    
    def clear_employee_form(self):
        """Clear the employee form"""
        self.name_entry.delete(0, tk.END)
        self.position_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.hire_date_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.emp_id_entry.delete(0, tk.END)
    
    def on_payroll_employee_select(self, event=None):
        """Handle payroll employee selection"""
        selection = self.payroll_employee_var.get()
        if selection:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT hourly_rate FROM employees WHERE name = ?", (selection,))
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    self.payroll_rate_entry.config(state="normal")
                    self.payroll_rate_entry.delete(0, tk.END)
                    self.payroll_rate_entry.insert(0, f"${result[0]:.2f}")
                    self.payroll_rate_entry.config(state="readonly")
                    self.calculate_payroll()
            except Exception as e:
                messagebox.showerror("Error", f"Could not load employee data: {str(e)}")
    
    def calculate_payroll(self, event=None):
        """Calculate payroll for selected employee"""
        try:
            # Get values
            regular_hours = float(self.regular_hours_entry.get() or 0)
            overtime_hours = float(self.overtime_hours_entry.get() or 0)
            bonus = float(self.bonus_entry.get() or 0)
            deductions = float(self.deductions_entry.get() or 0)
            
            # Get hourly rate
            rate_text = self.payroll_rate_entry.get().replace("$", "")
            hourly_rate = float(rate_text) if rate_text else 0
            
            # Calculate gross pay (overtime is 1.5x regular rate)
            regular_pay = regular_hours * hourly_rate
            overtime_pay = overtime_hours * hourly_rate * 1.5
            gross_pay = regular_pay + overtime_pay + bonus
            
            # Get tax rates from settings
            federal_rate = float(self.federal_tax_rate.get()) if hasattr(self, 'federal_tax_rate') else 0.15
            ss_rate = float(self.ss_tax_rate.get()) if hasattr(self, 'ss_tax_rate') else 0.062
            medicare_rate = float(self.medicare_tax_rate.get()) if hasattr(self, 'medicare_tax_rate') else 0.0145
            state_rate = float(self.state_tax_rate.get()) if hasattr(self, 'state_tax_rate') else 0.05
            
            # Calculate taxes
            federal_tax = gross_pay * federal_rate
            ss_tax = gross_pay * ss_rate
            medicare_tax = gross_pay * medicare_rate
            state_tax = gross_pay * state_rate
            total_taxes = federal_tax + ss_tax + medicare_tax + state_tax
            
            # Calculate net pay
            net_pay = gross_pay - total_taxes - deductions
            
            # Update result fields
            results = {
                "gross_pay": f"${gross_pay:.2f}",
                "federal_tax": f"${federal_tax:.2f}",
                "ss_tax": f"${ss_tax:.2f}",
                "medicare_tax": f"${medicare_tax:.2f}",
                "state_tax": f"${state_tax:.2f}",
                "total_taxes": f"${total_taxes:.2f}",
                "net_pay": f"${net_pay:.2f}"
            }
            
            for field, value in results.items():
                entry = self.payroll_result_entries[field]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, value)
                entry.config(state="readonly")
                
        except ValueError:
            # Clear results if invalid input
            for entry in self.payroll_result_entries.values():
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.config(state="readonly")
    
    def save_payroll(self):
        """Save payroll run"""
        if not self.validate_payroll_form():
            return
        
        try:
            # Get employee ID
            employee_name = self.payroll_employee_var.get()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM employees WHERE name = ?", (employee_name,))
            emp_result = cursor.fetchone()
            
            if not emp_result:
                messagebox.showerror("Error", "Employee not found")
                return
            
            emp_id = emp_result[0]
            
            # Get form values
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            regular_hours = float(self.regular_hours_entry.get() or 0)
            overtime_hours = float(self.overtime_hours_entry.get() or 0)
            bonus = float(self.bonus_entry.get() or 0)
            deductions = float(self.deductions_entry.get() or 0)
            
            # Get calculated values
            gross_pay = float(self.payroll_result_entries["gross_pay"].get().replace("$", ""))
            federal_tax = float(self.payroll_result_entries["federal_tax"].get().replace("$", ""))
            ss_tax = float(self.payroll_result_entries["ss_tax"].get().replace("$", ""))
            medicare_tax = float(self.payroll_result_entries["medicare_tax"].get().replace("$", ""))
            state_tax = float(self.payroll_result_entries["state_tax"].get().replace("$", ""))
            total_taxes = float(self.payroll_result_entries["total_taxes"].get().replace("$", ""))
            net_pay = float(self.payroll_result_entries["net_pay"].get().replace("$", ""))
            
            total_hours = regular_hours + overtime_hours
            
            # Create payroll run
            cursor.execute("""
                INSERT INTO payroll_runs (employee_id, run_date, frequency)
                VALUES (?, ?, ?)
            """, (emp_id, end_date, "Custom"))
            
            run_id = cursor.lastrowid
            
            # Create payroll details
            cursor.execute("""
                INSERT INTO payroll_details 
                (payroll_run_id, employee_id, hours_worked, gross_pay, federal_tax, ss_tax, 
                 medicare_tax, ma_state_tax, total_taxes, net_pay, bonus, deductions, 
                 regular_hours, overtime_hours, pay_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (run_id, emp_id, total_hours, gross_pay, federal_tax, ss_tax, medicare_tax, 
                  state_tax, total_taxes, net_pay, bonus, deductions, regular_hours, 
                  overtime_hours, end_date))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Payroll saved successfully!")
            self.clear_payroll_form()
            self.load_payroll_history()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save payroll: {e}")
    
    def validate_payroll_form(self):
        """Validate payroll form"""
        if not self.payroll_employee_var.get():
            messagebox.showerror("Validation Error", "Please select an employee")
            return False
        
        if not self.start_date_entry.get() or not self.end_date_entry.get():
            messagebox.showerror("Validation Error", "Please enter start and end dates")
            return False
        
        # Validate date format
        try:
            datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d")
            datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter dates in YYYY-MM-DD format")
            return False
        
        if not self.regular_hours_entry.get() and not self.overtime_hours_entry.get():
            messagebox.showerror("Validation Error", "Please enter hours worked")
            return False
        
        return True
    
    def clear_payroll_form(self):
        """Clear the payroll form"""
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.regular_hours_entry.delete(0, tk.END)
        self.overtime_hours_entry.delete(0, tk.END)
        self.bonus_entry.delete(0, tk.END)
        self.deductions_entry.delete(0, tk.END)
        
        for entry in self.payroll_result_entries.values():
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.config(state="readonly")
    
    def load_payroll_history(self):
        """Load payroll history for the history tree"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pd.id, e.name, pd.pay_date, pd.hours_worked, pd.gross_pay, pd.net_pay
                FROM payroll_details pd
                JOIN employees e ON pd.employee_id = e.id
                ORDER BY pd.pay_date DESC
                LIMIT 20
            """)
            payroll_data = cursor.fetchall()
            conn.close()
            
            for record in payroll_data:
                self.history_tree.insert("", tk.END, values=(
                    record[1],  # employee name
                    record[2],  # date
                    f"{record[3]:.1f}",  # hours
                    f"${record[4]:.2f}",  # gross pay
                    f"${record[5]:.2f}"  # net pay
                ))
        except Exception as e:
            pass  # Silent error - don't interrupt user experience
    
    def delete_payroll_record(self):
        """Delete selected payroll record"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a payroll record to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this payroll record?"):
            try:
                # Note: This is a simplified implementation
                # In a real app, you'd need to get the record ID and use it
                messagebox.showinfo("Info", "Delete functionality would be implemented here")
                self.load_payroll_history()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {e}")

    # Past payrolls and filtering methods
    def load_all_payrolls(self):
        """Load all payroll records for the past payrolls tab"""
        # Clear existing items
        for item in self.payroll_tree.get_children():
            self.payroll_tree.delete(item)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pd.id, e.name, pd.pay_date, pd.hours_worked, pd.gross_pay, pd.total_taxes, pd.net_pay
                FROM payroll_details pd
                JOIN employees e ON pd.employee_id = e.id
                ORDER BY pd.pay_date DESC
            """)
            payroll_data = cursor.fetchall()
            conn.close()
            
            for record in payroll_data:
                self.payroll_tree.insert("", tk.END, values=(
                    record[0],  # ID
                    record[1],  # Employee name
                    record[2],  # Date
                    f"{record[3]:.1f}",  # Hours
                    f"${record[4]:.2f}",  # Gross pay
                    f"${record[5]:.2f}",  # Total taxes
                    f"${record[6]:.2f}"  # Net pay
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payroll data: {e}")
    
    def apply_payroll_filter(self, event=None):
        """Apply filters to payroll data"""
        start_date = self.filter_start_date.get()
        end_date = self.filter_end_date.get()
        employee_filter = self.filter_employee_var.get()
        
        # Clear existing items
        for item in self.payroll_tree.get_children():
            self.payroll_tree.delete(item)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build query with filters
            query = """
                SELECT pd.id, e.name, pd.pay_date, pd.hours_worked, pd.gross_pay, pd.total_taxes, pd.net_pay
                FROM payroll_details pd
                JOIN employees e ON pd.employee_id = e.id
                WHERE 1=1
            """
            params = []
            
            if start_date:
                query += " AND pd.pay_date >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND pd.pay_date <= ?"
                params.append(end_date)
            
            if employee_filter and employee_filter != "All":
                query += " AND e.name = ?"
                params.append(employee_filter)
            
            query += " ORDER BY pd.pay_date DESC"
            
            cursor.execute(query, params)
            payroll_data = cursor.fetchall()
            conn.close()
            
            for record in payroll_data:
                self.payroll_tree.insert("", tk.END, values=(
                    record[0],  # ID
                    record[1],  # Employee name
                    record[2],  # Date
                    f"{record[3]:.1f}",  # Hours
                    f"${record[4]:.2f}",  # Gross pay
                    f"${record[5]:.2f}",  # Total taxes
                    f"${record[6]:.2f}"  # Net pay
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {e}")
    
    def show_all_payrolls(self):
        """Show all payroll records"""
        self.filter_start_date.delete(0, tk.END)
        self.filter_end_date.delete(0, tk.END)
        self.filter_employee_var.set("All")
        self.load_all_payrolls()
    
    def view_payroll_details(self, event=None):
        """View detailed payroll information"""
        selection = self.payroll_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a payroll record to view")
            return
        
        item = self.payroll_tree.item(selection[0])
        payroll_id = item['values'][0]
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.name, pd.pay_date, pd.regular_hours, pd.overtime_hours, pd.hourly_rate,
                       pd.gross_pay, pd.federal_tax, pd.ss_tax, pd.medicare_tax, pd.ma_state_tax,
                       pd.total_taxes, pd.net_pay, pd.bonus, pd.deductions
                FROM payroll_details pd
                JOIN employees e ON pd.employee_id = e.id
                WHERE pd.id = ?
            """, (payroll_id,))
            record = cursor.fetchone()
            conn.close()
            
            if record:
                details = f"""
Payroll Details for {record[0]}

Pay Date: {record[1]}
Regular Hours: {record[2]:.2f}
Overtime Hours: {record[3]:.2f}
Hourly Rate: ${record[4]:.2f}

Gross Pay: ${record[5]:.2f}
Federal Tax: ${record[6]:.2f}
Social Security: ${record[7]:.2f}
Medicare: ${record[8]:.2f}
State Tax: ${record[9]:.2f}
Total Taxes: ${record[10]:.2f}
Net Pay: ${record[11]:.2f}

Bonus: ${record[12]:.2f}
Deductions: ${record[13]:.2f}
                """
                messagebox.showinfo("Payroll Details", details)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load payroll details: {e}")
    
    def export_payroll_to_excel(self):
        """Export payroll data to Excel"""
        if not OPENPYXL_AVAILABLE:
            messagebox.showwarning("Excel Export Not Available", 
                                 "Excel export requires openpyxl package.\nInstall with: pip install openpyxl")
            return
        
        try:
            # Get all visible items
            items = []
            for item in self.payroll_tree.get_children():
                values = self.payroll_tree.item(item)['values']
                items.append(values)
            
            if not items:
                messagebox.showwarning("No Data", "No payroll records to export")
                return
            
            # Create Excel file
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Payroll History"
            
            # Headers
            headers = ["Run ID", "Employee", "Pay Date", "Hours", "Gross Pay", "Total Taxes", "Net Pay"]
            ws.append(headers)
            
            # Data
            for item in items:
                ws.append(item)
            
            # Save file
            filename = f"payroll_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            wb.save(filename)
            
            messagebox.showinfo("Export Complete", f"Payroll history exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {e}")
    
    def delete_selected_payroll(self):
        """Delete selected payroll record"""
        selection = self.payroll_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a payroll record to delete")
            return
        
        item = self.payroll_tree.item(selection[0])
        run_id = item['values'][0]
        employee_name = item['values'][1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete payroll record for {employee_name} (Run ID: {run_id})?"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM payroll_details WHERE id = ?", (run_id,))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Payroll record deleted successfully!")
                self.load_all_payrolls()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {e}")
    
    # Import functionality
    def import_master_payroll(self):
        """Import Master Payroll CSV file"""
        try:
            # Try to use the local file first
            csv_file = "Master Payroll.csv"
            if not os.path.exists(csv_file):
                csv_file = filedialog.askopenfilename(
                    title="Select Master Payroll CSV File",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
                )
                if not csv_file:
                    return
            
            self.import_status_label.config(text="Reading CSV file...")
            self.root.update()
            
            # Read and parse the CSV
            employees_data = {}
            payroll_data = []
            
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                current_date = None
                
                for row in reader:
                    if len(row) > 0 and row[0].strip():
                        # Check if this is a date row (e.g., "01/12/25")
                        if re.match(r'\d{2}/\d{2}/\d{2}', row[0]):
                            current_date = row[0]
                        # Check if this is a header row
                        elif row[0] == "Employee":
                            continue
                        # Check if this is employee data
                        elif row[0].startswith('"') and len(row) >= 5:
                            # Extract employee name (remove quotes)
                            name = row[0].strip('"')
                            job_title = row[1]
                            regular_hours = float(row[2] or 0)
                            overtime_hours = float(row[3] or 0)
                            hourly_rate = float(row[4] or 0)
                            regular_pay = float(row[5] or 0)
                            overtime_pay = float(row[6] or 0)
                            total_pay = float(row[7] or 0)
                            net_sales = float(row[8] or 0)
                            total_gratuity = float(row[9] or 0)
                            employee_id = row[10] if len(row) > 10 else ""
                            job_code = row[11] if len(row) > 11 else ""
                            location = row[12] if len(row) > 12 else ""
                            
                            # Store employee data
                            if name not in employees_data:
                                employees_data[name] = {
                                    'name': name,
                                    'position': job_title,
                                    'hourly_rate': hourly_rate,
                                    'employee_id': employee_id,
                                    'job_code': job_code,
                                    'location': location
                                }
                            
                            # Store payroll data
                            if current_date and total_pay > 0:
                                payroll_data.append({
                                    'employee_name': name,
                                    'pay_date': current_date,
                                    'regular_hours': regular_hours,
                                    'overtime_hours': overtime_hours,
                                    'hourly_rate': hourly_rate,
                                    'regular_pay': regular_pay,
                                    'overtime_pay': overtime_pay,
                                    'total_pay': total_pay,
                                    'net_sales': net_sales,
                                    'total_gratuity': total_gratuity
                                })
            
            self.import_status_label.config(text=f"Found {len(employees_data)} employees and {len(payroll_data)} payroll records")
            self.root.update()
            
            # Import employees
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            imported_employees = 0
            for employee in employees_data.values():
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO employees (name, position, hourly_rate, employee_id, job_code, location)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (employee['name'], employee['position'], employee['hourly_rate'], 
                          employee['employee_id'], employee['job_code'], employee['location']))
                    imported_employees += 1
                except Exception as e:
                    print(f"Error importing employee {employee['name']}: {e}")
            
            # Import payroll data
            imported_payroll = 0
            for payroll in payroll_data:
                try:
                    # Get employee ID
                    cursor.execute("SELECT id FROM employees WHERE name = ?", (payroll['employee_name'],))
                    emp_result = cursor.fetchone()
                    if emp_result:
                        emp_id = emp_result[0]
                        
                        # Create payroll run
                        cursor.execute("""
                            INSERT OR IGNORE INTO payroll_runs (employee_id, run_date, frequency)
                            VALUES (?, ?, ?)
                        """, (emp_id, payroll['pay_date'], "Imported"))
                        
                        run_id = cursor.lastrowid
                        
                        # Create payroll details
                        cursor.execute("""
                            INSERT OR IGNORE INTO payroll_details 
                            (payroll_run_id, employee_id, hours_worked, gross_pay, total_taxes, net_pay, 
                             regular_hours, overtime_hours, pay_date, net_sales, total_gratuity)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (run_id, emp_id, 
                              payroll['regular_hours'] + payroll['overtime_hours'],
                              payroll['total_pay'], 0, payroll['total_pay'],
                              payroll['regular_hours'], payroll['overtime_hours'],
                              payroll['pay_date'], payroll['net_sales'], payroll['total_gratuity']))
                        imported_payroll += 1
                except Exception as e:
                    print(f"Error importing payroll for {payroll['employee_name']}: {e}")
            
            conn.commit()
            conn.close()
            
            # Update status and reload data
            self.import_status_label.config(text=f"Import complete! {imported_employees} employees, {imported_payroll} payroll records")
            self.load_employees()
            
            messagebox.showinfo("Import Complete", 
                              f"Successfully imported:\n"
                              f"• {imported_employees} employees\n"
                              f"• {imported_payroll} payroll records\n\n"
                              f"Your data is now available in the Employees and Payroll tabs!")
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import CSV file:\n{str(e)}")
            self.import_status_label.config(text="Import failed")
    
    def import_employees_csv(self):
        """Import employees from a simple CSV file"""
        try:
            filename = filedialog.askopenfilename(
                title="Select Employees CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not filename:
                return
            
            self.import_status_label.config(text="Importing employees...")
            self.root.update()
            
            imported_count = 0
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                
                for row in reader:
                    if len(row) >= 3:
                        name = row[0].strip()
                        position = row[1].strip() if len(row) > 1 else ""
                        hourly_rate = float(row[2]) if len(row) > 2 and row[2] else 0
                        employee_id = row[3].strip() if len(row) > 3 else ""
                        phone = row[4].strip() if len(row) > 4 else ""
                        email = row[5].strip() if len(row) > 5 else ""
                        location = row[6].strip() if len(row) > 6 else ""
                        
                        if name and hourly_rate > 0:
                            try:
                                cursor.execute("""
                                    INSERT OR IGNORE INTO employees 
                                    (name, position, hourly_rate, employee_id, phone, email, location)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (name, position, hourly_rate, employee_id, phone, email, location))
                                imported_count += 1
                            except Exception as e:
                                print(f"Error importing employee {name}: {e}")
            
            conn.commit()
            conn.close()
            
            self.import_status_label.config(text=f"Imported {imported_count} employees")
            self.load_employees()
            
            messagebox.showinfo("Import Complete", f"Successfully imported {imported_count} employees!")
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import employees:\n{str(e)}")
            self.import_status_label.config(text="Import failed")
    
    def import_payroll_csv(self):
        """Import payroll records from a simple CSV file"""
        try:
            filename = filedialog.askopenfilename(
                title="Select Payroll CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not filename:
                return
            
            self.import_status_label.config(text="Importing payroll records...")
            self.root.update()
            
            imported_count = 0
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                
                for row in reader:
                    if len(row) >= 5:
                        employee_name = row[0].strip()
                        pay_date = row[1].strip()
                        regular_hours = float(row[2]) if len(row) > 2 and row[2] else 0
                        overtime_hours = float(row[3]) if len(row) > 3 and row[3] else 0
                        hourly_rate = float(row[4]) if len(row) > 4 and row[4] else 0
                        bonus = float(row[5]) if len(row) > 5 and row[5] else 0
                        deductions = float(row[6]) if len(row) > 6 and row[6] else 0
                        net_sales = float(row[7]) if len(row) > 7 and row[7] else 0
                        gratuity = float(row[8]) if len(row) > 8 and row[8] else 0
                        
                        if employee_name and pay_date:
                            try:
                                # Get employee ID
                                cursor.execute("SELECT id FROM employees WHERE name = ?", (employee_name,))
                                emp_result = cursor.fetchone()
                                if emp_result:
                                    emp_id = emp_result[0]
                                    
                                    # Calculate pay amounts
                                    regular_pay = regular_hours * hourly_rate
                                    overtime_pay = overtime_hours * hourly_rate * 1.5
                                    gross_pay = regular_pay + overtime_pay + bonus - deductions
                                    
                                    # Create payroll run
                                    cursor.execute("""
                                        INSERT INTO payroll_runs 
                                        (employee_id, employee_name, pay_date, regular_hours, overtime_hours, 
                                         hourly_rate, regular_pay, overtime_pay, bonus, deductions, 
                                         gross_pay, net_sales, total_gratuity)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    """, (emp_id, employee_name, pay_date, regular_hours, overtime_hours,
                                          hourly_rate, regular_pay, overtime_pay, bonus, deductions,
                                          gross_pay, net_sales, gratuity))
                                    imported_count += 1
                            except Exception as e:
                                print(f"Error importing payroll for {employee_name}: {e}")
            
            conn.commit()
            conn.close()
            
            self.import_status_label.config(text=f"Imported {imported_count} payroll records")
            self.load_payroll_history()
            
            messagebox.showinfo("Import Complete", f"Successfully imported {imported_count} payroll records!")
            
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import payroll records:\n{str(e)}")
            self.import_status_label.config(text="Import failed")
    
    def quick_add_employees(self):
        """Quickly add multiple employees from text input"""
        try:
            text_content = self.quick_add_text.get(1.0, tk.END).strip()
            if not text_content:
                messagebox.showwarning("Warning", "Please enter employee data first.")
                return
            
            lines = text_content.split('\n')
            imported_count = 0
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for line in lines:
                line = line.strip()
                if line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        name = parts[0].strip()
                        position = parts[1].strip()
                        hourly_rate = float(parts[2]) if parts[2] else 0
                        employee_id = parts[3].strip() if len(parts) > 3 else ""
                        
                        if name and hourly_rate > 0:
                            try:
                                cursor.execute("""
                                    INSERT OR IGNORE INTO employees 
                                    (name, position, hourly_rate, employee_id)
                                    VALUES (?, ?, ?, ?)
                                """, (name, position, hourly_rate, employee_id))
                                imported_count += 1
                            except Exception as e:
                                print(f"Error adding employee {name}: {e}")
            
            conn.commit()
            conn.close()
            
            self.import_status_label.config(text=f"Quick added {imported_count} employees")
            self.load_employees()
            
            # Clear the text area
            self.quick_add_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Quick Add Complete", f"Successfully added {imported_count} employees!")
            
        except Exception as e:
            messagebox.showerror("Quick Add Error", f"Failed to add employees:\n{str(e)}")
    
    def bulk_add_payroll(self):
        """Quickly add multiple payroll entries from text input"""
        try:
            text_content = self.bulk_payroll_text.get(1.0, tk.END).strip()
            if not text_content:
                messagebox.showwarning("Warning", "Please enter payroll data first.")
                return
            
            lines = text_content.split('\n')
            imported_count = 0
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for line in lines:
                line = line.strip()
                if line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 4:
                        employee_name = parts[0].strip()
                        pay_date = parts[1].strip()
                        regular_hours = float(parts[2]) if parts[2] else 0
                        overtime_hours = float(parts[3]) if len(parts) > 3 and parts[3] else 0
                        bonus = float(parts[4]) if len(parts) > 4 and parts[4] else 0
                        deductions = float(parts[5]) if len(parts) > 5 and parts[5] else 0
                        
                        if employee_name and pay_date:
                            try:
                                # Get employee ID and hourly rate
                                cursor.execute("SELECT id, hourly_rate FROM employees WHERE name = ?", (employee_name,))
                                emp_result = cursor.fetchone()
                                if emp_result:
                                    emp_id, hourly_rate = emp_result
                                    
                                    # Calculate pay amounts
                                    regular_pay = regular_hours * hourly_rate
                                    overtime_pay = overtime_hours * hourly_rate * 1.5
                                    gross_pay = regular_pay + overtime_pay + bonus - deductions
                                    
                                    # Create payroll run
                                    cursor.execute("""
                                        INSERT INTO payroll_runs 
                                        (employee_id, employee_name, pay_date, regular_hours, overtime_hours, 
                                         hourly_rate, regular_pay, overtime_pay, bonus, deductions, 
                                         gross_pay, net_pay)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    """, (emp_id, employee_name, pay_date, regular_hours, overtime_hours,
                                          hourly_rate, regular_pay, overtime_pay, bonus, deductions,
                                          gross_pay, gross_pay))  # net_pay = gross_pay for now
                                    imported_count += 1
                                else:
                                    print(f"Employee not found: {employee_name}")
                            except Exception as e:
                                print(f"Error adding payroll for {employee_name}: {e}")
            
            conn.commit()
            conn.close()
            
            self.import_status_label.config(text=f"Quick added {imported_count} payroll entries")
            self.load_payroll_history()
            
            # Clear the text area
            self.bulk_payroll_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Bulk Payroll Complete", f"Successfully added {imported_count} payroll entries!")
            
        except Exception as e:
            messagebox.showerror("Bulk Payroll Error", f"Failed to add payroll entries:\n{str(e)}")
    
    # Export and report methods
    def export_employees(self):
        """Export employee list to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT name, position, hourly_rate, hire_date, phone, email, employee_id 
                    FROM employees ORDER BY name
                """)
                employees = cursor.fetchall()
                conn.close()
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Name', 'Position', 'Hourly Rate', 'Hire Date', 'Phone', 'Email', 'Employee ID'])
                    writer.writerows(employees)
                
                messagebox.showinfo("Success", f"Employee list exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export employees: {e}")
    
    def export_payroll_history(self):
        """Export payroll history to CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT e.name, e.position, pd.pay_date, pd.regular_hours, pd.overtime_hours, 
                           pd.hourly_rate, pd.gross_pay, pd.total_taxes, pd.net_pay
                    FROM payroll_details pd
                    JOIN employees e ON pd.employee_id = e.id
                    ORDER BY e.name, pd.pay_date
                """)
                payroll_data = cursor.fetchall()
                conn.close()
                
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Employee', 'Position', 'Pay Date', 'Regular Hours', 'Overtime Hours', 
                                   'Hourly Rate', 'Gross Pay', 'Total Taxes', 'Net Pay'])
                    writer.writerows(payroll_data)
                
                messagebox.showinfo("Success", f"Payroll history exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export payroll history: {e}")
    
    def generate_payroll_report(self):
        """Generate comprehensive payroll report"""
        try:
            start_date = self.report_start_date.get()
            end_date = self.report_end_date.get()
            
            if not start_date or not end_date:
                messagebox.showerror("Error", "Please enter start and end dates for the report")
                return
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.name, e.position, pd.pay_date, pd.hours_worked, pd.gross_pay, 
                       pd.total_taxes, pd.net_pay, pd.bonus, pd.deductions
                FROM payroll_details pd
                JOIN employees e ON pd.employee_id = e.id
                WHERE pd.pay_date BETWEEN ? AND ?
                ORDER BY e.name, pd.pay_date
            """, (start_date, end_date))
            data = cursor.fetchall()
            conn.close()
            
            if not data:
                messagebox.showinfo("No Data", "No payroll data found for the specified period")
                return
            
            # Calculate totals
            total_gross = sum(row[4] for row in data)
            total_taxes = sum(row[5] for row in data)
            total_net = sum(row[6] for row in data)
            total_bonus = sum(row[7] for row in data)
            total_deductions = sum(row[8] for row in data)
            
            # Create report
            report = f"""
PAYROLL REPORT
Period: {start_date} to {end_date}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY:
Total Gross Pay: ${total_gross:.2f}
Total Taxes: ${total_taxes:.2f}
Total Net Pay: ${total_net:.2f}
Total Bonuses: ${total_bonus:.2f}
Total Deductions: ${total_deductions:.2f}

DETAILED BREAKDOWN:
"""
            
            current_employee = None
            for row in data:
                if row[0] != current_employee:
                    current_employee = row[0]
                    report += f"\n{current_employee} ({row[1]}):\n"
                
                report += f"  {row[2]}: {row[3]:.1f} hrs, Gross: ${row[4]:.2f}, Net: ${row[6]:.2f}\n"
            
            # Show report
            self.show_report_window("Payroll Report", report)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def generate_employee_report(self):
        """Generate employee summary report"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.name, e.position, e.hourly_rate, e.hire_date,
                       COUNT(pd.id) as payroll_count,
                       SUM(pd.hours_worked) as total_hours,
                       SUM(pd.gross_pay) as total_gross,
                       SUM(pd.net_pay) as total_net
                FROM employees e
                LEFT JOIN payroll_details pd ON e.id = pd.employee_id
                GROUP BY e.id, e.name, e.position, e.hourly_rate, e.hire_date
                ORDER BY e.name
            """)
            data = cursor.fetchall()
            conn.close()
            
            if not data:
                messagebox.showinfo("No Data", "No employee data found")
                return
            
            # Create report
            report = f"""
EMPLOYEE SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EMPLOYEE DETAILS:
"""
            
            total_employees = len(data)
            total_payroll_runs = sum(row[4] for row in data)
            total_hours = sum(row[5] or 0 for row in data)
            total_gross = sum(row[6] or 0 for row in data)
            total_net = sum(row[7] or 0 for row in data)
            
            for row in data:
                report += f"""
{row[0]} ({row[1]})
  Hourly Rate: ${row[2]:.2f}
  Hire Date: {row[3] or 'Not specified'}
  Payroll Runs: {row[4]}
  Total Hours: {row[5] or 0:.1f}
  Total Gross: ${row[6] or 0:.2f}
  Total Net: ${row[7] or 0:.2f}
"""
            
            report += f"""

SUMMARY:
Total Employees: {total_employees}
Total Payroll Runs: {total_payroll_runs}
Total Hours Worked: {total_hours:.1f}
Total Gross Pay: ${total_gross:.2f}
Total Net Pay: ${total_net:.2f}
"""
            
            # Show report
            self.show_report_window("Employee Report", report)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def show_report_window(self, title, content):
        """Show report in a new window"""
        report_window = tk.Toplevel(self.root)
        report_window.title(title)
        report_window.geometry("600x500")
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(report_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert content
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        
        # Add close button
        ttk.Button(report_window, text="Close", command=report_window.destroy).pack(pady=10)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = EnhancedPayrollApp()
        app.run()
    except Exception as e:
        # Show error in a simple window
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Application Error", f"Failed to start application:\n{e}")
        root.destroy()

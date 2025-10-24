#!/usr/bin/env python3
"""
Simple test version of the payroll app to diagnose loading issues
"""

import tkinter as tk
from tkinter import messagebox
import os
import sys

def test_dependencies():
    """Test if all required dependencies are available"""
    results = []
    
    # Test tkinter
    try:
        import tkinter
        results.append("✅ tkinter - OK")
    except ImportError as e:
        results.append(f"❌ tkinter - FAILED: {e}")
    
    # Test openpyxl
    try:
        import openpyxl
        results.append("✅ openpyxl - OK")
    except ImportError as e:
        results.append(f"❌ openpyxl - FAILED: {e}")
    
    # Test tkcalendar
    try:
        from tkcalendar import Calendar
        results.append("✅ tkcalendar - OK")
    except ImportError as e:
        results.append(f"❌ tkcalendar - FAILED: {e}")
    
    # Test sqlite3
    try:
        import sqlite3
        results.append("✅ sqlite3 - OK")
    except ImportError as e:
        results.append(f"❌ sqlite3 - FAILED: {e}")
    
    return results

def test_file_access():
    """Test file and directory access"""
    results = []
    
    # Test current directory
    try:
        current_dir = os.getcwd()
        results.append(f"✅ Current directory: {current_dir}")
    except Exception as e:
        results.append(f"❌ Current directory access failed: {e}")
    
    # Test profiles directory
    profiles_dir = "profiles"
    if os.path.exists(profiles_dir):
        results.append(f"✅ Profiles directory exists: {profiles_dir}")
    else:
        try:
            os.makedirs(profiles_dir)
            results.append(f"✅ Created profiles directory: {profiles_dir}")
        except Exception as e:
            results.append(f"❌ Failed to create profiles directory: {e}")
    
    # Test write permissions
    try:
        test_file = os.path.join(profiles_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        results.append("✅ Write permissions - OK")
    except Exception as e:
        results.append(f"❌ Write permissions failed: {e}")
    
    return results

def show_diagnostic_window():
    """Show diagnostic information in a window"""
    root = tk.Tk()
    root.title("Payroll App Diagnostic")
    root.geometry("600x400")
    
    # Create text widget
    text_widget = tk.Text(root, wrap=tk.WORD, padx=10, pady=10)
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    # Add scrollbar
    scrollbar = tk.Scrollbar(root, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)
    
    # Add diagnostic information
    text_widget.insert(tk.END, "=== PAYROLL APP DIAGNOSTIC ===\n\n")
    
    # System info
    text_widget.insert(tk.END, "SYSTEM INFORMATION:\n")
    text_widget.insert(tk.END, f"Python version: {sys.version}\n")
    text_widget.insert(tk.END, f"Platform: {sys.platform}\n")
    text_widget.insert(tk.END, f"Executable: {sys.executable}\n\n")
    
    # Dependencies
    text_widget.insert(tk.END, "DEPENDENCIES:\n")
    for result in test_dependencies():
        text_widget.insert(tk.END, f"{result}\n")
    text_widget.insert(tk.END, "\n")
    
    # File access
    text_widget.insert(tk.END, "FILE ACCESS:\n")
    for result in test_file_access():
        text_widget.insert(tk.END, f"{result}\n")
    text_widget.insert(tk.END, "\n")
    
    # Try to import main app
    text_widget.insert(tk.END, "MAIN APP IMPORT:\n")
    try:
        import payroll_gui_advanced
        text_widget.insert(tk.END, "✅ Main app imports successfully\n")
    except Exception as e:
        text_widget.insert(tk.END, f"❌ Main app import failed: {e}\n")
    
    # Make text read-only
    text_widget.config(state=tk.DISABLED)
    
    # Add close button
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    show_diagnostic_window()

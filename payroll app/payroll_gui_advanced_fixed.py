import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import os
import csv
from datetime import datetime
import payroll_db
import atexit
import time
import sys

# Add this import at the top
try:
    from tkcalendar import Calendar
    TKCALENDAR_AVAILABLE = True
except ImportError:
    TKCALENDAR_AVAILABLE = False
    Calendar = None # Ensure Calendar is None if import fails

# Fix for executable path issues
def get_app_directory():
    """Get the directory where the application is running from"""
    if getattr(sys, 'frozen', False):
        # Running as executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

# Set up profile directory relative to executable location
APP_DIR = get_app_directory()
PROFILE_DIR = os.path.join(APP_DIR, 'profiles')

# Ensure profiles directory exists
if not os.path.exists(PROFILE_DIR):
    try:
        os.makedirs(PROFILE_DIR)
        print(f"Created profiles directory: {PROFILE_DIR}")
    except Exception as e:
        print(f"Error creating profiles directory: {e}")
        # Fallback to current directory
        PROFILE_DIR = 'profiles'
        if not os.path.exists(PROFILE_DIR):
            os.makedirs(PROFILE_DIR)

def select_user_profile():
    """Prompt the user to select or create a profile. Returns the profile name and db path."""
    try:
        root = tk.Tk()
        root.withdraw() # Hide the main Tkinter window

        # Create profile selection dialog
        dialog = tk.Toplevel(root)
        dialog.title("Select Profile")
        dialog.geometry("400x200")
        dialog.transient(root)
        dialog.grab_set()
        dialog.resizable(False, False)

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")

        profile_name_var = tk.StringVar()
        db_path_var = tk.StringVar()
        selected_profile = {"name": None, "db_path": None}

        def on_select():
            try:
                profile_name = profile_listbox.get(profile_listbox.curselection())
                selected_profile["name"] = profile_name
                selected_profile["db_path"] = os.path.join(PROFILE_DIR, f"{profile_name}.db")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to select profile: {e}")

        def on_create():
            try:
                new_profile_name = simpledialog.askstring("Create Profile", "Enter new profile name:")
                if new_profile_name:
                    # Basic validation
                    if not new_profile_name.strip():
                        messagebox.showerror("Error", "Profile name cannot be empty.")
                        return
                    if any(char in r'/\:*?"<>|' for char in new_profile_name):
                        messagebox.showerror("Error", "Profile name contains invalid characters.")
                        return
                    
                    # Check if profile already exists
                    existing_profiles = []
                    if os.path.exists(PROFILE_DIR):
                        existing_profiles = [f.replace('.db', '') for f in os.listdir(PROFILE_DIR) if f.endswith('.db')]
                    
                    if new_profile_name in existing_profiles:
                        messagebox.showerror("Error", "Profile name already exists.")
                        return

                    selected_profile["name"] = new_profile_name
                    selected_profile["db_path"] = os.path.join(PROFILE_DIR, f"{new_profile_name}.db")
                    # Initialize a new database for the profile
                    payroll_db.set_db_name(selected_profile["db_path"])
                    payroll_db.create_tables()
                    dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create profile: {e}")

        def on_cancel():
            selected_profile["name"] = None
            selected_profile["db_path"] = None
            dialog.destroy()

        tk.Label(dialog, text="Select an existing profile or create a new one:").pack(pady=10)

        profile_listbox = tk.Listbox(dialog, height=5)
        profile_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Populate listbox with existing profiles
        existing_profiles = []
        if os.path.exists(PROFILE_DIR):
            existing_profiles = [f.replace('.db', '') for f in os.listdir(PROFILE_DIR) if f.endswith('.db')]
        
        for profile in existing_profiles:
            profile_listbox.insert(tk.END, profile)

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Select", command=on_select, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Create New", command=on_create, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=on_cancel, width=10).pack(side=tk.LEFT, padx=5)

        root.wait_window(dialog) # Wait for the dialog to close

        if selected_profile["name"] is None:
            # User cancelled or closed the dialog
            return None, None
        return selected_profile["name"], selected_profile["db_path"]
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to show profile selection: {e}")
        return None, None

# Copy the rest of the original file here
# For now, let's create a simple test version

class SimplePayrollApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Professional Payroll System - Test")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Professional Payroll System", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Status
        status_label = tk.Label(main_frame, text="✅ Application loaded successfully!", 
                               font=("Arial", 12), fg="green")
        status_label.pack(pady=(0, 20))
        
        # Profile info
        profile_info = tk.Label(main_frame, text=f"Profile Directory: {PROFILE_DIR}", 
                               font=("Arial", 10))
        profile_info.pack(pady=(0, 20))
        
        # Test buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Test Profile Selection", 
                 command=self.test_profile_selection).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Exit", 
                 command=self.root.destroy).pack(side=tk.LEFT, padx=5)
    
    def test_profile_selection(self):
        profile_name, db_path = select_user_profile()
        if profile_name:
            messagebox.showinfo("Success", f"Selected profile: {profile_name}\nDatabase: {db_path}")
        else:
            messagebox.showinfo("Info", "No profile selected or cancelled")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = SimplePayrollApp()
        app.run()
    except Exception as e:
        # Show error in a simple window
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Application Error", f"Failed to start application:\n{e}")
        root.destroy()

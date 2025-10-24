import os
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, MULTIPLE

RECIPE_DIR = os.path.join(os.path.dirname(__file__), 'recipe_library')
CONVERT_SCRIPT = os.path.join(os.path.dirname(__file__), 'convert_to_excel.py')

class RecipeDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Recipe Library Dashboard')
        self.geometry('400x300')
        tk.Button(self, text='Search Recipes', command=self.search_recipes, height=2, width=30).pack(pady=10)
        tk.Button(self, text='Merge Recipes into a Folder', command=self.merge_recipes, height=2, width=30).pack(pady=10)
        tk.Button(self, text='Convert Recipes', command=self.convert_recipes, height=2, width=30).pack(pady=10)

    def search_recipes(self):
        # Simple search by filename
        search_term = simpledialog.askstring('Search Recipes', 'Enter search term (filename):')
        if not search_term:
            return
        matches = [f for f in os.listdir(RECIPE_DIR) if search_term.lower() in f.lower()]
        if not matches:
            messagebox.showinfo('No Results', 'No recipes found.')
            return
        result = '\n'.join(matches)
        messagebox.showinfo('Search Results', result)

    def merge_recipes(self):
        # Select recipes
        files = os.listdir(RECIPE_DIR)
        select_win = tk.Toplevel(self)
        select_win.title('Select Recipes to Merge')
        lb = Listbox(select_win, selectmode=MULTIPLE, width=60)
        lb.pack(padx=10, pady=10)
        for f in files:
            lb.insert(tk.END, f)
        def do_merge():
            selected = [files[i] for i in lb.curselection()]
            if not selected:
                messagebox.showwarning('No Selection', 'No recipes selected.')
                return
            dest = filedialog.askdirectory(title='Select Destination Folder')
            if not dest:
                return
            for fname in selected:
                shutil.copy(os.path.join(RECIPE_DIR, fname), os.path.join(dest, fname))
            messagebox.showinfo('Done', f'Merged {len(selected)} recipes to {dest}')
            select_win.destroy()
        tk.Button(select_win, text='Merge Selected', command=do_merge).pack(pady=5)

    def convert_recipes(self):
        # Run the conversion script
        try:
            subprocess.run(['python', CONVERT_SCRIPT], check=True)
            messagebox.showinfo('Done', 'All recipes converted!')
        except Exception as e:
            messagebox.showerror('Error', f'Conversion failed: {e}')

if __name__ == '__main__':
    app = RecipeDashboard()
    app.mainloop() 
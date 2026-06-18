import tkinter as tk
from tkinter import ttk
from .generator import GeneratorTab
from .checker import CheckerTab
from .vault import VaultTab


# Dark theme colors
THEME = {
    'bg': '#1a1a1a',
    'bg_light': '#2a2a2a',
    'fg': '#b0b0b0',
    'accent': '#4a90d9',
    'success': '#6b9b6b',
    'warning': '#c9a84c',
    'error': '#c94c4c',
    'border': '#353535',
}


class PasswordManagerApp:
    """Main application window."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.geometry("600x700")
        self.root.minsize(500, 500)
        self._apply_theme()
        self._create_widgets()

    def _apply_theme(self):
        """Apply dark theme to the application."""
        self.root.configure(bg=THEME['bg'])

        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure('TFrame', background=THEME['bg'])
        style.configure('TLabel', background=THEME['bg'], foreground=THEME['fg'])
        style.configure('TButton', background=THEME['border'], foreground=THEME['fg'])
        style.configure('TCheckbutton', background=THEME['bg'], foreground=THEME['fg'])
        style.configure('TLabelframe', background=THEME['bg'], foreground=THEME['fg'])
        style.configure('TLabelframe.Label', background=THEME['bg'], foreground=THEME['fg'])
        style.configure('Treeview', background=THEME['bg_light'], foreground=THEME['fg'],
                        fieldbackground=THEME['bg_light'], borderwidth=0)
        style.configure('Treeview.Heading', background=THEME['border'], foreground=THEME['fg'])
        style.map('Treeview', background=[('selected', '#3a3a3a')],
                  foreground=[('selected', THEME['fg'])])

        # Entry style - no visible border
        style.configure('TEntry', fieldbackground=THEME['bg_light'], foreground=THEME['fg'],
                        borderwidth=0, relief='flat', insertcolor=THEME['fg'])

        # Notebook (tabs) style
        style.configure('TNotebook', background=THEME['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=THEME['bg_light'], foreground=THEME['fg'],
                        padding=[15, 5])
        style.map('TNotebook.Tab',
                  background=[('selected', '#3a3a3a')],
                  foreground=[('selected', THEME['fg'])])

        # Scale (slider) style
        style.configure('TScale', background=THEME['bg'], troughcolor=THEME['border'])

    def _create_widgets(self):
        """Create the main notebook with tabs."""
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.generator_tab = GeneratorTab(self.notebook, THEME)
        self.checker_tab = CheckerTab(self.notebook, THEME)
        self.vault_tab = VaultTab(self.notebook, THEME)

        # Add tabs to notebook
        self.notebook.add(self.generator_tab, text="Generator")
        self.notebook.add(self.checker_tab, text="Checker")
        self.notebook.add(self.vault_tab, text="Vault")

        # Bind tab change event to lock vault
        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def _on_tab_changed(self, event):
        """Lock vault when switching to another tab."""
        selected_tab = self.notebook.index(self.notebook.select())
        vault_tab_index = 2  # Vault is the 3rd tab (index 2)
        if selected_tab != vault_tab_index:
            self.vault_tab.lock_vault()

    def run(self):
        """Start the application."""
        self.root.mainloop()

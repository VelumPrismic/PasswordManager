import tkinter as tk
from tkinter import ttk
from .generator import GeneratorTab
from .checker import CheckerTab
from .vault import VaultTab


THEME = {
    'bg': '#1e2025',
    'bg_light': '#282c34',
    'bg_card': '#2e3440',
    'fg': '#c8ccd4',
    'fg_dim': '#7a8094',
    'accent': '#5294e2',
    'accent_hover': '#6baaf5',
    'success': '#5a9e6f',
    'warning': '#d4a44c',
    'error': '#bf6060',
    'border': '#3a3f4b',
    'border_light': '#454c5c',
    'selected': '#3b4252',
}


class PasswordManagerApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Manager")
        self.root.geometry("600x700")
        self.root.minsize(500, 500)
        self._apply_theme()
        self._create_widgets()

    def _apply_theme(self):
        self.root.configure(bg=THEME['bg'])

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=THEME['bg'])
        style.configure('TLabel', background=THEME['bg'], foreground=THEME['fg'],
                        font=('Segoe UI', 10))
        style.configure('TButton',
                        background=THEME['bg_card'],
                        foreground=THEME['fg'],
                        borderwidth=1,
                        relief='flat',
                        padding=[10, 5],
                        font=('Segoe UI', 9))
        style.map('TButton',
                  background=[('active', THEME['border_light']), ('pressed', THEME['selected'])],
                  foreground=[('active', '#ffffff')])
        style.configure('Accent.TButton',
                        background=THEME['accent'],
                        foreground='#ffffff',
                        borderwidth=0,
                        relief='flat',
                        padding=[12, 6],
                        font=('Segoe UI', 9, 'bold'))
        style.map('Accent.TButton',
                  background=[('active', THEME['accent_hover']), ('pressed', '#4080cc')],
                  foreground=[('active', '#ffffff')])
        style.configure('TCheckbutton', background=THEME['bg'], foreground=THEME['fg'],
                        font=('Segoe UI', 10))
        style.map('TCheckbutton', background=[('active', THEME['bg'])])
        style.configure('TLabelframe', background=THEME['bg'],
                        bordercolor=THEME['border'], relief='flat', borderwidth=1)
        style.configure('TLabelframe.Label', background=THEME['bg'],
                        foreground=THEME['fg_dim'], font=('Segoe UI', 9))
        style.configure('Treeview',
                        background=THEME['bg_card'],
                        foreground=THEME['fg'],
                        fieldbackground=THEME['bg_card'],
                        borderwidth=0,
                        rowheight=28,
                        font=('Segoe UI', 10))
        style.configure('Treeview.Heading',
                        background=THEME['bg_light'],
                        foreground=THEME['fg_dim'],
                        borderwidth=0,
                        relief='flat',
                        font=('Segoe UI', 9, 'bold'))
        style.map('Treeview',
                  background=[('selected', THEME['selected'])],
                  foreground=[('selected', '#ffffff')])
        style.map('Treeview.Heading',
                  background=[('active', THEME['border'])])
        style.configure('TEntry',
                        fieldbackground=THEME['bg_card'],
                        foreground=THEME['fg'],
                        borderwidth=1,
                        relief='flat',
                        insertcolor=THEME['fg'],
                        padding=[6, 4],
                        font=('Segoe UI', 10))
        style.map('TEntry',
                  fieldbackground=[('focus', THEME['bg_card'])],
                  bordercolor=[('focus', THEME['accent'])])
        style.configure('TNotebook',
                        background=THEME['bg'],
                        borderwidth=0,
                        tabmargins=[0, 0, 0, 0])
        style.configure('TNotebook.Tab',
                        background=THEME['bg_light'],
                        foreground=THEME['fg_dim'],
                        padding=[18, 8],
                        font=('Segoe UI', 10),
                        borderwidth=0)
        style.map('TNotebook.Tab',
                  background=[('selected', THEME['bg']), ('active', THEME['bg_card'])],
                  foreground=[('selected', THEME['accent']), ('active', THEME['fg'])])
        style.configure('TScale',
                        background=THEME['bg'],
                        troughcolor=THEME['border'],
                        sliderrelief='flat')
        style.configure('TScrollbar',
                        background=THEME['bg_light'],
                        troughcolor=THEME['bg'],
                        borderwidth=0,
                        arrowcolor=THEME['fg_dim'],
                        relief='flat')
        style.map('TScrollbar',
                  background=[('active', THEME['border_light'])])

    def _create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.generator_tab = GeneratorTab(self.notebook, THEME)
        self.checker_tab = CheckerTab(self.notebook, THEME)
        self.vault_tab = VaultTab(self.notebook, THEME)

        self.notebook.add(self.generator_tab, text="Generator")
        self.notebook.add(self.checker_tab, text="Checker")
        self.notebook.add(self.vault_tab, text="Vault")

        self.notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def _on_tab_changed(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        vault_tab_index = 2
        if selected_tab != vault_tab_index:
            self.vault_tab.lock_vault()

    def run(self):
        self.root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from ..core.storage import PasswordStorage
from ..core.generator import PasswordGenerator


class VaultTab(ttk.Frame):
    """Password Vault tab UI."""

    AUTO_LOCK_TIMEOUT = 5 * 60 * 1000  # 5 minutes in milliseconds

    def __init__(self, parent, theme_colors: dict):
        super().__init__(parent)
        self.theme = theme_colors
        self.storage = PasswordStorage()
        self.generator = PasswordGenerator()
        self.unlocked = False
        self._lock_timer = None
        self._create_widgets()
        self._show_login()
        self._bind_activity_events()

    def _create_widgets(self):
        # Login frame
        self.login_frame = ttk.Frame(self)
        self._create_login_widgets()

        # Vault frame (hidden initially)
        self.vault_frame = ttk.Frame(self)
        self._create_vault_widgets()

    def _bind_activity_events(self):
        """Bind events that reset the auto-lock timer."""
        for event_type in ['<Motion>', '<KeyPress>', '<ButtonRelease>']:
            self.bind(event_type, self._reset_lock_timer)
        self.vault_frame.bind('<Motion>', self._reset_lock_timer)

    def _reset_lock_timer(self, event=None):
        """Reset the auto-lock timer."""
        if self._lock_timer is not None:
            self.after_cancel(self._lock_timer)
        if self.unlocked:
            self._lock_timer = self.after(self.AUTO_LOCK_TIMEOUT, self._auto_lock)

    def _auto_lock(self):
        """Auto-lock the vault after timeout."""
        if self.unlocked:
            self._lock()
            messagebox.showinfo("Auto-Locked", "Vault locked due to inactivity.")

    def _create_login_widgets(self):
        # Title
        title = ttk.Label(self.login_frame, text="Password Vault", font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(40, 20))

        if not self.storage.is_setup():
            # Setup new master password
            ttk.Label(self.login_frame, text="Create Master Password", font=('Segoe UI', 11)).pack(pady=(0, 10))
            ttk.Label(self.login_frame, text="(This will be used to unlock your vault)").pack(pady=(0, 20))
        else:
            ttk.Label(self.login_frame, text="Enter Master Password", font=('Segoe UI', 11)).pack(pady=20)

        # Password input
        input_frame = ttk.Frame(self.login_frame)
        input_frame.pack(pady=5)

        ttk.Label(input_frame, text="Password:").pack(anchor='w')
        self.master_password_var = tk.StringVar()
        self.master_entry = ttk.Entry(input_frame, textvariable=self.master_password_var, show='*', width=30)
        self.master_entry.pack()
        self.master_entry.bind('<Return>', lambda e: self._unlock())

        # Confirm password (only for setup)
        self.confirm_frame = ttk.Frame(self.login_frame)
        self.confirm_var = tk.StringVar()

        if not self.storage.is_setup():
            self.confirm_frame.pack(pady=5)
            ttk.Label(self.confirm_frame, text="Confirm Password:").pack(anchor='w')
            self.confirm_entry = ttk.Entry(self.confirm_frame, textvariable=self.confirm_var, show='*', width=30)
            self.confirm_entry.pack()

        # Login button
        btn_text = "Create Vault" if not self.storage.is_setup() else "Unlock"
        ttk.Button(self.login_frame, text=btn_text, command=self._unlock).pack(pady=20)

    def _create_vault_widgets(self):
        # Header
        header_frame = ttk.Frame(self.vault_frame)
        header_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(header_frame, text="Your Passwords", font=('Segoe UI', 14, 'bold')).pack(side='left')

        ttk.Button(header_frame, text="Lock", command=self._lock).pack(side='right')

        # Search frame
        search_frame = ttk.Frame(self.vault_frame)
        search_frame.pack(fill='x', padx=10, pady=(0, 10))

        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self._on_search)
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)

        # Add button
        ttk.Button(search_frame, text="+ Add New", command=self._show_add_dialog).pack(side='right')

        # Entries list
        list_frame = ttk.Frame(self.vault_frame)
        list_frame.pack(fill='both', expand=True, padx=10)

        # Treeview
        columns = ('site', 'label', 'username')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('site', text='Site')
        self.tree.heading('label', text='Label')
        self.tree.heading('username', text='Username')
        self.tree.column('site', width=150)
        self.tree.column('label', width=100)
        self.tree.column('username', width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        # Action buttons
        action_frame = ttk.Frame(self.vault_frame)
        action_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(action_frame, text="Copy Password", command=self._copy_password).pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="Edit", command=self._show_edit_dialog).pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="Delete", command=self._delete_entry).pack(side='left')

        # Status bar
        self.status_var = tk.StringVar(value="")
        ttk.Label(self.vault_frame, textvariable=self.status_var).pack(pady=5)

    def _show_login(self):
        self.vault_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
        self.master_entry.focus()

    def _show_vault(self):
        self.login_frame.pack_forget()
        self.vault_frame.pack(fill='both', expand=True)
        self._refresh_list()

    def _unlock(self):
        password = self.master_password_var.get()

        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return

        if not self.storage.is_setup():
            # First time setup
            if password != self.confirm_var.get():
                messagebox.showerror("Error", "Passwords do not match")
                return

            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return

            self.storage.setup_master(password)
            self.unlocked = True
            self._show_vault()
            self._reset_lock_timer()
            messagebox.showinfo("Success", "Vault created successfully!")
        else:
            # Unlock existing vault
            if self.storage.unlock(password):
                self.unlocked = True
                self._show_vault()
                self._reset_lock_timer()
            else:
                messagebox.showerror("Error", "Incorrect password")

    def _lock(self):
        self.unlocked = False
        self.master_password_var.set('')
        self.confirm_var.set('')
        if self._lock_timer is not None:
            self.after_cancel(self._lock_timer)
            self._lock_timer = None
        self._show_login()

    def lock_vault(self):
        """Public method to lock the vault (called when switching tabs)."""
        if self.unlocked:
            self._lock()

    def _refresh_list(self, entries=None):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if entries is None:
            entries = self.storage.get_all_entries()

        for entry in entries:
            self.tree.insert('', 'end', values=(entry['site'], entry.get('label', ''), entry['username']))

        self.status_var.set(f"{len(entries)} password(s) stored")

    def _on_search(self, *args):
        query = self.search_var.get()
        if query:
            entries = self.storage.search_entries(query)
        else:
            entries = self.storage.get_all_entries()
        self._refresh_list(entries)

    def _on_select(self, event):
        # Could show details here if needed
        pass

    def _get_selected_entry(self):
        selection = self.tree.selection()
        if not selection:
            return None

        item = self.tree.item(selection[0])
        site, label, username = item['values']

        # Find full entry
        for entry in self.storage.get_all_entries():
            if entry['site'] == site and entry['username'] == username:
                return entry
        return None

    def _copy_password(self):
        entry = self._get_selected_entry()
        if entry:
            pyperclip.copy(entry['password'])
            self.status_var.set(f"Copied password for {entry['site']}")
        else:
            messagebox.showwarning("Warning", "Please select an entry")

    def _show_add_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Password")
        dialog.geometry("420x260")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(bg='#1a1a1a')

        # Center dialog on parent window
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 420) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 260) // 2
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Site:", font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        site_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=site_var, width=35).grid(row=0, column=1, pady=(0, 5), padx=(10, 0))

        ttk.Label(main_frame, text="Username:", font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=(0, 5))
        username_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=username_var, width=35).grid(row=1, column=1, pady=(0, 5), padx=(10, 0))

        ttk.Label(main_frame, text="Password:", font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=password_var, width=25).grid(row=2, column=1, sticky='w', pady=(0, 5), padx=(10, 0))

        ttk.Label(main_frame, text="Label (optional):", font=('Segoe UI', 10)).grid(row=3, column=0, sticky='w', pady=(0, 5))
        label_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=label_var, width=35).grid(row=3, column=1, pady=(0, 5), padx=(10, 0))
        ttk.Label(main_frame, text="e.g., Personal, Work", font=('Segoe UI', 8)).grid(row=4, column=1, sticky='w', padx=(10, 0))

        def generate_password():
            pw = self.generator.generate()
            password_var.set(pw)

        def save():
            if site_var.get() and username_var.get() and password_var.get():
                self.storage.add_entry(site_var.get(), username_var.get(), password_var.get(), label_var.get())
                self._refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0))

        ttk.Button(btn_frame, text="Generate", command=generate_password).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="Save", command=save).pack(side='left')

    def _show_edit_dialog(self):
        entry = self._get_selected_entry()
        if not entry:
            messagebox.showwarning("Warning", "Please select an entry")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Edit Password")
        dialog.geometry("420x260")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(bg='#1a1a1a')

        # Center dialog on parent window
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 420) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 260) // 2
        dialog.geometry(f"+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Site:", font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=(0, 5))
        site_var = tk.StringVar(value=entry['site'])
        ttk.Entry(main_frame, textvariable=site_var, width=35).grid(row=0, column=1, pady=(0, 5), padx=(10, 0))

        ttk.Label(main_frame, text="Username:", font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=(0, 5))
        username_var = tk.StringVar(value=entry['username'])
        ttk.Entry(main_frame, textvariable=username_var, width=35).grid(row=1, column=1, pady=(0, 5), padx=(10, 0))

        ttk.Label(main_frame, text="Password:", font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=(0, 5))
        password_var = tk.StringVar(value=entry['password'])
        ttk.Entry(main_frame, textvariable=password_var, width=25).grid(row=2, column=1, sticky='w', pady=(0, 5), padx=(10, 0))

        ttk.Label(main_frame, text="Label (optional):", font=('Segoe UI', 10)).grid(row=3, column=0, sticky='w', pady=(0, 5))
        label_var = tk.StringVar(value=entry.get('label', ''))
        ttk.Entry(main_frame, textvariable=label_var, width=35).grid(row=3, column=1, pady=(0, 5), padx=(10, 0))
        ttk.Label(main_frame, text="e.g., Personal, Work", font=('Segoe UI', 8)).grid(row=4, column=1, sticky='w', padx=(10, 0))

        def generate_password():
            pw = self.generator.generate()
            password_var.set(pw)

        def save():
            if site_var.get() and username_var.get() and password_var.get():
                self.storage.update_entry(entry['id'], site_var.get(), username_var.get(), password_var.get(), label_var.get())
                self._refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0))

        ttk.Button(btn_frame, text="Generate", command=generate_password).pack(side='left', padx=(0, 10))
        ttk.Button(btn_frame, text="Save", command=save).pack(side='left')

    def _delete_entry(self):
        entry = self._get_selected_entry()
        if not entry:
            messagebox.showwarning("Warning", "Please select an entry")
            return

        if messagebox.askyesno("Confirm", f"Delete password for {entry['site']}?"):
            self.storage.delete_entry(entry['id'])
            self._refresh_list()
            self.status_var.set("Entry deleted")

import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from ..core.storage import PasswordStorage
from ..core.generator import PasswordGenerator


class VaultTab(ttk.Frame):

    AUTO_LOCK_TIMEOUT = 5 * 60 * 1000

    def __init__(self, parent, theme_colors: dict):
        super().__init__(parent)
        self.theme = theme_colors
        self.storage = PasswordStorage()
        self.generator = PasswordGenerator()
        self.unlocked = False
        self._lock_timer = None
        self._create_widgets()
        self._show_login()

    def _create_widgets(self):
        self.login_frame = ttk.Frame(self)
        self._create_login_widgets()

        self.vault_frame = ttk.Frame(self)
        self._create_vault_widgets()

    def _bind_activity_events(self):
        for event_type in ['<Motion>', '<KeyPress>', '<ButtonRelease>']:
            self.vault_frame.bind(event_type, self._reset_lock_timer)

    def _unbind_activity_events(self):
        for event_type in ['<Motion>', '<KeyPress>', '<ButtonRelease>']:
            self.vault_frame.unbind(event_type)

    def _reset_lock_timer(self, event=None):
        if self._lock_timer is not None:
            self.after_cancel(self._lock_timer)
        if self.unlocked:
            self._lock_timer = self.after(self.AUTO_LOCK_TIMEOUT, self._auto_lock)

    def _auto_lock(self):
        if self.unlocked:
            self._lock()
            messagebox.showinfo("Auto-Locked", "Vault locked due to inactivity.")

    def _create_login_widgets(self):
        spacer = ttk.Frame(self.login_frame)
        spacer.pack(expand=True)

        card = ttk.Frame(self.login_frame)
        card.pack(padx=40, pady=10)

        icon_label = ttk.Label(card, text="🔐", font=('Segoe UI', 32))
        icon_label.pack(pady=(0, 10))

        ttk.Label(card, text="Password Vault",
                  font=('Segoe UI', 16, 'bold'), foreground=self.theme['fg']).pack()

        if not self.storage.is_setup():
            ttk.Label(card, text="Create a master password to get started",
                      font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(pady=(4, 20))
        else:
            ttk.Label(card, text="Enter your master password to unlock",
                      font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(pady=(4, 20))

        fields_frame = ttk.Frame(card)
        fields_frame.pack(fill='x', pady=4)

        ttk.Label(fields_frame, text="Master Password",
                  font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(anchor='w')
        self.master_password_var = tk.StringVar()
        self.master_entry = ttk.Entry(fields_frame, textvariable=self.master_password_var,
                                      show='*', width=32)
        self.master_entry.pack(fill='x', pady=(3, 0))
        self.master_entry.bind('<Return>', lambda e: self._unlock())

        self.confirm_frame = ttk.Frame(card)
        self.confirm_var = tk.StringVar()

        if not self.storage.is_setup():
            self.confirm_frame.pack(fill='x', pady=(10, 0))
            ttk.Label(self.confirm_frame, text="Confirm Password",
                      font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(anchor='w')
            self.confirm_entry = ttk.Entry(self.confirm_frame, textvariable=self.confirm_var,
                                           show='*', width=32)
            self.confirm_entry.pack(fill='x', pady=(3, 0))

        btn_text = "Create Vault" if not self.storage.is_setup() else "Unlock Vault"
        ttk.Button(card, text=btn_text, command=self._unlock,
                   style='Accent.TButton').pack(fill='x', pady=(20, 0))

        spacer2 = ttk.Frame(self.login_frame)
        spacer2.pack(expand=True)

    def _create_vault_widgets(self):
        header_frame = ttk.Frame(self.vault_frame)
        header_frame.pack(fill='x', padx=16, pady=(14, 8))

        ttk.Label(header_frame, text="Your Passwords",
                  font=('Segoe UI', 14, 'bold'), foreground=self.theme['fg']).pack(side='left')
        ttk.Button(header_frame, text="Lock", command=self._lock).pack(side='right')

        toolbar_frame = ttk.Frame(self.vault_frame)
        toolbar_frame.pack(fill='x', padx=16, pady=(0, 8))

        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self._on_search)
        search_entry = ttk.Entry(toolbar_frame, textvariable=self.search_var, width=28)
        search_entry.pack(side='left')
        ttk.Label(toolbar_frame, text="  🔍",
                  font=('Segoe UI', 10), foreground=self.theme['fg_dim']).pack(side='left')

        ttk.Button(toolbar_frame, text="+ Add New",
                   command=self._show_add_dialog, style='Accent.TButton').pack(side='right')

        list_frame = ttk.Frame(self.vault_frame)
        list_frame.pack(fill='both', expand=True, padx=16)

        columns = ('site', 'label', 'username')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('site', text='Site')
        self.tree.heading('label', text='Label')
        self.tree.heading('username', text='Username')
        self.tree.column('site', width=160, minwidth=100)
        self.tree.column('label', width=110, minwidth=60)
        self.tree.column('username', width=160, minwidth=100)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_select)

        action_frame = ttk.Frame(self.vault_frame)
        action_frame.pack(fill='x', padx=16, pady=(8, 4))

        ttk.Button(action_frame, text="Copy Password",
                   command=self._copy_password).pack(side='left', padx=(0, 6))
        ttk.Button(action_frame, text="Copy Username",
                   command=self._copy_username).pack(side='left', padx=(0, 6))
        ttk.Button(action_frame, text="Edit",
                   command=self._show_edit_dialog).pack(side='left', padx=(0, 6))
        ttk.Button(action_frame, text="Delete",
                   command=self._delete_entry).pack(side='left')

        self.status_var = tk.StringVar(value="")
        ttk.Label(self.vault_frame, textvariable=self.status_var,
                  font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(
            anchor='w', padx=16, pady=(2, 8))

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
            if password != self.confirm_var.get():
                messagebox.showerror("Error", "Passwords do not match")
                return

            if len(password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters")
                return

            self.storage.setup_master(password)
            self.unlocked = True
            self._show_vault()
            self._start_auto_lock()
            messagebox.showinfo("Success", "Vault created successfully!")
        else:
            if self.storage.unlock(password):
                self.unlocked = True
                self._show_vault()
                self._start_auto_lock()
            else:
                messagebox.showerror("Error", "Incorrect password")

    def _start_auto_lock(self):
        self._bind_activity_events()
        self._reset_lock_timer()

    def _lock(self):
        self.unlocked = False
        self.master_password_var.set('')
        self.confirm_var.set('')
        if self._lock_timer is not None:
            self.after_cancel(self._lock_timer)
            self._lock_timer = None
        self._unbind_activity_events()
        self._show_login()

    def lock_vault(self):
        if self.unlocked:
            self._lock()

    def _refresh_list(self, entries=None):
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
        pass

    def _get_selected_entry(self):
        selection = self.tree.selection()
        if not selection:
            return None

        item = self.tree.item(selection[0])
        site, label, username = item['values']

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

    def _copy_username(self):
        entry = self._get_selected_entry()
        if entry:
            pyperclip.copy(entry['username'])
            self.status_var.set(f"Copied username for {entry['site']}")
        else:
            messagebox.showwarning("Warning", "Please select an entry")

    def _make_dialog(self, title, height=290):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry(f"440x{height}")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(bg=self.theme['bg'])
        dialog.resizable(False, False)
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 440) // 2
        y = self.winfo_rooty() + (self.winfo_height() - height) // 2
        dialog.geometry(f"+{x}+{y}")
        return dialog

    def _build_entry_form(self, parent, site='', username='', password='', label=''):
        parent.columnconfigure(1, weight=1)

        fields = [
            ("Site", site),
            ("Username", username),
            ("Password", password),
            ("Label", label),
        ]
        vars_ = []
        for i, (lbl, val) in enumerate(fields):
            ttk.Label(parent, text=lbl,
                      font=('Segoe UI', 9), foreground=self.theme['fg_dim']).grid(
                row=i * 2, column=0, columnspan=2, sticky='w', pady=(8 if i > 0 else 0, 2))
            var = tk.StringVar(value=val)
            show = '*' if lbl == "Password" else ''
            entry = ttk.Entry(parent, textvariable=var, show=show)
            entry.grid(row=i * 2 + 1, column=0, columnspan=2, sticky='ew', pady=(0, 0))
            vars_.append(var)

        hint = ttk.Label(parent, text="e.g., Personal, Work",
                         font=('Segoe UI', 8), foreground=self.theme['fg_dim'])
        hint.grid(row=7, column=0, columnspan=2, sticky='w', pady=(2, 0))

        return vars_[0], vars_[1], vars_[2], vars_[3]

    def _show_add_dialog(self):
        dialog = self._make_dialog("Add Password", height=310)

        main_frame = ttk.Frame(dialog, padding=(20, 16, 20, 16))
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Add New Entry",
                  font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 6))

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        form_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        site_var, username_var, password_var, label_var = self._build_entry_form(form_frame)

        def generate_password():
            pw = self.generator.generate()
            password_var.set(pw)

        def save():
            if site_var.get() and username_var.get() and password_var.get():
                self.storage.add_entry(site_var.get(), username_var.get(),
                                       password_var.get(), label_var.get())
                self._refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(16, 0), sticky='w')

        ttk.Button(btn_frame, text="Generate Password",
                   command=generate_password).pack(side='left', padx=(0, 8))
        ttk.Button(btn_frame, text="Save",
                   command=save, style='Accent.TButton').pack(side='left')

    def _show_edit_dialog(self):
        entry = self._get_selected_entry()
        if not entry:
            messagebox.showwarning("Warning", "Please select an entry")
            return

        dialog = self._make_dialog("Edit Password", height=310)

        main_frame = ttk.Frame(dialog, padding=(20, 16, 20, 16))
        main_frame.pack(fill='both', expand=True)

        ttk.Label(main_frame, text="Edit Entry",
                  font=('Segoe UI', 12, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 6))

        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        form_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        site_var, username_var, password_var, label_var = self._build_entry_form(
            form_frame,
            site=entry['site'],
            username=entry['username'],
            password=entry['password'],
            label=entry.get('label', '')
        )

        def generate_password():
            pw = self.generator.generate()
            password_var.set(pw)

        def save():
            if site_var.get() and username_var.get() and password_var.get():
                self.storage.update_entry(entry['id'], site_var.get(),
                                          username_var.get(), password_var.get(), label_var.get())
                self._refresh_list()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "All fields are required")

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(16, 0), sticky='w')

        ttk.Button(btn_frame, text="Generate Password",
                   command=generate_password).pack(side='left', padx=(0, 8))
        ttk.Button(btn_frame, text="Save",
                   command=save, style='Accent.TButton').pack(side='left')

    def _delete_entry(self):
        entry = self._get_selected_entry()
        if not entry:
            messagebox.showwarning("Warning", "Please select an entry")
            return

        if messagebox.askyesno("Confirm", f"Delete password for {entry['site']}?"):
            self.storage.delete_entry(entry['id'])
            self._refresh_list()
            self.status_var.set("Entry deleted")

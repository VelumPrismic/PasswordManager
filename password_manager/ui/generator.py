import tkinter as tk
from tkinter import ttk
import pyperclip
from ..core.generator import PasswordGenerator
from ..core.strength import StrengthChecker


class GeneratorTab(ttk.Frame):

    def __init__(self, parent, theme_colors: dict):
        super().__init__(parent)
        self.theme = theme_colors
        self.generator = PasswordGenerator()
        self.strength_checker = StrengthChecker()
        self._create_widgets()

    def _create_widgets(self):
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=24, pady=(24, 4))
        ttk.Label(header_frame, text="Password Generator",
                  font=('Segoe UI', 15, 'bold'), foreground=self.theme['fg']).pack(anchor='w')
        ttk.Label(header_frame, text="Customize and generate a secure password",
                  font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(anchor='w', pady=(2, 0))

        length_frame = ttk.LabelFrame(self, text="Length", padding=(12, 8))
        length_frame.pack(fill='x', padx=24, pady=(14, 0))

        slider_row = ttk.Frame(length_frame)
        slider_row.pack(fill='x')

        self.length_var = tk.IntVar(value=16)
        self.length_label = ttk.Label(slider_row, textvariable=self.length_var, width=3,
                                      font=('Segoe UI', 11, 'bold'), foreground=self.theme['accent'])
        self.length_label.pack(side='right')

        self.length_slider = ttk.Scale(
            slider_row, from_=8, to=64,
            variable=self.length_var, orient='horizontal',
            command=self._on_length_change
        )
        self.length_slider.pack(side='left', fill='x', expand=True, padx=(0, 10))

        options_frame = ttk.LabelFrame(self, text="Character Options", padding=(12, 10))
        options_frame.pack(fill='x', padx=24, pady=(12, 0))

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        opts_inner = ttk.Frame(options_frame)
        opts_inner.pack(fill='x')
        opts_inner.columnconfigure(0, weight=1)
        opts_inner.columnconfigure(1, weight=1)

        ttk.Checkbutton(opts_inner, text="Uppercase  (A-Z)", variable=self.uppercase_var).grid(row=0, column=0, sticky='w', pady=2)
        ttk.Checkbutton(opts_inner, text="Lowercase  (a-z)", variable=self.lowercase_var).grid(row=0, column=1, sticky='w', pady=2)
        ttk.Checkbutton(opts_inner, text="Numbers  (0-9)", variable=self.numbers_var).grid(row=1, column=0, sticky='w', pady=2)
        ttk.Checkbutton(opts_inner, text="Symbols  (!@#$%^&*)", variable=self.symbols_var).grid(row=1, column=1, sticky='w', pady=2)

        generate_btn = ttk.Button(self, text="Generate Password",
                                  command=self._generate, style='Accent.TButton')
        generate_btn.pack(pady=(16, 0), padx=24, anchor='w')

        display_frame = ttk.LabelFrame(self, text="Generated Password", padding=(12, 10))
        display_frame.pack(fill='x', padx=24, pady=(14, 0))

        self.password_var = tk.StringVar(value="")
        self._placeholder = "Click ‘Generate’ to create a password"
        self.password_entry = ttk.Entry(
            display_frame, textvariable=self.password_var,
            font=('Consolas', 12), state='readonly', width=40
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.password_var.set(self._placeholder)

        copy_btn = ttk.Button(display_frame, text="Copy", command=self._copy_password)
        copy_btn.pack(side='right')

        strength_frame = ttk.LabelFrame(self, text="Strength", padding=(12, 10))
        strength_frame.pack(fill='x', padx=24, pady=(14, 0))

        self.strength_bar = tk.Canvas(strength_frame, height=8,
                                      bg=self.theme['border'], highlightthickness=0)
        self.strength_bar.pack(fill='x', pady=(0, 8))

        self.strength_label = ttk.Label(strength_frame, text="No password generated",
                                        font=('Segoe UI', 9), foreground=self.theme['fg_dim'])
        self.strength_label.pack(anchor='w')

    def _on_length_change(self, value):
        self.generator.length = int(float(value))

    def _generate(self):
        self.generator.set_options(
            length=self.length_var.get(),
            uppercase=self.uppercase_var.get(),
            lowercase=self.lowercase_var.get(),
            numbers=self.numbers_var.get(),
            symbols=self.symbols_var.get()
        )
        password = self.generator.generate()
        self.password_var.set(password)
        self._update_strength(password)

    def _copy_password(self):
        password = self.password_var.get()
        if password and password != "Click 'Generate' to create a password":
            pyperclip.copy(password)
            self.strength_label.config(text="Copied to clipboard!")
            self.after(2000, lambda: self.strength_label.config(text=self._last_strength_text))

    def _update_strength(self, password):
        result = self.strength_checker.check(password)
        self._last_strength_text = f"Strength: {result['label']} ({result['score']}/100)"
        self.strength_label.config(text=self._last_strength_text)

        self.strength_bar.delete('all')
        bar_width = self.strength_bar.winfo_width() * (result['score'] / 100)
        self.strength_bar.create_rectangle(0, 0, bar_width, 8, fill=result['color'], outline='')

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
        title = ttk.Label(self, text="Password Generator", font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(0, 20))

        length_frame = ttk.Frame(self)
        length_frame.pack(fill='x', padx=20, pady=5)

        ttk.Label(length_frame, text="Length:").pack(side='left')
        self.length_var = tk.IntVar(value=16)
        self.length_label = ttk.Label(length_frame, textvariable=self.length_var, width=3)
        self.length_label.pack(side='right')

        self.length_slider = ttk.Scale(
            length_frame, from_=8, to=64,
            variable=self.length_var, orient='horizontal',
            command=self._on_length_change
        )
        self.length_slider.pack(side='left', fill='x', expand=True, padx=(10, 10))

        options_frame = ttk.LabelFrame(self, text="Character Options", padding=10)
        options_frame.pack(fill='x', padx=20, pady=10)

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(options_frame, text="Uppercase (A-Z)", variable=self.uppercase_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Lowercase (a-z)", variable=self.lowercase_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Numbers (0-9)", variable=self.numbers_var).pack(anchor='w')
        ttk.Checkbutton(options_frame, text="Symbols (!@#$%^&*)", variable=self.symbols_var).pack(anchor='w')

        generate_btn = ttk.Button(self, text="Generate Password", command=self._generate)
        generate_btn.pack(pady=15)

        display_frame = ttk.LabelFrame(self, text="Generated Password", padding=10)
        display_frame.pack(fill='x', padx=20, pady=10)

        self.password_var = tk.StringVar(value="Click 'Generate' to create a password")
        self.password_entry = ttk.Entry(
            display_frame, textvariable=self.password_var,
            font=('Consolas', 12), state='readonly', width=40
        )
        self.password_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        copy_btn = ttk.Button(display_frame, text="Copy", command=self._copy_password)
        copy_btn.pack(side='right')

        strength_frame = ttk.LabelFrame(self, text="Strength", padding=10)
        strength_frame.pack(fill='x', padx=20, pady=10)

        self.strength_bar = tk.Canvas(strength_frame, height=20, bg='#353535')
        self.strength_bar.pack(fill='x', pady=(0, 5))

        self.strength_label = ttk.Label(strength_frame, text="No password generated", font=('Segoe UI', 10))
        self.strength_label.pack()

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
        self.strength_bar.create_rectangle(0, 0, bar_width, 20, fill=result['color'], outline='')

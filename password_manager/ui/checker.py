import tkinter as tk
from tkinter import ttk
from ..core.strength import StrengthChecker


class CheckerTab(ttk.Frame):

    def __init__(self, parent, theme_colors: dict):
        super().__init__(parent)
        self.theme = theme_colors
        self.strength_checker = StrengthChecker()
        self._create_widgets()

    def _create_widgets(self):
        title = ttk.Label(self, text="Password Strength Checker", font=('Segoe UI', 16, 'bold'))
        title.pack(pady=(0, 20))

        input_frame = ttk.LabelFrame(self, text="Enter Password", padding=10)
        input_frame.pack(fill='x', padx=20, pady=10)

        self.password_var = tk.StringVar()
        self.password_var.trace_add('write', self._on_password_change)

        self.password_entry = ttk.Entry(
            input_frame, textvariable=self.password_var,
            font=('Consolas', 12), width=40, show='*'
        )
        self.password_entry.pack(fill='x', padx=(0, 0))

        self.show_var = tk.BooleanVar(value=False)
        show_toggle = ttk.Checkbutton(input_frame, text="Show", variable=self.show_var, command=self._toggle_show)
        show_toggle.pack(anchor='w', pady=(5, 0))

        strength_frame = ttk.LabelFrame(self, text="Strength Analysis", padding=15)
        strength_frame.pack(fill='x', padx=20, pady=10)

        score_frame = ttk.Frame(strength_frame)
        score_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(score_frame, text="Score:", font=('Segoe UI', 11)).pack(side='left')
        self.score_var = tk.StringVar(value="0/100")
        ttk.Label(score_frame, textvariable=self.score_var, font=('Segoe UI', 11, 'bold')).pack(side='left', padx=(5, 0))

        self.label_var = tk.StringVar(value="Enter a password")
        ttk.Label(score_frame, textvariable=self.label_var, font=('Segoe UI', 11)).pack(side='right')

        self.strength_bar = tk.Canvas(strength_frame, height=25, bg='#353535')
        self.strength_bar.pack(fill='x', pady=(0, 10))

        details_frame = ttk.Frame(strength_frame)
        details_frame.pack(fill='x')

        self.details_text = tk.Text(
            details_frame, height=8, wrap='word',
            font=('Segoe UI', 10), state='disabled',
            bg='#2a2a2a', fg='#b0b0b0', relief='flat'
        )
        self.details_text.pack(fill='x')

        clear_btn = ttk.Button(self, text="Clear", command=self._clear)
        clear_btn.pack(pady=10)

    def _toggle_show(self):
        if self.show_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def _on_password_change(self, *args):
        password = self.password_var.get()
        result = self.strength_checker.check(password)

        self.score_var.set(f"{result['score']}/100")
        self.label_var.set(result['label'])

        self.strength_bar.delete('all')
        bar_width = self.strength_bar.winfo_width() * (result['score'] / 100)
        self.strength_bar.create_rectangle(0, 0, bar_width, 25, fill=result['color'], outline='')

        self.details_text.config(state='normal')
        self.details_text.delete('1.0', 'end')
        self.details_text.insert('1.0', '\n'.join(result['details']))
        self.details_text.config(state='disabled')

    def _clear(self):
        self.password_var.set('')
        self.score_var.set("0/100")
        self.label_var.set("Enter a password")
        self.strength_bar.delete('all')
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', 'end')
        self.details_text.config(state='disabled')

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
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=24, pady=(24, 4))
        ttk.Label(header_frame, text="Strength Checker",
                  font=('Segoe UI', 15, 'bold'), foreground=self.theme['fg']).pack(anchor='w')
        ttk.Label(header_frame, text="Analyze how strong your password is",
                  font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(anchor='w', pady=(2, 0))

        input_frame = ttk.LabelFrame(self, text="Password", padding=(12, 10))
        input_frame.pack(fill='x', padx=24, pady=(14, 0))

        self.password_var = tk.StringVar()
        self.password_var.trace_add('write', self._on_password_change)

        self.password_entry = ttk.Entry(
            input_frame, textvariable=self.password_var,
            font=('Consolas', 12), width=40, show='*'
        )
        self.password_entry.pack(fill='x')

        toggle_row = ttk.Frame(input_frame)
        toggle_row.pack(fill='x', pady=(6, 0))
        self.show_var = tk.BooleanVar(value=False)
        show_toggle = ttk.Checkbutton(toggle_row, text="Show password",
                                      variable=self.show_var, command=self._toggle_show)
        show_toggle.pack(side='left')

        strength_frame = ttk.LabelFrame(self, text="Strength Analysis", padding=(12, 12))
        strength_frame.pack(fill='x', padx=24, pady=(14, 0))

        score_frame = ttk.Frame(strength_frame)
        score_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(score_frame, text="Score",
                  font=('Segoe UI', 9), foreground=self.theme['fg_dim']).pack(side='left')
        self.score_var = tk.StringVar(value="0 / 100")
        ttk.Label(score_frame, textvariable=self.score_var,
                  font=('Segoe UI', 11, 'bold'), foreground=self.theme['accent']).pack(side='left', padx=(6, 0))

        self.label_var = tk.StringVar(value="Enter a password")
        ttk.Label(score_frame, textvariable=self.label_var,
                  font=('Segoe UI', 10), foreground=self.theme['fg_dim']).pack(side='right')

        self.strength_bar = tk.Canvas(strength_frame, height=8,
                                      bg=self.theme['border'], highlightthickness=0)
        self.strength_bar.pack(fill='x', pady=(0, 12))

        details_frame = ttk.Frame(strength_frame)
        details_frame.pack(fill='x')

        self.details_text = tk.Text(
            details_frame, height=7, wrap='word',
            font=('Segoe UI', 10), state='disabled',
            bg=self.theme['bg_card'], fg=self.theme['fg'],
            relief='flat', borderwidth=0,
            selectbackground=self.theme['selected'],
            padx=4, pady=4
        )
        self.details_text.pack(fill='x')

        btn_row = ttk.Frame(self)
        btn_row.pack(fill='x', padx=24, pady=(14, 0))
        clear_btn = ttk.Button(btn_row, text="Clear", command=self._clear)
        clear_btn.pack(side='left')

    def _toggle_show(self):
        if self.show_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def _on_password_change(self, *args):
        password = self.password_var.get()
        result = self.strength_checker.check(password)

        self.score_var.set(f"{result['score']} / 100")
        self.label_var.set(result['label'])

        self.strength_bar.delete('all')
        bar_width = self.strength_bar.winfo_width() * (result['score'] / 100)
        self.strength_bar.create_rectangle(0, 0, bar_width, 8, fill=result['color'], outline='')

        self.details_text.config(state='normal')
        self.details_text.delete('1.0', 'end')
        self.details_text.insert('1.0', '\n'.join(result['details']))
        self.details_text.config(state='disabled')

    def _clear(self):
        self.password_var.set('')
        self.score_var.set("0 / 100")
        self.label_var.set("Enter a password")
        self.strength_bar.delete('all')
        self.details_text.config(state='normal')
        self.details_text.delete('1.0', 'end')
        self.details_text.config(state='disabled')

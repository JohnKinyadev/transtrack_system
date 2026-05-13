import tkinter as tk
from tkinter import messagebox

from transtrack.controllers.auth_controller import AuthController
from transtrack.views import styles


class LoginView(tk.Frame):
    def __init__(self, master, on_success):
        super().__init__(master, bg=styles.BG)
        self.on_success = on_success
        self.auth = AuthController()
        self.build()

    def build(self):
        shell = tk.Frame(self, bg=styles.BG)
        shell.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.82, relheight=0.72)
        shell.columnconfigure(0, weight=1)
        shell.columnconfigure(1, weight=1)
        shell.rowconfigure(0, weight=1)

        intro = tk.Frame(shell, bg=styles.PRIMARY, padx=34, pady=34)
        intro.grid(row=0, column=0, sticky="nsew")
        tk.Label(
            intro,
            text="TransTrack",
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            font=("Segoe UI", 30, "bold"),
        ).pack(anchor="w")
        tk.Label(
            intro,
            text="Keep owners, vehicles, trips, collections, expenses, and payouts in one tidy workspace.",
            bg=styles.PRIMARY,
            fg="#dbeafe",
            font=("Segoe UI", 12),
            wraplength=360,
            justify="left",
        ).pack(anchor="w", pady=(12, 28))

        for label, value in (("Records", "Structured"), ("Dashboards", "Role based"), ("Reports", "Quick export")):
            row = tk.Frame(intro, bg=styles.PRIMARY)
            row.pack(anchor="w", fill="x", pady=5)
            tk.Label(row, text=value, bg="#dbeafe", fg=styles.PRIMARY, font=styles.FONT_SMALL, padx=9, pady=4).pack(
                side="left"
            )
            tk.Label(row, text=label, bg=styles.PRIMARY, fg=styles.WHITE, font=styles.FONT_BODY).pack(
                side="left", padx=(10, 0)
            )

        card = tk.Frame(shell, bg=styles.WHITE, padx=34, pady=34, highlightthickness=1, highlightbackground=styles.BORDER)
        card.grid(row=0, column=1, sticky="nsew")

        tk.Label(card, text="Welcome back", bg=styles.WHITE, fg=styles.TEXT, font=("Segoe UI", 22, "bold")).pack(
            anchor="w", pady=(8, 2)
        )
        tk.Label(card, text="Sign in to continue", bg=styles.WHITE, fg=styles.MUTED, font=styles.FONT_BODY).pack(
            anchor="w", pady=(0, 24)
        )

        tk.Label(card, text="Username", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY).pack(anchor="w")
        self.username = tk.Entry(
            card,
            font=styles.FONT_BODY,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
            highlightcolor=styles.PRIMARY,
        )
        self.username.pack(fill="x", pady=(4, 14), ipady=6)

        tk.Label(card, text="Password", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_BODY).pack(anchor="w")
        self.password = tk.Entry(
            card,
            show="*",
            font=styles.FONT_BODY,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=styles.BORDER,
            highlightcolor=styles.PRIMARY,
        )
        self.password.pack(fill="x", pady=(4, 20), ipady=6)

        tk.Button(
            card,
            text="Login",
            command=self.login,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            activebackground=styles.PRIMARY_HOVER,
            activeforeground=styles.WHITE,
            relief="flat",
            font=styles.FONT_HEADING,
            cursor="hand2",
        ).pack(fill="x", ipady=8)

        tk.Label(
            card,
            #text="Default demo login: admin / admin123",
            bg=styles.WHITE,
            fg=styles.MUTED,
            font=styles.FONT_SMALL,
        ).pack(anchor="w", pady=(18, 0))

        self.password.bind("<Return>", lambda _event: self.login())

    def login(self):
        ok, user = self.auth.login(self.username.get(), self.password.get())
        if ok:
            self.on_success(user)
            return
        messagebox.showerror("Login failed", "Invalid username or password.")

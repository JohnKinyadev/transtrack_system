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
        card = tk.Frame(self, bg=styles.WHITE, padx=34, pady=30)
        card.place(relx=0.5, rely=0.5, anchor="center", width=430)

        tk.Label(card, text="TransTrack", bg=styles.WHITE, fg=styles.TEXT, font=("Segoe UI", 24, "bold")).pack(
            anchor="w"
        )
        tk.Label(card, text="Transport operations platform", bg=styles.WHITE, fg=styles.MUTED).pack(
            anchor="w", pady=(0, 24)
        )

        tk.Label(card, text="Username", bg=styles.WHITE, fg=styles.TEXT).pack(anchor="w")
        self.username = tk.Entry(card, font=styles.FONT_BODY)
        self.username.pack(fill="x", pady=(4, 14), ipady=6)

        tk.Label(card, text="Password", bg=styles.WHITE, fg=styles.TEXT).pack(anchor="w")
        self.password = tk.Entry(card, show="*", font=styles.FONT_BODY)
        self.password.pack(fill="x", pady=(4, 20), ipady=6)

        tk.Button(
            card,
            text="Login",
            command=self.login,
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            relief="flat",
            font=styles.FONT_HEADING,
            cursor="hand2",
        ).pack(fill="x", ipady=8)

        tk.Label(
            card,
            text="Default demo login: admin / admin123",
            bg=styles.WHITE,
            fg=styles.MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(18, 0))

        self.password.bind("<Return>", lambda _event: self.login())

    def login(self):
        ok, user = self.auth.login(self.username.get(), self.password.get())
        if ok:
            self.on_success(user)
            return
        messagebox.showerror("Login failed", "Invalid username or password.")

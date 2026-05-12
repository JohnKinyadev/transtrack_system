import tkinter as tk

from transtrack.controllers.auth_controller import AuthController
from transtrack.utils.session import get_current_user
from transtrack.views import styles
from transtrack.views.widgets import clear_frame


class BaseDashboard(tk.Frame):
    title = "Dashboard"
    menu_items = ()

    def __init__(self, master, on_logout):
        super().__init__(master, bg=styles.BG)
        self.on_logout = on_logout
        self.auth = AuthController()
        self.sidebar = tk.Frame(self, bg=styles.SIDEBAR, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.content = tk.Frame(self, bg=styles.BG)
        self.content.pack(side="right", fill="both", expand=True)
        self.build_sidebar()
        self.show_home()

    def build_sidebar(self):
        user = get_current_user() or {}
        tk.Label(
            self.sidebar,
            text="TransTrack",
            bg=styles.SIDEBAR,
            fg=styles.WHITE,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", padx=18, pady=(22, 6))
        tk.Label(
            self.sidebar,
            text=user.get("full_name", "User"),
            bg=styles.SIDEBAR,
            fg="#d1d5db",
            font=styles.FONT_BODY,
        ).pack(anchor="w", padx=18, pady=(0, 18))

        for label, command in self.menu_items:
            tk.Button(
                self.sidebar,
                text=label,
                command=command,
                bg=styles.SIDEBAR,
                fg=styles.WHITE,
                activebackground=styles.SIDEBAR_HOVER,
                activeforeground=styles.WHITE,
                relief="flat",
                anchor="w",
                padx=18,
                pady=10,
                cursor="hand2",
                font=styles.FONT_BODY,
            ).pack(fill="x")

        tk.Button(
            self.sidebar,
            text="Logout",
            command=self.logout,
            bg="#991b1b",
            fg=styles.WHITE,
            relief="flat",
            anchor="w",
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(side="bottom", fill="x", pady=16)

    def page(self, title):
        clear_frame(self.content)
        tk.Label(self.content, text=title, bg=styles.BG, fg=styles.TEXT, font=styles.FONT_TITLE).pack(
            anchor="w", padx=24, pady=(22, 14)
        )
        body = tk.Frame(self.content, bg=styles.WHITE, padx=16, pady=16)
        body.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        return body

    def show_home(self):
        body = self.page(self.title)
        tk.Label(body, text="Welcome to your workspace.", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(
            anchor="w"
        )

    def logout(self):
        self.auth.logout()
        self.on_logout()

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
        self.sidebar.pack_propagate(False)
        self.content = tk.Frame(self, bg=styles.BG)
        self.content.pack(side="right", fill="both", expand=True)
        self.build_sidebar()
        self.show_home()

    def build_sidebar(self):
        user = get_current_user() or {}
        header = tk.Frame(self.sidebar, bg=styles.SIDEBAR)
        header.pack(fill="x")
        tk.Label(
            header,
            text="TransTrack",
            bg=styles.SIDEBAR,
            fg=styles.WHITE,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", padx=18, pady=(22, 6))
        tk.Label(
            header,
            text=user.get("full_name", "User"),
            bg=styles.SIDEBAR,
            fg="#f5dc78",
            font=styles.FONT_BODY,
        ).pack(anchor="w", padx=18, pady=(0, 18))

        menu_area = tk.Frame(self.sidebar, bg=styles.SIDEBAR)
        menu_area.pack(fill="both", expand=True)
        menu_canvas = tk.Canvas(menu_area, bg=styles.SIDEBAR, highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(menu_area, orient="vertical", command=menu_canvas.yview, bg=styles.SIDEBAR)
        menu = tk.Frame(menu_canvas, bg=styles.SIDEBAR)
        menu_window = menu_canvas.create_window((0, 0), window=menu, anchor="nw")

        def sync_scroll_region(_event=None):
            menu_canvas.configure(scrollregion=menu_canvas.bbox("all"))

        def sync_menu_width(event):
            menu_canvas.itemconfigure(menu_window, width=event.width)

        def scroll_with_wheel(event):
            menu_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"

        menu.bind("<Configure>", sync_scroll_region)
        menu_canvas.bind("<Configure>", sync_menu_width)
        menu_canvas.bind("<MouseWheel>", scroll_with_wheel)
        menu_canvas.bind("<Button-4>", lambda _event: menu_canvas.yview_scroll(-1, "units"))
        menu_canvas.bind("<Button-5>", lambda _event: menu_canvas.yview_scroll(1, "units"))
        menu_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        menu_canvas.pack(side="left", fill="both", expand=True)

        for label, command in self.menu_items:
            tk.Button(
                menu,
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
            menu,
            text="Logout",
            command=self.logout,
            bg="#991b1b",
            fg=styles.WHITE,
            relief="flat",
            anchor="w",
            padx=18,
            pady=10,
            cursor="hand2",
        ).pack(fill="x", pady=(16, 18))

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
        tk.Label(
            body,
            text="Welcome to your TransTrack workspace.",
            bg=styles.WHITE,
            fg=styles.TEXT,
            font=styles.FONT_HEADING,
        ).pack(anchor="w")

    def logout(self):
        self.auth.logout()
        self.on_logout()

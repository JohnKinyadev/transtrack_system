import tkinter as tk

from transtrack.db.connection import get_db
from transtrack.views import styles


class ReportsView(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=styles.WHITE)
        self.db = get_db()
        self.build()

    def build(self):
        totals = {
            "Owners": self.db.owners.count_documents({}),
            "Vehicles": self.db.vehicles.count_documents({}),
            "Drivers": self.db.drivers.count_documents({}),
            "Routes": self.db.routes.count_documents({}),
            "Trips": self.db.trips.count_documents({}),
            "Collections": self.db.collections.count_documents({}),
            "Expenses": self.db.expenses.count_documents({}),
            "Payouts": self.db.payouts.count_documents({}),
        }
        grid = tk.Frame(self, bg=styles.WHITE)
        grid.pack(anchor="nw")
        for index, (label, value) in enumerate(totals.items()):
            card = tk.Frame(grid, bg="#eef2ff", padx=18, pady=14)
            card.grid(row=index // 4, column=index % 4, padx=8, pady=8, sticky="nsew")
            tk.Label(card, text=label, bg="#eef2ff", fg=styles.MUTED, font=styles.FONT_BODY).pack(anchor="w")
            tk.Label(card, text=str(value), bg="#eef2ff", fg=styles.TEXT, font=("Segoe UI", 22, "bold")).pack(anchor="w")

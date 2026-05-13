import tkinter as tk

from transtrack.db.connection import get_db
from transtrack.utils.numbers import to_float
from transtrack.views import styles
from transtrack.views.collections_view import CollectionsView
from transtrack.views.conductors_view import ConductorsView
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.deductions_view import DeductionsView
from transtrack.views.drivers_view import DriversView
from transtrack.views.expenses_view import ExpensesView
from transtrack.views.owners_view import OwnersView
from transtrack.views.payouts_view import PayoutsView
from transtrack.views.reports_view import ReportsView
from transtrack.views.routes_view import RoutesView
from transtrack.views.trips_view import TripsView
from transtrack.views.user_management_view import UserManagementView
from transtrack.views.vehicles_view import VehiclesView


class AdminDashboard(BaseDashboard):
    title = "Company Operations"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("Routes", lambda: self.show_view("Route Management", RoutesView)),
            ("Owners", lambda: self.show_view("Vehicle Owner Management", OwnersView)),
            ("Vehicles", lambda: self.show_view("Vehicle Management", VehiclesView)),
            ("Drivers", lambda: self.show_view("Driver Management", DriversView)),
            ("Conductors", lambda: self.show_view("Conductor Management", ConductorsView)),
            ("Trips", lambda: self.show_view("Trip Management", TripsView)),
            ("Collections", lambda: self.show_view("Collections Overview", CollectionsView)),
            ("Expenses", lambda: self.show_view("Expense Overview", ExpensesView)),
            ("Deductions", lambda: self.show_view("Deductions Management", DeductionsView)),
            ("Payouts", lambda: self.show_view("Payout Processing", PayoutsView)),
            ("Reports", lambda: self.show_view("Reports", ReportsView)),
            ("Users", lambda: self.show_view("User Management", UserManagementView)),
        )
        super().__init__(master, on_logout)

    def show_view(self, title, view_class):
        body = self.page(title)
        view_class(body).pack(fill="both", expand=True)

    def show_home(self):
        body = self.page(self.title)
        db = get_db()
        total_collections = sum(to_float(row.get("amount_collected", 0)) for row in db.collections.find({}))
        total_expenses = sum(to_float(row.get("amount", 0)) for row in db.expenses.find({}))
        active_trips = db.trips.count_documents({"status": {"$ne": "Completed"}})
        pending_payouts = db.owners.count_documents({"status": "Active"}) - db.payouts.count_documents({})
        cards = (
            ("Owners", db.owners.count_documents({}), "Vehicle Owner Management", OwnersView),
            ("Vehicles", db.vehicles.count_documents({}), "Vehicle Management", VehiclesView),
            ("Drivers", db.drivers.count_documents({}), "Driver Management", DriversView),
            ("Active Trips", active_trips, "Trip Management", TripsView),
            ("Collections", f"{total_collections:,.0f}", "Collections Overview", CollectionsView),
            ("Expenses", f"{total_expenses:,.0f}", "Expense Overview", ExpensesView),
            ("Net Estimate", f"{total_collections - total_expenses:,.0f}", "Reports", ReportsView),
            ("Pending Payouts", max(pending_payouts, 0), "Payout Processing", PayoutsView),
        )
        grid = tk.Frame(body, bg=styles.WHITE)
        grid.pack(anchor="nw", fill="x")
        for index, (label, value, view_title, view_class) in enumerate(cards):
            card = tk.Button(
                grid,
                text=f"{label}\n{value}",
                command=lambda title=view_title, klass=view_class: self.show_view(title, klass),
                bg="#f8fafc",
                fg=styles.TEXT,
                activebackground="#eef2ff",
                relief="solid",
                bd=1,
                padx=16,
                pady=14,
                width=20,
                height=3,
                anchor="w",
                justify="left",
                cursor="hand2",
                font=("Segoe UI", 12, "bold"),
            )
            card.grid(row=index // 4, column=index % 4, padx=8, pady=8, sticky="nsew")

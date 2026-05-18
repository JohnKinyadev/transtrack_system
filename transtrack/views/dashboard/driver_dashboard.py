import tkinter as tk
from tkinter import messagebox

from transtrack.config import TRIP_STATUSES
from transtrack.views.deductions_view import DeductionsView
from transtrack.controllers.driver_controller import DriverController
from transtrack.controllers.expense_controller import ExpenseController
from transtrack.controllers.trip_controller import TripController
from transtrack.controllers.vehicle_controller import VehicleController
from transtrack.utils.session import get_current_user
from transtrack.utils.numbers import to_float
from transtrack.utils.relations import reference_query
from transtrack.views import styles
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.lookups import display_value
from transtrack.views.widgets import format_id, labeled_combo, labeled_entry, make_table, metric_card


class DriverDashboard(BaseDashboard):
    title = "Driver Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("My Trips", self.show_trips),
            ("Assigned Vehicle", self.show_vehicle),
            ("My Expenses", self.show_expenses),
            ("Deductions", lambda: self.show_view("Deductions", DeductionsView)),
            ("Log Expense", self.show_expense_form),
        )
        super().__init__(master, on_logout)

    def show_view(self, title, view_class):
        body = self.page(title)
        view_class(body).pack(fill="both", expand=True)

    def driver_id(self):
        return (get_current_user() or {}).get("linked_id")

    def current_driver(self):
        driver_id = self.driver_id()
        return DriverController().get(driver_id) if driver_id else None

    def assigned_vehicle_id(self):
        driver = self.current_driver() or {}
        return driver.get("assigned_vehicle")

    def my_trips(self):
        driver_id = self.driver_id()
        return TripController().list_for_driver(driver_id) if driver_id else []

    def show_home(self):
        body = self.page("Driver Dashboard")
        trips = self.my_trips()
        active = [trip for trip in trips if trip.get("status") != "Completed"]
        expenses = (
            ExpenseController().list_all(reference_query("vehicle_id", "vehicles", self.assigned_vehicle_id()))
            if self.assigned_vehicle_id()
            else []
        )
        total_expenses = sum(to_float(expense.get("amount")) for expense in expenses)
        cards = (
            ("Assigned Trips", len(trips), styles.SUCCESS_BG, styles.SUCCESS_FG),
            ("Active Trips", len(active), styles.ACCENT_SOFT, styles.ACCENT),
            ("Logged Expenses", len(expenses), styles.SURFACE_SOFT, styles.TEXT),
            ("Expense Total", f"{total_expenses:,.0f}", styles.SURFACE_SOFT, styles.TEXT),
        )
        grid = tk.Frame(body, bg=styles.WHITE)
        grid.pack(anchor="nw", fill="x")
        for index, (label, value, bg, fg) in enumerate(cards):
            card = metric_card(grid, label, value, bg, fg)
            card.grid(row=0, column=index, sticky="ew", padx=8, pady=8)
            grid.columnconfigure(index, weight=1)

    def show_trips(self):
        body = self.page("My Trips")
        control = tk.Frame(body, bg=styles.WHITE)
        control.pack(fill="x", pady=(0, 12))
        trip_id = labeled_entry(control, "Trip ID", 0)
        status = labeled_combo(control, "New Status", 1, TRIP_STATUSES)
        tk.Button(
            control,
            text="Update Status",
            command=lambda: self.update_status(trip_id.get(), status.get()),
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
        ).grid(row=2, column=1, sticky="e", padx=8, pady=8)

        table_frame = tk.Frame(body, bg=styles.WHITE)
        table_frame.pack(fill="both", expand=True)
        table = make_table(table_frame, ("id", "vehicle_id", "route_id", "date", "status", "departure_time", "arrival_time"))
        for trip in self.my_trips():
            table.insert(
                "",
                "end",
                values=(
                    format_id(trip),
                    display_value("vehicle_id", trip.get("vehicle_id", "")),
                    display_value("route_id", trip.get("route_id", "")),
                    trip.get("date", ""),
                    trip.get("status", ""),
                    trip.get("departure_time", ""),
                    trip.get("arrival_time", ""),
                ),
            )

    def update_status(self, trip_id, status):
        try:
            TripController().update_status(trip_id, status)
            messagebox.showinfo("Trip updated", "Trip status updated successfully.")
            self.show_trips()
        except Exception as exc:
            messagebox.showerror("Update failed", str(exc))

    def show_vehicle(self):
        body = self.page("Assigned Vehicle")
        table = make_table(body, ("id", "plate", "make", "model", "capacity", "status"))
        vehicle_id = self.assigned_vehicle_id()
        vehicle = VehicleController().get(vehicle_id) if vehicle_id else None
        if not vehicle:
            return
        table.insert(
            "",
            "end",
            values=(
                format_id(vehicle),
                vehicle.get("plate", ""),
                vehicle.get("make", ""),
                vehicle.get("model", ""),
                vehicle.get("capacity", ""),
                vehicle.get("status", ""),
            ),
        )

    def show_expenses(self):
        body = self.page("My Expenses")
        table = make_table(body, ("id", "trip_id", "vehicle_id", "type", "amount", "date"))
        vehicle_id = self.assigned_vehicle_id()
        expenses = (
            ExpenseController().list_all(reference_query("vehicle_id", "vehicles", vehicle_id), [("date", -1)])
            if vehicle_id
            else []
        )
        for expense in expenses:
            table.insert(
                "",
                "end",
                values=(
                    format_id(expense),
                    display_value("trip_id", expense.get("trip_id", "")),
                    display_value("vehicle_id", expense.get("vehicle_id", "")),
                    expense.get("type", ""),
                    expense.get("amount", 0),
                    expense.get("date", ""),
                ),
            )

    def show_expense_form(self):
        body = self.page("Log Expense")
        trip_id = labeled_entry(body, "Trip ID", 0)
        vehicle_id = labeled_entry(body, "Vehicle ID", 1, value=self.assigned_vehicle_id() or "")
        expense_type = labeled_combo(body, "Type", 2, ("fuel", "toll", "allowance", "repair", "service"))
        amount = labeled_entry(body, "Amount", 3)
        tk.Button(
            body,
            text="Save Expense",
            command=lambda: self.save_expense(trip_id.get(), vehicle_id.get(), expense_type.get(), amount.get()),
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
        ).grid(row=4, column=1, sticky="e", padx=8, pady=10)

    def save_expense(self, trip_id, vehicle_id, expense_type, amount):
        try:
            ExpenseController().log_expense(trip_id, vehicle_id, expense_type, amount)
            messagebox.showinfo("Expense saved", "Trip expense logged successfully.")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

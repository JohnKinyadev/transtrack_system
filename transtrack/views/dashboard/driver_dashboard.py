import tkinter as tk
from tkinter import messagebox

from transtrack.config import TRIP_STATUSES
from transtrack.controllers.expense_controller import ExpenseController
from transtrack.controllers.trip_controller import TripController
from transtrack.utils.session import get_current_user
from transtrack.views import styles
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.widgets import labeled_combo, labeled_entry, make_table


class DriverDashboard(BaseDashboard):
    title = "Driver Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("My Trips", self.show_trips),
            ("Log Expense", self.show_expense_form),
        )
        super().__init__(master, on_logout)

    def driver_id(self):
        return (get_current_user() or {}).get("linked_id")

    def show_home(self):
        body = self.page("Driver Dashboard")
        trips = TripController().list_for_driver(self.driver_id()) if self.driver_id() else []
        active = [trip for trip in trips if trip.get("status") != "Completed"]
        tk.Label(body, text=f"Assigned trips: {len(trips)}", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(
            anchor="w"
        )
        tk.Label(body, text=f"Active trips: {len(active)}", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(
            anchor="w", pady=8
        )

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

        table = make_table(body, ("id", "vehicle_id", "route_id", "date", "status", "departure_time", "arrival_time"))
        for trip in TripController().list_for_driver(self.driver_id()):
            table.insert(
                "",
                "end",
                values=(
                    trip.get("public_id") or str(trip.get("_id")),
                    trip.get("vehicle_id", ""),
                    trip.get("route_id", ""),
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

    def show_expense_form(self):
        body = self.page("Log Expense")
        trip_id = labeled_entry(body, "Trip ID", 0)
        vehicle_id = labeled_entry(body, "Vehicle ID", 1)
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

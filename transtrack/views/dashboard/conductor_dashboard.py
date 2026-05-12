import tkinter as tk
from tkinter import messagebox

from transtrack.controllers.collection_controller import CollectionController
from transtrack.controllers.trip_controller import TripController
from transtrack.utils.session import get_current_user
from transtrack.views import styles
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.widgets import labeled_entry, make_table


class ConductorDashboard(BaseDashboard):
    title = "Conductor Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("My Trips", self.show_trips),
            ("Log Collection", self.show_collection_form),
        )
        super().__init__(master, on_logout)

    def conductor_id(self):
        return (get_current_user() or {}).get("linked_id")

    def show_home(self):
        body = self.page("Conductor Dashboard")
        trips = TripController().list_for_conductor(self.conductor_id()) if self.conductor_id() else []
        tk.Label(body, text=f"Assigned trips: {len(trips)}", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(
            anchor="w"
        )

    def show_trips(self):
        body = self.page("My Trips")
        table = make_table(body, ("id", "vehicle_id", "route_id", "date", "status"))
        for trip in TripController().list_for_conductor(self.conductor_id()):
            table.insert(
                "",
                "end",
                values=(
                    trip.get("public_id") or str(trip.get("_id")),
                    trip.get("vehicle_id", ""),
                    trip.get("route_id", ""),
                    trip.get("date", ""),
                    trip.get("status", ""),
                ),
            )

    def show_collection_form(self):
        body = self.page("Log Collection")
        trip_id = labeled_entry(body, "Trip ID", 0)
        vehicle_id = labeled_entry(body, "Vehicle ID", 1)
        amount = labeled_entry(body, "Amount Collected", 2)
        tk.Button(
            body,
            text="Save Collection",
            command=lambda: self.save_collection(trip_id.get(), vehicle_id.get(), amount.get()),
            bg=styles.PRIMARY,
            fg=styles.WHITE,
            relief="flat",
            padx=16,
            pady=8,
        ).grid(row=3, column=1, sticky="e", padx=8, pady=10)

    def save_collection(self, trip_id, vehicle_id, amount):
        try:
            CollectionController().log_collection(trip_id, vehicle_id, self.conductor_id(), amount)
            messagebox.showinfo("Collection saved", "Trip collection logged successfully.")
        except Exception as exc:
            messagebox.showerror("Save failed", str(exc))

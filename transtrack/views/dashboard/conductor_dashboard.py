import tkinter as tk
from tkinter import messagebox

from transtrack.controllers.collection_controller import CollectionController
from transtrack.controllers.conductor_controller import ConductorController
from transtrack.controllers.trip_controller import TripController
from transtrack.controllers.vehicle_controller import VehicleController
from transtrack.utils.session import get_current_user
from transtrack.utils.numbers import to_float
from transtrack.utils.relations import reference_query
from transtrack.views import styles
from transtrack.views.collections_view import CollectionsView
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.expenses_view import ExpensesView
from transtrack.views.lookups import display_value
from transtrack.views.widgets import format_id, labeled_entry, make_table, metric_card


class ConductorDashboard(BaseDashboard):
    title = "Conductor Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("My Trips", self.show_trips),
            ("Assigned Vehicle", self.show_vehicle),
            ("My Collections", self.show_collections),
            ("Collections", lambda: self.show_view("Collections", CollectionsView)),
            ("Expenses", lambda: self.show_view("Expenses", ExpensesView)),
            ("Log Collection", self.show_collection_form),
        )
        super().__init__(master, on_logout)

    def show_view(self, title, view_class):
        body = self.page(title)
        view_class(body).pack(fill="both", expand=True)

    def conductor_id(self):
        return (get_current_user() or {}).get("linked_id")

    def current_conductor(self):
        conductor_id = self.conductor_id()
        return ConductorController().get(conductor_id) if conductor_id else None

    def assigned_vehicle_id(self):
        conductor = self.current_conductor() or {}
        return conductor.get("assigned_vehicle")

    def my_trips(self):
        conductor_id = self.conductor_id()
        return TripController().list_for_conductor(conductor_id) if conductor_id else []

    def show_home(self):
        body = self.page("Conductor Dashboard")
        trips = self.my_trips()
        active = [trip for trip in trips if trip.get("status") != "Completed"]
        collections = (
            CollectionController().list_all(reference_query("conductor_id", "conductors", self.conductor_id()))
            if self.conductor_id()
            else []
        )
        total = sum(to_float(row.get("amount_collected")) for row in collections)
        cards = (
            ("Assigned Trips", len(trips), styles.SUCCESS_BG, styles.SUCCESS_FG),
            ("Active Trips", len(active), styles.ACCENT_SOFT, styles.ACCENT),
            ("Collections", len(collections), styles.SURFACE_SOFT, styles.TEXT),
            ("Collected Total", f"{total:,.0f}", styles.SUCCESS_BG, styles.SUCCESS_FG),
        )
        grid = tk.Frame(body, bg=styles.WHITE)
        grid.pack(anchor="nw", fill="x")
        for index, (label, value, bg, fg) in enumerate(cards):
            card = metric_card(grid, label, value, bg, fg)
            card.grid(row=0, column=index, sticky="ew", padx=8, pady=8)
            grid.columnconfigure(index, weight=1)

    def show_trips(self):
        body = self.page("My Trips")
        table = make_table(body, ("id", "vehicle_id", "route_id", "date", "status"))
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
                ),
            )

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

    def show_collections(self):
        body = self.page("My Collections")
        table = make_table(body, ("id", "trip_id", "vehicle_id", "amount_collected", "date"))
        collections = CollectionController().list_all(
            reference_query("conductor_id", "conductors", self.conductor_id()), [("date", -1)]
        )
        for row in collections:
            table.insert(
                "",
                "end",
                values=(
                    format_id(row),
                    display_value("trip_id", row.get("trip_id", "")),
                    display_value("vehicle_id", row.get("vehicle_id", "")),
                    row.get("amount_collected", 0),
                    row.get("date", ""),
                ),
            )

    def show_collection_form(self):
        body = self.page("Log Collection")
        trip_id = labeled_entry(body, "Trip ID", 0)
        vehicle_id = labeled_entry(body, "Vehicle ID", 1, value=self.assigned_vehicle_id() or "")
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

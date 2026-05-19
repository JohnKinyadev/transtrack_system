import tkinter as tk

from transtrack.controllers.trip_controller import TripController
from transtrack.controllers.vehicle_controller import VehicleController
from transtrack.utils.relations import reference_query
from transtrack.utils.session import get_current_user
from transtrack.views import styles
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.trips_view import TripsView
from transtrack.views.widgets import metric_card


class StageManagerDashboard(BaseDashboard):
    title = "Stage Manager Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("Trips", lambda: self.show_view("Trip Management", TripsView)),
        )
        super().__init__(master, on_logout)

    def show_view(self, title, view_class):
        body = self.page(title)
        view_class(body).pack(fill="both", expand=True)

    def stage_manager_id(self):
        return (get_current_user() or {}).get("linked_id")

    def my_trips(self):
        manager_id = self.stage_manager_id()
        if manager_id:
            return TripController().list_all(reference_query("stage_manager_id", "stage_managers", manager_id), [("date", -1)])
        return TripController().list_all(sort=[("date", -1)])

    def show_home(self):
        body = self.page("Stage Manager Dashboard")
        trips = self.my_trips()
        active = [trip for trip in trips if trip.get("status") != "Completed"]
        scheduled = [trip for trip in trips if trip.get("status") == "Scheduled"]
        vehicles = VehicleController().list_all({})
        cards = (
            ("Assigned Trips", len(trips), styles.SUCCESS_BG, styles.SUCCESS_FG),
            ("Active Trips", len(active), styles.ACCENT_SOFT, styles.ACCENT),
            ("Scheduled", len(scheduled), styles.SURFACE_SOFT, styles.TEXT),
            ("Vehicles", len(vehicles), styles.SUCCESS_BG, styles.SUCCESS_FG),
        )
        grid = tk.Frame(body, bg=styles.WHITE)
        grid.pack(anchor="nw", fill="x")
        for index, (label, value, bg, fg) in enumerate(cards):
            card = metric_card(grid, label, value, bg, fg)
            card.grid(row=0, column=index, sticky="ew", padx=8, pady=8)
            grid.columnconfigure(index, weight=1)

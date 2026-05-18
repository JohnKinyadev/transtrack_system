import tkinter as tk
from datetime import datetime

from transtrack.controllers.collection_controller import CollectionController
from transtrack.controllers.deduction_controller import DeductionController
from transtrack.controllers.conductor_controller import ConductorController
from transtrack.controllers.driver_controller import DriverController
from transtrack.controllers.payout_controller import PayoutController
from transtrack.controllers.trip_controller import TripController
from transtrack.controllers.vehicle_controller import VehicleController
from transtrack.utils.session import get_current_user
from transtrack.utils.numbers import to_float
from transtrack.utils.relations import reference_query, reference_values, resolve_document
from transtrack.utils.validators import parse_date
from transtrack.views import styles
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.lookups import display_value
from transtrack.views.widgets import format_id, make_table, metric_card


class OwnerDashboard(BaseDashboard):
    title = "Owner Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("My Vehicles", self.show_vehicles),
            ("My Trips", self.show_trips),
            ("Daily Earnings", self.show_daily_earnings),
            ("Drivers & Conductors", self.show_crew),
            ("My Payouts", self.show_payouts),
            ("My Deductions", self.show_deductions),
        )
        super().__init__(master, on_logout)

    def owner_id(self):
        user = get_current_user() or {}
        return user.get("linked_id")

    def owner_vehicles(self):
        owner_id = self.owner_id()
        return VehicleController().list_for_owner(owner_id) if owner_id else []

    def owner_vehicle_ids(self):
        ids = set()
        for vehicle in self.owner_vehicles():
            ids.update(reference_values("vehicles", format_id(vehicle)))
        return ids

    def owner_crew(self, controller):
        vehicle_ids = self.owner_vehicle_ids()
        if not vehicle_ids:
            return []
        return [person for person in controller.list_all({}) if str(person.get("assigned_vehicle")) in vehicle_ids]

    def crew_for_vehicle(self, controller, vehicle):
        vehicle_ids = set(reference_values("vehicles", format_id(vehicle)))
        for person in controller.list_all({}):
            if str(person.get("assigned_vehicle")) in vehicle_ids:
                return person
        return None

    def owner_trips(self):
        vehicle_ids = self.owner_vehicle_ids()
        if not vehicle_ids:
            return []
        return TripController().list_all({"vehicle_id": {"$in": list(vehicle_ids)}}, [("date", -1)])

    def total_collections(self, vehicles):
        controller = CollectionController()
        total = 0
        for vehicle in vehicles:
            ids = reference_values("vehicles", format_id(vehicle))
            total += sum(to_float(row.get("amount_collected")) for row in controller.list_all({"vehicle_id": {"$in": ids}}))
        return total

    def trips_today_for_vehicle(self, vehicle):
        today = datetime.now().date()
        count = 0
        for trip in TripController().list_for_vehicle(format_id(vehicle)):
            try:
                trip_date = parse_date(trip.get("date"))
            except ValueError:
                continue
            if trip_date == today:
                count += 1
        return count

    def expected_revenue_for_vehicle(self, vehicle):
        route_id = vehicle.get("route_id")
        if not route_id:
            return 0
        route = resolve_document("routes", route_id)
        return to_float((route or {}).get("expected_revenue"))

    def daily_earning_for_vehicle(self, vehicle):
        return self.trips_today_for_vehicle(vehicle) * self.expected_revenue_for_vehicle(vehicle)

    def show_home(self):
        body = self.page("Owner Dashboard")
        owner_id = self.owner_id()
        vehicles = self.owner_vehicles()
        gross = self.total_collections(vehicles)
        deductions = DeductionController().total_for_owner(owner_id) if owner_id else 0
        drivers = self.owner_crew(DriverController())
        conductors = self.owner_crew(ConductorController())
        trips = self.owner_trips()
        cards = (
            ("Vehicles", len(vehicles), styles.SUCCESS_BG, styles.SUCCESS_FG),
            ("Drivers", len(drivers), styles.ACCENT_SOFT, styles.ACCENT),
            ("Conductors", len(conductors), styles.SURFACE_SOFT, styles.TEXT),
            ("Trips", len(trips), styles.SUCCESS_BG, styles.SUCCESS_FG),
            ("Gross Collections", f"{gross:,.0f}", styles.SUCCESS_BG, styles.SUCCESS_FG),
            ("Deductions", f"{deductions:,.0f}", styles.ACCENT_SOFT, styles.ACCENT),
            ("Estimated Net", f"{gross - deductions:,.0f}", styles.SURFACE_SOFT, styles.TEXT),
        )
        grid = tk.Frame(body, bg=styles.WHITE)
        grid.pack(anchor="nw", fill="x")
        for index, (label, value, bg, fg) in enumerate(cards):
            card = metric_card(grid, label, value, bg, fg)
            card.grid(row=index // 3, column=index % 3, sticky="ew", padx=8, pady=8)
            grid.columnconfigure(index % 3, weight=1)

    def show_vehicles(self):
        body = self.page("My Vehicles")
        table = make_table(
            body,
            ("id", "plate", "make", "model", "driver_id", "conductor_id", "route_id", "trips_today", "status"),
        )
        for vehicle in self.owner_vehicles():
            driver = self.crew_for_vehicle(DriverController(), vehicle)
            conductor = self.crew_for_vehicle(ConductorController(), vehicle)
            table.insert(
                "",
                "end",
                values=(
                    format_id(vehicle),
                    vehicle.get("plate", ""),
                    vehicle.get("make", ""),
                    vehicle.get("model", ""),
                    display_value("driver_id", format_id(driver)) if driver else "",
                    display_value("conductor_id", format_id(conductor)) if conductor else "",
                    display_value("route_id", vehicle.get("route_id", "")),
                    self.trips_today_for_vehicle(vehicle),
                    vehicle.get("status", ""),
                ),
            )

    def show_daily_earnings(self):
        body = self.page("Daily Earnings")
        table = make_table(body, ("id", "plate", "route_id", "trips_today", "expected_revenue", "net_payout"))
        for vehicle in self.owner_vehicles():
            expected = self.expected_revenue_for_vehicle(vehicle)
            trips_today = self.trips_today_for_vehicle(vehicle)
            table.insert(
                "",
                "end",
                values=(
                    format_id(vehicle),
                    vehicle.get("plate", ""),
                    display_value("route_id", vehicle.get("route_id", "")),
                    trips_today,
                    f"{expected:,.2f}",
                    f"{trips_today * expected:,.2f}",
                ),
            )

    def show_trips(self):
        body = self.page("My Trips")
        table = make_table(body, ("id", "vehicle_id", "driver_id", "conductor_id", "route_id", "date", "status"))
        for trip in self.owner_trips():
            table.insert(
                "",
                "end",
                values=(
                    format_id(trip),
                    display_value("vehicle_id", trip.get("vehicle_id", "")),
                    display_value("driver_id", trip.get("driver_id", "")),
                    display_value("conductor_id", trip.get("conductor_id", "")),
                    display_value("route_id", trip.get("route_id", "")),
                    trip.get("date", ""),
                    trip.get("status", ""),
                ),
            )

    def show_crew(self):
        body = self.page("Drivers & Conductors")
        tk.Label(body, text="Drivers", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(anchor="w")
        drivers_frame = tk.Frame(body, bg=styles.WHITE)
        drivers_frame.pack(fill="both", expand=True, pady=(8, 0))
        drivers_table = make_table(drivers_frame, ("id", "full_name", "license_no", "contact", "assigned_vehicle"))
        for driver in self.owner_crew(DriverController()):
            drivers_table.insert(
                "",
                "end",
                values=(
                    format_id(driver),
                    driver.get("full_name", ""),
                    driver.get("license_no", ""),
                    driver.get("contact", ""),
                    display_value("assigned_vehicle", driver.get("assigned_vehicle", "")),
                ),
            )

        tk.Label(body, text="Conductors", bg=styles.WHITE, fg=styles.TEXT, font=styles.FONT_HEADING).pack(
            anchor="w", pady=(18, 0)
        )
        conductors_frame = tk.Frame(body, bg=styles.WHITE)
        conductors_frame.pack(fill="both", expand=True, pady=(8, 0))
        conductors_table = make_table(conductors_frame, ("id", "full_name", "contact", "assigned_vehicle"))
        for conductor in self.owner_crew(ConductorController()):
            conductors_table.insert(
                "",
                "end",
                values=(
                    format_id(conductor),
                    conductor.get("full_name", ""),
                    conductor.get("contact", ""),
                    display_value("assigned_vehicle", conductor.get("assigned_vehicle", "")),
                ),
            )

    def show_payouts(self):
        body = self.page("My Payouts")
        table = make_table(body, ("id", "period", "gross_earnings", "total_deductions", "net_payout", "date"))
        for payout in PayoutController().list_all(reference_query("owner_id", "owners", self.owner_id()), [("date", -1)]):
            table.insert(
                "",
                "end",
                values=(
                    format_id(payout),
                    payout.get("period", ""),
                    payout.get("gross_earnings", 0),
                    payout.get("total_deductions", 0),
                    payout.get("net_payout", 0),
                    payout.get("date", ""),
                ),
            )

    def show_deductions(self):
        body = self.page("My Deductions")
        table = make_table(body, ("id", "type", "amount", "date", "reason"))
        for deduction in DeductionController().list_all(
            reference_query("owner_id", "owners", self.owner_id()), [("date", -1)]
        ):
            table.insert(
                "",
                "end",
                values=(
                    format_id(deduction),
                    deduction.get("type", ""),
                    deduction.get("amount", 0),
                    deduction.get("date", ""),
                    deduction.get("reason", ""),
                ),
            )

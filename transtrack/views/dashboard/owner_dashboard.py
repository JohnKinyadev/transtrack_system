import tkinter as tk

from transtrack.controllers.collection_controller import CollectionController
from transtrack.controllers.deduction_controller import DeductionController
from transtrack.controllers.payout_controller import PayoutController
from transtrack.controllers.vehicle_controller import VehicleController
from transtrack.utils.session import get_current_user
from transtrack.views import styles
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.widgets import make_table


class OwnerDashboard(BaseDashboard):
    title = "Owner Portal"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("My Vehicles", self.show_vehicles),
            ("My Payouts", self.show_payouts),
            ("My Deductions", self.show_deductions),
        )
        super().__init__(master, on_logout)

    def owner_id(self):
        user = get_current_user() or {}
        return user.get("linked_id")

    def show_home(self):
        body = self.page("Owner Dashboard")
        owner_id = self.owner_id()
        vehicles = VehicleController().list_for_owner(owner_id) if owner_id else []
        gross = sum(CollectionController().total_for_vehicle(vehicle["_id"]) for vehicle in vehicles)
        deductions = DeductionController().total_for_owner(owner_id) if owner_id else 0
        for label, value in (
            ("Vehicles", len(vehicles)),
            ("Gross Collections", gross),
            ("Deductions", deductions),
            ("Estimated Net", gross - deductions),
        ):
            card = tk.Frame(body, bg="#ecfdf5", padx=18, pady=14)
            card.pack(side="left", padx=8, pady=8)
            tk.Label(card, text=label, bg="#ecfdf5", fg=styles.MUTED).pack(anchor="w")
            tk.Label(card, text=str(value), bg="#ecfdf5", fg=styles.TEXT, font=("Segoe UI", 18, "bold")).pack(anchor="w")

    def show_vehicles(self):
        body = self.page("My Vehicles")
        table = make_table(body, ("id", "plate", "make", "model", "capacity", "status"))
        for vehicle in VehicleController().list_for_owner(self.owner_id()):
            table.insert(
                "",
                "end",
                values=(
                    vehicle.get("public_id") or str(vehicle.get("_id"))[-6:],
                    vehicle.get("plate", ""),
                    vehicle.get("make", ""),
                    vehicle.get("model", ""),
                    vehicle.get("capacity", ""),
                    vehicle.get("status", ""),
                ),
            )

    def show_payouts(self):
        body = self.page("My Payouts")
        table = make_table(body, ("id", "period", "gross_earnings", "total_deductions", "net_payout", "date"))
        for payout in PayoutController().list_all({"owner_id": self.owner_id()}, [("date", -1)]):
            table.insert(
                "",
                "end",
                values=(
                    payout.get("public_id") or str(payout.get("_id"))[-6:],
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
        for deduction in DeductionController().list_all({"owner_id": self.owner_id()}, [("date", -1)]):
            table.insert(
                "",
                "end",
                values=(
                    deduction.get("public_id") or str(deduction.get("_id"))[-6:],
                    deduction.get("type", ""),
                    deduction.get("amount", 0),
                    deduction.get("date", ""),
                    deduction.get("reason", ""),
                ),
            )

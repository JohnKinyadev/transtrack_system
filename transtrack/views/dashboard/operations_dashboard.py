from transtrack.views.collections_view import CollectionsView
from transtrack.views.conductors_view import ConductorsView
from transtrack.views.dashboard.admin_dashboard import AdminDashboard
from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.drivers_view import DriversView
from transtrack.views.expenses_view import ExpensesView
from transtrack.views.reports_view import ReportsView
from transtrack.views.routes_view import RoutesView
from transtrack.views.trips_view import TripsView
from transtrack.views.vehicles_view import VehiclesView


class OperationsDashboard(AdminDashboard):
    title = "Operations Workspace"

    def __init__(self, master, on_logout):
        self.menu_items = (
            ("Dashboard", self.show_home),
            ("Routes", lambda: self.show_view("Routes", RoutesView)),
            ("Vehicles", lambda: self.show_view("Vehicle Overview", VehiclesView)),
            ("Drivers", lambda: self.show_view("Driver Management", DriversView)),
            ("Conductors", lambda: self.show_view("Conductor Management", ConductorsView)),
            ("Trips", lambda: self.show_view("Trip Assignments", TripsView)),
            ("Collections", lambda: self.show_view("Collections", CollectionsView)),
            ("Expenses", lambda: self.show_view("Expenses", ExpensesView)),
            ("Reports", lambda: self.show_view("Operations Reports", ReportsView)),
        )
        BaseDashboard.__init__(self, master, on_logout)

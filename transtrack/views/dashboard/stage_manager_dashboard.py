from transtrack.views.dashboard.base_dashboard import BaseDashboard
from transtrack.views.trips_view import TripsView


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

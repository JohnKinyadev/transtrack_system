import tkinter as tk

from transtrack.config import APP_NAME
from transtrack.views.dashboard.admin_dashboard import AdminDashboard
from transtrack.views.dashboard.conductor_dashboard import ConductorDashboard
from transtrack.views.dashboard.driver_dashboard import DriverDashboard
from transtrack.views.dashboard.operations_dashboard import OperationsDashboard
from transtrack.views.dashboard.owner_dashboard import OwnerDashboard
from transtrack.views.login_view import LoginView
from transtrack.views.widgets import clear_frame


class TransTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1200x760")
        self.minsize(980, 640)
        self.show_login()

    def show_login(self):
        clear_frame(self)
        LoginView(self, self.show_dashboard).pack(fill="both", expand=True)

    def show_dashboard(self, user):
        clear_frame(self)
        role = user.get("role")
        dashboards = {
            "admin": AdminDashboard,
            "operations": OperationsDashboard,
            "owner": OwnerDashboard,
            "driver": DriverDashboard,
            "conductor": ConductorDashboard,
        }
        dashboard_class = dashboards.get(role, OwnerDashboard)
        dashboard_class(self, self.show_login).pack(fill="both", expand=True)

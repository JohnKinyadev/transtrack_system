from transtrack.config import TRIP_STATUSES
from transtrack.controllers.trip_controller import TripController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import conductor_options, driver_options, route_options, vehicle_options


class TripsView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "vehicle_id", "label": "Vehicle", "type": "select", "values": vehicle_options, "relation": True},
            {"key": "driver_id", "label": "Driver", "type": "select", "values": driver_options, "relation": True},
            {"key": "conductor_id", "label": "Conductor", "type": "select", "values": conductor_options, "relation": True},
            {"key": "route_id", "label": "Route", "type": "select", "values": route_options, "relation": True},
            {"key": "date", "label": "Date", "type": "date"},
            {"key": "departure_time", "label": "Departure Time"},
            {"key": "arrival_time", "label": "Arrival Time"},
            {"key": "status", "label": "Status", "type": "select", "values": TRIP_STATUSES},
        ]
        columns = (
            "id",
            "vehicle_id",
            "driver_id",
            "conductor_id",
            "route_id",
            "date",
            "status",
            "departure_time",
            "arrival_time",
        )
        super().__init__(master, TripController(), "Trip", fields, columns)

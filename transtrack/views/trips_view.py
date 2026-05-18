from datetime import datetime

from transtrack.config import TRIP_STATUSES
from transtrack.controllers.trip_controller import TripController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import conductor_options, driver_options, route_options, vehicle_options


class TripsView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "vehicle_id", "label": "Vehicle", "type": "select", "values": vehicle_options, "relation": True},
            {
                "key": "driver_id",
                "label": "Driver",
                "type": "select",
                "values": driver_options,
                "relation": True,
                "readonly": True,
            },
            {
                "key": "conductor_id",
                "label": "Conductor",
                "type": "select",
                "values": conductor_options,
                "relation": True,
                "readonly": True,
            },
            {
                "key": "route_id",
                "label": "Route",
                "type": "select",
                "values": route_options,
                "relation": True,
                "readonly": True,
            },
            {"key": "date", "label": "Date", "type": "date", "value": datetime.now().strftime("%Y-%m-%d"), "readonly": True},
            {"key": "status", "label": "Status", "type": "select", "values": TRIP_STATUSES, "value": "Scheduled", "readonly": True},
        ]
        detail_columns = (
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
        columns = ("id", "vehicle_id", "driver_id", "route_id", "date", "status")
        autofill_rules = [
            {"trigger": "vehicle_id", "mode": "copy", "collection": "vehicles", "fields": {"route_id": "route_id"}},
            {
                "trigger": "vehicle_id",
                "mode": "lookup",
                "collection": "drivers",
                "match_field": "assigned_vehicle",
                "target": "driver_id",
            },
            {
                "trigger": "vehicle_id",
                "mode": "lookup",
                "collection": "conductors",
                "match_field": "assigned_vehicle",
                "target": "conductor_id",
            },
        ]
        super().__init__(master, TripController(), "Trip", fields, columns, detail_columns, autofill_rules)

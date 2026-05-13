from transtrack.controllers.collection_controller import CollectionController
from transtrack.views.crud_view import CrudView
from transtrack.views.lookups import conductor_options, trip_options, vehicle_options


class CollectionsView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "trip_id", "label": "Trip", "type": "select", "values": trip_options, "relation": True},
            {"key": "vehicle_id", "label": "Vehicle", "type": "select", "values": vehicle_options, "relation": True},
            {"key": "conductor_id", "label": "Conductor", "type": "select", "values": conductor_options, "relation": True},
            {"key": "amount_collected", "label": "Amount Collected"},
            {"key": "date", "label": "Date", "type": "date"},
        ]
        detail_columns = ("id", "trip_id", "vehicle_id", "conductor_id", "amount_collected", "date")
        columns = ("id", "vehicle_id", "conductor_id", "amount_collected", "date")
        autofill_rules = [
            {
                "trigger": "trip_id",
                "mode": "copy",
                "collection": "trips",
                "fields": {"vehicle_id": "vehicle_id", "conductor_id": "conductor_id"},
            },
            {
                "trigger": "vehicle_id",
                "mode": "lookup",
                "collection": "conductors",
                "match_field": "assigned_vehicle",
                "target": "conductor_id",
            },
        ]
        super().__init__(master, CollectionController(), "Collection", fields, columns, detail_columns, autofill_rules)

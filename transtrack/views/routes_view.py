from transtrack.controllers.route_controller import RouteController
from transtrack.views.crud_view import CrudView


class RoutesView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "name", "label": "Route Name"},
            {"key": "origin", "label": "Origin"},
            {"key": "destination", "label": "Destination"},
            {"key": "stages", "label": "Stages"},
            {"key": "fare_structure", "label": "Fare Structure"},
            {"key": "expected_revenue", "label": "Expected Revenue"},
        ]
        detail_columns = ("id", "name", "origin", "destination", "stages", "fare_structure", "expected_revenue")
        columns = ("id", "name", "origin", "destination", "expected_revenue")
        super().__init__(master, RouteController(), "Route", fields, columns, detail_columns)

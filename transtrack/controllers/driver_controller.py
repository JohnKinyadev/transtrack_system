from transtrack.controllers.base_controller import BaseController


class DriverController(BaseController):
    collection_name = "drivers"
    module_name = "drivers"
    id_prefix = "D"
    reference_fields = {
        "assigned_vehicle": {"collection": "vehicles", "label": "Assigned Vehicle ID"},
    }
    future_date_fields = {"license_expiry": "License expiry"}

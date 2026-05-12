from transtrack.controllers.base_controller import BaseController


class ConductorController(BaseController):
    collection_name = "conductors"
    module_name = "conductors"
    id_prefix = "C"
    reference_fields = {
        "assigned_vehicle": {"collection": "vehicles", "label": "Assigned Vehicle ID"},
    }

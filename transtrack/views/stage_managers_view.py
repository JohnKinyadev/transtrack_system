from transtrack.controllers.stage_manager_controller import StageManagerController
from transtrack.views.crud_view import CrudView


class StageManagersView(CrudView):
    def __init__(self, master):
        fields = [
            {"key": "full_name", "label": "Full Name"},
            {"key": "contact", "label": "Contact"},
            {"key": "stage_name", "label": "Stage Name", "optional": True},
        ]
        detail_columns = ("id", "full_name", "contact", "stage_name")
        columns = ("id", "full_name", "contact", "stage_name")
        super().__init__(master, StageManagerController(), "Stage Manager", fields, columns, detail_columns)

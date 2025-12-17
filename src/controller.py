
class Controller:
    def __init__(self, view, app):
        self._view = view
        self._app = app



    def submitEquipment(self, equipment: dict):
        self._app.submitEquipmentToDatabase(equipment)
        self._view.refreshMainContent('inventory')


    def submitRequest(self, request: dict):
        self._app.submitRequestToDatabase(request)

    def cancelRequest(self, request: dict):
        self._app.cancelRequestFromDatabase(request)

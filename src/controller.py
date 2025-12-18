
class Controller:
    def __init__(self, view, app):
        self._view = view
        self._app = app

    """
    USER
    """
    def submitUserdata(self, userdata: dict):
        self._app.submitUserDataToDatabase(userdata)

    def updateUserdata(self, userdata: dict):
        self._app.updateUserDataFromDatabase(userdata)

    def deleteUserdata(self, userdata: dict):
        self._app.deleteUserFromDatabase(userdata)


    """
    EQUIPMENT
    """
    def submitEquipment(self, equipment: dict):
        self._app.submitEquipmentToDatabase(equipment)
        self._view.refreshMainContent('inventory')

    def deleteEquipment(self, equipment: dict) -> bool:
        return self._app.deleteEquipmentFromDatabase(equipment)


    """
    REQUEST
    """
    def submitRequest(self, request: dict):
        self._app.submitRequestToDatabase(request)

    def cancelRequest(self, request: dict):
        self._app.cancelRequestFromDatabase(request)

    def validateRequest(self, request: dict):
        self._app.validateRequestFromDatabase(request)
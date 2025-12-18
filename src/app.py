from src.model.equipment_repository import EquipmentRepository
from src.model.request_repository import RequestRepository
from src.model.user_repository import UserRepository


class App:
    def __init__(self):
        ...

    """
    USER
    """
    @classmethod
    def submitUserDataToDatabase(cls, userdata: dict):
        UserRepository.addUser(userdata)

    @classmethod
    def updateUserDataFromDatabase(cls, userdata: dict):
        UserRepository.updateUser(userdata)

    @classmethod
    def deleteUserFromDatabase(cls, userdata: dict):
        UserRepository.deleteUser(userdata)

    """
    EQUIPMENT
    """
    # CREATE
    @classmethod
    def submitEquipmentToDatabase(cls, equipment):
        EquipmentRepository.addEquipment(equipment)

    # DELETE
    @classmethod
    def deleteEquipmentFromDatabase(cls, equipment: dict) -> bool:
        return EquipmentRepository.deleteEquipment(equipment)


    """
    REQUEST
    """
    # CREATE
    @classmethod
    def submitRequestToDatabase(cls, request):
        RequestRepository.addRequest(request)

    # UPDATE
    @classmethod
    def validateRequestFromDatabase(cls, request: dict):
        RequestRepository.validateUserRequest(request)

    # DELETE
    @classmethod
    def cancelRequestFromDatabase(cls, request: dict):
        RequestRepository.deleteUserRequest(request)

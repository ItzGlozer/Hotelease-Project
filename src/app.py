from src.model.equipment_repository import EquipmentRepository
from src.model.request_repository import RequestRepository


class App:
    def __init__(self):
        ...

    @classmethod
    def submitEquipmentToDatabase(cls, equipment):
        EquipmentRepository.addEquipment(equipment)

    @classmethod
    def submitRequestToDatabase(cls, request):
        RequestRepository.addRequest(request)

    @classmethod
    def cancelRequestFromDatabase(cls, request: dict):
        RequestRepository.deleteUserRequest(request)

from src.model.database import Database


class EquipmentRepository:

    @staticmethod
    def addEquipment(data: dict):
        cursor = Database.get_cursor()
        query = "INSERT INTO `equipment`(`name`, `quantity`) VALUES (%s, %s)"
        cursor.execute(query, (data['name'], data['quantity'],))
        Database.commit()
        Database.close()

    @staticmethod
    def fetch_equipment(name: str) -> dict:
        ...

    @staticmethod
    def fetchAll(is_dictionary=True) -> list[dict | tuple] :
        cursor = Database.get_cursor(is_dictionary)
        cursor.execute("SELECT * FROM equipment")
        equipments = cursor.fetchall()
        Database.close()
        return equipments

    @staticmethod
    def fetchAllLowStocks(is_dictionary=True) -> list[dict | tuple]:
        cursor = Database.get_cursor(is_dictionary)
        cursor.execute("SELECT * FROM equipment WHERE `quantity` <= 20")
        equipments = cursor.fetchall()
        Database.close()
        return equipments






if __name__ == '__main__':

    equipment = {"name": "sample", "quantity": 20}
    # EquipmentRepository.addEquipment(equipment)


    items = EquipmentRepository.fetchAll()
    print(type(items))
    for item in items:
        # Loop through the keys of the current dictionary
        print(item)



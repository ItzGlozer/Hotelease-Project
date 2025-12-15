from src.model.database import Database


class EquipmentRepository:

    @staticmethod
    def fetchAll():
        cursor = Database.get_cursor()
        cursor.execute("SELECT * FROM equipment")
        equipments = cursor.fetchall()
        Database.connect().close()
        return equipments






if __name__ == '__main__':
    result = EquipmentRepository.fetchAll()

    for dict_item in result:
        # Loop through the keys of the current dictionary
        for i, key in enumerate(dict_item.keys()):
            print(f"{i} | Key: {key}, Value: {dict_item[key]}")
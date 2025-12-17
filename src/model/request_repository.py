from src.model.database import Database


class RequestRepository:

    @staticmethod
    def addRequest(request: dict):
        cursor = Database.get_cursor()
        query = """INSERT INTO `request`(`requested_by_id`, `equipment_id`, `quantity`,`entry_type`) 
                   VALUES (%s, %s, %s, %s);"""
        cursor.execute(query, (request["user_id"], request["item_id"], request["quantity"], request["type"],))
        Database.commit()
        Database.close()

    @staticmethod
    def fetchAllRequests() -> list:
        cursor = Database.get_cursor()
        query = "SELECT * FROM `request`;"
        cursor.execute(query)
        requests = cursor.fetchall()
        Database.close()
        return requests

    @staticmethod
    def fetchUserRequests(user_id: int):
        cursor = Database.get_cursor()
        query = """
        SELECT
            r.id,
            e.name,
            r.quantity,
            r.entry_type,
            r.status,
            IFNULL(CONCAT(u1.firstname, ' ', u1.lastname), 'Not Approved') AS approved_by_name,
            r.requested_at,
            r.approved_at
        FROM request r
        JOIN equipment e on r.equipment_id = e.id
        LEFT JOIN user u1 ON r.approved_by_id = u1.id
        WHERE r.requested_by_id = %s;
        """
        cursor.execute(query, (user_id,))
        requests = cursor.fetchall()
        Database.close()
        return requests


    @staticmethod
    def deleteUserRequest(request: dict):
        cursor = Database.get_cursor()
        query = "DELETE FROM request where id = %s;"
        cursor.execute(query, (request["id"],))
        Database.commit()
        Database.close()


if __name__ == '__main__':
    data = {
        "user_id": 1,
        "item_id": 1,
        "type": 'stock in',
        "quantity": 2
    }
    # RequestRepository.addRequest(data)
    results = RequestRepository.fetchUserRequests(2)
    print(results)

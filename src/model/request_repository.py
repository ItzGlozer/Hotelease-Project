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
        query = """
        SELECT
            r.id,
            e.name AS equipment_name,
            r.quantity,
            r.entry_type,
            r.status,
            CONCAT(u1.firstname, ' ', u1.lastname) AS requested_by,
            CONCAT(u2.firstname, ' ', u2.lastname) AS validated_by,
            r.requested_at,
            r.approved_at
        FROM request r
        JOIN equipment e ON r.equipment_id = e.id
        JOIN `user` u1 ON r.requested_by_id = u1.id
        LEFT JOIN `user` u2 ON r.approved_by_id = u2.id;
        """
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
    def validateUserRequest(request: dict):
        cursor = Database.get_cursor()
        query = """
        UPDATE `request`
        SET `status`=%s, `approved_by_id`=%s, approved_at=CURRENT_TIMESTAMP
        WHERE `id`=%s;"""
        cursor.execute(query, (request['status'], request['user_id'], request['id'],))
        Database.commit()
        Database.close()

    @staticmethod
    def deleteUserRequest(request: dict):
        cursor = Database.get_cursor()
        query = "DELETE FROM request where id = %s;"
        cursor.execute(query, (request["id"],))
        Database.commit()
        Database.close()




if __name__ == '__main__':
    create_request = {
        "user_id": 1,
        "item_id": 1,
        "type": 'stock in',
        "quantity": 2
    }
    # RequestRepository.addRequest(create_request)

    validate_request = {
        'id': 6,
        'user_id': 1,
        'status': 'approved'
    }
    # RequestRepository.validateUserRequest(validate_request)


    # results = RequestRepository.fetchUserRequests(2)
    # print(results)

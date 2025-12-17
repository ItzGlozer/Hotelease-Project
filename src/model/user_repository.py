from src.model.database import Database


class UserRepository:


    @staticmethod
    def addUser(userdata: dict):
        cursor = Database.get_cursor()
        query = """INSERT INTO users (`username`, `password`, `firstname`, `lastname`) 
                   VALUES (?, ?, ?, ?)
                """
        cursor.execute(query,)


    @staticmethod
    def validateCredentials(userdata: dict) -> dict:
        cursor = Database.get_cursor()
        query = 'SELECT * FROM user WHERE username = %s AND password = %s'
        cursor.execute(query, (userdata['username'], userdata['password']))
        return cursor.fetchone()

    @staticmethod
    def fetchAll():
        cursor = Database.get_cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        Database.connect().close()
        return users







if __name__ == '__main__':
    credentials = {
        "username": "admin",
        "password": "admin123"
    }

    result = UserRepository.validateCredentials(credentials)






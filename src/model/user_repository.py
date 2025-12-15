from src.model.database import Database


class UserRepository:

    @staticmethod
    def validateCredentials(credentials: dict):
        cursor = Database.get_cursor()
        query = 'SELECT * FROM user WHERE username = %s AND password = %s'
        cursor.execute(query, (credentials['username'], credentials['password']))
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






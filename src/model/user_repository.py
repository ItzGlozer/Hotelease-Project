from src.model.database import Database


class UserRepository:

    @staticmethod
    def addUser(userdata: dict):
        username = userdata['firstname'].split(' ')[0].lower()
        password = userdata['lastname'].replace(' ', '').lower() +'123'

        cursor = Database.get_cursor()
        query = """INSERT INTO user (`username`, `password`, `firstname`, `lastname`, `role`) 
                   VALUES (%s, %s, %s, %s, %s)
                """
        cursor.execute(query,(username, password, userdata['firstname'], userdata['lastname'], userdata['role']))
        Database.commit()
        Database.close()


    @staticmethod
    def validateCredentials(userdata: dict) -> dict:
        """
        Used for logging in
        """
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

    @staticmethod
    def fetchUser(userdata: dict) -> dict:
        cursor = Database.get_cursor()
        query = 'SELECT * FROM user WHERE id = %s'
        cursor.execute(query, (userdata['id'],))
        user = cursor.fetchall()[0]
        Database.close()
        return user

    @staticmethod
    def updateUser(userdata: dict):
        cursor = Database.get_cursor()
        query = "UPDATE user SET firstname = %s, lastname = %s, role = %s WHERE id = %s"
        cursor.execute(query, (userdata['firstname'], userdata['lastname'], userdata['role'], userdata['id']))
        Database.commit()
        Database.close()

    @staticmethod
    def deleteUser(userdata: dict):
        cursor = Database.get_cursor()
        query = "DELETE FROM user WHERE id = %s"
        cursor.execute(query, (userdata['id'],))
        Database.commit()
        Database.close()






if __name__ == '__main__':
    credentials = {
        "username": "admin",
        "password": "admin123"
    }
    result = UserRepository.fetchUser({'id': '1'})
    print(result)

    # # result = UserRepository.validateCredentials(credentials)
    # username = credentials['username'].split(' ')[0].lower()
    # print(username)
    #






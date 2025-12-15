
import mysql.connector
from mysql.connector import Error


class Database:
    _conn = None

    @classmethod
    def connect(cls):
        if cls._conn is None or not cls._conn.is_connected():
            cls._conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="hotelease"
            )
        return cls._conn

    @classmethod
    def get_cursor(cls, dictionary=True):
        conn = cls.connect()
        return conn.cursor(dictionary=dictionary)

    @classmethod
    def close(cls):
        if cls._conn and cls._conn.is_connected():
            cls._conn.close()
            cls._conn = None



if __name__ == '__main__':
    cursor = Database.get_cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    print(users)
    cursor.close()
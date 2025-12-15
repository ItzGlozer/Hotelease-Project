


class UserData:
    _user_data: dict = {}

    def __new__(cls, credentials: dict = None):
        if not cls._user_data and credentials:
            cls._user_data['firstname'] = credentials.get('firstname', '')
            cls._user_data['lastname'] = credentials.get('lastname', '')
            cls._user_data['role'] = credentials.get('role', '')
        return super().__new__(cls)

    @classmethod
    @property
    def firstname(cls) -> str:
        return cls._user_data.get('firstname', '')

    @classmethod
    @property
    def lastname(cls) -> str:
        return cls._user_data.get('lastname', '')

    @classmethod
    @property
    def role(cls) -> str:
        return cls._user_data.get('role', '')



if __name__ == '__main__':
    data = {
        'firstname': 'myFirst',
        'lastname': 'myLast',
        'role': 'myRole'
    }
    UserData(data)
    set = UserData()

    result = set.firstname

    print(result)
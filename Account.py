class Account:
    def __init__(self, username=None, password=None):
        self.__username = username
        self.__password = password

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password



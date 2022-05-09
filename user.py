import os
import pwd


class User:

    def __init__(self):
        self._user = self.get_username()

    def __repr__(self):
        name = self.get_user()
        return f"User({name=})"

    def set_user(self, user):
        self._user = user

    def get_user(self):
        return self._user

    @classmethod
    def get_username(cls):
        return pwd.getpwuid(os.getuid())[0]


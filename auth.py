import json
import os

class Auth:

    FILE_NAME = "user.json"

    @staticmethod
    def login(username, password):
        if not os.path.exists(Auth.FILE_NAME) or os.path.getsize(Auth.FILE_NAME) == 0:
            return False

        try:
            with open(Auth.FILE_NAME, "r") as file:
                users = json.load(file)
        except json.JSONDecodeError:
            return False

        for user in users:
            if (
                user.get("username") == username
                and
                user.get("password") == password
            ):
                return True
        return False


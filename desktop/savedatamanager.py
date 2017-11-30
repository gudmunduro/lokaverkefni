# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 30/11/2017
from json import *


class SaveDataManager:

    def __init__(self):
        self.values = {}
        self.load()

    def load(self):
        try:
            with open(self.json_name(), "r") as json_file:
                self.values = loads(json_file.read())
        except:
            return {}

    def save(self):
        with open(self.json_name(), "w") as json_file:
            json_str = dumps(self.values)
            json_file.write(json_str)

    def json_name(self):
        """Overidde this to return name of json file"""
        return ""


class LoginDataManager(SaveDataManager):

    def set_user_info(self, username, password):
        self.values["username"] = username
        self.values["password"] = password
        self.save()

    def json_name(self):
        return "loginData.json"

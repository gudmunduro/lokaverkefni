# Lokaverkefni - Guðmundur Óli og Helgi Steinarr - 30/11/2017
from json import *
from os import path


class SaveDataManager:

    def __init__(self):
        self.values = {}
        self.load()

    def load(self):
        """Loads json file to values property"""
        try:
            if not path.isfile(self.json_name()):
                self.values = self.default_json_values()
            with open(self.json_name(), "r") as json_file:
                self.values = loads(json_file.read())
        except:
            print("Failed to load from json file")
            self.values = self.default_json_values()

    def save(self):
        """Saves values to json file"""
        try:
            with open(self.json_name(), "w") as json_file:
                json_str = dumps(self.values)
                json_file.write(json_str)
        except:
            print("Error: Writing data to file failed")

    def reset(self):
        """Resets json to default values"""
        self.values = self.default_json_values()
        self.save()

    def json_name(self):
        """Override this to return name of json file"""
        return ""

    def default_json_values(self):
        """Override this to return default json values"""
        return {}


class LoginDataManager(SaveDataManager):

    def __init__(self):
        super(LoginDataManager, self).__init__()

    @property
    def username(self):
        return self.values["username"]

    @username.setter
    def username(self, username):
        self.values["username"] = username
        self.values["userInfoSaved"] = True
        self.save()

    @property
    def password(self):
        return self.values["password"]

    @password.setter
    def password(self, password):
        self.values["password"] = password
        self.values["userInfoSaved"] = True
        self.save()

    @property
    def user_info_saved(self):
        return self.values["userInfoSaved"]

    def json_name(self):
        return "loginData.json"

    def default_json_values(self):
        return {"username": "", "password": "", "userInfoSaved": False}

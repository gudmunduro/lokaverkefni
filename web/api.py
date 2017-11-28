import pymysql.cursors
import json
from bottle import *


class ConnectAndCommit:
    def __init__(self, query):
        self.query = query
        self.connection = None
        self.cursor = None

    def est_connection(self):
        self.connection = pymysql.connect(
            user='VEF',
            password='ab123',
            host='gudmunduro.com',
            database='VEF',
            charset='utf8mb4'
        )

    def execute_n_commit(self):
        self.cursor = self.connection.cursor()
        result = self.cursor.execute(self.query)
        self.connection.commit()
        return result

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

# TODO: SQL Error checker

@route("/api/cars")
def cars():
    # Only a mock-up, not the real code.
    cac = ConnectAndCommit("SELECT * FROM cars")
    cac.est_connection()
    car_list = cac.execute_n_commit()
    cac.close_connection()
    return json.dumps({"cars": car_list})


@route("/api/login", method="post")
def login():
    login_status = 0
    if request.forms.username == "user" and request.forms.password == "ab123":
        login_status = 1
    return json_dumps({"login_status": login_status})


@route("/api/admin/login", method="post")
def admin_login():
    login_status = 0
    if request.forms.username == "admin" and request.forms.password == "ab123":
        login_status = 1
    return json_dumps({"login_status": login_status})


@route("/api/download/desktopClient")
def cars():
    return static_file("desktop.zip", root="incl/download/")

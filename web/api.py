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


class Data:
    def __init__(self):
        self.errText = None
        self.cac = None

    def try_for_mysql_errors(self, query):
        try:
            self.cac = ConnectAndCommit(query)
            self.cac.est_connection()
            self.cac.execute_n_commit()
            return True
        except pymysql.MySQLError as err:
            self.errText = ("Something went wrong :( Error: {}".format(err))
            if err.args[0] == 1062:
                self.errText = "Pöntun þegar til.. (Error: {})".format(err.args[0])
            elif err.args[0] == 1045:
                self.errText = "Tenging við gagnagrunn ekki leyfð. (Error: {})".format(err.args[0])
            elif err.args[0] == 2003:
                self.errText = "Forrit náði ekki að tengjast netinu.. " \
                               "Vinsamlegast athugaðu nettenginguna þína (Error: {})".format(err.args[0])

            return False

    def send_order(self, data_dict):
        pass

    def get_car_list(self):
        query = "SELECT * FROM car_type inner join categories on car_types.category_id = categories.cat_id"
        if self.try_for_mysql_errors(query):
            fetch = self.cac.cursor.fetchall()
            self.cac.close_connection()
            """cat_names = []
            for car in fetch:
                if self.try_for_mysql_errors("SELECT category_name FROM categories WHERE cat_id ={}".format(car[7])):
                    cat_names.append(car)
                    self.cac.close_connection()"""
            return fetch


@route("/api/cars")
def cars():
    cars = Data().get_car_list()
    return json.dumps(cars)


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

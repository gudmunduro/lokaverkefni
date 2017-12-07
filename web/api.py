import pymysql.cursors
import json
from bottle import *


class ConnectAndCommit:
    def __init__(self, query, params):
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def est_connection(self):
        self.connection = pymysql.connect(
            user='VEF',
            password='ab123',
            host='localhost',
            database='VEF',
            charset='utf8mb4'
        )

    def execute_n_commit(self, params):
        self.cursor = self.connection.cursor()
        result = self.cursor.execute(self.query, params)
        self.connection.commit()
        return result

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class Data:
    def __init__(self):
        self.errText = None
        self.cac = None

    def try_for_mysql_errors(self, query, params=(,)):
        try:
            self.cac = ConnectAndCommit(query, params)
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

    def send_order(self, customer_fullname, customer_phone, customer_email, nationality, card_number, CVN, card_exp_date, order_date, return_date, car_id, driver_id_nr):
        query = """INSERT INTO orders (customer_fullname, customer_phone, customer_email, nationality, card_number, CVN, card_exp_date, order_date, return_date, car_id, driver_id_nr)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        if self.try_for_mysql_errors(query, (customer_fullname, customer_phone, customer_email, nationality, card_number, CVN, card_exp_date, order_date, return_date, car_id, driver_id_nr)):
            self.cac.close_connection()
            return True
        self.cac.close_connection()
        return False

    def get_car_list(self):
        query = "SELECT * FROM car_types inner join categories on car_types.category_id = categories.cat_id"
        if self.try_for_mysql_errors(query):
            fetch = self.cac.cursor.fetchall()
            self.cac.close_connection()
            return fetch

def post_data_exists(*args):
    for a in args:
        if request.forms.get(a) == None:
            return False;
    return True;


@route("/api/cars")
def cars():
    cars = Data().get_car_list()
    return json.dumps(cars)


@route("/api/order")
def order():
    if not post_data_exists("customer_fullname", "customer_phone", "customer_email", "nationality", "card_number", "CVN", "card_exp_date", "order_date", "return_date", "car_id", "driver_id_nr"):
        return json.dumps({"order_status": 0, "error_msg": "Order failed"})
    Data().send_order()


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
def download_desktop_client():
    return static_file("desktop.zip", root="incl/download/")

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

    def execute_n_commit(self):
        self.cursor = self.connection.cursor()
        result = self.cursor.execute(self.query, self.params)
        self.connection.commit()
        return result

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


class Data:
    def __init__(self):
        self.errText = None
        self.cac = None

    def try_for_mysql_errors(self, query, params=tuple()):
        try:
            self.cac = ConnectAndCommit(query, params)
            self.cac.est_connection()
            self.cac.execute_n_commit()
            return True
        except pymysql.MySQLError as err:
            self.errText = ("Something went wrong :( Error: {}".format(err))
            if err.args[0] == 1062:
                self.errText = "PÃ¶ntun Ã¾egar til.. (Error: {})".format(err.args[0])
            elif err.args[0] == 1045:
                self.errText = "Tenging viÃ° gagnagrunn ekki leyfÃ°. (Error: {})".format(err.args[0])
            elif err.args[0] == 2003:
                self.errText = "Forrit nÃ¡Ã°i ekki aÃ° tengjast netinu.. " \
                               "Vinsamlegast athugaÃ°u nettenginguna Ã¾Ã­na (Error: {})".format(err.args[0])

            return False

    def send_order(self, customer_fullname, customer_phone, customer_email, nationality, card_number, CVN,
                   card_exp_date, order_date, return_date, car_id, driver_id_nr):
        query = """INSERT INTO orders (customer_fullname, customer_phone, customer_email, nationality, card_number, CVN,
         card_exp_date, order_date, return_date, car_id, driver_id_nr)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        if self.try_for_mysql_errors(query, (customer_fullname, customer_phone, customer_email, nationality,
                                             card_number, CVN, card_exp_date, order_date, return_date, car_id,
                                             driver_id_nr)):
            self.cac.close_connection()
            return True
        self.cac.close_connection()
        return False

    def remove_order(self, id):
        query = "DELETE FROM orders WHERE id = %s"
        if self.try_for_mysql_errors(query, (id,)):
            self.cac.close_connection()
            return True
        self.cac.close_connection()
        return False

    def get_order_list(self):
        query = """SELECT * FROM orders"""
        if self.try_for_mysql_errors(query):
            fetch = self.cac.cursor.fetchall()
            self.cac.close_connection()
            return fetch
        return []

    def get_car_list(self):
        query = """SELECT * FROM cars
        inner join car_types on cars.car_type = car_types.type_id
        inner join categories on car_types.category_id = categories.cat_id"""
        if self.try_for_mysql_errors(query):
            fetch = self.cac.cursor.fetchall()
            self.cac.close_connection()
            return fetch
        return []

    def get_car_info(self, id):
        query = """SELECT * FROM cars
                inner join car_types on cars.car_type = car_types.type_id
                inner join categories on car_types.category_id = categories.cat_id
                where cars.car_id = %s"""
        if self.try_for_mysql_errors(query, tuple(id)):
            fetch = self.cac.cursor.fetchall()
            self.cac.close_connection()
            return fetch
        self.cac.close_connection()
        return []


def post_data_exists(*args):
    for a in args:
        if request.forms.get(a) is None:
            return False
    return True


@route("/api/cars")
def cars():
    data = Data()
    cars = data.get_car_list()
    return json.dumps(cars)


@route("/api/car/<id>")
def car(id):
    data = Data()
    car_info = data.get_car_info(id)
    if len(car_info) > 0:
        return json_dumps(car_info[0])
    return "[]"


@route("/api/order", method="post")
def order():
    if not post_data_exists("customer_fullname", "customer_phone", "customer_email", "nationality", "card_number",
                            "CVN", "card_exp_date", "order_date", "return_date", "car_id", "driver_id_nr"):
        return json.dumps({"order_status": 0, "error_msg": "Vantar upplýsingar"})
    customer_fullname = request.forms.get("customer_fullname")
    customer_phone = request.forms.get("customer_phone")
    customer_email = request.forms.get("customer_email")
    nationality = request.forms.get("nationality")
    card_number = request.forms.get("card_number")
    CVN = request.forms.get("CVN")
    card_exp_date = request.forms.get("card_exp_date")
    order_date = request.forms.get("order_date")
    return_date = request.forms.get("return_date")
    car_id = request.forms.get("car_id")
    driver_id_nr = request.forms.get("driver_id_nr")
    data = Data()
    status = data.send_order(customer_fullname, customer_phone, customer_email, nationality, card_number, CVN, card_exp_date,
                      order_date, return_date, car_id, driver_id_nr)
    return json.dumps({"order_status": status, "error_msg": data.errText})


@route("/api/order/remove", method="post")
def remove_order():
    if request.forms.get("id") is not None:
        id = request.forms.get("id")
        data = Data()
        status = data.remove_order(id)
        return json.dumps({"status": status, "error_msg": data.errText})
    return json.dumps({"status": 0})


@route("/api/orders")
def orders():
    data = Data().get_order_list()
    print(data[0][8])
    print(data[0][9])
    new_data = [[d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], str(d[8]),
                 str(d[9]), d[10], d[11]] for d in data]
    return json.dumps(new_data)


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

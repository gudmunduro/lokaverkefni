# Lokaverkefni vef hluti - Guðmundur Óli og Helgi Steinarr
from api import *


@route("/")
def main():
    return static_file("index.html", root="./")


@route("/car_fleet")
@view("car_fleet")
def car_fleet():
    cars = Data().get_car_list()
    return dict(cars=cars)


@route("/order")
@view("order")
def order():
    cars = Data().get_car_list()
    if "selected" in request.query:
        return dict(cars=cars, selected=int(request.query["selected"]))
    return dict(cars=cars, selected=None)


@route("/order", method="post")
@view("order")
def order():
    if not post_data_exists("customer_fullname", "customer_phone", "customer_email", "nationality", "card_number",
                            "CVN", "card_exp_date", "order_date", "return_date", "car_id", "driver_id_nr"):
        return {"order_status": 0, "error_msg": "Vantar upplýsingar", "cars": Data().get_car_list()}
    customer_fullname = request.forms.get("customer_fullname")
    customer_phone = request.forms.get("customer_phone")
    customer_email = request.forms.get("customer_email")
    nationality = request.forms.nationality
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
    return {"order_status": status, "error_msg": data.errText, "cars": Data().get_car_list(), "selected": None}


@route("/incl/<file:path>")
def static(file):
    return static_file(file, root="incl/")


if __name__ == '__main__':
    # connect_to_db()
    run()

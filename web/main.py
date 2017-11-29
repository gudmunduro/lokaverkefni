# Lokaverkefni vef hluti - Guðmundur Óli og Helgi Steinarr
from api import *

@route("/car_fleet")
def car_fleet():
    cars = Data().get_car_list()
    return static_file("car_fleet.html", root="./")

@route("/")
def main():
    return static_file("index.html", root="./")

@route("/incl/<file:path>")
def static(file):
    return static_file(file, root="incl/")


if __name__ == '__main__':
    # connect_to_db()
    run()

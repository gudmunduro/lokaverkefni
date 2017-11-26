import pymysql.cursors
import json
from bottle import *


def connect_to_db():
    conn = pymysql.connect(host="gudmunduro.com",
                           user="VEF",
                           password="xb5tDSayArJNYdG6",
                           db='db',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


@route("/api/cars")
def cars():
    return json.dumps({"cars": []})


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

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

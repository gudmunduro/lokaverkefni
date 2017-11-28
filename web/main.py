# Lokaverkefni vef hluti - Guðmundur Óli og Helgi Steinarr
from api import *


@route("/")
def main():
    return static_file("index.html", root="./")

@route("/incl/<file:path>")
def static(file):
    return static_file(file, root="incl/")

if __name__ == '__main__':
    # connect_to_db()
    run()

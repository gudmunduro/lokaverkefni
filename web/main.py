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
    print("b4")
    cac = ConnectAndCommit("CREATE TABLE test_table (col1 varchar(42),col2 int(11))")
    cac.est_connection()
    cac.execute_n_commit()
    cac.close_connection()
    print("after")
    run()

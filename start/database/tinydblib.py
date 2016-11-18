#
#
#
from {{appname}}.config import database
from tinydb import TinyDB, Query

tinydb = database.get("tinydb", None)

if tinydb:
    conn_str = tinydb["dbname"]
    print(" ... setting it up for tinyDB: " + conn_str)
    tinydb = TinyDB(conn_str)
else:
    raise Exception("I had a problem setting up tinyDB")
    

    
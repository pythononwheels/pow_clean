#
#
#
from {{appname}}.config import database
from tinydb import TinyDB, Query

tinydb = database.get("tinydb", None)

if tinydb:
    conn_str = tinydb["dbname"]

    tinydb = TinyDB(conn_str)
    

    


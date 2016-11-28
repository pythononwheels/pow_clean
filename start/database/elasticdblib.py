#
# dblib for elastic 
#
from {{appname}}.config import database
from elasticsearch import Elasticsearch
import requests

elastic = database.get("elastic", None)
if elastic:
    es = Elasticsearch( [{ 'host': elastic["host"], 'port': elastic["port"]}] )

if es:
    print(" ... setting it up for Elasticsearch: " + str(es))
    res = requests.get("http://" + es["host"] + ":" + es["port"])
    print(res.content)
else:
    raise Exception("I had a problem setting up Elasticsearch")
    

    

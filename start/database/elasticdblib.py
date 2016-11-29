#
# dblib for elastic 
#
from {{appname}}.config import database
from elasticsearch import Elasticsearch
import requests

elastic = database.get("elastic", None)
es=None
if elastic:
    es = Elasticsearch( [{ 'host': elastic["host"], 'port': elastic["port"]}] )
    dbname=elastic.get("dbname", None)
if es:
    print(" ... setting it up for Elasticsearch: " + str(es))
    res = requests.get("http://" + es["host"] + ":" + es["port"])
    print(res.content)
else:
    raise Exception("I had a problem setting up a connection to Elasticsearch")
    

    
# Basic elastic  terminology:
#--------------------------------
# index ~= database
# type ~= table 
# document = yes, what you thought ;)

# create the index, ignore if the index (~= db) already exists
es.indices.create(index=elastic["dbname"], ignore=400)
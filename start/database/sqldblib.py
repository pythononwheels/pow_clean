#
#
#
from {{appname}}.config import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

sqldb = database["sql"]
conn_str = sqldb["type"] + "://" 
if sqldb["user"]:
    conn_str += sqldb["user"] 
if sqldb["passwd"]:
    conn_str += ":" + sqldb["passwd"] 
if sqldb["host"]:
    conn_str += "@" +sqldb["host"] 
if sqldb["port"]:
    conn_str += ":" +str(sqldb["port"]) 
if sqldb["dbname"]:
    conn_str += "/" + sqldb["dbname"]

engine = create_engine(conn_str)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
Transaction = Session
session = Session()

from sqlalchemy.ext.declarative import declarative_base
from {{appname}}.models.sql.basemodel import SqlBaseModel

Base = declarative_base(cls=SqlBaseModel, metadata=metadata)
Base.metadata.bind = engine


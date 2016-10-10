#
#
#
from {{appname}}.config import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


conn_str = database["type"] + "://" 
if database["user"]:
    conn_str += database["user"] 
if database["passwd"]:
    conn_str += ":" + database["passwd"] 
if database["host"]:
    conn_str += "@" +database["host"] 
if database["port"]:
    conn_str += ":" +str(database["port"]) 
if database["dbname"]:
    conn_str += "/" + database["dbname"]

engine = create_engine(conn_str)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy.ext.declarative import declarative_base
from {{appname}}.models.basemodel import BaseModel

Base = declarative_base(cls=BaseModel, metadata=metadata)
Base.metadata.bind = engine


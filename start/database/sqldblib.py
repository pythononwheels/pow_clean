#
#
#
from {{appname}}.config import database, myapp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import logging

db_log_file_name = myapp["logfile"]
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)


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

engine = create_engine(conn_str, echo=False)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
Transaction = Session
session = Session()

from sqlalchemy.ext.declarative import declarative_base
from {{appname}}.models.sql.basemodel import SqlBaseModel

Base = declarative_base(cls=SqlBaseModel, metadata=metadata)
Base.metadata.bind = engine


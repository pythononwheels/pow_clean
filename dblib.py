#
#
#
from {{appname}}.config import database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


conn_str = database["type"] + "://" + database["user"] + ":" + database["passwd"] + "@" +database["host"] + ":" +str(database["port"]) + "/" + database["name"]

engine = create_engine(conn_str)
metadata = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy.ext.declarative import declarative_base
from {{appname}}.models.basemodel import BaseModel

Base = declarative_base(cls=BaseModel, metadata=metadata)
Base.metadata.bind = engine


#
# Model
#
from sqlalchemy import Column, Integer, String, Sequence, Text
from {{appname}}.powlib import relation
from {{appname}}.dblib import Base 

#@relation.many_to_many("groups")
class User(Base):
    login = Column(String)
    password = Column(String)
    #email = Column(String)
    #test = Column(Text)
    

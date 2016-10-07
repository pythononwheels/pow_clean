#
# Model {{model_class_name}}
#
from sqlalchemy import Column, Integer, String, Boolean, Sequence
from sqlalchemy import BigInteger, Date, DateTime, Float, Numeric
from {{appname}}.powlib import relation
from {{appname}}.dblib import Base 

#@relation.has_many("<plural_other_models>")
class {{model_class_name}}(Base):
    #
    # put your column definition here:
    #
    #title = Column(String(50))
    #text = Column(String)
    
    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    # your methods down here

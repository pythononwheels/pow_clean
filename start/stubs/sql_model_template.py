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
    # 
    # sqlalchemy classic style
    # which offer you all sqlalchemy options
    #
    #title = Column(String(50))
    #text = Column(String)
    
    #
    # or the new (cerberus) schema style 
    # which offer you immediate validation 
    #
    # schema = {
    #     # string sqltypes can be TEXT or UNICODE or nothing
    #     'name': {'type': 'string', 'maxlength' : 35},
    #     'text': {'type': 'string'}
    # }

    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    # your methods down here

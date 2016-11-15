#
# TinyDB Model:  {{model_class_name}}
#
from {{appname}}.models.tinydb.basemodel import TinyBaseModel

class {{model_class_name}}(TinyBaseModel):

    #
    # Use the cerberus schema style 
    # which offer you immediate validation with cerberus
    # Remember: There are no "sql" or "sqltype" keyowrds
    # allowed since this is a TinyDB Model.
    #
    schema = {
        'text': {'type': 'string'},
        'name': {'type': 'string', 'maxlength' : 35},
        'last': {
            'type': 'number',
        }
    }


    #__table_args__ = { "extend_existing": True }

    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #

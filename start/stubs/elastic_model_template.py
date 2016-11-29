#
# Elastic Model:  {{model_class_name}}
#
from elasticsearch_dsl import DocType, String, Date, Nested, Boolean, \
    analyzer, InnerObjectWrapper, Completion
from {{appname}}.models.elastic.basemodel import ElasticBaseModel
from {{appname}}.powlib import relation

@relation.setup_elastic_schema()
class {{model_class_name}}(ElasticBaseModel):

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
            "elastic" : {    
                "analyzer"  : "snowball"
            }
        }
    }


    #__table_args__ = { "extend_existing": True }

    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)
    #
    # your model's methods down here
    #

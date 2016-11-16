
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.expression import func 
from {{appname}}.sqldblib import engine,session
from {{appname}}.powlib import pluralize
import datetime
from sqlalchemy import orm
import sqlalchemy.inspection
from cerberus import Validator
import xmltodict
import json
import datetime, decimal
from {{appname}}.config import myapp

#print ('importing module %s' % __name__)
class SqlBaseModel():
    
    #__table_args__ = { "extend_existing": True }

    id =  Column(Integer, primary_key=True)
    # create_date column will be populated with the result of the now() SQL function 
    #(which, depending on backend, compiles into NOW() or CURRENT_TIMESTAMP in most cases
    # see: http://docs.sqlalchemy.org/en/latest/core/defaults.html
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, onupdate=datetime.datetime.now, default=func.now())
    session = session

    @orm.reconstructor
    def init_on_load(self, *args, **kwargs):
        #
        # setup a mashmallow schema to be able to dump (serialize) and load (deserialize)
        # models to json quick, safe and easy.
        # see: http://marshmallow-sqlalchemy.readthedocs.io/en/latest/
        # and link it to the model. (as jsonify attribute)
        # this enables the model to load / dump json
        # 
        #print(kwargs)
        self.class_name = self.__class__.__name__.capitalize()
        from marshmallow_sqlalchemy import ModelSchema
        cls_meta=type("Meta", (object,),{"model" : self.__class__})
        jschema_class = type(self.class_name+'Schema', (ModelSchema,),
            {"Meta": cls_meta}
            )
        setattr(self, "_jsonify", jschema_class())
        self.session=session
        self.table = self.metadata.tables[pluralize(self.__class__.__name__.lower())]
        
        #
        # if there is a schema (cerberus) set it in the instance
        #
        #print(str(self.__class__.__dict__.keys()))
        if "schema" in self.__class__.__dict__:
            print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = self.__class__.__dict__["schema"]
        # add the sqlcolumns schema definitions to the cerberus schema (if there are any)
        if myapp["auto_schema"]:
            self._setup_schema_from_sql()
            

        #
        # setup values from kwargs or from init_from_<format> if format="someformat"
        # example: m = Model( data = { 'test' : 1 }, format="json")
        # will call m.init_from_json(data)
        #
        if "format" in kwargs:
            # set the format and call the according init_from_<format> method
            # which initializes the instance with the given vaules (from data)
            # e.g. Model(format=json, data={data})
            f = getattr(self, "init_from_" + kwargs["format"], None)
            if f:
                f(kwargs)
        else:
            # initializes the instanmce with the given kwargs values:
            # e.g.: Model(test="sometext", title="sometitle")
            for key in kwargs.keys():
                if key in self.__class__.__dict__:
                    setattr(self, key, kwargs[key])
        

    @declared_attr
    def __tablename__(cls):
        """ returns the tablename for this model """
        return pluralize(cls.__name__.lower())
    
    def api(self):
        """ just for conveniance """
        return self.show_api()

    def show_api(self):
        """
            prints the "external API of the class.
            No under or dunder methods
            And methods only.

            Uses inspect module.
        """
        import inspect
        print(50*"-")
        print("  external API for " + self.__class__.__name__)
        print(50*"-")
        for elem in inspect.getmembers(self, predicate=inspect.ismethod):
            meth = elem[0]

            if not meth.startswith("_"):
                print("  .. " + str(elem[0]) , end="")
                func=getattr(self,elem[0])
                if func:
                    print( str(func.__doc__)[0:100])
                else:
                    print()

    def _setup_schema_from_sql(self):
        """
            Constructs a cerberus definition schema 
            from a given sqlalchemy column definition
            for this model.
        """
        print(" .. setup schema from sql for : " + str(self.class_name))
        for idx,col in enumerate(self.table.columns.items()):
            # looks like this: 
            # ('id', 
            #  Column('id', Integer(), table=<comments>, primary_key=True, 
            #     nullable=False))
            col_type = col[1].type.python_type
            col_name = str(col[0]).lower()
            exclude_list = [elem for elem in self.schema.keys()]
            exclude_list.append( ["id", "created_at", "last_updated"] )
            #print("    #" + str(idx) + "->" + str(col_name) + " -> " + str(col_type))
            # dont check internal columns or relation columns.
            if ( col_name not in exclude_list ) and ( col[1].foreign_keys != set() ): 
                print("  .. adding to schema: " + col_name)  
                if col_type == int:
                    # sqlalchemy: Integer, BigInteger
                    # cerberus: integer
                    pass
                elif col_type == str:
                    # sqlalchemy: String, Text
                    # cerberus: string
                    # python: str
                    pass
                elif col_type == bool:
                    # sqlalchemy: Boolean
                    # cerberus: boolean
                    # python: bool
                    pass
                elif col_type == datetime.date:
                    # sqlalchemy: Date
                    # cerberus: date
                    # python: datetime.date
                    pass
                elif col_type == datetime.datetime:
                    # sqlalchemy: DateTime
                    # cerberus: datetime
                    # python: datetime.datetime
                    pass
                elif col_type == float:
                    # sqlalchemy: Float
                    # cerberus: float
                    # python: float
                    pass
                elif col_type == decimal.Decimal:
                    # sqlalchemy: Numeric
                    # cerberus: number
                    # python: decimal.Decimal
                    pass
                elif col_type == bytes:
                    # sqlalchemy: LargeBinary
                    # cerberus: binary
                    # python: bytes
                    pass
            else:
                print("  .. skipping: " + col_name )
      
    def validate(self):
        """
            checks if the instance has a schema.
            validatees the current values
        """
        if getattr(self,"schema", False):
            # if instance has a schema. (also see init_on_load)
            #v = cerberus.Validator(self.schema)
            v = Validator(self.schema)
            if v.validate(self.dict_dump()):
                return True
            else:
                return v

    def init_from_xml(self, data, root="root"):
        """
            makes a py dict from input xml and
            sets the instance attributes 
            root defines the xml root node
            
        """
        d=xmltodict.parse(data)
        d=d[root]
        for key in d:
            print("key: " + key + " : " + str(d[key]) )
            if isinstance(d[key],dict):
                print(d[key])
                for elem in d[key]:
                    if elem.startswith("#"):
                        if key in self.__class__.__dict__:
                            setattr(self, key, d[key][elem])
            else:
                if key in self.__class__.__dict__:
                    setattr(self, key, d[key])

    def init_from_json(self, data):
        """
            makes a py dict from input json and
            sets the instance attributes 
        """
        d=json.loads(data)
        for key in d:
            if key in self.__class__.__dict__:
                setattr(self, key, d[key])

    def init_from_csv(self, keys, data):
        """
            makes a py dict from input ^csv and
            sets the instance attributes 
            csv has the drawback coompared to json (or xml)
            that the data structure is flat.

            first row must be the "column names"
        """
        #assert len(keys) == len(data), raise AssertionError("keys and data must have the same lenght.")
        if not len(keys) == len(data):
            raise AssertionError("keys and data must have the same lenght.")
        for k,d in zip(keys, data):
            setattr(self, k, d)




    def json_dump(self):
        return self._jsonify.dump(self).data

    def json_load_from_db(self, data, keep_id=False):
        if keep_id:
            self = self._jsonify.load(data, session=session).data
            return self
        else:
            obj = self.__class__()
            obj = obj._jsonify.load(data, session=session).data
            obj.id = None
            return obj

    def print_schema(self):
        print(50*"-")
        print("Schema for: " + str(self.__class__))
        print("{0:30s} {1:20s}".format("Column", "Type"))
        print(50*"-")
        for col in self.__table__._columns:
            print("{0:30s} {1:20s}".format(str(col), str(col.type)))
            #print(dir(col))

    def dict_dump(self):
        d = {}
        exclude_list=["_jsonify","_sa_instance_state", "session", "schema", "table", "tree_parent_id", "tree_children"]
        if getattr(self, "exclude_list", False):
            exclude_list += self.exclude_list
        for elem in vars(self).keys():
            if not elem in exclude_list:
                d[elem] = vars(self)[elem]
        return d

    def get_relationships(self):
        """
            returns the raw relationships
            see: http://stackoverflow.com/questions/21206818/sqlalchemy-flask-get-relationships-from-a-db-model
        """
        return sqlalchemy.inspection.inspect(self.__class__).relationships

    def get_relations(self):
        """
            returns a list of the relation names
            see: http://stackoverflow.com/questions/21206818/sqlalchemy-flask-get-relationships-from-a-db-model
        """
        rels = sqlalchemy.inspection.inspect(self.__class__).relationships
        return rels.keys()

    def print_full(self):
        #
        # prints everything including related objects in FULL
        # lenghty but you see everything.
        #
        from pprint import pformat
        d = {}
        for k in self.__dict__.keys():
            if not k.startswith("_"):
                d[k] = self.__dict__.get(k)

        # add the related objects:
        for elem in self.get_relations():
            #print(elem)
            d[elem] = str(getattr(self, elem))

        return pformat(d,indent=4)

    def __repr__(self):
        #
        # __repr__ method is what happens when you look at it with the interactive prompt
        # or (unlikely: use the builtin repr() function)
        # usage: at interactive python prompt
        # p=Post()
        # p
        from pprint import pformat
        d = self.json_dump()
        return pformat(d,indent=+4)

    def __str__(self):
        #
        # The __str__ method is what happens when you print the object
        # usage:
        # p=Post()
        # print(p)
        return self.__repr__()
            
            
    def create_table(self):
        """
            created the physical table in the DB
        """
        self.__table__.create(bind=engine)

    def drop_table(self):
        """
            created the physical table in the DB
        """
        self.__table__.drop(bind=engine)
    
    def upsert(self, session=None):
        if not session:
            session = self.session
        session.add(self)
        session.commit()        

    def get(self, id):
        return self.query(self.__class__).get(id)

    def from_statement(self, statement):
        return self.query(self.__class__).from_statement(statement)

    def page(self, *criterion, limit=None, offset=None):
        res = session.query(self.__class__).filter(*criterion).limit(limit).offset(offset).all()
        return res

    def find(self,*criterion):
        return session.query(self.__class__).filter(*criterion)
    
    def find_all(self, *criterion, raw=False, as_json=False, limit=None, offset=None):
        if raw:
            return session.query(self.__class__).filter(*criterion).limit(limit).offset(offset)
        res = session.query(self.__class__).filter(*criterion).limit(limit).offset(offset).all()
        if as_json:
            return[x.json_dump() for x in res]
        return res
    
    def find_one(self, *criterion, as_json=False):
        res = session.query(self.__class__).filter(*criterion).one()
        if as_json:
            return[x.json_dump() for x in res]
        return res

    def find_first(self, *criterion, as_json=False):
        res = session.query(self.__class__).filter(*criterion).first()
        if as_json:
            return[x.json_dump() for x in res]
        return res

    def q(self):
        return session.query(self.__class__)

    def find_dynamic(self, filter_condition = [('name', 'eq', 'klaas')]):
        dynamic_filtered_query_class = DynamicFilter(query=None, model_class=self,
                                  filter_condition=filter_condition)
        dynamic_filtered_query = dynamic_filtered_query_class.return_query()
        return dynamic_filtered_query

class DynamicFilter():
    def __init__(self, query=None, model_class=None, filter_condition=None):
        #super().__init__(*args, **kwargs)
        self.query = query
        self.model_class = model_class.__class__
        self.filter_condition = filter_condition
        self.session = get_session()


    def get_query(self):
        '''
        Returns query with all the objects
        :return:
        '''
        if not self.query:
            self.query = self.session.query(self.model_class)
        return self.query


    def filter_query(self, query, filter_condition):
        '''
        Return filtered queryset based on condition.
        :param query: takes query
        :param filter_condition: Its a list, ie: [(key,operator,value)]
        operator list:
            eq for ==
            lt for <
            ge for >=
            in for in_
            like for like
            value could be list or a string
        :return: queryset
        '''

        if query is None:
            query = self.get_query()
        #model_class = self.get_model_class()  # returns the query's Model
        model_class = self.model_class
        for raw in filter_condition:
            try:
                key, op, value = raw
            except ValueError:
                raise Exception('Invalid filter: %s' % raw)
            column = getattr(model_class, key, None)
            if not column:
                raise Exception('Invalid filter column: %s' % key)
            if op == 'in':
                if isinstance(value, list):
                    filt = column.in_(value)
                else:
                    filt = column.in_(value.split(','))
            else:
                try:
                    attr = list(filter(
                        lambda e: hasattr(column, e % op),
                        ['%s', '%s_', '__%s__']
                    ))[0] % op
                except IndexError:
                    raise Exception('Invalid filter operator: %s' % op)
                if value == 'null':
                    value = None
                filt = getattr(column, attr)(value)
            query = query.filter(filt)
        return query


    def return_query(self):
        return self.filter_query(self.get_query(), self.filter_condition)
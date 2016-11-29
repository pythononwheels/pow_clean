from {{appname}}.powlib import pluralize
import datetime
from cerberus import Validator
import xmltodict
import simplejson as json
import datetime, decimal
from {{appname}}.config import myapp
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.encoders import pow_json_serializer

class ModelObject():
    """
        The BaseClass for all PoW Model Classes
    """    
    # if you need a basic schema in the class override this (see tinyDB BaseModel)
    basic_schema={}

    def init_on_load(self, *args, **kwargs):
        """
            should be called from instances or BaseModels __init__
            will be called by sqlalchemy automatically on model creation
        """
        self.tablename = pluralize(self.__class__.__name__.lower())
        
        self.setup_instance_schema()        
        
        if "format" in kwargs:
            self.setup_from_format( args, kwargs)
    
    #
    # These Methods can normally be inherited
    # 
    def setup_instance_schema(self):
        """
            if there is a schema (cerberus) set it in the instance
        """
        if "schema" in self.__class__.__dict__:
            print(" .. found a schema for: " +str(self.__class__.__name__) + " in class dict")
            self.schema = merge_two_dicts(
                self.__class__.__dict__["schema"],
                basic_schema)
        print("  .. Schema is now: " + str(self.schema))

    def setup_from_format(self, *args, **kwargs):
        """
            setup values from kwargs or from init_from_<format> if format="someformat"
            example: m = Model( data = { 'test' : 1 }, format="json")
            will call m.init_from_json(data)
        """
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
                print("{0:30s}".format("  .. " +str.strip(meth)), end="")
                #  print("  method:  " + str.strip(meth) , end="")
                func=getattr(self,meth)
                if func:
                    if func.__doc__:
                        print( "  -->  " + str.strip(func.__doc__[0:50]))
                    else:
                        #print( "             No docstring  ")
                        print()
                else:
                    print()

    def validate(self):
        """
            checks if the instance has a schema.
            validatees the current values
        """
        if getattr(self,"schema", False):
            # if instance has a schema. (also see init_on_load)
            #v = cerberus.Validator(self.schema)
            v = Validator(self.schema)
            if v.validate(self.db_dict_dump()):
                return True
            else:
                return v

    def init_from_xml(self, data, root="root", ignore=True):
        """
            makes a py dict from input xml and
            sets the instance attributes 
            root defines the xml root node
            
        """
        d=xmltodict.parse(data)
        d=d[root]
        for key in d:
            #print("key: " + key + " : " + str(d[key]) )
            if isinstance(d[key],dict):
                print(d[key])
                for elem in d[key]:
                    if elem.startswith("#"):
                        if key in self.__class__.__dict__:
                            setattr(self, key, d[key][elem])
            else:
                #if key in self.__class__.__dict__:
                if ignore:
                    setattr(self, key, d[key])
                else:
                    if key in self.schema:
                        setattr(self, key, d[key])
                    else:
                        raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)

    def init_from_json(self, data, ignore=True):
        """
            makes a py dict from input json and
            sets the instance attributes 
        """
        d=json.loads(data)
        for key in d:
            if ignore:
                setattr(self, key, d[key])
            else:
                if key in self.schema:
                    setattr(self, key, d[key])
                else:
                    raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)


    def init_from_csv(self, keys, data, ignore=True):
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
            if ignore:
                setattr(self, k, d)
            else:
                if key in self.schema:
                    setattr(self, key, d[key])
                else:
                    raise Exception(" Key: " + str(key) + " is not in schema for: " + self.__class__.__name__)
    
    def json_dumps(self, *args, **kwargs):
        """ just dump to json formatted string"""
        return json.dumps(self.db_dict_dump(), *args, default=pow_json_serializer, **kwargs)

    def json_dump(self, *args, **kwargs):
        """ just dump to json """
        return json.loads(self.json_dumps(*args, **kwargs))

    def db_dict_dump(self, validate=False):
        """
            return the attributes defined in the schema 
            as a dictionary
            validate if forced.
        """
        if validate:
            ret = self.validate()
            if ret == True:
                return self.dict_dump(from_schema=True)
            else:
                raise AssertionError("Schema validation failed for model: " + 
                    self.__class__.__name__ + str(ret))
        else:
            return self.dict_dump(from_schema=True)
            

    def dict_dump(self, from_schema=True):
        """
            return vars / attributes of this instance as dict
            raw = True => all (almost: except for those in exclude_list)
            raw = False => only those defined in schema
        """
        d = {}
        if not from_schema:
            # return  "almost all attributes"
            exclude_list=["_jsonify","_sa_instance_state", "session", "schema", "table", "tree_parent_id", "tree_children"]
            if getattr(self, "exclude_list", False):
                exclude_list += self.exclude_list
            for elem in vars(self).keys():
                if not elem in exclude_list:
                    d[elem] = vars(self)[elem]
            return d
        else:
            # return just the attributes that are defined in the schema 
            for elem in self.schema.keys():
                d[elem] = getattr(self,elem, None)
            return d
        


    def print_full(self):
        """ Subclasses should overwrite this Method. 
            prints every attribute including related objects in FULL
            lenghty but you see everything.
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def __repr__(self):
        """
            __repr__ method is what happens when you look at it with the interactive prompt
            or (unlikely: use the builtin repr() function)
            usage: at interactive python prompt
            p=Post()
            p
        """
        from pprint import pformat
        j = self.json_dump()
        return pformat(j,indent=+4)

    def __str__(self):
        """
            The __str__ method is what happens when you print the object
            usage:
            p=Post()
            print(p)
        """
        return self.__repr__()
                       
    #
    # These Mehtods should be implemented by every subclass
    # 
    def json_load_from_db(self, data, keep_id=False):
        """  refresh the object from db and return json """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def print_db_schema(self):
        """ Subclasses should overwrite this Method. 
            Shows the schema as returned by the db
        """ 
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def get_relationships(self):
        """ Subclasses should overwrite this Method. 
            Shows all related classes
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def get_relations(self):
        """ Subclasses should overwrite this Method. 
            Shows all related classes
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def create_table(self):
        """
            created the physical table in the DB
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def drop_table(self):
        """
            created the physical table in the DB
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def upsert(self, session=None):
        """ insert oro update intelligently """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def get_by_id(self, id):
        """ return result by id (only)"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def from_statement(self, statement):
        """ execute a given DB statement raw """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def page(self, *criterion, limit=None, offset=None):
        """ return the next page of results. See config["myapp"].page_size """
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find(self,*criterion):
        """ Find something given a query or criterion """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def find_all(self, *criterion, raw=False, as_json=False, limit=None, offset=None):
        """ Find something given a query or criterion and parameters """
        raise NotImplementedError("Subclasses should overwrite this Method.")
    
    def find_one(self, *criterion, as_json=False):
        """ find only one result. Raise Excaption if more than one was found"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def find_first(self, *criterion, as_json=False):
        """ return the first hit, or None"""
        raise NotImplementedError("Subclasses should overwrite this Method.")

    def q(self):
        """ return a raw query so the user can do
            everything the DB offers without limitations
        
            for sqlalchemy: return session.query(self.__class__)
            for elastic: return  Q
            for tinyDB return Query
        """
        raise NotImplementedError("Subclasses should overwrite this Method.")
        




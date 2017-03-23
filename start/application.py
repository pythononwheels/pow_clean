import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys

import {{appname}}.config as cfg
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.database.sqldblib import Base, Session, engine
from {{appname}}.config import myapp
from {{appname}}.config import routes
from tornado.log import access_log
import logging
import datetime


# global logger settings
formatter = myapp["logformat"]
log_handler = logging.FileHandler(os.path.abspath(os.path.normpath(myapp["logfile"])))
#log_handler.setLevel(db_handler_log_level)
log_handler.setFormatter(formatter)

class Application(tornado.web.Application):
    #
    # handlers class variable is filled by the @add_route decorator.
    # merged with the instance variable in __init__
    # so classic routes and @add_routes are merged.
    #
    handlers=[]

    #routing list to handle absolute route positioning
    handlers_tmp = []

    def __init__(self):
        self.handlers = routes
        # importing !"activates" the add_route decorator
        self.import_all_handlers()
        h=getattr(self.__class__, "handlers", None)
        #self.handlers+=h

        # use the absolute positioning routing table
        #htmp=getattr(self.__class__, "handlers_tmp", None)
        def get_key(item):
            return item[1]
        #print(list(reversed(sorted(htmp, key=get_key))))
        self.show_positioned_routes( list(reversed(sorted(h, key=get_key))) )
        hordered=[x[0] for x in reversed(sorted(h, key=get_key))]
        #print(str(hordered))
        self.handlers+=hordered

        # merge two dictionaries:  z = { **a, **b }
        # http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
        settings = merge_two_dicts( dict(
            template_path=os.path.join(os.path.dirname(__file__), cfg.server_settings["template_path"]),
            static_path=os.path.join(os.path.dirname(__file__), cfg.server_settings["static_path"])
        ) , cfg.server_settings)
        super(Application, self).__init__(self.handlers, **settings)
        self.Session = Session
        self.engine = engine
        self.Base = Base

    def log_request(self, handler, message=None):
        """ 
            custom log method
            access_log is importef from tornado.log (http://www.tornadoweb.org/en/stable/_modules/tornado/log.html)
            access_log = logging.getLogger("tornado.access")
            you can define you own log_function in config.py server_settings
        """
        #super().log_request(handler)
        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        #log_method("%d %s %.2fms", handler.get_status(),
        #           handler._request_summary(), request_time)
        log_method("%s %d %s %.2fms", handler.request.remote_ip, handler.get_status(),
                handler._request_summary(), request_time)
        if message:
            log_method("%s %d %s", handler.request.remote_ip, handler.get_status(), str(message))

    
    def import_all_handlers(self):
        """
            imports all handlers to execue the @add_routes decorator.
        """
        import os
        exclude_list=["base", "powhandler"]

        #
        # the list of handlers (excluding base. Add more you dont want
        # to be loaded or inspected to exclude_list above.)
        #
        mods=[]
        module_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'handlers'))
        #print("importing handlers from: " + module_path)
        for mod in os.listdir( module_path ):
            mod = mod.split(".")[0]
            if not mod.startswith("_") and not mod in exclude_list:
                #print("  now processing: " + str(mod))
                mods.append(mod)
                
        #print("mods: " + str(mods))
        class_list = []
        # load all the models from their modules (mods)
        #print(str(mods))
        import importlib
        for m in mods:
            #print("importing: " + '{{appname}}.handlers.' + m)    
            try:
                mod = importlib.import_module('{{appname}}.handlers.' + m)
            except:
                pass
            #print(dir(mod))

    def show_positioned_routes(self, routes):
        """
            show all current routes.
        """
        print(55*"-")
        print("  Positioned Routes:")
        print(55*"-")
        for elem in routes:
            print(str(elem))

    def show_routes(self):
        """
            show all current routes.
        """
        routelist= [(handler.regex.pattern, handler.handler_class) for handler in self.handlers[0][1]]
        print(55*"-")
        print("  Routing table (order matters) :")
        print(55*"-")
        for elem in routelist:
            print('{0:<20} {1:<30} '.format(elem[0], str(elem[1])))

    
    #
    # the RESTful route decorator v2
    # with dedicated routes. One per default action
    #
    def add_rest_routes(self, route, api=None, pos=0):
        """
            cls is the class that will get the RESTful routes
            it is automatically the decorated class
            self in this decorator is Application
            api will insert the given api version into the route (e.g. route=post, api=1.0)
            /post/1.0/**all restroutes follow this pattern
            1  GET    /items            #=> index (list)
            2  GET    /items/1          #=> show
            3  GET    /items/new        #=> new
            4  GET    /items/1/edit     #=> edit
            5  GET    /items/page/0     #=> page  
            6  PUT    /items/1          #=> update
            7  POST   /items            #=> create
            8  DELETE /items/1          #=> destroy
        """
        def decorator(cls):
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            #print(cls_name)
            action=route
            
            action_part = action
            if api:
                action_part + r"/" + str(api)
            
            routes = [
                # tuple (http_method, route, { http_method : method_to_call_in_handler, .. })
                ( r"/" + action_part + r"/search/?" , { "get" : "search" }),
                ( r"/" + action_part + r"/(?P<id>[0-9]+)/edit/?" , { "get" : "edit", "params" : ["id"] }),
                ( r"/" + action_part + r"/page/?(?P<page>[0-9]+)?/?", { "get" : "page", "params" : ["page"] }),
                ( r"/" + action_part + r"/new/?", {"get" : "new"}),
                ( r"/" + action_part + r"/?(?P<id>[0-9]+)?/?", 
                    { "get" : "show" , "put" : "update", "delete" : "delete", "params" : ["id"]} ),
                 ( r"/" + action_part + r"/show/?(?P<id>[0-9]+)?/?", { "get" : "show" , "params" : ["id"]} ),
                ( r"/" + action_part + r"/?", { "get" : "list", "post" : "create" })                
            ]
            # BETA: Add the .format regex to the RESTpattern   
            # this makes it possible to add a .format at an URL. Example /test/12.json (or /test/12/.json)
            if cfg.beta_settings["dot_format"]:
                routes = [(x[0]+ r"(?:/?\.\w+)?/?", x[1]) for x in routes]  
            #print("added the following routes: " + r)
            handlers=getattr(self.__class__, "handlers", None)
            for elem in routes:
                handlers.append( ((elem[0],cls, elem[1]), pos) ) 
            print("ROUTING: added RESTful routes for: " + cls.__name__ +  " as /" + action)
            #print(dir())
            return cls
        return decorator

    
    #
    # the direct route decorator
    #
    def add_route(self, route, dispatch={}, pos=0):
        """
            cls is the class that will get the given route / API route
            cls is automatically the decorated class
            self in this decorator is Application
            this will take a 1:1 raw tornado route

            for regex with optional parts that are dropped 
            (Non copturing like: (?: ...) see:
            http://stackoverflow.com/questions/9018947/regex-string-with-optional-parts
        """
        def decorator(cls):
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            handlers=getattr(self.__class__, "handlers", None)
            # BETA: this regex is added to every route to make 
            # 1.the slash at the end optional
            # 2.it possible to add a .format paramter.
            # Example: route = /test -> also test.json will work
            # Example: route = /test/([0-9]+) -> also /test/12.xml will work 
            if cfg.beta_settings["dot_format"]:
                fin_route = route  + r"(?:/?\.\w+)?/?"
            else:
                fin_route = route
            route_tuple = (fin_route,cls, dispatch)
            handlers.append((route_tuple,pos))
            #print("handlers: " + str(self.handlers))
            print("ROUTING: added route for: " + cls.__name__ +  ": " + route + " -> " + fin_route)
            return cls
        return decorator
    
   
app=Application()
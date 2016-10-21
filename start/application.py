import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import os.path
import sys

from {{appname}}.config import server_settings as app_settings
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.dblib import Base, session, engine

from {{appname}}.config import routes
from tornado.log import access_log

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
        htmp=getattr(self.__class__, "handlers_tmp", None)
        def get_key(item):
            return item[1]
        #print(list(reversed(sorted(htmp, key=get_key))))
        self.show_positioned_routes( list(reversed(sorted(htmp, key=get_key))) )
        hordered=[x[0] for x in reversed(sorted(htmp, key=get_key))]
        #print(str(hordered))
        self.handlers+=hordered

        # merge two dictionaries:  z = { **a, **b }
        # http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
        settings = merge_two_dicts( dict(
            template_path=os.path.join(os.path.dirname(__file__), app_settings["template_path"]),
            static_path=os.path.join(os.path.dirname(__file__), app_settings["static_path"]),
            db=engine,
            Base=Base
        ) , app_settings)
        super(Application, self).__init__(self.handlers, **settings)
        self.session = session
        self.engine = engine
        self.Base = Base

     def log_request(self, handler):
        """ 
            custom log method
            access_log is importef from tornado.log (http://www.tornadoweb.org/en/stable/_modules/tornado/log.html)
            access_log = logging.getLogger("tornado.access")
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
    
    def import_all_handlers(self):
        """
            imports all handlers to execue the @add_routes decorator.
        """
        import os
        exclude_list=["base"]

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
    # the RESTful route decorator
    #
    def add_rest_routes(self, route=None, api=None):
        """
            cls is the class that will get the RESTful routes
            it is automatically the decorated class
            self in this decorator is Application
            api will insert the given api version into the route (e.g. route=post, api=1.0)
            /post/1.0/**all restroutes follow this pattern
            1  GET    /items            #=> index
            2  GET    /items/1          #=> show
            3  GET    /items/new        #=> new
            4  GET    /items/1/edit     #=> edit
            5  GET    /items/page/0     #=> pagination     
            6  PUT    /items/1          #=> update
            7  POST   /items            #=> create
            8  DELETE /items/1          #=> destroy
        """
        def decorator(cls):
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            #print(cls_name)
            # default REST is the following pattern:
            # (r"/post/(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?/?(?P<param3>[^\/]+)?", PostHandler),
            action=""
            if cls_name.endswith("handler"):
                action=action[:-7]
            else:
                action = cls_name
            if route:
                action=route

            r="/"+action+"/(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?/?(?P<param3>[^\/]+)?"
            if api:
                # render the given api in the route URL
                r="/"+action+"/"+str(api)+"/(?P<param1>[^\/]+)/?(?P<param2>[^\/]+)?/?(?P<param3>[^\/]+)?"
            
            #print("added the following routes: " + r)
            handlers=getattr(self.__class__, "handlers", None)
            handlers.append((r,cls))
            r="/"+action+"/*"
            #print("added the following routes: " + r)
            handlers.append((r,cls))
            #print("handlers: " + str(self.handlers))
            print("ROUTING: added RESTful routes for: " + cls.__name__ +  " as /" + action)
            #print(dir())
            return cls
        return decorator

    #
    # the RESTful route decorator
    #
    #todo
    def add_route(self, route, pos=0):
        """
            cls is the class that will get the given route / API route
            cls is automatically the decorated class
            self in this decorator is Application
            this will take a 1:1 raw tornado route
        """
        def decorator(cls):
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            #print("added the following routes: " + r)
            handlers=getattr(self.__class__, "handlers", None)
            handlers_tmp=getattr(self.__class__, "handlers_tmp", None)
            handlers_tmp.append(((route,cls),pos))
            if pos < 0:
                if pos == -1:
                    handlers.append((route,cls))
                else:
                    handlers.insert(len(handlers)-(pos+1),(route,cls))
            elif pos >= 0:
                handlers.insert(pos,(route,cls))
            
            #print("handlers: " + str(self.handlers))
            print("ROUTING: added route for: " + cls.__name__ +  ": " + route)
            return cls
        return decorator

app=Application()
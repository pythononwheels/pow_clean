import tornado.web
import tornado.escape
import json
from {{appname}}.config import myapp 
from {{appname}}.models.sql.user import User
#
#
# Base PoW handler (Controller)
# automatically adds RESTful routing:
# 1  GET    /items            #=> index
# 2  GET    /items/1          #=> show
# 3  GET    /items/new        #=> new
# 4  GET    /items/1/edit     #=> edit
# 5  GET    /items/page/0     #=> pagination     
# 6  PUT    /items/1          #=> update
# 7  POST   /items            #=> create
# 8  DELETE /items/1          #=> destroy

# you will also be able to add custom routes (Tornado routes)
# or handle POUPs (Plain Old Url ParameterS ;)
# like this: /post/search?name=pythononwheels&email=info@pythononwheels.org
# 

class BaseHandler(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        print("  .. in initialize")
        print("  .. .. args: " + str(args))
        print("  .. .. kwargs: " + str(kwargs))
        if "method" in kwargs.keys():
            # direct route to a method.
            self.dispatch = {
                "method"    :   kwargs.get("method", None),
                "verbs"     :   kwargs.get("verbs", [])
            }
            print(" .. direct route." + str(self.dispatch))
        else:
            self.dispatch = {
                "method"    :   "rest",
                "verbs"     :   []
            }
           

        
    def prepare(self):
        """
            Called at the beginning of a request before get/post/etc.
        """
        
        #print(self.request)
        self.uri = self.request.uri
        print("Request:" )
        print(30*"-")
        print(" Mehtod: " + self.request.method)
        print(" URI: " + self.uri)
        print(" Handler: " + self.__class__.__name__)
        self.path = self.request.uri.split('?')[0]
        self.action = self.path.split('/')[-1]
        self.default_methods = {}
        #
        # You can use the before_handler in a local controller to
        # process your own prepare stuff.
        # a common use case is to call: self.print_debug_info().
        # which then applies only to this specific Controller.
        # 
        before_handler = getattr(self, "before_handler", None)
        if callable(before_handler):
            print("calling before_handler for " +  str(self.__class__))
            before_handler()
        self.format = None

    def get_current_user(self):
        """
            very simple implementation. 
            change to you own needs here or in your own subclassed base handler.

        """
        if myapp["enable_authentication"]:
            # try to find the user
            user_id = self.get_secure_cookie("blogdemo_user")
            if not user_id: return None
            u=User()
            u=u.find_one(User.id==user_id)
            return u
        else:
            # if authentication is disabled return a dummy guest user
            u=User()
            u.login="pow_guest"
            return u


    def get_accept_format(self, format_param):

        if not format_param:
            return myapp["default_format"]
        if format_param in myapp["supported_formats"]:
            return format_param
        else:
            print("format error")
            return self.error(
                    message="Format not supported. (see data.format)",
                    data={
                        "format was" : format_param,
                        "supported_formats" : myapp["supported_formats"]
                    }
                )

    def dispatch_rest_route(self, **params):
        # GET    /items         #=> index    CASE 1
        # GET    /items/1       #=> show     CASE 2
        # GET    /items/1/edit  #=> edit     CASE 3 
        # GET    /items/new     #=> new      CASE 4 
        # GET    /items/page/0  #=> page     CASE 5
        # GET    /items/search  #=> search   CASE 6
        
        # the last parameter may always be a format specification
        # (json, xml, csv, html)
        print("Get Parameters: " + str(params))
        if params == {}:
            # if there are no params we call index CASE 1
            self.format=myapp["default_format"]
            #return getattr(self, "index" + "_" + format)()
            return self.index()
        try:
            p1 = params.get("param1", None)
            int(p1)
            # if param1 is an integer and param2 is == "edit" we call edit(id) CASE 3
            if str(params.get("param2", None)).lower() == "edit":
                self.format = self.get_accept_format(params.get("param3"))
                return self.edit(p1)
            #
            # if param1 is an Int we treat it as an ID and call show(id) CASE 2
            #
            self.format = self.get_accept_format(params.get("param2"))
            return self.show(p1)
        except ValueError:
            #
            # if param 1 is new we call new (return the new html form) CASE 4
            # if param 1 is search we call new 
            #       (you have to handle the URL parameters yourself) CASE 6
            # or if param2 is given we take this as the result format.
            #
            if str(params.get("param1", None)).lower() not in ["new", "search", "page"]:
                #it is a format or an error
                self.format = self.get_accept_format(params.get("param1"))
                print("self format is:" +str(self.format))
                return self.index()
            if str(params.get("param1", None)).lower() == "new":
                self.format = self.get_accept_format(params.get("param2"))
                return self.new()
            elif str(params.get("param1", None)).lower() == "search":
                self.format = self.get_accept_format(params.get("param2"))
                return self.new()

            #
            # if param 1 is page (and param2 is an int) we call page (paginated list) CASE 5
            elif str(params.get("param1", None)).lower() == "page":
                p2=params.get("param2", None)
                try:
                    int(p2)
                    self.format = self.get_accept_format(params.get("param3"))
                    self.page(int(p2))
                except:
                    return self.error(500, params, "for page the next parameter page_num must be an int. Example: /page/0")        
            elif str(params.get("param1", None)) in myapp["supported_formats"]:
                # someone wanted the index action with a special format
                # /post/json => index_json
                self.format = self.get_accept_format(params.get("param1", None))
                self.index()
                
        return self.error(500, params, "You didnt match any of the supported REST routes ....")

    #
    # GET
    #
    def get(self, *args, **params):
        #url_params=self.get_arguments("id")
        print("  .. GET params : " + str(params))
        print("  .. GET args : " + str(args))
        if self.dispatch["method"] == "rest":
            # route a rest_route: @app.add_rest_route("base_name")
            return self.dispatch_rest_route(**params)
        else:
            # route a direct route: @app.add_route("/regex/", method="name", verbs=["get"])
            if "get" in self.dispatch["verbs"]:
                # only proceed if this route is valid for this request verb
                try:
                    f=getattr(self, self.dispatch["method"])
                    print(str(f))
                    if callable(f):
                        # call the given method
                        return f(*args, **params)
                except TypeError:
                    self.application.log_event(self, 
                        message="""method was None. But you also did not implement
                        one of the to standard HTTP methods (get,put ...)""")
                    self.error(
                    message="""method was None. But you also did not implement
                        one of the to standard HTTP methods (get,put ...)""",
                    data = { "request" : str(self.request )},
                    http_code = 405
                    )
            else:
                self.error(
                    message=" HTTP Method: GET not supported for this route. ",
                    data = { "request" : str(self.request )},
                    http_code = 405
                    )

        self.write(params)
    
    #
    # POST   /items     #=> create
    #
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        return self.create(data)

    #
    # PUT    /items/1      #=> update
    #
    def put(self, **params):
        #data = tornado.escape.json_decode(self.request.body)
        try:
            p1 = params.get("param1", None)
            int(p1)
            # if param1 is an integer we call update
            return self.update(p1)
        except ValueError:
            return self.error(500, params, "HTTP/UPDATE needs an ID. ID must be an int")
    
    #
    # DELETE /items/1      #=> destroy
    # 
    def delete(self, **params):
        #data = tornado.escape.json_decode(self.request.body)
        try:
            p1 = params.get("param1", None)
            int(p1)
            # if param1 is an integer we call update
            return self.destroy(p1)
        except ValueError:
            return self.error(500, params, "HTTP/UPDATE needs an ID. ID must be an int")


    def success(self, message=None, data=None, succ=None, prev=None,
        http_code=200, format=None, encoder=None):
        """
            returns data and http_code.
            data will be converted to format.  (std = json)
            for other formats you have to define an encoder in config.py
            (see json as an example)
        """
        if not format:
            format = self.format
        if not format:
            format = myapp["default_format"]
        self.set_status(http_code)
        if encoder:
            encoder = encoder
        else:
            encoder = myapp["encoder"][format]
        self.write(encoder.dumps({
            "status"    : http_code,
            "message"   : message,
            "data"      : data,
            "next"      : succ,
            "prev"      : prev
        }))
        self.finish()

    def error(self, message=None, data=None, succ=None, prev=None,
        http_code=500, format=None, encoder=None):
        self.set_status(http_code)
        
        if not format:
            format = self.format
        if not format:
            format = myapp["default_format"]
        if encoder:
            encoder = encoder
        else:
            encoder = myapp["encoder"][format]
        self.write(encoder.dumps({
            "status"    : http_code,
            "data"      : data,
            "error"     : {
                "message"   : message
                },
            "next"      : succ,
            "prev"      : prev
        }))
        self.finish()

    def write_error(status_code, **kwargs):
        """
            write_error may call write, render, set_header, etc to produce 
            output as usual.
            If this error was caused by an uncaught exception 
            (including HTTPError), an exc_info triple will be available as 
            kwargs["exc_info"]. Note that this exception may not be the 
            âcurrentâ exception for purposes of methods like sys.exc_info() 
            or traceback.format_exc.
        """
        #if status_code == 404:
        return self.render("404.tmpl")


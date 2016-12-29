import tornado.web
import tornado.escape
import json
from {{appname}}.config import myapp 
from {{appname}}.models.{{dbtype}}.user import User



class BaseHandler2(tornado.web.RequestHandler):

    def initialize(self, *args, **kwargs):
        """
            receives the URL dict parameter.
            For PoW RESTroutes this looks like this:
            { "get" : "some_method" }
            { "http_verb" : "method_to_call", ...}
        """
        print("  .. in initialize")
        print("  .. .. args: " + str(args))
        print("  .. .. kwargs: " + str(kwargs))
        self.dispatch_kwargs = kwargs
        self.dispatch_args = args

        
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
        # path = anything before url-parameters
        self.path = self.request.uri.split('?')[0]
        print(" path: " + self.path)
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
            user_id = self.get_secure_cookie("user_id")
            if not user_id: return None
            u=User()
            u=u.find_one(User.id==user_id)
            return u
        else:
            # if authentication is disabled return a dummy guest user
            u=User()
            u.login="pow_guest"
            return None


    def get_accept_format(self):
        """
            format is either added as .format to the path
            or default_format
            example: /post/12.json (will return json)
        """

        if len (self.path.split(".")) > 1:
            format = self.path.split(".")[-1]
        else:
            format = myapp["default_format"]
        
        if format in myapp["supported_formats"]:
            return format
        else:
            print("format error")
            return self.error(
                    message="Format not supported. (see data.format)",
                    data={
                        "format was" : format,
                        "supported_formats" : myapp["supported_formats"]
                    }
            )
                
    #
    # GET
    #
    def get(self, *args, **params):
        #url_params=self.get_arguments("id")
        print(" ------------- GET / BaseHandler2")
        print("  .. GET params : " + str(params))
        print("  .. GET args : " + str(args))
        print("  .. GET slef.dispatch_kwargs : " + str(self.dispatch_kwargs))
        if self.dispatch_kwargs.get("get", None):
            try:
                f=getattr(self, self.dispatch_kwargs.get("get"))
                print("  .. trying to call: " + str(f))
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


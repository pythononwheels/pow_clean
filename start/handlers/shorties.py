import tornado.ioloop
import tornado.web
from {{appname}}.handlers.base import BaseHandler
from {{appname}}.application import app
#
# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 
@app.add_route("/dash/*")
class DashboardHandler(BaseHandler):
    def get(self):
        self.render("dash.tmpl")

@app.add_route("/thanks/*", method="_get")
# if you specify a method, this method will be called for this route
@app.add_route("/thanks/([0-9]+)*", method="testme")
class ThanksHandler(BaseHandler):
    def _get(self, *args, **kwargs):
        self.render("thanks.tmpl")
        
    def testme(self, index=0 ):
        print("  .. in testme: index = " + str(index))
        self.render("thanks.tmpl", index=index)
    
# if you DON't specify a method, the standard HTTP verb method (e.g. get(), put() will be called)
@app.add_route("/index/([0-9]+)*")
@app.add_route("/", pos=-9)
class IndexdHandler(BaseHandler):
    def get(self, index=None):
        print("  index:" + str(index))
        self.render("index.tmpl")

@app.add_route(".*", pos=-10)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.render("404.tmpl", url=self.request.uri)
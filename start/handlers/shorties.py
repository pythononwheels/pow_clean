import tornado.ioloop
import tornado.web
from {{appname}}.handlers.base2 import BaseHandler2
from {{appname}}.application import app
#
# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 


#  ( r"/" + action + r"/" + r"/(?P<id>.+)/edit/?" , { "get" : "edit", "params" : ["id"] }),
@app.add_route2("/dash/*")
class DashboardHandler(BaseHandler2):
    def get(self):
        self.render("dash.tmpl")

# if you specify a method, this method will be called for this route
@app.add_route2("/thanks/*", dispatch={"get": "_get"} )
@app.add_route2("/thanks/([0-9]+)*", dispatch={"get": "testme"})
class ThanksHandler(BaseHandler2):
    def _get(self, index=0 ):
        print("  .. in _get: index = " + str(index))
        self.render("thanks.tmpl", index=index)

    def testme(self, index=0 ):
        print("  .. in testme: index = " + str(index))
        self.render("thanks.tmpl", index=index)
    
# if you DON't specify a method, the standard HTTP verb method (e.g. get(), put() will be called)
@app.add_route2("/index/([0-9]+)*")
@app.add_route2("/", pos=-2)
class IndexdHandler(BaseHandler2):
    def get(self, index=None):
        print("  index:" + str(index))
        self.render("index.tmpl")

# this will be the last route 
@app.add_route2(".*", pos=-3)
class ErrorHandler(BaseHandler2):
    def get(self):
        return self.render("404.tmpl", url=self.request.uri)


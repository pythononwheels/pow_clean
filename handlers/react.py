import tornado.ioloop
import tornado.web
from {{appname}}.server import app

@app.add_route("/react/*")
class ReactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("react.tmpl")

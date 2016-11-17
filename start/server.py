#
#
# pow server
# khz / 2016
#

import tornado.httpserver
import os
import os.path
import sys

from {{appname}}.config import server_settings as app_settings
from {{appname}}.config import myapp 
from {{appname}}.config import database as db_settings
from {{appname}}.powlib import merge_two_dicts
from {{appname}}.application import Application

app=Application()
if __name__ == "__main__":

    #tornado.options.parse_command_line()
    #from tornado.log import enable_pretty_logging
    #enable_pretty_logging()
    #print(dir(tornado.options.options))

    tornado.options.options.log_file_prefix = myapp["logfile"]
    tornado.options.options.log_file_num_backups=5
    # size of a single logfile
    tornado.options.options.log_file_max_size = 10 * 1000 * 1000
    tornado.options.parse_command_line()

    #app = tornado.web.Application(handlers=routes, **app_settings)
    print()
    print(50*"-")
    print("starting the pow server Server ")
    print(50*"-")
    print("visit: https://localhost:" + str(app_settings["port"]))
    for idx, elem in enumerate(db_settings.keys()):
        if elem.lower() == "sql":
            print("  DB #" +str(idx) + ": " + db_settings[elem]["type"])
        else:
            print("  DB #" +str(idx) + ": " + elem)
    #app.listen(app_settings["port"], **server_settings)#
    #app=Application()
    #print(app)
    print()
    print(50*"-")
    print("Final routes (order matters from here on ;) " )
    print(50*"-")
    for idx,elem in enumerate(app.handlers[0][1]):
        print("#"+str(idx)+": " + str(elem.regex) + " --> " + str(elem.handler_class))

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(app_settings["port"])
    tornado.ioloop.IOLoop.instance().start()

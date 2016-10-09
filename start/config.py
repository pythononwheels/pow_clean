#
#
# pow settings file
# 
import json
import {{appname}}.encoders
import os

server_settings = {
    "app_name"          :   "{{appname}}",
    "port"              :   8080,
    "debug"             :   True,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "cookie_secret"     :   "254f2254-6bb0-1312-1104-3a0786ce285e",
}

templates = {
    "template_path"     :   server_settings["template_path"],
    "handler_path"      :   os.path.join(os.path.dirname(__file__), "handlers"),
    "model_path"        :   os.path.join(os.path.dirname(__file__), "models"),
    "stubs_path"        :   os.path.join(os.path.dirname(__file__), "stubs")
}

myapp = {
    "default_format"    :   "json",
    "supported_formats" :   ["json", "csv", "xml"],
    "base_url"          :   "https://localhost",
    "encoder"           :   {
            "json"  :   json,
            "csv"   :   {{appname}}.encoders.JsonToCsv(),
            "xml"   :   {{appname}}.encoders.JsonToXml()
    },
    "page_size"         : 10,
}


database = {
    "type"      :   "postgresql",
    "dbname"    :   "powtest",
    "host"      :   "localhost",
    "port"      :   5432,
    "user"      :   "powtest",
    "passwd"    :   "powtest"
}

#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
        ]


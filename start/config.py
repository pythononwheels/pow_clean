#
#
# pow settings file
# 
import simplejson as json
import {{appname}}.encoders
import os
import logging

server_settings = {
    "app_name"          :   "{{appname}}",
    "port"              :   8080,
    "debug"             :   True,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "xsrf_cookies"      :   True,
    #"log_function"      :   you can give your own log function here.
    "cookie_secret"     :   "254f2254-6bb0-1312-1104-3a0786ce285e"
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
    "enable_authentication"     :   False,   # False, simple or custom
    "sql_auto_schema"   :   True,
    "logfile"           :   "pow.log",
    "logformat"         :   logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    #"environment"       :   "development"       # set the current environment (also see the db section)
}


database = {
    "sql"   : {
        "type"      :   "sqlite",
        "dbname"    :   r"sql.sqlite",   # better leave the r to enable absolute paths with backslashes 
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   True
    },
    "tinydb" : {
        "dbname"    :   r"tiny.db",   # better leave the r to enable absolute paths with backslashes 
        "host"      :   None,       
        "port"      :   None,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False
    },
    "elastic" : {
        "dbname"    :   "testdb",   # == elasticsearch index 
        "hosts"     :   ["localhost"],       
        "port"      :   9200,   
        "user"      :   None,
        "passwd"    :   None,
        "enabled"   :   False
    }
}



#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
        ]


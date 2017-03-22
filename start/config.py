#
#
# pow settings file
# 
import simplejson as json
import {{appname}}.encoders
import os
import logging

server_settings = {
    "base_url"          :   "http://localhost",
    "port"              :   8080,
    "debug"             :   True,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "xsrf_cookies"      :   True,
    #"log_function"      :   you can give your own log function here.
    "cookie_secret"     :   "{{cookie_secret}}"
}

templates = {
    "template_path"     :   server_settings["template_path"],
    "handler_path"      :   os.path.join(os.path.dirname(__file__), "handlers"),
    "model_path"        :   os.path.join(os.path.dirname(__file__), "models"),
    "stubs_path"        :   os.path.join(os.path.dirname(__file__), "stubs")
}

myapp = {
    "app_name"          :   "{{appname}}",
    "default_format"    :   "json",
    "supported_formats" :   ["json", "csv", "xml"],
    "encoder"           :   {
            "json"  :   json,
            "csv"   :   {{appname}}.encoders.JsonToCsv(),
            "xml"   :   {{appname}}.encoders.JsonToXml()
    },
    "page_size"         : 5,
    "enable_authentication"     :   False,   # False, simple or custom
    "sql_auto_schema"   :   True,
    "logfile"           :   os.path.join(os.path.dirname(__file__),"pow.log"),
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

beta_settings = {
    # Beta settings are erxperimental. You can find details for each Beta setting
    # on www.pythononwheels.org/beta
    
    # Name          :    Enabled ?
    "dot_format"    :   False
}

#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
        ]


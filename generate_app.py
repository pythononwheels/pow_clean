#
# generate app
#

import argparse
import tornado.template as template
import os
from {{appname}}.config import templates
from {{appname}}.powlib import pluralize

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def pump_file(infile, outfile, appname):
    """ 
        pump ther infile thru the template engine in case
        there is something to render.
        most probably the correct import path startign with appname
    """
    ofile = open(outfile, "wb")
    res = loader.load(infile).generate(appname=appname)
    ofile.write(res)
    ofile.close()
    return True

def generate_app(app_name=None):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """
    #
    # set some attributes
    #
    loader = template.Loader(templates["stubs_path"])
    #
    # create the model
    #
    
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="name", help='-n appname',
                        required=True)
    #
    # db type
    # 
    # parser.add_argument('-d', "--db", action="store", 
    #                     dest="db", help='-d which_db (mongo || tiny || peewee_sqlite) default = tiny',
    #                     default="tiny", required=True)
    args = parser.parse_args()
    #
    # show some args
    #
    print("all args: ", args)
    #print(dir(args))
    #print("pluralized model name: ", pluralize(args.name))
    generate_app(args.name)
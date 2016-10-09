#
# generate model
#

import argparse
import tornado.template as template
import os.path
import timeit
import {{appname}}.powlib as lib
from {{appname}}.config import templates


def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_handler(handler_name):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """
    #
    # set some attributes
    #
    loader = template.Loader(templates["stubs_path"])
    handler_class_name = camel_case(handler_name)
    #
    # create the controller
    #
    ofile = open(os.path.join(templates["handler_path"], handler_name+".py"), "wb")
    res = loader.load("handler_template.py").generate( 
        handler_name=handler_name, 
        handler_class_name=handler_class_name,
        handler_model_class_name=handler_class_name,
        appname="powtest"
        )
    ofile.write(res)
    ofile.close()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="name", help='-n handler name',
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
    print("CamelCased handler name: ", camel_case(args.name))
    generate_handler(args.name)
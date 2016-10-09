#
# generate app
#

import argparse
import tornado.template
import os
import sys
import datetime

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
    loader = template.Loader(os.path.dirname(os.path.normpath(infile)))
    ofile = open(outfile, "wb")
    res = loader.load(infile).generate(appname=appname)
    ofile.write(res)
    ofile.close()
    return True

def generate_app(appname, force=False):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """
    #
    # walk down the dirtree pow/*
    # pump all files thru the template engine and copy the result to
    # appname/*
    # exclude generate_app
    #
    print("  generating app: " + str(appname))
    print("  ..processing(root): " +  os.path.dirname(os.path.abspath(__file__)))
    exclude_file_list = ["generate_app.py"]
    exclude_dir_list=[".git", "scripts", "tcl", "lib", "include"]
    basename=os.path.dirname(os.path.abspath(__file__))
    run=0
    for root, dirs, files in os.walk(basename):
        print("  ..processing(root): " +  root)
        if str(root.split(os.path.pathsep)[-1:]) not in exclude_dir_list:
            print(" New root: " + os.path.basename(os.path.dirname(root)))
            for elem in dirs:
                print(" dirs: " + str(dirs))
                print(" the dir: " + elem)
                if os.path.basename(os.path.dirname(elem)) not in exclude_dir_list:
                    outpath =  os.path.join(root.replace("pow",appname))
                    abs_dir_path = os.path.normpath( os.path.join( outpath, elem ))
                    print("  ..creating (sub)directory: ", abs_dir_path)
                    try:
                        os.makedirs(abs_dir_path, exist_ok=force)
                    except:
                        print("    ... could not create dir: ", sys.exc_info()[0])
                else:
                    print("  ..Skipping dir: " + str(elem))
            for elem in files:
                outpath =  os.path.join(root.replace("pow",appname))
                abs_dest_file_path = os.path.normpath( os.path.join( outpath, elem ))
                abs_source_file_path = os.path.normpath( os.path.join( root, elem ))
                if elem not in exclude_file_list:
                    print("  ..processing file: ", abs_source_file_path )
                    f = open(abs_source_file_path, "r", encoding="utf-8")
                    instr = f.read()
                    f.close()
                    template = tornado.template.Template(instr)
                    out = template.generate(  
                            appname=appname,
                            current_date=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                            )
                    f = open(abs_dest_file_path, "w", encoding="utf-8")
                    f.write(out.decode("unicode_escape"))
                    f.close()
                else:
                    print("  ..skipped: " + str(elem))
        else:
            print(" skipped: " + root)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
        dest="name", help='-n appname',
        required=True)
    parser.add_argument("-f", "--force", 
        action="store_true", dest="force", default=False,
        help="force overwriting if invoked on existing app [default]")

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
    #print("all args: ", args)
    #print(dir(args))
    #print("pluralized model name: ", pluralize(args.name))
    print(50*"-")
    print(" Generating your app: " + args.name)
    print(50*"-")
    generate_app(args.name, args.force)
    print()
    print(50*"-")
    print("Your next steps: ")
    print("  cd to you new apps directory: ../" + args.name )
    print("  run: python server.py")
    print("  and open your browser with http://localhost:8080")
    print(50*"-")
    print()
    print(50*"-")
    print("Remark:")
    print("  You can move your app subdir to wherever you want")
    print("  as long as its on the pythonpath")
    print(50*"-")
    print()
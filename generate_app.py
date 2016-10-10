#
# generate app
#

import argparse
import tornado.template
import os
import sys
import datetime
import shutil
from pathlib import Path

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def copy_or_pump(src, dest, copy=False, appname=None):
    if not copy:
        print("    pumping to ----->", dest )
        f = open(src, "r", encoding="utf-8")
        instr = f.read()
        f.close()
        template = tornado.template.Template(instr)
        out = template.generate(  
                appname=appname,
                current_date=datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                )
        f = open(dest, "w", encoding="utf-8")
        f.write(out.decode("unicode_escape"))
        f.close()
    else:
        # just copy file
        print("    copying to ----->", dest )
        shutil.copy( src, dest )

def generate_app(appname, force=False):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """    
    print("  generating app: " + str(appname))
    base=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    print("  base: " + base)
    root=os.path.join(os.path.dirname(os.path.abspath(__file__)), "start")
    print("  root: " +  root)
    
    outdir=os.path.normpath(os.path.join(base, appname))
    #outdir = os.path.join(outdir, appname)
    print("  ..creating in: " +  outdir)
    
    os.makedirs(outdir, exist_ok=True)
    template_exts = [".py", ".tmpl"]
    exclude_dirs = ["static", "stubs", "views"]

    #
    # walk the root (/pow/start)
    # and copy (for .py and .tmpl pump thru template engine first)
    # all files to the new app dir (appname)
    # 
    for dirname, dirs, files in os.walk(root):
        for f in files:
            print(" processing: " + f)
            print("  in: " + dirname)
            path=Path(dirname)
            index = path.parts.index("start")
            opath = Path(outdir).joinpath(*path.parts[index+1:])
            print("  out: " + str(opath))
            filename, file_extension = os.path.splitext(f)
            print("  filename: " + filename)
            print("  file ext: " + file_extension)
            
            if not os.path.exists(str(opath)):
                os.makedirs(str(opath), exist_ok=True)
            if (file_extension in template_exts) and not (path.parts[-1] in exclude_dirs):
                copy_or_pump(
                    os.path.normpath(os.path.join(dirname, f)),
                    os.path.normpath(os.path.join(str(opath), f)),
                    copy=False,
                    appname=appname
                    )
            else:
                copy_or_pump(
                    os.path.normpath(os.path.join(dirname, f)),
                    os.path.normpath(os.path.join(str(opath), f)),
                    copy=True,
                    appname=appname
                    )

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

    base=os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    apppath=os.path.normpath(os.path.join(base, args.name))
    tpath=os.path.normpath(os.path.join(base, "migrations"))
    # make the versions dir
    os.makedirs(os.path.normpath(os.path.join(tpath, "versions")), exist_ok=True)

    print()
    print(50*"-")
    print("Your next steps: ")
    print("  1. cd to you new apps directory: " + apppath)
    print("  3. run: python server.py")
    print("  3. open your browser with http://localhost:8080")
    print(50*"-")
    print()
    print(50*"-")
    print("Remark:")
    print("  You can move your app subdir to wherever you want")
    print("  as long as its on the pythonpath")
    print("  Windows: set PYTHONPATH=%PYTHONPATH%;"+base)
    print("  linux/osx: export PYTHONPATH=$PYTHONPATH:"+base)
    print(50*"-")
    print()
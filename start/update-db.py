#
# update-db
#
import os
import alembic.config
import sys
from {{appname}}.dblib import engine
from alembic.config import Config
from alembic import command
import argparse

#
# this will execute 
# alembic upgrade head
# where message is the first cli parameter
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--direction", action="store", default="up",
        dest="direction", help='-d up (or down) default = up',
        required=False)
    #
    # db type
    # 
    parser.add_argument('-n', "--number", action="store",
        dest="number", help='-n 1 (default = 1)',
        default="1", required=False)

    parser.add_argument('-r', "--revision", action="store",
        dest="revision", help='-r 6669c0b62b06 (take the unique part from a migration id)',
        default=None, required=False)
    args = parser.parse_args()
    #
    # show some args
    #
    print("all args: ", args)

    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    if args.direction == "up":
        # upgrade
        if args.revision:
            args.revision
            command.upgrade(alembic_cfg, revision=args.revision)
        if args.number == "head":
            command.upgrade(alembic_cfg, "head")
        else:
            command.upgrade(alembic_cfg, "+" + args.number)
    else:
        # downgrade
        command.downgrade(alembic_cfg, "-" + args.number)
    
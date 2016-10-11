#
# generate_migration
#
import os
import alembic.config
import sys
from test.dblib import engine
from alembic.config import Config
from alembic import command
import argparse

#
# this will execute 
# alembic revision --autogenerate -m "message"
# where message is the first cli parameter
#
if __name__ == "__main__":
    parser.add_argument('-n', "--name", action="store",
        dest="message", help='-n my_first_migration',
        default=None, required=True)

    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    if args.message:
        command.revision(alembic_cfg, autogenerate=True, message=message)

    
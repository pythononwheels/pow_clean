#
# generate_migration
#
import os
import alembic.config
import sys
from {{appname}}.dblib import engine
from alembic.config import Config
from alembic import command

#
# this will execute 
# alembic revision --autogenerate -m "message"
# where message is the first cli parameter
#
if __name__ == "__main__":
    message=None
    if len(sys.argv) > 1:
        message=sys.argv[1]
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    command.revision(alembic_cfg, autogenerate=True, message=message)
    
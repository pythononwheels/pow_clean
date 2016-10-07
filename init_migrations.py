#
# adapts the alembic migrations ini
# to changes in the pow db config
#
from {{appname}}.dblib import conn_str
import configparser

#config= configparser.ConfigParser.RawConfigParser()
config= configparser.ConfigParser()
config.read(r'alembic.ini')
config.set('alembic','sqlalchemy.url',conn_str)
with open(r'alembic.ini', 'w') as configfile:
    config.write(configfile)
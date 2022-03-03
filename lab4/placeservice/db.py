import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

# The database URL is provided as an env. variable
if 'DB_URL' in os.environ:
    db_url = os.environ['DB_URL']
else:
    db_url = 'sqlite:///place.db'
engine = create_engine(db_url)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))
# https://docs.sqlalchemy.org/en/13/orm/session.html
Session = sessionmaker(bind=engine)
# https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/api.html
Base = declarative_base()

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

engine = create_engine(os.getenv("POSTGRES_URL"))

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)
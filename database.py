# Modified from:
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
import os
import shutil
from sqlalchemy import create_engine
from sys import argv

from app import app
from app import db
from app.models import *
#from migrate.versioning import api


SQLALCHEMY_DATABASE_URI = app.config["SQLALCHEMY_DATABASE_URI"]
SQLALCHEMY_MIGRATE_REPO = app.config["SQLALCHEMY_MIGRATE_REPO"]

def create():
    print 'creating db '+SQLALCHEMY_DATABASE_URI
   
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    print engine
    db.create_all()
    db.session.commit()

def drop():
    os.remove(SQLALCHEMY_DATABASE_URI.split('///')[-1])
    shutil.rmtree(SQLALCHEMY_MIGRATE_REPO)

def reset():
    # Remove old database if it's there
    try:
        os.remove(SQLALCHEMY_DATABASE_URI.split('///')[-1])
    except OSError:
        print("Database not found; creating new database.")

    db.create_all()

def clean():
    """Restore cache and roll back the session.
    """

    db.session.rollback()
    db.session.expunge_all()

if __name__ == "__main__":
    if len(argv)==1:
        argv.append(raw_input('enter operation:\n'))
    print argv
    if argv[1] == "create":
        create()
    elif argv[1] == "drop":
        drop()
    elif argv[1] == "reset":
        reset()
    else:
        print(str(argv[1]) + " is not a valid database operation.")


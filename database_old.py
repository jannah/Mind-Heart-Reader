# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 1, 2014 1:19:29 PM$"

import MySQLdb
from flask import Flask ,render_template, redirect, url_for
#from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.mhreader import mhrbp
#from app import db
from .models import *




engine = create_engine('sqlite:////db/test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from . import models
    print 'initiating database'
#    print engine
    Base.metadata.create_all(bind=engine)
engine = None
Session = None

Base = declarative_base()




def __init__():
    pass
#    connect_to_db()
'''
def connect_to_db():
    db = MySQLdb.connect(host=DB_HOST, # your host, usually localhost
                     user=DB_USER, # your username
                      passwd=DB_PASS, # your password
                      db=DB_NAME) # name of the data base
    engine = create_engine('mysql://'+DB_USER+':'+DB_PASS+'@'+DB_HOST+'/'+DB_NAME)

'''
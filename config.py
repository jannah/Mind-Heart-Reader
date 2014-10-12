# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 2, 2014 1:04:16 AM$"
import os
ROOT = os.path.abspath(os.path.dirname(__file__))
APP_NAME = os.path.basename(ROOT)
DB_USER='jannah'
DB_PASS='podiumapp'
DB_HOST='harbinger.ischool.berkeley.edu:3306'
DB_NAME='jannah'
REMOTE_DB = {'SQLALCHEMY_DATABASE_URI':'mysql://'+DB_USER\
                        +':'+DB_PASS+'@'\
                        + DB_HOST+'/' \
                        + DB_NAME}

LOCAL_DATABASE_PATH= os.path.join(ROOT, APP_NAME + ".db")
LOCAL_DATABASE_URI = 'sqlite:///' + LOCAL_DATABASE_PATH
LOCAL_DB = {'SQLALCHEMY_DATABASE_URI':LOCAL_DATABASE_URI,
        'SQLALCHEMY_MIGRATE_REPO' : os.path.join(ROOT, 'db')}

#SQLALCHEMY_MIGRATE_REPO = os.path.join(ROOT, 'db')
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


import os
import config
from flask import Flask, redirect, url_for,render_template
__author__="Hassan"
__date__ ="$Sep 24, 2014 1:55:19 PM$"
#__name__ = 'mhreader_app'
app = Flask(__name__)
print __name__
mode = 'local'
DB_CONFIG = {}
if mode=='local':
    DB_CONFIG = config.LOCAL_DB
else:
    DB_CONFIG = config.REMOTE_DB

for key in DB_CONFIG:
    app.config[key] = DB_CONFIG[key]
#app.config['APPLICATION_ROOT'] = config.APPLICATION_ROOT
#app.config['SERVER_NAME'] = config.SERVER_NAME
app.config['IP_ADDRESS'] = config.IP_ADDRESS
app.config['PORT'] = config.PORT
print app.config['APPLICATION_ROOT'], app.config['PORT']

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from models import *


from mhreader import mhreader, views
print app.config['APPLICATION_ROOT'], app.config['SERVER_NAME']
app.register_blueprint(mhreader.mhrbp, url_prefix='%s%s'%(config.APPLICATION_ROOT, '/mhreader'))

import logging
log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)



@app.route('/')
def index():
    print 'redirct to ' ,  url_for('mhreader.home_page')
#    print 'redirct to ' ,  url_for('base.html')
#    return 'done'
    return redirect(url_for('mhreader.home_page'))
#    render_template(url_for('base.html'))
    
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from flask import Flask, redirect, url_for
from mhreader import *
__author__="Hassan"
__date__ ="$Sep 24, 2014 1:55:19 PM$"

app = Flask(__name__)
app.register_blueprint(mhreader.mhrbp, url_prefix='/mhreader')

@app.route('/')
def index():
    print 'redirct to ' ,  url_for('mhreader.home_page')
    return redirect(url_for('mhreader.home_page'))
    
__author__="Hassan"
__date__ ="$Sep 24, 2014 2:06:20 PM$"
from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from app import app
from . import mhrbp
from .modules.mindwave import indra_client
from app import db
from app.models import *
import threading
import json
mwc = None
mwc_thread = None
def __init__():
    global mwc_thread
    mwc_thread = indra_client.Client()
    
mindwave_data =[]
@mhrbp.route('/')
def home_page():
    global mwc
    #mwc = mindwave_client.Client()
    
    return render_template('home.html')
   

#mwc_thread = mindwave_client.Client()
#mwc_thread.setDaemon(True)

@mhrbp.route('/start_random_mindwave')
def start_random_mindwave():
    global mwc_thread
    print 'starting random mindwave'
#    mwc_thread = dummy_data_generator.DummyGenerator()
    if not mwc_thread.getStarted():
        mwc_thread.start(run_offline=True , ship_to_server = True)
    else:
        mwc_thread.__init__()
        mwc_thread.setDaemon(True)
        mwc_thread.start()
    #mwc_thread.join()
    
    return 'Started'
   


@mhrbp.route('/start_mindwave')
def start_mindwave():
    global mwc_thread
    mwc_thread = indra_client.Client()
    print 'starting mindwave'
    if not mwc_thread.getStarted():
        mwc_thread.start(run_offline=True , ship_to_server = True, username='Hassan', windows_port = '6', paired = True)
    else:
        mwc_thread.__init__()
#        mwc_thread.setDaemon(True)
        mwc_thread.start()
    #mwc_thread.join()
    
    return 'Started'
   

@mhrbp.route('/stop_mindwave')
def stop_mindwave():
    global mwc_thread
    #mwc_thread.stop()
    mwc_thread.stop()
    mwc_thread = None
    return 'Stopped'
   
@mhrbp.route('/get_mindwave_status', methods=['GET'])
def get_mindwave_status():
    global mwc_thread
    if mwc_thread:
        return mwc_thread.getStatus()
    return 'Unavailable'

@mhrbp.route('/get_mindwave_data', methods = ['GET'])
@mhrbp.route('/get_mindwave_data?<int:last_count>', methods = ['GET'])
@mhrbp.route('/get_mindwave_data/<int:last_count>', methods = ['GET'])
def get_mindwave_data(last_count):
    global mwc_thread
    print 'getting data'
    data = []
    
    if mwc_thread and  mwc_thread.getAlive():
        print 'joining'
        mwc_thread.join(.001)
        data = mwc_thread.get_data(last_count)
    print len(data)
#    if last_count>0 and len(data)>last_count:
#        data = data[-last_count:]
    return json.dumps(data)

@mhrbp.route('/get_data_map', methods = ['GET'])
def get_data_map():
    global mwc_thread
    if mwc_thread:
        data_map = mwc_thread.get_data_map()
        return json.dumps(data_map)
    return '[]'

@mhrbp.route('/dump_data')
@mhrbp.route('/dump_data/<filename>')
def dump_data(filename = 'output.log'):
    global mwc_thread
    mwc_thread.dump_data(filename)
    return 'dumped'
    

@mhrbp.route('/post_data', methods = ['POST'])
def post_data():
    #data = request.form(['data'])
    print 'data'




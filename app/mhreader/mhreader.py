__author__="Hassan"
__date__ ="$Sep 24, 2014 2:06:20 PM$"
from flask import Flask, render_template, redirect, url_for
from . import mhrbp
from .modules import mindwave_client, dummy_data_generator
import threading
import json
mwc = None

mindwave_data =[]
@mhrbp.route('/')
def home_page():
    global mwc
    #mwc = mindwave_client.Client()
    
    return render_template('home.html')
    
#mwc_started = False
'''
def start_mindwave_thread():
    global mwc
    #global mwc_thread
    print 'start mindwave thread'
    #if not mwc_thread.is_alive():
    mwc.run()'''     
#mwc_thread = Thread(target = start_mindwave_thread)
#mwc_thread.daemon = True
'''
class MWC_Thread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None
        self.mwc = mindwave_client.Client()
        self.mwc_started = False
    

    def run(self):
        print "Starting " + self.name
        self.mwc_started = True
        self.process = self.mwc.run()
        #cmd = [ "bash", 'process.sh']
        
        self.process = p = subprocess.Popen(cmd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
        for line in iter(p.stdout.readline, b''):
            print ("-- " + line.rstrip())
        print "Exiting " + self.name

    def stop(self):
        print "Trying to stop thread "
        if self.process is not None:
            self.process.terminate()
            self.process = None
    def get_mwc(self):
        return self.mwc

mwc_thread = MWC_Thread()
'''
random_thread = dummy_data_generator.DummyGenerator()
#random_thread = mindwave_client.Client()
random_thread.setDaemon(True)
@mhrbp.route('/start_mindwave')
def start_mindwave():
    #global mwc_thread
    #global mwc_started
    
    print 'starting mindwave'
    #mwc_thread.start()
    #mwc_thread.join()
    if not random_thread.getStarted():
        random_thread.start()
    else:
        random_thread.__init__()
        random_thread.setDaemon(True)
        random_thread.start()
    #random_thread.join()
    
    return 'Started'
    '''
    if mwc_started == False:
        mwc_thread.start()
        mwc_started = True
        #mwc_thread.join()
        print 'started'
        return 'started %s\t%s' % (mwc_thread.name,  mwc_thread.is_alive())
    else:
        print "mindwave thread already started"
        return 'already started'
    #mwc_thread.join()
    '''

@mhrbp.route('/stop_mindwave')
def stop_mindwave():
    #mwc_thread.stop()
    random_thread.stop()
    return 'Stopped'
    '''
    if mwc_thread.is_alive()or True:
        mwc_thread.process.terminate()
        print 'stopped'
        global mwc_started
        mwc_started = False
        return 'stopped %s' % mwc_thread.name
    else:
        return "no thread was started"
    '''
@mhrbp.route('/get_mindwave_status', methods=['GET'])
def get_mindwave_status():
    return random_thread.getStatus()

@mhrbp.route('/get_mindwave_data', methods = ['GET'])
@mhrbp.route('/get_mindwave_data?<int:last_count>', methods = ['GET'])
@mhrbp.route('/get_mindwave_data/<int:last_count>', methods = ['GET'])
def get_mindwave_data(last_count):
    print 'getting data'
    data = []
    if random_thread.getAlive():
        print 'joining'
        random_thread.join(.001)
        data = random_thread.get_data(last_count)
    print len(data)
#    if last_count>0 and len(data)>last_count:
#        data = data[-last_count:]
    return json.dumps(data)

@mhrbp.route('/get_data_map', methods = ['GET'])
def get_data_map():
    data_map = random_thread.get_data_map()
    return json.dumps(data_map)

@mhrbp.route('/post_data', methods = ['POST'])
def post_data():
    #data = request.form(['data'])
    print 'data'


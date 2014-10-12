
#
#  indra client
#
# (c) 2014 ffff (http://cosmopol.is) 
# MIT license 

from entropy import compute_entropy
from mindwave_mobile import ThinkGearProtocol, ThinkGearRawWaveData, ThinkGearEEGPowerData, ThinkGearPoorSignalData
import threading
import json, requests; from datetime import datetime, date
import time
import dateutil.parser; import dateutil.relativedelta
import sys, platform, random

username = ''
entropy_window = 1024
linux_port = '/dev/tty.MindWaveMobile-DevA'
default_windows_port = '5'
use_port = linux_port
data_maps ={'eeg_power':[
                            {'name':'delta', 'band':'(0.5 - 2.75Hz)', 'order':0},
                            {'name':'theta', 'band' : '(3.5 - 6.75Hz)', 'order':1},
                            {'name':'low-alpha', 'band' : '(7.5 - 9.25Hz)', 'order':2},
                            {'name':'high-alpha', 'band' : '(10 - 11.75Hz)', 'order':3},
                            {'name':'low-beta', 'band' : '(13 - 16.75Hz)', 'order':4},
                            {'name':'high-beta', 'band' : '(18 - 29.75Hz)', 'order':5},
                            {'name':'low-gamma', 'band' : '(31 - 39.75Hz)', 'order':6},
                            {'name':'mid-gamma', 'band' : '(41 - 49.75Hz)', 'order':7}
                            ]}

class Client(threading.Thread):

    def __init__(self, data_type='eeg_power'):
        self.STATUS_LIST = {'started':'Started', 
        'stopped':'Stopped', 
        'unavailable':'Unavailable',
        'error':''}
        threading.Thread.__init__(self)
        self.port = linux_port
        self.data_type = data_type
        self.process = None
        self.alive = False
        self.started = False
        self.status = self.STATUS_LIST['unavailable']
        self.username = None
        self.output_file_writer = None
        self.print_to_console = True
        self.print_output = False
        self.entropy_window = 1024
        self.raw_log = []
        self.start_time = None
	self.end_time = None
	self.signal_quality = 0
        self.timediff = None
        self.setDaemon(True)
        self.ship_to_server = True
        self.paired = False
        self.data=[]
        try:
            self.data_map  =  data_maps[data_type]
        except KeyError:
            self.data_map = {}
            pass
        
    # calculates the diff between our local time and the server's time
    def set_timediff(self, server_time_string):
        server_time = dateutil.parser.parse(server_time_string).replace(tzinfo=None)
        now = datetime.utcnow().replace(tzinfo=None)
        self.timediff = dateutil.relativedelta.relativedelta(now,server_time)

    def get_server_time(self):
        return datetime.utcnow().replace(tzinfo=None) + self.timediff

    def ship_biodata(self):
        # handler for the date
        dthandler = lambda obj: (
            obj.isoformat()
            if isinstance(obj, datetime)
            or isinstance(obj, date)
            else None)
    # construct json
        j = json.dumps({'username':self.username,
              'start_time':self.start_time,
              'end_time':self.end_time,
	      'signal_quality':self.signal_quality,
	      'raw_values':self.raw_log,
              'data_type': self.data_type}, 
	default=dthandler)
        if self.print_to_console:
            print j
#        self.data[:0]=[j]
        self.data.append(j)
        if self.print_output:
            self.output_file_writer.write(j+'\n')
            self.output_file_writer.flush()
        
    # post json
        if self.ship_to_server:
            r = requests.post(
                'http://indra.coolworld.me',
                data=j,
                headers={'content-type': 'application/json'}
            )
            print('.')
    ''' get the data, if limit >0, it will get the first limit items.
    if limit < 0, it will get the last limit items    
    '''
    def get_data(self, limit = 100):
        if limit ==0 or len(self.data)< abs(limit):
            return self.data
        elif limit<0:
            return self.data[limit:]
        else:
            return self.data[:limit]
        
    def reset_data(self):
        self.data=[]
        
    def get_data_map(self):
        return self.data_map
    
    def is_alive(self):
        return self.alive
    
    def is_started(self):
        return self.started
    
    def get_status(self):
        return self.status
    
    
    def start(self, username=None, windows_port=None, paired = False, output_file = None, print_to_console = True, run_offline = False, ship_to_server = True):
        self.started = True
        self.print_to_console = print_to_console
        self.ship_to_server = ship_to_server
        self.username = username
        self.windows_port = windows_port
        self.run_offline = run_offline
        self.paired = paired
        print "Starting " + self.name
        #self.mwc_started = True
        self.alive = True
        self.status = self.STATUS_LIST['started']
        if output_file:
            self.output_file = output_file
            self.print_output = True
            self.output_file_writer = open(output_file, 'w')
        super(Client, self).start()
    def stop(self, dumpfile = None):
        if dumpfile:
            self.dump_data(dumpfile)
        print "Trying to stop thread "
        if self.process is not None:
            self.process.terminate()
            self.process = None
        self.alive = False
        self.status = self.STATUS_LIST['stopped']

    def run(self):

        #store the client as a process that could be killed
        self.process = self.run_client() if not self.run_offline \
            else self.run_offline_client()
    
    def dump_data(self, dumpfile):
        if dumpfile:
            print 'dumping data to ', dumpfile
            with open(dumpfile, 'w') as f:
                f.write(str("\n".join(self.data)))
                f.flush()
                f.close()
    
    def run_client(self):

        # get username
        if not self.username:
            self.username = raw_input('Enter a username: ')
        if 'Windows' in platform.system():
            port_number = self.windows_port if self.windows_port \
                else raw_input('Windows OS detected. Please select proper COM part number (default is %s):'%windows_port)
            self.port= "COM%s"%port_number if len(port_number)>0 else "COM%s"%default_windows_port
        if not self.paired:
            raw_input('Pair your mindwave with your laptop. Just flip the switch on the side of the device. Press ENTER when it\'s paired.')
            self.paired = True

        print '\nconnecting to server...'
        # set the timediff before doing anything
        self.set_timediff(
            requests.get('http://indra.coolworld.me').json()['time']
        )
        print 'connected! when you see periods being printed, data is being shipped to the server. thanks for participating.'
        try:
            for pkt in ThinkGearProtocol(self.port).get_packets():

                for d in pkt:
                    if isinstance(d, ThinkGearPoorSignalData):
                        self.signal_quality += int(str(d))
                        
                    if isinstance(d, ThinkGearRawWaveData): 

                        #how/can/should we cast this data beforehand?
                        self.raw_log.append(float(str(d))) 

                        if len(self.raw_log) == 1:
                            self.start_time = self.get_server_time()
                        if len(self.raw_log) == self.entropy_window:
                            self.end_time = self.get_server_time()
                            self.ship_biodata()
                            # reset variables
                            self.raw_log = []
                            self.signal_quality = 0
        except Exception as e:
            print 'ERROR', str(e)
            self.alive = False
            self.started = False
            self.status = str(e)
            print self.status
            pass
        
    def run_offline_client(self,array_size = 1024,random_number_base = 1000, sleep=1):
        self.set_timediff(
            requests.get('http://indra.coolworld.me').json()['time']
        )
        print 'running offline mode'
        while True:
            entry_data=[]
            for i in range(array_size):
                entry_data.append(float(random.randrange(-random_number_base, random_number_base, 1)))
            self.raw_log = entry_data
#            time_now = datetime.now()
#            entry = {'time':str(time_now), 'values' : entry_data}
            self.ship_to_server = False
            self.ship_biodata()
            self.raw_log = []
            time.sleep(sleep)
        #generate3 random data
        pass
    
import atexit
'''def exit_dump(client, dumpfile):
    print 'exit dump to '%dumpfile
    client.stop(dumpfile)
   ''' 
if __name__ == '__main__':
    output_file = None
    if len(sys.argv)>1:
        output_file = sys.argv[1]
        print 'printing output to %s' % output_file
        
    client = Client()
    client.start(output_file = output_file, run_offline=False , ship_to_server = True, username='Hassan', windows_port = '6', paired = True) 
    atexit.register(client.stop, 'exit_dump.log')
    print 'thread started'
    while True:
#        time.sleep(10)
#        print 'hello'
#        print client.get_data(-2)
        pass

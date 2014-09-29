
#
#  indra client
#
# (c) 2014 ffff (http://cosmopol.is) 
# MIT license 

from entropy import compute_entropy
from mindwave_mobile import ThinkGearProtocol, ThinkGearRawWaveData, ThinkGearEEGPowerData
import json, requests; from datetime import datetime, date
import time
import dateutil.parser; import dateutil.relativedelta
import sys, platform
from .. import mhrbp
from flask import url_for

username = ''
entropy_window = 1024
#linux_port = '/dev/tty.MindWaveMobile-DevA'
windows_port = '5'
#use_port = linux_port
output_file = ''
print_output = False

class Client():
    
    def __init__(self):
        self.username = None
        self.entropy_window = 1024
        self.raw_log = []
        self.timediff = None
        self.data=[]

    # calculates the diff between our local time and the server's time
    def set_timediff(self, server_time_string):
        server_time = dateutil.parser.parse(server_time_string).replace(tzinfo=None)
        now = datetime.utcnow().replace(tzinfo=None)
        self.timediff = dateutil.relativedelta.relativedelta(now,server_time)

    def get_server_time(self):
        return datetime.utcnow().replace(tzinfo=None) + self.timediff

    def ship_biodata(self, data_type, payload):
        # handler for the date
        dthandler = lambda obj: (
            obj.isoformat()
            if isinstance(obj, datetime)
            or isinstance(obj, date)
            else None)
    # construct json
        j = json.dumps({'username':self.username,
              'time':self.get_server_time(),
           'data_type':data_type, 
           'payload':payload}, default=dthandler)
    # post json
        r = requests.post(
            'http://indra.coolworld.me',
            data=j,
            headers={'content-type': 'application/json'}
        )
        r2 = requests.post(
            url_for('mhreader.post_data'),
            data=j,
            headers={'content-type': 'application/json'}
        )
    def get_data(self, last_entries = 100):
        
        return self.data[last_entries:]
    
    def run(self, use_port="COM%s"%windows_port):

        # get username
        self.username = 'MindHeart Raeder'
        '''self.username = raw_input('Enter a username: ')
        if 'Windows' in platform.system():
            port_number = raw_input('Windows OS detected. Please select proper COM part number (default is %s):'%windows_port)
            use_port= "COM%s"%port_number if len(port_number)>0 else "COM%s"%windows_port
        raw_input('Pair your mindwave with your laptop. Just flip the switch on the side of the device. Press ENTER when it\'s paired.')
        '''
        print '\nconnecting...',
        # set the timediff before doing anything
        self.set_timediff(
            requests.get('http://indra.coolworld.me').json()['time']
        )
        print('connected! starting to read mindwave data....') 
        if print_output:
            output_file_writer = open(output_file, 'w')

        for pkt in ThinkGearProtocol(use_port).get_packets():

            for d in pkt:

                if isinstance(d, ThinkGearRawWaveData): 
                    self.raw_log.append(float(str(d))) #how/can/should we cast this data beforehand?

                    # compute and ship entropy when we have > 512 raw values
                    if len(self.raw_log) > self.entropy_window:
                        entropy = compute_entropy(self.raw_log)
                        #print entropy
                        #ship_biodata('entropy',entropy)
                        self.raw_log = []

                if isinstance(d, ThinkGearEEGPowerData): 
                    # TODO: this cast is really embarrassing
                    reading = eval(str(d).replace('(','[').replace(')',']'))
                    reading2 = '"%s": %s'%(datetime.utcnow().replace(tzinfo=None), reading)
                    print reading2
                    if print_output:
                        output_file_writer.write(str(reading2)+'\n')
                        output_file_writer.flush()
                    self.ship_biodata('eeg_power',reading)

'''if __name__ == '__main__':
    if len(sys.argv)>1:
        output_file = sys.argv[1]
        print_output = True
        print 'printing output to %s' % output_file
    client = Client()
    client.run() '''

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import threading
import random, time
from datetime import datetime, date
class DummyGenerator(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.process = None
        self.data=[]
        self.alive = False
        self.started = False
        self.setDaemon(True)
        self.data_map  =  [
                            {'name':'delta', 'band':'(0.5 - 2.75Hz)', 'order':0},
                            {'name':'theta', 'band' : '(3.5 - 6.75Hz)', 'order':1},
                            {'name':'low-alpha', 'band' : '(7.5 - 9.25Hz)', 'order':2},
                            {'name':'high-alpha', 'band' : '(10 - 11.75Hz)', 'order':3},
                            {'name':'low-beta', 'band' : '(13 - 16.75Hz)', 'order':4},
                            {'name':'high-beta', 'band' : '(18 - 29.75Hz)', 'order':5},
                            {'name':'low-gamma', 'band' : '(31 - 39.75Hz)', 'order':6},
                            {'name':'mid-gamma', 'band' : '(41 - 49.75Hz)', 'order':7}
                            ]

    def generate_random(self, array_size = 8,random_number_base = 1000, sleep=1):
        
        while True:
            entry_data=[]
            for i in range(array_size):
                entry_data.append(int(random.random() * random_number_base/2)+random_number_base/2)
            time_now = datetime.now()
            entry = {'time':str(time_now), 'values' : entry_data}
            #print entry
            self.data[:0]=[entry]
            time.sleep(sleep)
        #return data
    def get_data(self, last = 100):
       
        if last ==0 or len(self.data)<last:
            return self.data
        else:
            return self.data[:last]
    def get_data_map(self):
        return self.data_map
    def run(self):
        self.started = True
        print "Starting " + self.name
        #self.mwc_started = True
        self.alive = True
        self.process = self.generate_random()
        #cmd = [ "bash", 'process.sh']
    def dump_data(self, outputfile):
        if outputfile:
            with open(outputfile, 'w') as f:
                f.write(str(self.data))
                f.flush()
                f.close()
            with open("%s.csv"%outputfile, 'w') as f:
                f.write("time,%s\n"%",".join([str(i) for i in range(len(self.data[0]['values']))]))
                for d in self.data:
                    f.write("%s,%s\n"%(d['time'], ",".join([str(i) for i in d['values']])))
                f.close()
    
    def getAlive(self):
        return self.alive
    def getStarted(self):
        return self.started
    
    def getStatus(self):
        return 'Started' if self.alive else 'Stopped'
    
    def stop(self):
        print "Trying to stop thread "
        if self.process is not None:
            self.process.terminate()
            self.process = None
        self.alive = False


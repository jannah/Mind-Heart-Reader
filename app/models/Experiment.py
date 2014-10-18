# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 2, 2014 1:49:14 PM$"


from app.mhreader import mhrbp
from .. import db
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
import json

class Experiment(db.Model):
    __tablename__ = "mhreader_experiments"
    __name__='experiment'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('mhreader_users.id'))
    experiment_set_id  = Column(Integer, ForeignKey('mhreader_experiment_sets.id'))
    remarks = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    completed = Column(Boolean)
    logs = relationship('ExperimentLog', backref=backref('experiment'), order_by='ExperimentLog.timestamp')
    
    def start(self):
        self.start_time = datetime.now()
    def stop(self):
        self.end_time = datetime.now()
        self.completed = True
    def update_remarks(self, remarks ):
        self.remarks = remarks   
    def __init__(self, title, user_id, experiment_set_id , start_time=None, end_time=None, remarks=None):
        self.title= title
        self.user_id = user_id
        self.experiment_set_id = experiment_set_id 
        self.start_time = start_time
        self.end_time = end_time
        self.completed = end_time is not None
        self.remarks=remarks
    def __repr__(self):
        
        rep = {self.__name__:{'id':self.id, 'title':self.title,'user_id':self.user_id,'experiment_set_id':self.experiment_set_id,
                                'start_time': self.start_time,'end_time': self.end_time,'completed':self.completed,'remarks':self.remarks}}
        return json.dumps(rep)
    def to_json(self):
        j = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            j[col.name] = getattr(self, col.name)
        j['start_time'] = str(self.start_time)
        j['end_time'] = str(self.end_time)
        j['user'] = self.user.to_json()
        j['logs'] = [log.to_json() for log in self.logs]
        return j
#        return '''{"%s":{"id":%d, "title":"%s", "user_id":%d, "experiment_set_id":%d, "start_time":"%s", "end_time":"%s", "remarks":"%s"}}'''\
#                    % (self.__name__, self.id, self.title, self.user_id, self.experiment_set_id, self.start_time, self.end_time, self.remarks)
# 
        
#    def __repr__(self):
#        return '''{"%s":{"id":%d, "title":"%s", "user_id":%d, "experiment_set_id":%d, "start_time":"%s", "end_time":"%s", "remarks":"%s"}}'''\
#                    % (self.__name__, self.id, self.title, self.user_id, self.experiment_set_id, self.start_time, self.end_time, self.remarks) 
#        return str("{'test':'test'}")

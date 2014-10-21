# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 2, 2014 1:49:14 PM$"


from app.mhreader import mhrbp
from .. import db
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
from dateutil.tz import tzlocal
import pytz, json

class ExperimentLog(db.Model):
    __tablename__ = "mhreader_experiment_logs"
    __name__='experiment_log'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('mhreader_users.id'))
    experiment_id = Column(Integer, ForeignKey('mhreader_experiments.id'))
    action = Column(Integer)
    timestamp = Column(DateTime( timezone = True))
    action_type = Column(String)
    experiment_file_id = Column(Integer, ForeignKey('mhreader_experiment_files.id'))
    result = Column(String)

    
    def __init__(self, user_id, experiment_id, action, action_type=None,timestamp=None,  experiment_file_id = None, result = None):
        self.user_id = user_id
        self.experiment_id = experiment_id
        self.timestamp = timestamp if timestamp else datetime.now()
        self.timestamp = self.timestamp.replace(microsecond=0)
        self.action = action
        self.action_type = action_type
        self.experiment_file_id = experiment_file_id
        self.result = result
        
    def __repr__(self):
        '''return {"%s":{
                    "id":"%s",
                    "user_id":"%s",
                    "experiment_id":"%s",
                    "timestamp":"%s",
                    "action_type":"%s",
                    "experiment_file_id":"%s",
                    "result":"%s"}}
                 
                %(
                    self.id, self.user_id, 
                    self.experiment_id, 
                    self.timestamp, 
                    self.action_type,
                    self.experiment_file_id,
                    self.result)
        '''
        return json.dumps(self.to_json())
            
    def to_json(self):
        j = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            j[col.name] = getattr(self, col.name)
        j['timestamp'] = str(self.timestamp)
        if self.experiment_file:
            j['file'] = self.experiment_file.to_json(target_gender=self.experiment.experiment_set.target_gender)
        return j
    
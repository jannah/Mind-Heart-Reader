# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 19, 2014 11:28:22 PM$"

'''
Attention	Meditation	Familiarity	MentalEffort	Appreciation	SignalQuality	EventTagging	Delta	Theta	Alpha	Beta	Gamma

'''

from app.mhreader import mhrbp
from .. import db
from sqlalchemy import Column, Integer,Float, String, Sequence, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
from dateutil.tz import tzlocal
import json
import pytz

class MindwaveLog(db.Model):
    __tablename__ = "mhreader_mindwave_logs"
    __name__='mindwave_log'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    experiment_id  = Column(Integer, ForeignKey('mhreader_experiments.id'))
    timestamp = Column(DateTime(timezone = True))
    attention = Column(Float)
    meditation = Column(Float)
    familiarity = Column(Float)
    mental_effort = Column(Float)
    appreciation = Column(Float)
    signal_quality = Column(Integer)
    evant_tagger = Column(Integer)
    delta = Column(Float)
    theta = Column(Float)
    alpha = Column(Float)
    beta = Column(Float)
    gamma = Column(Float)
    response = Column(String)
    new_image = Column(Boolean)
    image_order = Column(Integer)
    image_order_index = Column(Integer)
    experiment_file_id = Column(Integer, ForeignKey('mhreader_experiment_files.id'))
    experiment_log_id = Column(Integer, ForeignKey('mhreader_experiment_logs.id'))
    
#    logs = relationship('ExperimentLog', backref=backref('experiment'), order_by='ExperimentLog.timestamp')
   
    def __init__(self, experiment_id ,  timestamp, attention=0.0,\
    meditation=0.0,familiarity=0.0,mental_effort=0.0,\
    appreciation=0.0,signal_quality = 0, event_tagger = -1, delta=0.0,theta=0.0,alpha=0.0,beta=0.0,gamma=0.0, response = None,\
        index = 0,new_image = False, image_order =0, image_order_index=0, experiment_file_id=None):
        self.experiment_id =experiment_id
        self.index = index
        self.timestamp = timestamp
        self.attention=attention	
        self.meditation=meditation	
        self.familiarity=familiarity	
        self.mental_effort=mental_effort
        self.appreciation=appreciation
        self.signal_quality = signal_quality
        self.event_tagger = event_tagger
        self.delta=delta	
        self.theta=theta	
        self.alpha=alpha	
        self.beta=beta
        self.gamma=gamma
        self.response = response
        self.new_image = new_image
        self.image_order = image_order
        self.image_order_index = image_order_index
        self.experiment_file_id = experiment_file_id

    def __repr__(self):
        return json.dumps(self.to_json())
#        return json.dumps(rep)
    def to_json(self):
        j = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            j[col.name] = getattr(self, col.name)
        j['timestamp'] = str(self.timestamp)
        j['experiment_title']=self.experiment.title
        j['experiment_user']=self.experiment.user.name
        j['filename'] = ''
        j['projected_male_response'] = ''
        j['projected_female_response'] = ''
        if self.experiment_file_id:
            j['filename']=self.experiment_file.filename
            j['projected_male_response'] = self.experiment_file.male_response
            j['projected_female_response'] = self.experiment_file.female_response
        return j
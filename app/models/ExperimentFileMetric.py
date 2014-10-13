# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 12, 2014 1:49:14 PM$"


from app.mhreader import mhrbp
from .. import db
from sqlalchemy import Column, Integer, String, Float, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date

class ExperimentFileMetric(db.Model):
    __tablename__ = "mhreader_experiment_file_metrics"
    __name__='experiment_set_file'
    id = Column(Integer, primary_key=True)
    experiment_file_id = Column(Integer, ForeignKey('mhreader_experiment_files.id'),  onupdate="cascade")
    demographic= Column(String)
    pleasure_mean= Column(Float)
    pleasure_std= Column(Float)
    arrousal_mean= Column(Float)
    arrousal_std= Column(Float)
    dominance1_mean= Column(Float)
    dominance1_std= Column(Float)
    dominance2_mean= Column(Float)
    dominance2_std= Column(Float)
#    experiment_logs = relationship('ExperimentLog', backref=backref('experiment_set_file'))
    
    def __init__(self, experiment_file_id, demographic, \
        pleasure_mean=0, pleasure_std=0, arrousal_mean=0, arrousal_std=0,\
        dominance1_mean =0, dominance1_std =0, dominance2_mean=0, dominance2_std=0 ):
        
        self.experiment_file_id=experiment_file_id
        self.demographic=demographic 
        self.pleasure_mean=pleasure_mean if not isinstance(pleasure_mean, basestring) else 0
        self.pleasure_std=pleasure_std if not isinstance(pleasure_std, basestring)else 0
        self.arrousal_mean=arrousal_mean if not isinstance(arrousal_mean, basestring)else 0
        self.arrousal_std=arrousal_std if not isinstance(arrousal_std, basestring)else 0
        self.dominance1_mean =dominance1_mean if not isinstance(dominance1_mean, basestring)else 0
        self.dominance1_std =dominance1_std if not isinstance(dominance1_std, basestring)else 0
        self.dominance2_mean=dominance2_mean if not isinstance(dominance2_mean, basestring)else 0
        self.dominance2_std=dominance2_std if not isinstance(dominance2_std, basestring)else 0
        
    def __repr__(self):
        return '''{"%s":
                    {"id":%d, 
                    "experiment_file_id":%d, 
                    "demographic":"%s", 
                    "pleasure_mean":%.2f,
                    "pleasure_std":%.2f,
                    "arrousal_mean":%.2f,
                    "arrousal_std":%.2f,
                    "dominance1_mean":%.2f,
                    "dominance1_std":%.2f,
                    "dominance2_mean":%.2f,
                    "dominance2_std":%.2f,
                    }}'''\
                    % (self.__name__,
                    self.id, 
                    self.experiment_file_id, 
                    self.demographic, 
                    self.pleasure_mean,
                    self.pleasure_std,
                    self.arrousal_mean,
                    self.arrousal_std,
                    self.dominance1_mean,
                    self.dominance1_std,
                    self.dominance2_mean,
                    self.dominance2_std) 
    
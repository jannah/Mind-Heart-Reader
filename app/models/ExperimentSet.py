# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 2, 2014 1:49:14 PM$"


from app.mhreader import mhrbp
from .. import db
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date
import json

class ExperimentSet(db.Model):
    __tablename__ = "mhreader_experiment_sets"
    __name__='experiment_set'
    id= Column(Integer, primary_key=True)
    title = Column(String)
    target_gender = Column(String)
    stimulus_type = Column(String)
    remarks = Column(String)
    files = relationship('ExperimentSetFile', backref=backref('experiment_set'))
    experiments = relationship('Experiment', backref=backref('experiment_set'))
    
    def __init__(self, title, target_gender, stimulus_type, remarks =None):
        self.title= title
        self.target_gender = target_gender
        self.stimulus_type = stimulus_type
        self.remarks = remarks
    
    def __repr__(self):
        return '''{"%s":{"id":%d, "title":"%s", "target_gender":"%s", "stimulus_type":"%s", "remarks":"%s"}}'''\
                    % (self.__name__, self.id, self.title, self.target_gender, self.stimulus_type, self.remarks)
    def to_json(self):
        j = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            j[col.name] = getattr(self, col.name)
        j['set_files'] = [f.to_json() for f in self.files]
#        for f in self.files:
#            j['set_files']+=[f.to_json()]
       
        return j
    
    
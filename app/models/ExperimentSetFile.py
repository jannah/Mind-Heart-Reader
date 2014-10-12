# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 2, 2014 1:49:14 PM$"


from app.mhreader import mhrbp
from .. import db
from sqlalchemy import Column, Integer, String, Float, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime, date

class ExperimentSetFile(db.Model):
    __tablename__ = "mhreader_experiment_set_files"
    __name__='experiment_set_file'
    id = Column(Integer, primary_key=True)
    experiment_set_id = Column(Integer, ForeignKey('mhreader_experiment_sets.id'))
    experiment_file_id = Column(Integer, ForeignKey('mhreader_experiment_files.id'))
    
    def __init__(self, experiment_set_id, experiment_file_id):
        self.experiment_set_id=experiment_set_id
        self.experiment_file_id = experiment_file_id
    def __repr__(self):
        return '''{"%s":
                    {"id":%d, 
                    "experiment_set_id":%d, 
                    "experiment_file_id":%d
                    }}'''\
                    % (self.__name__,
                    self.id, 
                    self.experiment_set_id, 
                    self.experiment_file_id) 
    
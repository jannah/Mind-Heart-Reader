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
    experiment_file_order = Column(Integer)
    def __init__(self, experiment_set_id, experiment_file_id, experiment_file_order = None):
        self.experiment_set_id=experiment_set_id
        self.experiment_file_id = experiment_file_id
        if experiment_file_order:
            self.experiment_file_order = experiment_file_order
        else:
            ESF = ExperimentSetFile.query.filter_by(experiment_set_id=self.experiment_set_id).all()
            self.order = len(ESF) + 1 
        
    def __repr__(self):
        return '''{"%s":
                    {"id":%d, 
                    "experiment_set_id":%d, 
                    "experiment_file_id":%d,
                    "experiment_file":"%s",
                    "experiment_file_order":%d
                    }}'''\
                    % (self.__name__,
                    self.id, 
                    self.experiment_set_id, 
                    self.experiment_file_id,
                    self.experiment_file,
                    self.experiment_file_order) 
    def to_json(self):
        j = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            j[col.name] = getattr(self, col.name)
        j['experiment_file'] = self.experiment_file.to_json()
        return j
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 1, 2014 2:40:08 PM$"
#from database import Base
from app.mhreader import mhrbp
#from app import db
from .. import db
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship, backref


#Base = declarative_base()
class User(db.Model):
    __tablename__ = "mhreader_users"
    __name__='user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    description = Column(String)
    experiments = relationship('Experiment', backref=backref('user'))
    experiment_logs= relationship('ExperimentLog', backref=backref('user'))
    
    def __init__(self, name, age, gender, description):
        self.name = name
        self.age=age
        self.gender = gender
        self.description = description  
    def __repr__(self):
        return '''{"%s":{"id":%d, "name":"%s", "age":"%s", "gender":"%s", "description":"%s"}}''' \
    % (self.__name__, self.id if self.id else 0, self.name, self.age, self.gender, self.description) 
                            

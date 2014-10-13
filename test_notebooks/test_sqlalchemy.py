# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 7, 2014 1:28:20 AM$"

from optparse import __repr__
from app import app
from app.models import *
from app import db
import json





def flat_sql_dict(sql_object):
    title= sql_object.__name__
    flat = {title:{}}
    for item in sql_object.__dict__:
        if '_sa_' not in item:
            value = sql_object.__dict__[item]
            if value is None or value =="None":
                value = ""
            flat[title][item] = value
    return flat

def combine_sql_objects(parent, children, child_name=None):
    child_name = child_name if child_name else children[0].__name__
    parent_d={}
    parent_d[parent.__name__] = flat_sql_dict(parent)
    parent_d[parent.__name__][child_name+'s']=[]
    for child in children:
#        print child
        parent_d[parent.__name__][child_name+'s'].append(flat_sql_dict(child))
    print parent_d
    return parent_d

users = db.session.query(User).all()

users_d = []
for user in users:
    users_d.append(combine_sql_objects(user, user.experiments))


#json.dumps(str(users_d))

exp = Experiment.query.all()
print exp
exp2 = json.dumps(str(exp))
exp2 = json.loads(exp2)

print exp2



exp_sets = ExperimentSet.query.filter_by().first()
for exp_set in [exp_sets]:
    print str(exp_set)
#    files = []
#    for exp_set_file in exp_set.files:
#        files+=[exp_set_file.experiment_file]
#    print files
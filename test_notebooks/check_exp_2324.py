# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 26, 2014 12:50:30 AM$"

from app import db
from app.models import * 

ids=[23,24]
exps = Experiment.query.all()
print len(exps)
for id in ids:
    exp = Experiment.query.filter_by(id=id).first()
    for log in exp.logs:
        print log.timestamp
    
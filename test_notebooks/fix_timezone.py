# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 21, 2014 2:59:02 AM$"

from app import db
from app.models import *
from datetime import timedelta


target_ids = [7, 10,11,12,13,15,16,17,18]
for experiment_id in target_ids:
    exp_logs = ExperimentLog.query.filter_by(experiment_id=experiment_id).all()

    for exp_log in exp_logs:
        print exp_log.timestamp
#        exp_log.timestamp = exp_log.timestamp+timedelta(hours=-7)
    #    print exp_log.timestamp
        exp_log.timestamp = exp_log.timestamp.replace(microsecond=0)
        db.session.add(exp_log)
        db.session.flush()
    db.session.commit()
    exps = Experiment.query.filter_by(id=experiment_id).all()
    for exp in exps:
        if exp.start_time:
#            exp.start_time = exp.start_time+timedelta(hours=-7)
            exp.start_time = exp.start_time.replace(microsecond=0)
        if exp.end_time:
            exp.end_time = exp.end_time+timedelta(hours=-7)
            exp.end_time = exp.end_time.replace(microsecond=0)
        db.session.add(exp)
        db.session.flush()
db.session.commit()
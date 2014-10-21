# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 21, 2014 3:27:51 AM$"
from app import db
from app.models import * 
from datetime import timedelta
experiment_id=5
experiment = Experiment.query.filter_by(id=experiment_id).first()
print experiment
exp_logs = ExperimentLog.query.filter_by(experiment_id=experiment_id).all()
print len(exp_logs)
previous_timestamp = experiment.start_time + timedelta(seconds=-1)
for exp_log in exp_logs:
    mlogs = db.session.query(MindwaveLog).filter(MindwaveLog.experiment_id == experiment_id, \
                MindwaveLog.timestamp<=exp_log.timestamp, \
                MindwaveLog.timestamp>previous_timestamp).all()
    for mlog in mlogs:
        mlog.response = exp_log.action
        db.session.add(mlog)
    db.session.flush()
    previous_timestamp = exp_log.timestamp
    print len(mlogs)
db.session.commit()
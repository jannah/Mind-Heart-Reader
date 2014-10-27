# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 20, 2014 4:01:35 PM$"
from app import db
from app.models import *
from datetime import timedelta
def upload_mindwave_data(experiment_id=None, mindwave_file=None):
    if not experiment_id:
        experiment_id= request.form['experiment_id']

    if not mindwave_file:
        mindwave_file = request.files['mindwave_file']
        print mindwave_file
        print mindwave_file.filename
        

    mindwave_data =  csv.reader(mindwave_file)
    last_timesatmp = get_timestamp_from_filename(mindwave_file.filename)
    headers = []
    experiment = Experiment.query.filter_by(id=experiment_id).first()
    MindwaveLog.query.filter_by(experiment_id=experiment_id).delete()
    rows = [row for row in mindwave_data]
    for i in range(len(rows)):
        row = rows[i]
        if i==0:
            headers =dict([(MINDWAVE_HEADER_MAP[row[i]], i) for i in range(len(row)) ])
            print headers
        else:
            row_ts = last_timesatmp+timedelta(seconds=-(len(rows)-i-1))
            timestamp = row_ts
            attention=row[headers['attention']]	
            meditation=row[headers['meditation']]
            familiarity=row[headers['familiarity']]	
            mental_effort=row[headers['mental_effort']]
            appreciation=row[headers['appreciation']]
            signal_quality = row[headers['signal_quality']]
            event_tagger = row[headers['event_tagger']]
            delta=row[headers['delta']]
            theta=row[headers['theta']]
            alpha=row[headers['alpha']]
            beta=row[headers['beta']]
            gamma=row[headers['gamma']]
            response = None
            
            db.session.flush()
            
#            response = row[headers['response']]
            mlog = MindwaveLog(experiment_id=experiment_id, \
                    timestamp = timestamp,attention=attention,	\
                    meditation=meditation,familiarity=familiarity,\
                    mental_effort=mental_effort,appreciation=appreciation,\
                    signal_quality = signal_quality,event_tagger = event_tagger,\
                    delta=delta,theta=theta,	\
                    alpha=alpha,beta=beta,\
                    gamma=gamma,response = response)
            db.session.add(mlog)
            db.session.flush()
    
#    mlogs = MindwaveLog.query.filter_by(experiment_id=experiment_id).all()
#    for i in range(len(mlogs)-1, 0, -1):
    exp_logs = ExperimentLog.query.filter_by(experiment_id=experiment_id).all()
    print experiment
    previous_timestamp = experiment.start_time + timedelta(seconds=-1)
    for exp_log in exp_logs:
        mlogs = db.session.query(MindwaveLog).filter(MindwaveLog.experiment_id == experiment_id, \
                    MindwaveLog.timestamp<=exp_log.timestamp, \
                    MindwaveLog.timestamp>previous_timestamp).all()
        print len(mlogs)
        
        for mlog in mlogs:
            mlog.response = exp_log.action
            mlog.experiment_file_id = exp_log.experiment_file_id
            mlog.experiment_log_id = exp_log.id
            db.session.add(mlog)
        db.session.flush()
        previous_timestamp = exp_log.timestamp           
    db.session.commit()

        
        
    return 'uploaded'

def fix_mindwave_log(experiment_id):
    experiment = Experiment.query.filter_by(id=experiment_id).first()
    if experiment.start_time:
        exp_logs = ExperimentLog.query.filter_by(experiment_id=experiment_id).all()

        pre_mlogs = db.session.query(MindwaveLog).filter(MindwaveLog.experiment_id == experiment_id, \
            MindwaveLog.timestamp<=experiment.start_time).all()
        #fix pre experiment entries

        for i in range(len(pre_mlogs)):
            pmlog = pre_mlogs[i]
            pmlog.index = i - len(pre_mlogs)
            pmlog.image_order = None
            db.session.add(pmlog)
            db.session.flush()

        index = 0
        previous_timestamp = experiment.start_time + timedelta(seconds=-1)
        for i in range(len(exp_logs)):
            exp_log = exp_logs[i]
            mlogs = db.session.query(MindwaveLog).filter(MindwaveLog.experiment_id == experiment_id, \
                    MindwaveLog.timestamp<=exp_log.timestamp, \
                    MindwaveLog.timestamp>previous_timestamp).all()
            image_order_index = 1
            if len(mlogs)>0:
                mlogs[0].new_image = True
                db.session.add(mlogs[0])
                db.session.flush()
                for mlog in mlogs:
                    mlog.response = exp_log.action
                    mlog.new_image = True if mlog.new_image == True else False
                    mlog.index = index
                    mlog.image_order = i+1
                    mlog.image_order_index = image_order_index
                    mlog.experiment_file_id = exp_log.experiment_file_id
                    mlog.experiment_log_id = exp_log.id
                    index += 1
                    image_order_index+=1
                    db.session.add(mlog)
            db.session.flush()
            previous_timestamp = exp_log.timestamp
        if experiment.end_time:
            post_mlogs = db.session.query(MindwaveLog).filter(MindwaveLog.experiment_id == experiment_id, \
                MindwaveLog.timestamp>experiment.end_time).all()
            for i in range(len(post_mlogs)):
                pmlog = post_mlogs[i]
                pmlog.index = index
                index+=1
                pmlog.image_order = None
                db.session.add(pmlog)
                db.session.flush()
        db.session.commit()

experiments = Experiment.query.all()
for exp in experiments:
    fix_mindwave_log(exp.id)
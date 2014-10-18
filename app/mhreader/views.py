# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 2, 2014 1:54:50 AM$"
from app.models import *
from app.mhreader import mhrbp
from flask import request, render_template, jsonify, make_response
from app import db
import json

def flat_sql_dict(sql_object):
    title= sql_object.__name__
    flat = {title:{}}
    for item in sql_object.__dict__:
        item = str(item)
        if '_sa_' not in item:
            value = sql_object.__dict__[item]
            if value is None or value =="None":
                value = ""
            flat[title][item] = value if not isinstance(value, str) else str(value).encode('utf-8')
    return flat

def combine_sql_objects(parent, children, child_name=None):
    if not isinstance(children, list):
        children = [children]
    
#    parent_d={}
    parent_d= flat_sql_dict(parent)
    if len(children)>0:
        child_name = child_name if child_name else children[0].__name__
        parent_d[parent.__name__][child_name+"s"]=[]
        for child in children:
    #        print child
            parent_d[parent.__name__][child_name+"s"].append(flat_sql_dict(child))
    #    print parent_d
    return parent_d


@mhrbp.route('/users')
def show_user_page():
    return render_template('users.html')

@mhrbp.route('/users/get_users')
def get_users():
    user_id = request.args.get('user_id', '')
    users = User.query.all()
    '''users_d =[]
    for user in users:
        users_d.append(combine_sql_objects(user, user.experiments))
    return json.dumps(users_d)'''
    return json.dumps([user.to_json(add_experiments=True) for user in users])

@mhrbp.route('/users/get_user')
def get_user():
    user_id = request.args.get('user_id', '')
    return str(User.query.filter_by(id=user_id))

@mhrbp.route('/users/add_user', methods=['POST'])
def add_user():
#    print request.args
#    for item in request.form:
#        print item, request.form[item]
    name = request.form['name']
    gender = request.form['gender']
    age = request.form['age']
    description = request.form['description']
#    print name, gender, age
    
    user = User(name = name, gender = gender, age=age, description = description)
    print user
    db.session.add(user)
    db.session.commit()
    print 'Adding user'
    return 'user'


@mhrbp.route('/users/delete_user')
def delete_user():
    user_id = request.args.get('id', '')
    if user_id:
#        print request.args
        print 'deleting user ', user_id
        user = User.query.filter_by(id=user_id).first()
#        print user
               
        db.session.delete(user)
        db.session.commit()
        return 'deleted'
    else:
        return 'ERROR: need user ID'

@mhrbp.route('/experiments/create_experiment', methods=['POST'])
def create_experiment():
    try:
        user_id = request.form['user_id']
        exp_set_id = request.form['experiment_set_id']
        title = request.form['title']
        remarks = request.form['remarks']
        exp = Experiment(title=title, user_id=user_id, experiment_set_id=exp_set_id, remarks=remarks)
        db.session.add(exp)
        db.session.commit()
    except Error:
        return 'Error: cannot add user experiment'
    return 'user experiment created'


@mhrbp.route('/experiments/get_experiment')
def get_experiment():
    if len(request.args)>0:
        exp_id = request.args.get('experiment_id', '')
        if exp_id:
            experiment = Experiment.query.filter_by(id=exp_id).first()
            return str(combine_sql_objects(experiment, experiment.experiment_set))
    else:
        exps = db.session.query(Experiment).all()
        return str(exps)
#        exps_d = []
#        for exp in exps:
#            exps_d.append(combine_sql_objects(exp, exp.experiment_set))
#        print exps_d
#        return json.dumps(exps_d, ensure_ascii=True)
    



@mhrbp.route('/experiments/get_experiment_set')
def get_experiment_set():
    if len(request.args)>0:
        exp_set_id = request.args.get('experiment_set_id', '')
        if exp_set_id:
            return str(ExperimentSet.query.filter_by(id=exp_set_id).first())
        exp_id = request.args.get('experiment_id', '')
        if exp_id:
            exp = Experiment.query.filter_by(id=exp_id).first()
            exp_set = ExperimentSet.query.filter_by(id=exp.experiment_set_id).first()
#            print json.dumps(exp_set.to_json())
            
            return json.dumps(exp_set.to_json())
        
    result = ExperimentSet.query.all()
#    print result
    return str(result)
    

@mhrbp.route('/experiments/get_experimen_files')
def get_experiment_files():
    if len(request.args)>0:
        exp_set = None
        exp_set_id = request.args.get('experiment_set_id', '')
        if exp_set_id:
            exp_set = ExperimentSetFile.query.filter_by(experiment_set_id=exp_set_id).first()
            
            return json.dumps(exp_set)
#            return str(ExperimentSetFile.query.filter_by(experiment_set_id=exp_set_id).all())
    return str(ExperimentSetFile.query.all())
    

@mhrbp.route('/experiments/')
def load_experiment_page(experiment_id=None):
    experiment_id = experiment_id if experiment_id else request.args.get('experiment_id')
    
    experiment = Experiment.query.filter_by(id=experiment_id).first()
    user = User.query.filter_by(id=experiment.user_id).first()
    return render_template('experiment.html', experiment=experiment, user=user)

@mhrbp.route('/experiments/start_experiment')
def start_experiment(experiment_id=None):
    if not experiment_id:
        experiment_id = request.args.get('experiment_id', '')
    experiment = Experiment.query.filter_by(id = experiment_id).first()
    log = ExperimentLog.query.filter_by(experiment_id = experiment_id).delete()
    db.session.flush()
    experiment.start()  
    db.session.add(experiment)
    db.session.commit()
    return 'started at %s' %str( experiment.start_time)

@mhrbp.route('/experiments/stop_experiment')
def stop_experiment(experiment_id=None):
    if not experiment_id:
        experiment_id = request.args.get('experiment_id', '')
    experiment = Experiment.query.filter_by(id = experiment_id).first()
    experiment.stop()
    db.session.add(experiment)
    db.session.commit()
    return 'finished at %s' %str( experiment.end_time)
    
@mhrbp.route('/experiments/add_user_response', methods=['POST'])
def add_user_response(experiment_id=None, experiment_file_id=None, user_id=None, action=None, action_type=None):
    experiment_id = experiment_id if experiment_id else request.form['experiment_id']
    experiment_file_id = experiment_file_id if experiment_file_id else request.form['experiment_file_id']
    user_id = user_id if user_id else request.form['user_id']
    action = action if action else request.form['action']
    action_type = action_type if action_type else request.form['action_type']
    print experiment_id, action
    exp_log = ExperimentLog(user_id=user_id, experiment_id=experiment_id, action=action, action_type=action_type,  experiment_file_id = experiment_file_id)
    db.session.add(exp_log)
    db.session.commit()
    return 'user log entry created %s at %s'% (exp_log.id, exp_log.timestamp)

def parse_user_data_dump(user_id = None, user=None):
    if not user:
        user = User.query.filter_by(id = user_id).first()


def get_experiment_data_dump(experiment_id=None, experiment=None):
    print experiment
    
    if experiment is None:
        experiment = Experiment.query.filter_by(id=experiment_id).first()
    return experiment.to_json()
    
    
    
    
@mhrbp.route('/experiments/get_data_dump')
def get_data_dump(experiment_id = None):

    
    if experiment_id:
        return parse_experiment_data_dump(experiment_id=experiment_id)
    else:
        results = []
        experiments = Experiment.query.all()
        for experiment in experiments:
            print experiment.id
            
            results.append(get_experiment_data_dump(experiment=experiment))
            
    response = make_response(json.dumps(results))
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=data_dump.json"
    return response
#    return json.dumps(results)



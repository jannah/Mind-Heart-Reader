# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 6, 2014 3:02:03 PM$"


from app.models import User, ExperimentSet, ExperimentSetFile, ExperimentFile
from app import db
ExperimentSet.query.delete()
ExperimentSetFile.query.delete()
db.session.commit()
expset1 = ExperimentSet(title='Male Images', target_gender='Male', stimulus_type='Images')
expset2 = ExperimentSet(title='Female Images', target_gender='Female', stimulus_type='Images')
expset3 = ExperimentSet(title='Male Sounds', target_gender='Male', stimulus_type='Sounds')
expset4 = ExperimentSet(title='Female Sounds', target_gender='Female', stimulus_type='Sounds')
db.session.add(expset1)
db.session.add(expset2)
db.session.add(expset3)
db.session.add(expset4)
db.session.flush()
db.session.commit()
#csv_vile = open('set_list.csv', 'r')
import csv, os
preference_list = csv.reader( open(os.path.join(os.path.dirname(__file__),'set_list.csv'), 'r'))
headers =[]
file_list = []
for line in preference_list:
    if len(headers)==0:
        headers = line
    else:
        extension = 'jpg' if headers[0] == 'IAPS' else 'wav'
        filename = '%s.%s'%(line[0], extension)
        print filename
        male_response = line[1]
        female_response = line[2]
        male_order = line[3]
        female_order = line[4]
        exp_file = ExperimentFile.query.filter_by(filename=filename).first()
        print exp_file
        exp_file.male_response=male_response
        exp_file.female_response=female_response
        db.session.add(exp_file)
        db.session.flush()
        if headers[0]=='IAPS':
            if male_response !='':
                exp_file_set = ExperimentSetFile(experiment_set_id = expset1.id, experiment_file_id = exp_file.id, experiment_file_order = male_order)
                db.session.add(exp_file_set)
            if female_response !='':
                exp_file_set = ExperimentSetFile(experiment_set_id = expset2.id, experiment_file_id = exp_file.id, experiment_file_order = female_order)
                db.session.add(exp_file_set)
        if headers[0]=='IADS':
            if male_response !='':
                exp_file_set = ExperimentSetFile(experiment_set_id = expset3.id, experiment_file_id = exp_file.id, experiment_file_order = male_order)
                db.session.add(exp_file_set)
            if female_response !='':
                exp_file_set = ExperimentSetFile(experiment_set_id = expset4.id, experiment_file_id = exp_file.id, experiment_file_order = female_order)
                db.session.add(exp_file_set)
            
        db.session.commit()



'''
def addFilesToSet(exp_set):
    exp_files1 = ExperimentFile.query.filter_by(stimulus_type=exp_set.stimulus_type).limit(30)
    for exp_file in exp_files1:
        exp_file_set = ExperimentSetFile(experiment_set_id = exp_set.id, experiment_file_id = exp_file.id)
        db.session.add(exp_file_set)
        db.session.flush()
addFilesToSet(expset1)
addFilesToSet(expset2)
addFilesToSet(expset3)
addFilesToSet(expset4)
'''
db.session.commit()


    
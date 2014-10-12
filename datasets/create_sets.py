# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 6, 2014 3:02:03 PM$"

if __name__ == "__main__":
    print "Hello World"


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

db.session.commit()

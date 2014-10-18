# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 1 2, 2014 1:49:53 PM$"

from xlrd import open_workbook
#import imp
#NF = imp.load_source('app', '../app/__init__.py')
#import app
from app import db
from app.models import User, ExperimentSet, ExperimentFile, ExperimentFileMetric

import os
print __file__
wb = open_workbook(os.path.join(os.path.dirname(__file__), 'Data_IAPS_IADS.xlsx'))

STIMULUS_MAP={'IAPS':{'name':'Images',
                        'extension':'jpg',
                        'root_folder':'http://people.ischool.berkeley.edu/~jannah/datasets/mhreader/images',
                        'headers':
                        {'title':'desc',
                        'filename':'IAPS',
                        'pleasure_mean':'valmn',
                        'pleasure_std':'valsd',
                        'arrousal_mean':'aromn',
                        'arrousal_std':'arosd',
                        'dominance1_mean':'dom1mn',
                        'dominance1_std':'dom1sd',
                        'dominance2_mean':'dom2mn',
                        'dominance2_std':'dom2sd',
                        'file_set_number':'set'}}, 
                'IADS':{'name':'Sounds',
                        'extension':'wav',
                        'root_folder':'http://people.ischool.berkeley.edu/~jannah/datasets/mhreader/sounds',
                        'headers':
                        {'title':'Sound',
                        'filename':'Number',
                        'pleasure_mean':'PlMN',
                        'pleasure_std':'PlSD',
                        'arrousal_mean':'AroMN',
                        'arrousal_std':'AroSD',
                        'dominance1_mean':'DomMN',
                        'dominance1_std':'DomSD',
                        'dominance2_mean':'DomMN',
                        'dominance2_std':'DomSD',
                        'file_set_number':''}}}
TARGET_FILE_COLS = ['stimulus_type', 'title', 'filename', 'path', 'file_set_number', 'remarks']
TARGET_FILE_METRIC_COLS = ['experiment_file_id', 'demographic', 'pleasure_mean',
                            'pleasure_std',
                            'arrousal_mean',
                            'arrousal_std',
                            'dominance1_mean',
                            'dominance1_std',
                            'dominance2_mean',
                            'dominance2_std']
ExperimentFile.query.delete()
ExperimentFileMetric.query.delete()
db.session.commit()
for s in wb.sheets():
    print 'Sheet:',s.name
    stimulus = ''
    demographic = ''
    try:
        stimulus , demographic= s.name.split(' - ')
        
    except Exception, e:
        print e
        pass
    if stimulus in STIMULUS_MAP:
        stimulus_type = STIMULUS_MAP[str(stimulus)]['name']
        print demographic, stimulus_type
        headers = dict([(str(s.cell(0, col).value ), col) for col in range(s.ncols)])
#        print headers
        for rownum in range(1, s.nrows):
            title = str(s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['title']]).value)
            filename = str(s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['filename']]).value).replace('.0', '')
            
            filename = "%s.%s"%(filename, str(STIMULUS_MAP[stimulus]['extension']))
            file_set_number = 0
            try:
                file_set_number =int(s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['file_set_number']]).value)
            except Exception, e:
                pass
            filepath = '%s/%s'%(STIMULUS_MAP[stimulus]['root_folder'],filename)
#            print stimulus_type, title, filename, file_set_number
            exp_file = ExperimentFile.query.filter_by(stimulus_type=stimulus_type, filename=filename).first()
#            print exp_file
            if exp_file is None:
                exp_file = ExperimentFile(stimulus_type=stimulus_type, title=title,filename=filename,filepath=filepath, file_set_number =file_set_number)
                db.session.add(exp_file)
                db.session.flush()
            else:
                print 'file %s already exists' % exp_file.filename
#            print exp_file.id
            pleasure_mean = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['pleasure_mean']]).value
            pleasure_std = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['pleasure_std']]).value
            arrousal_mean= s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['arrousal_mean']]).value
            arrousal_std = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['arrousal_std']]).value
            dominance1_mean = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['dominance1_mean']]).value
            dominance1_std = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['dominance1_std']]).value
            dominance2_mean = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['dominance2_mean']]).value
            dominance2_std = s.cell(rownum, headers[STIMULUS_MAP[stimulus]['headers']['dominance2_std']]).value
            
            exp_file_metric = ExperimentFileMetric(experiment_file_id = exp_file.id, demographic=demographic,
                                                    pleasure_mean=pleasure_mean,
                                                    pleasure_std=pleasure_std, arrousal_mean=arrousal_mean, arrousal_std=arrousal_std,
                                                    dominance1_mean=dominance1_mean, dominance1_std=dominance1_std,
                                                    dominance2_mean=dominance2_mean, dominance2_std=dominance2_std)
            db.session.add(exp_file_metric)
            db.session.flush()
                                                    
            
    db.session.commit()
            
    
    #    for row in range(s.nrows):
    #        values = []
    #        for col in range(s.ncols):
    #            values.append(s.cell(row,col).value)
    #        print ','.join([str(value) for value in values])
    #    print
    #    
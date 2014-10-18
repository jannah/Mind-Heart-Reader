# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 17, 2014 3:29:31 PM$"

from optparse import __repr__
from app import app
from app.models import *
from app import db
import json


experiments = Experiment.query.all()
output = []
for experiment in experiments:
    output.append(experiment.to_json())
    
print output

import sys
output_file = 'data_dump.json'
if len(sys.argv)>1:
    output_file = sys.argv[1]

with open(output_file, 'w') as f:
    f.write(str(output))
    f.close()
    
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 17, 2014 4:11:26 PM$"

from app import app
from app.models import *
from app import db
import json


exp_set = ExperimentSet.query.first()

ej= exp_set.to_json()

for f in ej['set_files']:

    print f['experiment_file_order']
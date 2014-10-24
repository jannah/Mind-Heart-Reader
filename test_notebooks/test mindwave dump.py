# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Oct 22, 2014 9:50:21 PM$"

from app import db
from app.models import *
mwls=MindwaveLog.query.all()

mwls = [mwl.to_json() for mwl in mwls]
headers = [key for key in mwls[0]]
data =[",".join([str(mwl[key]) for key in headers]) for mwl in mwls ]
results = [",".join(headers)] + data
r = '\n'.join(results)
print r
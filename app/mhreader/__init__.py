# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Sep 24, 2014 2:17:51 PM$"

from flask import Blueprint
from flask import redirect, request

mhrbp = Blueprint('mhreader', __name__
        , template_folder='templates'
        , static_folder="static",)
from . import mhreader
from .modules import *


    
#!/usr/bin/python27
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Hassan"
__date__ ="$Sep 24, 2014 1:34:35 PM$"
from app import app


if __name__ == '__main__':
	import sys
	port = 5000
	if len(sys.argv)>1:
		port = int(sys.argv[1])
	app.run('0.0.0.0', port = port, debug=True)


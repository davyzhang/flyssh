#!/usr/bin/env python2.7
#coding=utf-8

from subprocess import check_output,call
import sys
import json

if len(sys.argv) < 2:
	print "usage: ssh_checker.py config.json"
	sys.exit(1)

config = json.loads(open(sys.argv[1]).read())
ssh_username = config['ssh_username']
last_svr = config['last_server']

try:
	output = check_output('ps aux |grep %s@%s|grep -v grep'%(ssh_username,last_svr),shell=True)
except:
	call("./run.py %s --last"%(sys.argv[1]),shell=True)
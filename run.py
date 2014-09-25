#!/usr/bin/env python2.7
#coding=utf-8
import flyspeed
import random
from subprocess import call
import json
import sys
import os
import time

if len(sys.argv) < 2:
	print "usage: run.py config.json"
	sys.exit(1)

config = json.loads(open(sys.argv[1]).read())
username = config['username']
password = config['password']
productID = config['productID']
ssh_username = config['ssh_username']
ssh_password = config['ssh_password']
bind_ip = config['bind_ip']
last_svr = config['last_server']

if len(sys.argv) >= 3 and sys.argv[2] == "--last":
	call("./ssh_proxy.py %s %s %s %s"%(last_svr,ssh_username,ssh_password,bind_ip),shell=True)
	sys.exit(0)


ping_kv, download_kv = flyspeed.benchmark()

top_number = 5
if top_number > len(ping_kv): top_number = len(ping_kv)
if top_number == 1: sys.exit(0)
if top_number == 0:
    print ">>> No servers available!"
    sys.exit(2)

print ">>> Top %d Servers:" % top_number
print "PING:"
ping_list = sorted(ping_kv.items(), key=lambda item:item[1], reverse=False)
for i in ping_list[:top_number]:
    if i[1] > 99998: 
        print i[0], "(failed)"
    else:
        print i[0], "(%s ms)" % i[1]
print "DOWNLOAD:"
download_list = sorted(download_kv.items(), key=lambda item:item[1], reverse=True)
for i in download_list[:top_number]:
    print i[0], "(%s KB/s)" % i[1]

p = [x[0] for x in ping_list[:top_number]]
d = [x[0] for x in download_list[:top_number]]

ins = list(set(p) & set(d))
print "fastest server(s)",ins
if len(ins) == 0:
	svr = p[0]
else:
	svr = random.choice(ins)
print "choose:",svr
svr_no = svr.split(".")[0].lstrip('s')
print "svr no  ",svr_no
print "changing server on site..."
call("phantomjs flyssh_svr_changer.js %s %s %s %s"%(username,password,productID,svr_no), shell=True)

time.sleep(10)
print "changing local ssh proxy...",(svr,ssh_username,ssh_password,bind_ip)
call("./ssh_proxy.py %s %s %s %s"%(svr,ssh_username,ssh_password,bind_ip),shell=True)
config['last_server'] = svr
open(sys.argv[1],'w').write(json.dumps(config))
print "Done"

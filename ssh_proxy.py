#!/usr/bin/env python2.7
#coding=utf-8
'''
Created on Sep 14, 2011

@author: dawn
'''
import pexpect
import time
from subprocess import call
from sys import argv

if len(argv) < 2:
    print "usage: ssh_proxy.py server username password bind_ip"
else:
    server = argv[1]
    user_name = argv[2]
    password  = argv[3]
    if len(argv) > 4:
        bind_ip = argv[4]
    else:
        bind_ip = ''

bind_port = 7070
port = 22
shl = 'ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no\
 -p %(port)d -f -N -g -D %(bind_ip)s:%(bind_port)s %(user_name)s@%(server)s'%{'bind_ip':bind_ip,
                                                                            'bind_port':bind_port,
                                                                            'server':server,
                                                                            'user_name':user_name,
                                                                            'port':port}
token = '%(user_name)s@%(server)s'%{'user_name':user_name,'server':server}

def clear_host():
    call("ssh-keygen -R "+server,shell=True)

def start_tunnel(shl,password):
    try:
        ssh_tunnel = pexpect.spawn(shl)
        print 'shl run ',shl
        index = ssh_tunnel.expect(['yes/no','password:'])
        if index == 0:
            print 'ensure connection'
            ssh_tunnel.sendline('yes')
            index = ssh_tunnel.expect(['password:'])
            print 'password asking...'
            time.sleep(0.1)
            ssh_tunnel.sendline(password)
            print 'password sent waiting for done'
        else:
            print 'password asking...'
            time.sleep(0.1)
            ssh_tunnel.sendline(password)
            print 'password sent waiting for done'
        time.sleep(5)
        ssh_tunnel.expect(pexpect.EOF)
        print 'done'
    except Exception,e:
        print str(e)

def end_tunnel():
    call('pkill -f %s'%token,shell=True)


if __name__ == '__main__':
    clear_host()
    end_tunnel()
    start_tunnel(shl,password)

#!/usr/bin/env python

import pexpect
from threading import *
from pprint import pprint
import re
import sys
import getopt

def mevapush(index):
    global ipadd
    host = ipadd[index]

    session = pexpect.spawn('ssh -o ConnectTimeout=10 -oStricthostKeyChecking=no -l ' + YOURUSERNAME + " " + host, timeout=15)
    result = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])

    # Check for failure
    if result != 0:
        print 'ERROR: Timeout or unexpected reply from device: ' + host
        print '\r'
        print '\r'
        print '\r'
    return

    # Successfully got username prompt, enter username
    session.sendline(YOURPASSWORD)
    result = session.expect(Prompt1)
    print '---Login to ' + host + ' successful'

    #create logfile path
    logpath = '/home/ivan/lab/logs/' + host + '.txt'
    session.logfile = open(logpath, 'w')

    session.sendline('enable')
    result = session.expect('assword:')

    session.sendline(YOURENABLE)
    result = session.expect(Prompt2)
    print '--- enable successful'

    with open('commands', 'r') as g:
        cmdlist = [line2.strip() for line2 in g]

    for cmd in cmdlist:
        session.sendline(cmd)
        result = session.expect(Prompt2)
        print '---Running command: ' + cmd

    session.sendline()
    result = session.expect(Prompt2)
    session.sendline('exit')
    print '---Successfully exited device ' + host
    session.logfile.close()
    print '---Log created: ' + logpath
    print '\r'
    print '\r'
    print '\r'


#Start of Main
try:
    opts, args = getopt.getopt(sys.argv[1:], 'u:p:e:h', ['username=', 'password=', 'enablepass=', 'help'])
except getopt.GetoptError:
    print 'Usage: xxxx.py -u <username> -p <password> -e <enablepass>'
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print 'Usage: xxxx.py -u <username> -p <password> -e <enablepass>'
        sys.exit(2)
    elif opt in ('-u', '--username'):
        YOURUSERNAME = arg
    elif opt in ('-p', '--password'):
        YOURPASSWORD = arg
    elif opt in ('-e', '--enablepass'):
        YOURENABLE = arg
    else:
        print 'Usage: xxxx.py -u <username> -p <password> -e <enablepass>'
        sys.exit(2)

try:
    if YOURUSERNAME == "":
        print YOURUSERNAME
except:
    print 'no username defined. use -u option to enter username'
    exit()
try:
    if YOURPASSWORD == "":
        print YOURUSERNAME
except:
    print 'no password defined. use -p option to enter password'
    exit()
try:
    if YOURENABLE == "":
        print YOURUSERNAME
except:
    print 'no enablepass defined. use -e option to enter enablepass'
    exit()

# Create regular expressions to match interfaces and OSPF
Prompt1 = re.compile('>$')
Prompt2 = re.compile('#$')

class threadPush1(Thread):
    def __init__(self, index):
        i = index
    def run(self):
        mevapush(i)

class threadPush2(Thread):
    def __init__(self, index):
        i = index + 1
    def run(self):
        mevapush(i)

class threadPush3(Thread):
    def __init__(self, index):
        i = index + 2
    def run(self):
        mevapush(i)

with open('iplist', 'r') as f:
    ipadd = [line.strip() for line in f]

t1 = threadPush1()
t2 = threadPush2()
t3 = threadPush3()

t1.run(0)
t2.run(1)
t3.run(2)

print '--- end of test code'
exit()

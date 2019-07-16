#!/usr/bin/env python

import pexpect
from threading import *
from pprint import pprint
import re
import sys
import getopt


class threadClass(Thread):
    def __init__(self, host):
        super(threadClass, self).__init__()
        self.host = host

    def run(self):
        session = pexpect.spawn('ssh -o ConnectTimeout=10 -oStricthostKeyChecking=no -l ' + YOURUSERNAME + " " + self.host, timeout=15)
        result = session.expect(['assword:', pexpect.TIMEOUT, pexpect.EOF])
    
        # Check for failure
        if result != 0:
            print 'ERROR: Timeout or unexpected reply from device: ' + self.host
            print '\r'
            print '\r'
            print '\r'
	    return

        # Successfully got username prompt, enter username
        session.sendline(YOURPASSWORD)
        result = session.expect(Prompt1)
        print '---Login to ' + self.host + ' successful'

        #create logfile path
        logpath = '/home/ivan/lab/logs/' + self.host + '.txt'
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
        print '---Successfully exited device ' + self.host
        session.logfile.close()
        print '---Log created: ' + logpath
        print '\r'
        print '\r'
        print '\r'

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


with open('iplist', 'r') as f:
    ipadd = [line.strip() for line in f]

for i in ipadd:
    t = threadClass(i)
    t.run()

print '--- end of test code'
exit()
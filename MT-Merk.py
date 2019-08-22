#!/usr/bin/env /home/repos/public/Python/bin/python3.6

#Documentation stating API Call volume is rate limited to 5 calls per second per organization.
#https://documentation.meraki.com/zGeneral_Administration/Other_Topics/The_Cisco_Meraki_Dashboard_API#Every_request_must_specify_an_API_key_via_a_request_header

import time
from datetime import datetime
import sys
import os
import getpass
import xlrd
try:
    from meraki import meraki
except:
    os.system('pip install --user requests')
    os.system('pip install --user meraki')
try:
    print('---loading...')
    from meraki import meraki
except:
    sys.exit('installation failed. please contact admin')

def getNetID(myKey, SiteName):
    orgs = meraki.myorgaccess(myKey)
    orgNames = [org['name'] for org in orgs]
    index = orgNames.index('joco')
    myOrg = orgs[index]['id']
    
    currentNetworks = meraki.getnetworklist(myKey, myOrg)
    networkNames = [network['name'] for network in currentNetworks]
    
    mySiteName = 'joco-' + SiteName + '-combined'
    myNetID = currentNetworks[networkNames.index(mySiteName)]['id']
    
    myNetworkDevices = meraki.getnetworkdevices(myKey, myNetID)
    
    print('---Executing change for Organization: ' + myOrg)
    print('---Executing change for Site: ' + mySiteName)
    return myNetID, mySiteName, myNetworkDevices

def getSwitchesOnly(myNetworkDevices):
    #create a list with serial of MS meraki switches ONLY!
    switchIndexList = []
    switchSerialList = []
    for x in range(len(myNetworkDevices)):
        modelcheck = myNetworkDevices[x]['model']
        if 'MS' in modelcheck:
            switchIndexList.append(x)
        else:
            pass
    for x in switchIndexList:
        switchSerialList.append(myNetworkDevices[x]['serial'])
    return switchSerialList

def countdown(t):
    try:
        print('Review Ports. Press CTRL + C to terminate and exit')
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print('auto exit after: ', timeformat, end='\r')
            time.sleep(1)
            t -= 1
    except:
        print('\r')
        sys.exit('---Exiting script. Not Proceeding with Policy configuration')

def updatePolicy(myKey, serialNumber):
    portnumberList = []
    perSwitchPortDetails = meraki.getswitchports(myKey, serialNumber)
    for x in range(len(perSwitchPortDetails)):
        typecheck = perSwitchPortDetails[x]['type']
        vlancheck = perSwitchPortDetails[x]['vlan']
        if 'access' in str(typecheck):
            if '201' in str(vlancheck):
                portnumber = perSwitchPortDetails[x]['number']
                portnumberList.append(portnumber)
            else:
                pass
        else:
            continue
    
    print('Ports with vlan 201 {}'.format(portnumberList))
    countdown(60)
    
    for port in portnumberList:
        result = meraki.updateswitchport(myKey, serialNumber, port, accesspolicynum='1', suppressprint=True)
        if type(result) is dict:
            status = 'Success'
        else:
            status = 'Failed'
        print('Push status: {}'.format(status))

    postPerSwitchPortDetails = meraki.getswitchports(myKey, serialNumber)
    index = 0
    for x in range(len(postPerSwitchPortDetails)):
        policyNumCheck = postPerSwitchPortDetails[x]['accesspolicynum']
        if '1' == str(policyNumCheck):
            print('{0:2}: {1:15} {2:16} {3:15} {4:>2}-{5:4} {6:7} {7:6} {8:7} {9:13} {10:12} {11:20}'.format(index+1, serialNumber, postPerSwitchPortDetails[x]['number'], postPerSwitchPortDetails[x]['porttype'], postPerSwitchPortDetails[x]['vlan'], postPerSwitchPortDetails[x]['accesspolicynum'])
            index += 1 # increment our index
        else:
            continue
    return

def worker(myKey):
    threadName = threading.current_thread().getName()
    while (q.qsize() != 0):
        try:
            serialNumber = q.get()
            status = updatePolicy(myKey, serialNumber)
            for line in status:
                print('{}: {}'.format(threadName,line))
            q.task_done()
        except:
            return


########################## MAIN ##########################
userID = os.getlogin()
os.system('clear')
try:
    myKey = getpass.getpass('---Enter API Key (Press Ctrl + C to exit): ')
except:
    sys.exit('Exiting...')
myNetID, mySiteName, myNetworkDevices = getNetID(myKey, SiteName)
switchSerialList = getSwitchesOnly(myNetworkDevices)

q = Queue()
for item in switchSerialList:
    q.put(item)
maxAllowedThread = min(3, q.qsize())
threadList = []

#print summary before start execution
print('Total number of Device {0} queued'.format(q.qsize()))
print('Starting {0} threads at a time.'.format(maxAllowedThread))
os.system('clear')
print(header)
print('Summary:')
print('')
print('Idx Serial Number   Port#   Type    Vlan   Port PolicyNum')
print('--- --------------- ------- ------- ------ ---------------')

start = time.time()
for i in range(maxAllowedThread):
    t = threading.Thread(target = worker, args = (myKey))
    t.daemon = True
    t.start()
    threadList.append(t)
    print('---Starting thread {}'.format(i))
[t.join() for t in threadList]
q.join()

print('---End of code')
print('Entire job took: {}'.format(time.time()-start))
exit()



#def main():
#    os.system('clear')
#    try:
#        myKey = getpass.getpass('---Enter API Key (Press Ctrl + C to exit): ')
#    except:
#        sys.exit('Exiting...')
#    myNetID, mySiteName, myNetworkDevices = getNetID(myKey, SiteName)
#    switchSerialList = getSwitchesOnly(myNetworkDevices)
#    print('End of code')
#
#
#if __name__ == '__main__':
#    main()

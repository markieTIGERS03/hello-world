#!/usr/bin/env /home/repos/public/Python/bin/python3.6

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


os.system('clear')
userID = os.getlogin()
try:
    my_key = getpass.getpass('---Enter API Key (Press Ctrl + C to exit): ')
except:
    sys.exit('Exiting...')

orgs = meraki.myorgaccess(my_key)
org_names = [org['name'] for org in orgs]
index = org_names.index('joco')
my_org = orgs[index]['id']

current_networks = meraki.getnetworklist(my_key, my_org)
network_names = [network['name'] for network in current_networks]

mySiteName = 'joco-nj0122-combined'
myNetID = current_networks[network_names.index(mySiteName)]['id']

my_network_devices = meraki.getnetworkdevices(my_key, myNetID)

print('---Executing change for Organization: ' + my_org)
print('---Executing change for Site: ' + mySiteName)

#create a list with serial of MS meraki switches ONLY!
switchIndexList = []
switchSerialList = []
for x in range(len(my_network_devices)):
    modelcheck = my_network_devices[x]['model']
    if 'MS' in modelcheck:
        switchIndexList.append(x)
    else:
        pass
for x in switchIndexList:
    switchSerialList.append(my_network_devices[x]['serial'])
    
portnumberList = []
for serial in switchSerialList:
    perSwitchPortDetails = meraki.getswitchports(my_key, serial)
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

for port in portnumberList:
    print('Ports with vlan 201 {}'.format(port))

try:
    answer1 = input('---Do you want to proceed (Y/N, Default=N): ').lower()
    if answer1 in ['yes', 'y']:
        pass
    else:
        sys.exit('---Exiting code')
except:
    sys.exit('---Exiting code')

for serialNumber in switchSerialList:
    for port in portnumberList:
        result = meraki.updateswitchport(my_key, serialNumber, port, accesspolicynum='1', suppressprint=True)
        if type(result) is dict:
            status = 'Success'
        else:
            status = 'Failed'
        print('Push status: {}'.format(status))
    
print('End of code')

#!/usr/bin/env python

#Get your libraries
import time
import sys
import os
import getpass
import xlrd
import getpass


os.system('clear')
userID = getpass.getuser()
#print(header)
try:
    myKey = getpass.getpass('---Enter API Key (Press Ctrl + C to exit): ')
except:
    sys.exit('Exiting...')
myFile = '/home/' + userID + '/lab/meraki-API/API-TestExcel.xlsx'
try:
    book = xlrd.open_workbook(myFile)
    sheet1 = book.sheet_by_index(0)
except:
    sys.exit('---No input file found or incorrect input file name. Use \"IVAN-Meraki-Input.xlsx\"')


dlist = []
serialList = []
for i in range(8, sheet1.nrows):
    dlist.append(sheet1.row_values(i))
for i in range(len(dlist)):
    serialNumber = dlist[i][0]
    deviceName = dlist[i][1]
    if serialNumber in serialList:
        print('---Serial: ' + serialNumber + ' device name and address are already updated. skipping to next serial...')
        continue
    else:
        print('---Pushing Device-name and Address to: ' + serialNumber)
        #meraki.updatedevice(myKey, myNetID, serialNumber, name=deviceName, address=myAddress, move='true', suppressprint=True)
        serialList.append(serialNumber)
for i in range(len(dlist)):
    serialNumber = dlist[i][0]
    deviceName = dlist[i][1]
    portName = dlist[i][2]
    portStart = str(dlist[i][3]).split('.')[0]
    portEnd = str(dlist[i][4]).split('.')[0]
    portType = dlist[i][5]
    portVlan = str(dlist[i][6]).split('.')[0]
    portVoice = str(dlist[i][7]).split('.')[0]
    portAllowed = str(dlist[i][8])
    portSTP = dlist[i][9]
    try:
        if portVoice != '':
            for portNumber in range(int(portStart), int(portEnd)+1):
                print('---Pushing configuration with voice to Port: ' + str(portNumber) + ' of device: ' + deviceName)
                status = 'Success'
                #meraki.updateswitchport(myKey, serialNumber, portNumber, name=portName, porttype=portType, vlan=portVlan, voicevlan=portVoice, allowedvlans=portAllowed, stpguard=portSTP, suppressprint=True)
            if status == 'Success':
                dlist[i].append('Success')
            else:
                dlist[i].append('Failed')
        else:
            for portNumber in range(int(portStart), int(portEnd)+1):
                print('---Pushing configuration without voice to Port: ' + str(portNumber) + ' of device: ' + deviceName)
                status = 'Success'
                #meraki.updateswitchport(myKey, serialNumber, portNumber, name=portName, porttype=portType, vlan=portVlan, allowedvlans=portAllowed, stpguard=portSTP, suppressprint=True)
            if status == 'Success':
                dlist[i].append('Success')
            else:
                dlist[i].append('Failed')
    except:
        print('---No configuration pushed to device: ' + serialNumber)
        dlist[i].append('Failed')

os.system('clear')
##############
print('Summary:')
print('')
print('Idx Serial          Device Name  Port Label   Ports   Type    Vlan   Voice   Allowed-Vlan  STP          Status')
print('--- --------------- ------------ ------------ ------- ------- ------ ------- ------------- ------------ --------')
index = 0

for device_info in dlist:

    print('{0:2}: {1:15} {2:12} {3:12} {4:>2}-{5:4} {6:7} {7:6} {8:7} {9:13} {10:12} {11:8}'.format(index+1,
                                                    device_info[0],device_info[1],
                                                    device_info[2],str(device_info[3]).split('.')[0],
                                                    str(device_info[4]).split('.')[0],device_info[5],
                                                    str(device_info[6]).split('.')[0],str(device_info[7]).split('.')[0],
                                                    device_info[8],device_info[9],device_info[10]))

    index += 1 # increment our index

print('')
##############


print('Input file IVAN-Meraki-Input.xlsx is now deleted. Run batch file to transfer new input file')
print('---end of code')
print('---For any errors encountered. Please capture error and send to gmail')

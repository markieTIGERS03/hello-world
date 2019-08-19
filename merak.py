#!/usr/bin/env /home/repos/public/Python/bin/python3.6

#Get your libraries
import time
from datetime import datetime
import sys
import os
import getpass
import xlrd
try:
    from meraki import meraki
except:
    os.system('/home/repos/public/Python/bin/python3.6 /home/repos/public/Python/bin/pip install --user requests')
    os.system('/home/repos/public/Python/bin/python3.6 /home/repos/public/Python/bin/pip install --user meraki')
try:
    print('---loading...')
    from meraki import meraki
except:
    sys.exit('installation failed. please contact admin')


header = '''\
 ________  ______    ______         __       __  ________  _______    ______   __    __  ______ 

'''

os.system('clear')
userID = os.getlogin()
print(header)
try:
    myKey = getpass.getpass('---Enter API Key (Press Ctrl + C to exit): ')
except:
    sys.exit('Exiting...')
myFile = '/home/' + userID + '/MIME-Meraki-Input.xlsx'
try:
    book = xlrd.open_workbook(myFile)
    sheet1 = book.sheet_by_index(1)
except:
    sys.exit('---No input file found or incorrect input file name. Use \"MIME-Meraki-Input.xlsx\"')

#Update device information
def merUpdateInfo(myNetID, myAddress):
    dlist = []
    serialList = []
    checkSerialList = []
    myNetworkDeviceList = meraki.getnetworkdevices(myKey, myNetID, suppressprint=True)
    for i in range(len(myNetworkDeviceList)):
        checkSerialList.append(myNetworkDeviceList[i]['serial'])
    for i in range(8, sheet1.nrows):
        dlist.append(sheet1.row_values(i))
    for i in range(len(dlist)):
        serialNumber = dlist[i][0]
        deviceName = dlist[i][1]
        if serialNumber in checkSerialList:
            pass
        else:
            print('---Serial: {} not found on site device list. Skipping this device name and address update'.format(serialNumber))
            continue
        if serialNumber in serialList:
            #print('---Serial: ' + serialNumber + ' device name and address are already updated. skipping to next serial...')
            continue
        else:
            print('---Pushing Device-name and Address to: ' + serialNumber)
            meraki.updatedevice(myKey, myNetID, serialNumber, name=deviceName, address=myAddress, move='true', suppressprint=True)
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
        perPortStatus = []
        if serialNumber in checkSerialList:
            pass
        else:
            print('---Serial: {} not found on site device list. Skipping this port configuration update'.format(serialNumber))
            dlist[i].append('Serial not valid for this site')
            continue
        try:
            if portVoice != '':
                for portNumber in range(int(portStart), int(portEnd)+1):
                    print('---Pushing configuration with voice to Port: ' + str(portNumber) + ' of device: ' + deviceName)
                    result = meraki.updateswitchport(myKey, serialNumber, portNumber, name=portName, porttype=portType, vlan=portVlan, voicevlan=portVoice, allowedvlans=portAllowed, stpguard=portSTP, suppressprint=True)
                    if type(result) is dict:
                        perPortStatus.append('Success')
                    else:
                        perPortStatus.append('Failed')
                if perPortStatus.count('Failed') != 0:
                    dlist[i].append(str(perPortStatus.count('Failed')) + ' out of ' + str(len(range(int(portStart), int(portEnd)+1))) + ' Failed')
                else:
                    dlist[i].append(str(len(range(int(portStart), int(portEnd)+1))) + ' out of ' + str(len(range(int(portStart), int(portEnd)+1))) + ' Succeed')
            else:
                for portNumber in range(int(portStart), int(portEnd)+1):
                    print('---Pushing configuration without voice to Port: ' + str(portNumber) + ' of device: ' + deviceName)
                    result = meraki.updateswitchport(myKey, serialNumber, portNumber, name=portName, porttype=portType, vlan=portVlan, allowedvlans=portAllowed, stpguard=portSTP, suppressprint=True)
                    if type(result) is dict:
                        status = 'Success'
                    else:
                        status = 'Failed'
                if perPortStatus.count('Failed') != 0:
                    dlist[i].append(str(perPortStatus.count('Failed')) + ' out of ' + str(len(range(int(portStart), int(portEnd)+1))) + ' Failed')
                else:
                    dlist[i].append(str(len(range(int(portStart), int(portEnd)+1))) + ' out of ' + str(len(range(int(portStart), int(portEnd)+1))) + ' Succeed')
        except:
            print('---No configuration pushed to device: ' + serialNumber)
            
    os.system('clear')
    print(header)
    print('Summary:')
    print('')
    print('Idx Serial Number   Device Name      Port Label      Ports   Type    Vlan   Voice   Allowed-Vlan  STP          Status')
    print('--- --------------- ---------------- --------------- ------- ------- ------ ------- ------------- ------------ --------------------')
    index = 0
    for device_info in dlist:
        print('{0:2}: {1:15} {2:16} {3:15} {4:>2}-{5:4} {6:7} {7:6} {8:7} {9:13} {10:12} {11:20}'.format(index+1,device_info[0],device_info[1],device_info[2],str(device_info[3]).split('.')[0],str(device_info[4]).split('.')[0],device_info[5],str(device_info[6]).split('.')[0],str(device_info[7]).split('.')[0],device_info[8],device_info[9],device_info[10]))
        index += 1 # increment our index
    print('')


def main():
    startTime = datetime.now()
    #Get Organization number, sitename and address
    myOrg = sheet1.cell_value(4,1)
    myPartialSiteName = sheet1.cell_value(5,1)
    myAddress = sheet1.cell_value(6,1)
    try:
        orgs = meraki.myorgaccess(myKey, suppressprint=True)
    except:
        sys.exit('---Invalid keys. please try again')
    org_names = [org['name'] for org in orgs]
    try:
        index = org_names.index(myOrg)
        myOrgNumber = orgs[index]['id']
        mySiteName = myOrg + '-' + myPartialSiteName + '-combined'
        print('---Executing change for Organization: ' + myOrg)
        print('---Executing change for Site: ' + mySiteName)
    except:
        sys.exit('---Organization name or Site name not found. Please check input file')

    try:
        answer1 = input('---Do you want to proceed (Y/N, Default=N): ').lower()
        if answer1 in ['yes', 'y']:
            pass
        else:
            sys.exit('---Exiting code')
    except:
        sys.exit('---Exiting code')
        
    #Get Network ID
    current_networks = meraki.getnetworklist(myKey, myOrgNumber, suppressprint=True)
    network_names = [network['name'] for network in current_networks]
    if mySiteName in network_names:
        myNetID = current_networks[network_names.index(mySiteName)]['id']
        #print('---The network {0} already exists with ID {1}'.format(mySiteName, myNetID))
    else:
        sys.exit('---Network {0} does not exist. Please check your network name'.format(mySiteName))
    
    merUpdateInfo(myNetID, myAddress)
    
    os.system('rm -f ' + myFile)
    totalTime = datetime.now() - startTime
    print('Script run by: {}'.format(userID))
    print('Total script runtime: {}'.format(totalTime))
    print('Input file MIME-Meraki-Input.xlsx is now deleted. Run batch file to transfer new input file')
    print('---end of code')
    print('---For any errors encountered. Please capture error and send to mark.ivan.evaristo@intl.verizon.com')
    exit()


if __name__ == '__main__':
    main()

#Define a class called NetworkDevice. Define an initialization method (called __init__) 
#within the class that takes device information as parameters (device name, OS-type, IP address, username, and password.
#---- Class to hold information about a network device ----------------
class NetworkDevice():

    def __init__(self, name, ip, os, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.os_type    = os
        self.username = user
        self.password = pw

#Create a function that takes the name of the devices file as input, reads the device information from the file, and creates network device objects, adding them to a list of devices. 
#The result will be a list of network device objects, based on the information read from the file. The function should return the list of devices to the caller.
#---- Function to read device information from file -------------------
def read_device_info(devices_file):

    devices = [] # Create a list for all devices

    # Read in the devices from the file
    file = open(devices_file,'r')
    for line in file:

        device_info = line.strip().split(',') # Get device info into list

        # Create a device object with this data
        device = NetworkDevice(device_info[0],device_info[2],
                               device_info[1],device_info[3],device_info[4])

        devices.append(device) # add this device object to list

    file.close() # Close the file since we are done with it

    return devices # return a reference to the list we created


#Create a print function that takes as input a list of network device objects, and prints a table of the devices from the list.
#---- Function to go through devices printing them to table -----------
def print_device_info(devices_list):

    print ''
    print 'Name        OS-type  IP address       Username  Password'
    print '---------   -------  --------------   --------  --------'

    # Go through the list of devices, printing out values in nice format
    for device in devices_list:

        print '{0:11} {1:8} {2:16} {3:9} {4:9}'.format(device.name,
                                                       device.os_type,
                                                       device.ip_address,
                                                       device.username,
                                                       device.password)

    print ''

#Your main code will (a) call the function to read device information from the file, 
#and (b) print the device information. It will do this twice; once for the 'devices' file, and once for the 'real-devices' file.
#---- Main: read device info, then print ------------------------------

devices_list = read_device_info('devices')
print_device_info(devices_list)

devices_list = read_device_info('real-devices')
print_device_info(devices_list)


#Define a base class for a generic network device, with an initialization function 
#to set device name, IP, username, and password. Because the device type is unknown for a generic device, set os_type to 'unknown'.
#---- Class to hold information about a generic network device --------
class NetworkDevice():

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        self.name = name
        self.ip_address = ip
        self.username = user
        self.password = pw
        self.os_type = 'unknown'



#Define two child classes which derive from the base NetworkDevice class. 
#One class will be for IOS devices, the other will be for IOS-XR devices. 
#Each specific device class will have an initialization function which takes as input 
#the device name, IP, username, and password. It will set its os_type to the appropriate value.
#---- Class to hold information about an IOS-XE network device --------
class NetworkDeviceIOS(NetworkDevice):

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios'

#---- Class to hold information about an IOS-XR network device --------
class NetworkDeviceXR(NetworkDevice):

    def __init__(self, name, ip, user='cisco', pw='cisco'):
        NetworkDevice.__init__(self, name, ip, user, pw)
        self.os_type = 'ios-xr'

#Create a function which reads the devices file located in the PRNE/section13 folder, creates the device objects, and adds them to the list. 
#Your function will create different device objects depending on whether the os-type of the device that is read from 
#the file is an IOS device, an IOS-XR device, or neither. If neither, your function will ignore the device and continue reading the file.
#Your function should return a list of your created devices objects (note that some will be IOS objects, some will be IOS-XR objects.
#---- Function to read device information from file -------------------
def read_device_info(devices_file):

    devices_list = []

    # Read in the devices from the file
    file = open(devices_file,'r')
    for line in file:

        device_info = line.strip().split(',') # Get device info into list

        # Create a device object with this data
        if device_info[1] == 'ios':

            device = NetworkDeviceIOS(device_info[0],device_info[2],
                                      device_info[3],device_info[4])

        elif device_info[1] == 'ios-xr':

            device = NetworkDeviceXR(device_info[0],device_info[2],
                                     device_info[3],device_info[4])

        else:
            continue  # go to the next device in the file

        devices_list.append(device) # add this device object to list

    file.close() # Close the file since we are done with it
    return devices_list


#Create a function which prints the devices list that was created.

#---- Function to go through devices printing them to table -----------
def print_device_info(devices_list):

    print ''
    print 'Name     OS-type  IP address       Username  Password'
    print '------   -------  --------------   --------  --------'

    # Go through the list of devices, printing out values in nice format
    for device in devices_list:

        print '{0:8} {1:8} {2:16} {3:8} {4:8}'.format(device.name,
                                                      device.os_type,
                                                      device.ip_address,
                                                      device.username,
                                                      device.password)

    print ''


#Your main code should read the devices file, and print the device object information.
#---- Main: read device info, then print ------------------------------

devices = read_device_info('devices')
print_device_info(devices)

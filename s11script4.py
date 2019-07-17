#task1: Create a function that reads the device information from the file real-devices located in the PRNE/section11 folder. Return a list of devices, with information for each device stored in a dictionary.
import pexpect

#-----------------------------------------------------------
def read_devices_info(filename):

    devices_list = []

    file = open(filename,'r')
    for line in file:

        device_info_list = line.strip().split(',')

        device_info = {}
        device_info['name'] = device_info_list[0]
        device_info['ip'] = device_info_list[1]
        device_info['username'] = device_info_list[2]
        device_info['password'] = device_info_list[3]

        devices_list.append(device_info)

    return devices_list

#task2: Create a function to connect to a device, taking as parameters the IP address, username, and password for each device, and returning a Pexpect session.
# The following code connects to a device

def connect(dev_ip,username,password):

    print '--- connecting IOS: telnet '+dev_ip

    session = pexpect.spawn('telnet ' + dev_ip, timeout=20)

    result = session.expect(['Username:', pexpect.TIMEOUT])
    # Check for failure
    if result != 0:
        print '--- Timeout or unexpected reply from device'
        return 0

    print '--- attempting to: username: ' + username

    # Successfully got username prompt, logging with username
    session.sendline(username)

    result = session.expect(['Password:', pexpect.TIMEOUT])
    # Check for failure
    if result != 0:
        print '--- Timeout or unexpected reply from device'
        return 0

    print '--- attempting to: password: ' + password

    # Successfully got password prompt, logging in with password
    session.sendline(password)
    session.expect('>')

    return session  # return pexpect session object to caller
	
#task3:Create a function which runs a show interface summary command on a device, taking as input a session object for a connected device.
# The following function gets and returns interface information
def show_int_summary(session):

    session.sendline('show interface summary')
    result = session.expect('>')

    show_int_summary_output = session.before

    return show_int_summary_output

#task4: Create a function which prints information about a device, including device info (name, IP, username, password), and the interface information for the device.
# The following function prints device information

def print_device_info(device_info,show_int_output):

    print '-------------------------------------------------------'
    print '    Device Name:      ',device_info['name']
    print '    Device IP:        ',device_info['ip']
    print '    Device username:  ',device_info['username'],
    print '    Device password:  ',device_info['password']

    print ''
    print '    Show Interface Output'
    print ''

    print show_int_output
    print '-------------------------------------------------------'

#task5: Create main application code which (a) reads device information from a file, (b) iterates through the list of devices, using your created functions to connect to each one, read interface information, and print nicely formatted output for each device.
# Main program: connect to device, show interface, display

if __name__ == '__main__':

    devices_list = read_devices_info('real-devices')

    for device_info in devices_list:

        session = connect(device_info['ip'],
                          device_info['username'],
                          device_info['password'])
        if session == 0:
            print '--- Session attempt unsuccessful ---'
            continue

        show_int_output = show_int_summary(session)

        print_device_info(device_info,show_int_output)

        session.sendline('quit')
        session.kill(0)
#script will use function and return a value
#task1: Create a function which takes the IP address, username, and password of the device as input parameters. The function should use Pexpect to connect to the device. If successful, the function should return the Pexpect 'session' object. If unsuccessful, the function should return 0.
import pexpect

#-----------------------------------------------------------
# The following code connects to a device

def connect(dev_ip,username,password):
    """
    Connects to device using pexpect

    :dev_ip: The IP address of the device we are connectin to
    :username: The username that we should use when logging in
    :password: The password that we should use when logging in

    =return: pexpect session object if succssful, 0 otherwise

    """

    print '--- attempting to: telnet ' + dev_ip

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

#-----------------------------------------------------------
# The following function gets and returns interface information

def show_int_summary(session):
    """
    Runs 'show int summary' command on device and returns 
    output from device in a string

    :session: The pexpect session for communication with device

    =return: string of output from device
    """

    print '--- show interface summary command'
    session.sendline('show interface summary')
    result = session.expect('>')

    print '--- getting interface command output'
    show_int_brief_output = session.before

    return show_int_brief_output
    #-----------------------------------------------------------
# The following function gets and returns interface information

#task2: Create a function which takes as input a Pexpect session object, and performs a show interface brief command to receive interface information from the device. The function should return the output of the command.
def show_int_summary(session):
    """
    Runs 'show int summary' command on device and returns 
    output from device in a string

    :session: The pexpect session for communication with device

    =return: string of output from device
    """

    print '--- show interface summary command'
    session.sendline('show interface summary')
    result = session.expect('>')

    print '--- getting interface command output'
    show_int_brief_output = session.before

    return show_int_brief_output

#task3:Your main code should call your connect function, passing in the actual IP address, username, and password, and receiving the session object in return. The main code should then call your show int brief function, passing in the session object, and receiving the output of the command in return.
#------------------------------------------------------------
# Main program: connect to device, show interface, display

if __name__ == '__main__':

    session = connect('10.30.30.1','cisco','cisco')
    if session == 0:
        print '--- Session attempt unsuccessful, exiting.'
        exit()

    output_data = show_int_summary(session)
    
    print ''
    print 'Show Interface Output'
    print '-----------------------------------------------------'
    print ''

    print output_data

    session.sendline('quit')
    session.kill(0)
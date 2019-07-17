#!/usr/bin/env /home/repos/public/Python/bin/python3.6

import xlrd
path = "/home/evarima/piton/testsheet.xlsx"
book = xlrd.open_workbook(path)
Credentials = book.sheet_by_index(1)
IPsheet = book.sheet_by_index(2)
Commands = book.sheet_by_index(3)

#Function Create dictionary of credentials
cred_info = {}
for i in range(Credentials.nrows):
    data = (Credentials.row_values(i))
    cred_info[data[0]]= data[1]
   
#Function read IP sheet and create text file
iplist_file = open('iplist_sample.txt', 'w')
for i in range(IPsheet.nrows):
    data = IPsheet.row_values(i)
    iplist_file.writelines(data[0] + '\n')
iplist_file.close()

#Function read IP sheet and create text file
iplist_file = open('Commands_sample.txt', 'w')
for i in range(Commands.nrows):
    data = Commands.row_values(i)
    iplist_file.writelines(data[0] + '\n')
iplist_file.close()

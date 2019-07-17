#!/usr/bin/env /home/repos/public/Python/bin/python3.6

import xlwt
book = xlwt.Workbook()
sheet1 = book.add_sheet("PySheet1")
    
with open('testreadfile.txt', 'r') as f:
    ipadd = [line.strip() for line in f]

index = -1
    
for line in ipadd:
    index += 1
    row = sheet1.row(index)
    row.write(0, line)
    
book.save("test2.xls")
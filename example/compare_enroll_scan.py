import requests
import sqlite3
import datetime

#sqlite3 config
con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection
cursor = con.cursor()

enroll_list = []
scan_list = []

enroll_beacon =[]

# enroll beacon list
cursor.execute("SELECT * FROM enroll_beacon WHERE 1")
enroll_rows = cursor.fetchall()


for i in range(0,len(enroll_rows)):
    
    enroll_beacon =[]
    for j in range (1,len(enroll_rows[i])):
        enroll_beacon.append(enroll_rows[i][j])

    enroll_list.append(enroll_beacon)
                    
print(enroll_list)
    
# scan beacon list
now =datetime.datetime.now()
cursor.execute( "SELECT * FROM bluetooth_scan_log WHERE createdate between '"+ str(now - datetime.timedelta(seconds=30)) +"' and '"+str(now)+"' ")
scan_rows = cursor.fetchall()

for i in range(0,len(scan_rows)):
    scan_list.append(scan_rows[i][1])
print(scan_list)

enroll_scan = list(set(enroll_list).intersection(scan_rows))
print(enroll_scan)

con.commit()
con.close()



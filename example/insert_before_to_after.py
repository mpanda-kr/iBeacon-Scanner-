import sqlite3
import datetime
import requests
import json

#sqlite3 config
con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection

current = datetime.datetime.now()
print(current)
later = current - datetime.timedelta(minutes=1)
print(later)
 
cursor = con.cursor()
cursor.execute("SELECT * FROM enroll_scan_beacon WHERE createtime between  '"+ str(later) +"' and '"+str(current)+"' and utrla_trans is null")
utrla_srows = cursor.fetchall()

try:
    if utrla_srows:
        print("now utrla scan beacon data exist")
        cursor = con.cursor()
        cursor.execute("SELECT config_value FROM gateway_config WHERE config_property='center_id'")
        rows_c = cursor.fetchall()
        center = rows_c[0][0]        

        cursor = con.cursor()
        cursor.execute("SELECT config_value FROM gateway_config WHERE config_property='gateway'")
        rows_g = cursor.fetchall()
        gateway = rows_g[0][0]

        data='{"enroll_beacon":['

        for i in range(0,len(utrla_srows)):
            data+='{'
            data+='"gateway":"'+ gateway +'",'
            data+='"center":"'+ center +'",'
            data+='"createtime":"'+ utrla_srows[i][0] +'",'
            data+='"mac_address":"'+ utrla_srows[i][1] +'",'
            data+='"uuid":"'+ utrla_srows[i][2] +'",'
            data+='"major":'+ str(utrla_srows[i][3]) +','
            data+='"minor":'+ str(utrla_srows[i][4]) +','
            data+='"rssi":'+ str(utrla_srows[i][5]) +','
            data+='"tx_power":'+ str(utrla_srows[i][6]) +''
            if i < len(utrla_srows)-1:
                data+='},'
            else:
                data+='}'

        data+=']}'
       
        for i in range(0,len(utrla_srows)):
            cursor = con.cursor()
            cursor.execute("UPDATE enroll_scan_beacon SET utrla_trans = 1 WHERE createtime = '"+ utrla_srows[i][0] +"' AND mac_address  = '"+ utrla_srows[i][1] +"'")
            con.commit()

        url = "http://192.168.0.20:8080/gateway/ultra_insert" 
        res = requests.post(url, data=(data))
        
        print("=========")
        print(data)
        
        print("ultra beacon data gateway to server")

    else:
        print("no ultra beacon data")

finally:
    con.close()
    print(" == ultra scan gateway to server end == ")

    

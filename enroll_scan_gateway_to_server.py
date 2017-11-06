import requests
import json
import sqlite3
import datetime

#sqlite3 config
con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection

cursor = con.cursor()
cursor.execute("SELECT * FROM enroll_scan_beacon WHERE transmission is null")
enroll_rows = cursor.fetchall()

try:
    if enroll_rows:
        
        print("now enroll beacon data exist")
        cursor = con.cursor()
        cursor.execute("SELECT config_value FROM gateway_config WHERE config_property='center_id'")
        rows_c = cursor.fetchall()
        center = rows_c[0][0]

        cursor = con.cursor()
        cursor.execute("SELECT config_value FROM gateway_config WHERE config_property='gateway'")
        rows_g = cursor.fetchall()
        gateway = rows_g[0][0]

        data='{"enroll_beacon":['

        for i in range(0,len(enroll_rows)):
            data+='{'
            data+='"gateway":"'+ gateway +'",'
            data+='"center":"'+ center +'",'
            data+='"createtime":"'+ enroll_rows[i][0] +'",'
            data+='"mac_address":"'+ enroll_rows[i][1] +'",'
            data+='"uuid":"'+ enroll_rows[i][2] +'",'
            data+='"major":'+ str(enroll_rows[i][3]) +','
            data+='"minor":'+ str(enroll_rows[i][4]) +','
            data+='"rssi":'+ str(enroll_rows[i][5]) +','
            data+='"tx_power":'+ str(enroll_rows[i][6]) +''
            if i < len(enroll_rows)-1:
                data+='},'
            else:
                data+='}'

        data+=']}'

        for i in range(0,len(enroll_rows)):
            cursor = con.cursor()
            cursor.execute("UPDATE enroll_scan_beacon SET transmission = 1 WHERE createtime = '"+ enroll_rows[i][0] +"' AND mac_address  = '"+ enroll_rows[i][1] +"'")
            con.commit()

        url = "http://192.168.0.20:8080/gateway/enrollbeacon_insert" 
        res = requests.post(url, data=(data))
        print("enroll beacon data gateway to server")

    else:
        print("no enroll beacon data")

finally:
    con.close()
    print(" == enroll scan gateway to server end == ")

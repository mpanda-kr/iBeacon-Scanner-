# parser.py
import requests
import sqlite3


#sqlite3 config
con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection
cursor = con.cursor()

# HTTP GET Request
req = requests.get('http://192.168.0.20:8080/gateway/center_enrollbeacon_select')
enrollbeacon = req.json()

for i in range(0,len(enrollbeacon)):
    print(enrollbeacon[i]["beacon_uuid"])
    print(str(enrollbeacon[i]["beacon_major"]))
    print(str(enrollbeacon[i]["beacon_minor"]))
    print(enrollbeacon[i]["beacon_mac"])
  
    cursor.execute("INSERT INTO enroll_beacon ('beacon_mac','beacon_uuid','beacon_major','beacon_minor') VALUES ('"+enrollbeacon[i]["beacon_mac"]+"','"+enrollbeacon[i]["beacon_uuid"]+"',"+str(enrollbeacon[i]["beacon_major"])+","+str(enrollbeacon[i]["beacon_minor"])+");")
    con.commit()

con.close()

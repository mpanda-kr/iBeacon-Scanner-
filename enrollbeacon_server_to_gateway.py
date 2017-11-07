import requests
import sqlite3

#sqlite3 config
con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection
cursor = con.cursor()

# center_id = '2109059_01'

cursor.execute("SELECT config_value FROM gateway_config WHERE config_property='center_id'")
rows = cursor.fetchall()

center_id = (rows[0][0])

URL = 'http://192.168.0.20:8080/gateway/center_enrollbeacon_select'
req = requests.post(URL, data={'center_id':center_id})
enrollbeacon = req.json()

cursor.execute("DELETE FROM enroll_beacon;")
cursor.execute("DELETE FROM test_ultra_log;")

print("=================================")

for i in range(0,len(enrollbeacon)):
    print(enrollbeacon[i]["beacon_uuid"])
    print(str(enrollbeacon[i]["beacon_major"]))
    print(str(enrollbeacon[i]["beacon_minor"]))
    print(enrollbeacon[i]["beacon_mac"])
  
    cursor.execute("INSERT INTO enroll_beacon ('beacon_mac','beacon_uuid','beacon_major','beacon_minor') VALUES ('"+enrollbeacon[i]["beacon_mac"]+"','"+enrollbeacon[i]["beacon_uuid"]+"',"+str(enrollbeacon[i]["beacon_major"])+","+str(enrollbeacon[i]["beacon_minor"])+");")
    con.commit()
    
    print("=================================")

cursor.execute("DELETE FROM bluetooth_scan_log;")
con.commit()
    
con.close()

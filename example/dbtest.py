import sqlite3
con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection
cursor = con.cursor()
cursor.execute("INSERT INTO bluetooth_scan_log('mac_address','uuid','major','minor','rssi','tx_power') VALUES ('alguddl', '91fe354da86b4c5aa156b6c20707b204',179,47806,-65,-66)")
con.commit()
con.close()

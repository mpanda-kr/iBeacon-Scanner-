import requests
import sqlite3

#sqlite3 config
con1 = sqlite3.connect("/var/www/html/database/smart_bus3.db")
sqlite3.Connection
cursor1 = con1.cursor()

cursor1.execute("DELETE FROM bluetooth_scan_log;")
con1.commit()

con1.close()

import requests
import json

url = "http://192.168.0.20:8080/gateway/enrollbeacon_insert"

data='{"enroll_beacon":['
data+='{'
data+='"gateway":"2109059_01_G0_01",'
data+='"center":"2109059_01",'
data+='"createtime":"2017-10-23 18:26:17",'
data+='"mac_address":"ea:58:da:6d:e4:34",'
data+='"uuid":"91fe354da86b4c5aa156b6c20707b204",'
data+='"major":21332,'
data+='"minor":20302,'
data+='"rssi":69,'
data+='"tx_power":-91'
data+='},'



data+='{'
data+='"gateway":"2109059_01_G0_01",'
data+='"center":"2109059_01",'
data+='"createtime":"2017-10-23 18:26:17",'
data+='"mac_address":"ea:58:da:6d:e4:34",'
data+='"uuid":"91fe354da86b4c5aa156b6c20707b204",'
data+='"major":21332,'
data+='"minor":20302,'
data+='"rssi":69,'
data+='"tx_power":-91'
data+='}]}'


res = requests.post(url, data=(data))


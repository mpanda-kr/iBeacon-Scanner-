# BLE iBeaconScanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# JCS 06/07/14

DEBUG = False
# BLE scanner based on https://github.com/adamf/BLE/blob/master/ble-scanner.py
# BLE scanner, based on https://code.google.com/p/pybluez/source/browse/trunk/examples/advanced/inquiry-with-rssi.py

# https://github.com/pauloborges/bluez/blob/master/tools/hcitool.c for lescan
# https://kernel.googlesource.com/pub/scm/bluetooth/bluez/+/5.6/lib/hci.h for opcodes
# https://github.com/pauloborges/bluez/blob/master/lib/hci.c#L2782 for functions used by lescan

# performs a simple device inquiry, and returns a list of ble advertizements 
# discovered device

# NOTE: Python's struct.pack() will add padding bytes unless you make the endianness explicit. Little endian
# should be used for BLE. Always start a struct.pack() format string with "<"

import os
import sys
import struct
import bluetooth._bluetooth as bluez
import sqlite3
import time
import datetime

LE_META_EVENT = 0x3e
LE_PUBLIC_ADDRESS=0x00
LE_RANDOM_ADDRESS=0x01
LE_SET_SCAN_PARAMETERS_CP_SIZE=7
OGF_LE_CTL=0x08
OCF_LE_SET_SCAN_PARAMETERS=0x000B
OCF_LE_SET_SCAN_ENABLE=0x000C
OCF_LE_CREATE_CONN=0x000D

LE_ROLE_MASTER = 0x00
LE_ROLE_SLAVE = 0x01

# these are actually subevents of LE_META_EVENT
EVT_LE_CONN_COMPLETE=0x01
EVT_LE_ADVERTISING_REPORT=0x02
EVT_LE_CONN_UPDATE_COMPLETE=0x03
EVT_LE_READ_REMOTE_USED_FEATURES_COMPLETE=0x04

# Advertisment event types
ADV_IND=0x00
ADV_DIRECT_IND=0x01
ADV_SCAN_IND=0x02
ADV_NONCONN_IND=0x03
ADV_SCAN_RSP=0x04


def returnnumberpacket(pkt):
    myInteger = 0
    multiple = 256
    for c in pkt:
        myInteger +=  struct.unpack("B",c)[0] * multiple
        multiple = 1
    return myInteger 

def returnstringpacket(pkt):
    myString = "";
    for c in pkt:
        myString +=  "%02x" %struct.unpack("B",c)[0]
    return myString 

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])

def get_packed_bdaddr(bdaddr_string):
    packable_addr = []
    addr = bdaddr_string.split(':')
    addr.reverse()
    for b in addr: 
        packable_addr.append(int(b, 16))
    return struct.pack("<BBBBBB", *packable_addr)

def packed_bdaddr_to_string(bdaddr_packed):
    return ':'.join('%02x'%i for i in struct.unpack("<BBBBBB", bdaddr_packed[::-1]))

def hci_enable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x01)

def hci_disable_le_scan(sock):
    hci_toggle_le_scan(sock, 0x00)

def hci_toggle_le_scan(sock, enable):
# hci_le_set_scan_enable(dd, 0x01, filter_dup, 1000);
# memset(&scan_cp, 0, sizeof(scan_cp));
 #uint8_t         enable;
 #       uint8_t         filter_dup;
#        scan_cp.enable = enable;
#        scan_cp.filter_dup = filter_dup;
#
#        memset(&rq, 0, sizeof(rq));
#        rq.ogf = OGF_LE_CTL;
#        rq.ocf = OCF_LE_SET_SCAN_ENABLE;
#        rq.cparam = &scan_cp;
#        rq.clen = LE_SET_SCAN_ENABLE_CP_SIZE;
#        rq.rparam = &status;
#        rq.rlen = 1;

#        if (hci_send_req(dd, &rq, to) < 0)
#                return -1;
    cmd_pkt = struct.pack("<BB", enable, 0x00)
    bluez.hci_send_cmd(sock, OGF_LE_CTL, OCF_LE_SET_SCAN_ENABLE, cmd_pkt)


def hci_le_set_scan_parameters(sock):
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    SCAN_RANDOM = 0x01
    OWN_TYPE = SCAN_RANDOM
    SCAN_TYPE = 0x01

def compare_enrll_scan(enroll_list,mac_add):
    print enroll_list
    print mac_add
    
def parse_events(sock, loop_count=100):

    # enroll_list =========
    con = sqlite3.connect("/var/www/html/database/smart_bus3.db")
    sqlite3.Connection

    enroll_list = []
    cursor = con.cursor()
    cursor.execute("SELECT * FROM enroll_beacon WHERE 1")
    enroll_rows = cursor.fetchall()

    for i in range(0,len(enroll_rows)):
        enroll_list.append(enroll_rows[i][1])
    print enroll_list
    # enroll_list =========

 
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )
    done = False
    results = []
    myFullList = []
    for i in range(0, loop_count):
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        #print "--------------" 
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
		i =0
        elif event == bluez.EVT_NUM_COMP_PKTS:
                i =0 
        elif event == bluez.EVT_DISCONN_COMPLETE:
                i =0 
        elif event == LE_META_EVENT:
            subevent, = struct.unpack("B", pkt[3])
            pkt = pkt[4:]
            if subevent == EVT_LE_CONN_COMPLETE:
                le_handle_connection_complete(pkt)
            elif subevent == EVT_LE_ADVERTISING_REPORT:
                #print "advertising report"
                num_reports = struct.unpack("B", pkt[0])[0]
                report_pkt_offset = 0
                for i in range(0, num_reports):
		
		    if (DEBUG == True):
			print "-------------"
                    	#print "\tfullpacket: ", printpacket(pkt)
		    	print "\tUDID: ", printpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6])
		    	print "\tMAJOR: ", printpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4])
		    	print "\tMINOR: ", printpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2])
                    	print "\tMAC address: ", packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])
		    	# commented out - don't know what this byte is.  It's NOT TXPower
                    	txpower, = struct.unpack("b", pkt[report_pkt_offset -2])
                    	print "\t(Unknown):", txpower
	
                    	rssi, = struct.unpack("b", pkt[report_pkt_offset -1])
                    	print "\tRSSI:", rssi
		    # build the return string
		    
                    mac_add = packed_bdaddr_to_string(pkt[report_pkt_offset + 3:report_pkt_offset + 9])		    
		    b_uuid = returnstringpacket(pkt[report_pkt_offset -22: report_pkt_offset - 6]) 		   
		    b_major = "%i" % returnnumberpacket(pkt[report_pkt_offset -6: report_pkt_offset - 4]) 		   
		    b_mainor = "%i" % returnnumberpacket(pkt[report_pkt_offset -4: report_pkt_offset - 2]) 		   
		    b_rssi = "%i" % struct.unpack("b", pkt[report_pkt_offset -2])
		    b_tx = "%i" % struct.unpack("b", pkt[report_pkt_offset -1])
                    Adstring = str(datetime.datetime.now().date())+" "+str(datetime.datetime.now().time())+"\t"+mac_add +","+b_uuid+","+b_major+","+b_mainor+","+b_rssi+","+b_tx
		    #print "\tAdstring=", Adstring

                    mac_list = []
                    mac_list.append(mac_add)
                    cmpare_mac = list(set(enroll_list).intersection(mac_list))
                    ############need appand codeing ##################
                    if cmpare_mac:
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                        print(cmpare_mac)
                        cursor = con.cursor()
                        cursor.execute("INSERT INTO enroll_scan_beacon ('createtime','mac_address','uuid','major','minor','rssi','tx_power') VALUES('"+str(datetime.datetime.now()) +"','"+mac_add +"','"+b_uuid+"',"+b_major+","+b_mainor+","+b_rssi+","+b_tx+")")
                        con.commit()
                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
		    
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO bluetooth_scan_log ('createdate','mac_address','uuid','major','minor','rssi','tx_power') VALUES('"+str(datetime.datetime.now()) +"','"+mac_add +"','"+b_uuid+"',"+b_major+","+b_mainor+","+b_rssi+","+b_tx+")")
                    con.commit()

 		    myFullList.append(Adstring)
 		    #time.sleep(1)
                done = True
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    con.close()
    return myFullList


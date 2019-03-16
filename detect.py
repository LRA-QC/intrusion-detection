#!/usr/bin/python3
"""Device intrusion script

This script will scan the network of your choice and will alert you of devices not present in the whitelist. The whitelist is a list of MAC address that YOU trust. Every time you run the detection script, a list of detected devices will be written in 'devices.mac'. 
By default, all devices will show as untrusted. 

Edit devices.mac if needed and run the script below. It will mark as trusted every devices in the list.

sudo ./trust-devices.py  data.db devices.mac

Author: Luc Raymond lucraymond@gmail.com
License: MIT
Requirements : nmap and python
Privileges: sudo (for nmap to get the mac address)
"""
import os
import subprocess
import xml.etree.ElementTree as ET
import re
import datetime
import sys
import sqlite3
def unlink(filename):
    if os.path.isfile(filename):
        os.remove(filename)
    return

def getNmapScan(range):
    """This function will launch NMAP and scan the network mask you provided."""
    filename="/tmp/scanlog.xml"
    unlink(filename)
    unlink("devices.mac")
    f = open("devices.mac", "w")
    output = subprocess.run(["sudo","nmap","-v","-sn",range,"-oX",filename], capture_output=True)
    if output.returncode == 0:
        tree = ET.parse(filename)
        root = tree.getroot()
        hosts = root.findall("./host")
        if hosts:
            state=mac=ip=vendor=""
            for child in hosts:
                for attrib in child:
                    if attrib.tag == "status":
                        state = attrib.attrib["state"]
                    if attrib.tag == "address":
                        if attrib.attrib["addrtype"]=="mac":
                            mac = attrib.attrib["addr"]
                        if attrib.attrib["addrtype"]=="ipv4":
                            ip = attrib.attrib["addr"]
                        if "vendor" in attrib.attrib:
                            vendor = attrib.attrib["vendor"]
                if state == "down":
                    continue
                data = "%s|%s\n" % (mac,vendor)
                f.write(data)
                data = "insert or ignore into scans values (\"%s\",\"%s\",\"%s\",\"%s\"); " % (SCANID,ip,mac,vendor)
                conn.execute(data)
    f.close
    return

def validateHost():
    """This function will check the last scan for any devices that are not listed in the whitelist."""
    c = conn.cursor()
    c.execute("select distinct id from scans order by 1 desc limit 1;") #GET LAST SCAN ID
    row = c.fetchone()
    if row:
        c.execute("select * from scans where id = "+str(row[0])+" and mac not in (select mac from whitelist);")
        rows = c.fetchall()
        for row in rows:
            print("Intruder detected in scan [%d] IP:[%s] MAC:[%s] VENDOR:[%s]" % (row[0],row[1],row[2],row[3]))
    return

if len(sys.argv) != 3:
    print("Syntax\n\t./detect.py <network>/<mask> <database>")
else:
    SCANID = datetime.datetime.now().strftime("%Y%m%d%H%M")
    conn = sqlite3.connect(sys.argv[2])
    if conn:
        conn.execute('CREATE TABLE IF NOT EXISTS scans  (id integer, ip text, mac text, vendor text, PRIMARY KEY (id, ip));')
        conn.execute('CREATE TABLE IF NOT EXISTS whitelist  (mac text, description text, primary key (mac));')
        getNmapScan(sys.argv[1])    #SCAN NETWORK
        validateHost()
        conn.commit()
        conn.close()
    else:
        print("Error creating/accessing the database")
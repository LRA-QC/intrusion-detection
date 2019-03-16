#!/usr/bin/python3
"""Device intrusion script

This script will import devices listed in the second argumment into the database specified in the first argument. 

The detect.py script will detect devices in your network and generate a list of devices in detects in devices.mac. 
You can modify it if needed  and import it with this script.

Feel free to make adjustment to the list before importing it.

example:
    sudo ./trust-devices.py  data.db devices.mac 

To flush the whitelist table and startover : specify --flush at the end

example:
    sudo ./trust-devices.py  data.db devices.mac --flush

Author: Luc Raymond lucraymond@gmail.com
License: MIT
Requirements : nmap and python
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

if len(sys.argv) < 3:
    print("Syntax\n\t./trust.py <database> <devices.mac> [--flush]")
else:
    conn = sqlite3.connect(sys.argv[1])
    if conn:
        if len(sys.argv) == 4:
            if sys.argv[3]=="--flush":
                print( "- Flushing whitelist")
                conn.execute('drop table whitelist;')
                conn.commit()
                conn.execute('vacuum;')

        print( "- Creating table (if needed)")

        conn.execute('CREATE TABLE IF NOT EXISTS whitelist  (mac text, description text, primary key (mac));')

        f = open(sys.argv[2],"r")
        if f:
            print( "- processing whitelist")
            for r in f:
                r=r.strip()
                m = re.split("\|", r)
                if m:
                    sql="insert or ignore into whitelist values (\"%s\",\"%s\");" % (m[0],m[1])
                    conn.execute(sql)
            f.close

        conn.commit()
        conn.close()
    else:
        print("Error creating/accessing the database")
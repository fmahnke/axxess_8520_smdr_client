#!/usr/bin/env python2

import sqlite3
import string

import simple_socket
import sys

import config # configuration file

from axxess_8520_smdr_util import clean_line
from axxess_8520_smdr_util import insert_line_to_db

RECORD_LENGTH = 86 # length of line received by socket in bytes

# Received a filename for logging?
if (len(sys.argv) > 1):
    raw_file = sys.argv[1]

conn = sqlite3.connect(config.DATABASE_NAME)
cursor = conn.cursor()

s = simple_socket.SimpleSocket()
s.connect(config.AXXESS_IP, config.AXXESS_PORT)

# Introduce ourselves
s.send("02000000".decode("hex"))
s.send("8400".decode("hex"))

# Receive data forever
while (1):
    line = s.receive(RECORD_LENGTH)

    line = clean_line(line)

    if (raw_file is not None):
        f = open(raw_file, "a")

        if (f is not None):
            f.write(line)
            f.close()
        
    status = insert_line_to_db(line, cursor, None)
    if (status is True):
        conn.commit()

s.close()
conn.close()


import sqlite3
import string

import simple_socket
import sys

from axxess_8520_smdr_util import clean_line
from axxess_8520_smdr_util import insert_line_to_db

DATABASE_NAME = 'sqdatabase2.db'
RECORD_LENGTH = 86
AXXESS_IP = "192.168.128.220"
AXXESS_PORT = 4000

if (len(sys.argv) > 1):
    raw_file = sys.argv[1]

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

s = simple_socket.SimpleSocket()
s.connect(AXXESS_IP, AXXESS_PORT)

# Introduce ourselves
s.send("02000000".decode("hex"))
s.send("8400".decode("hex"))

while (1):
    line = s.receive(RECORD_LENGTH)
    print "Sock recv: " + line

    line = clean_line(line)

    if (raw_file is not None):
        f = open(raw_file, "a")

        if (f is not None):
            f.write(line)
            f.close()
        
    status = insert_line_to_db(line, cursor)
    if (status is True):
        conn.commit()

#s.close()
conn.close()


#!/usr/bin/env python2

import config # configuration file
import datetime
import logging
from os.path import basename
import re
import sqlite3
import sys

from axxess_8520_smdr_util import clean_line
from axxess_8520_smdr_util import line_to_cdr
from axxess_8520_smdr_util import insert_cdr_record

if (len(sys.argv) > 1):
	fileWithPath = sys.argv[1]
else:
    logging.critical("ERROR: Filename required")
    sys.exit(1)

fileName = basename(fileWithPath)
m        = re.match(r'phone_log_(\d+?)-(\d+?)-(\d+?)\.log', fileName)

if (m is None):
    logging.critical("Log file name is malformed.")
    logging.critical("Name must conform to phone_log_yyyy-mm-dd.log")
    sys.exit(1)

# Assemble datetime from filename
logYear  = int(m.group(1))
logMonth = int(m.group(2))
logDay   = int(m.group(3))
log_date = datetime.date(logYear, logMonth, logDay)

conn = sqlite3.connect(config.DATABASE_NAME)
cursor = conn.cursor()

f = open(fileWithPath)

for line in f:
    line = clean_line(line)
    cdr = line_to_cdr(line, log_date)
    insert_cdr_record(cdr, cursor)

f.close()

conn.commit()
conn.close()


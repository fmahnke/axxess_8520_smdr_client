import datetime
import re
import string
import sqlite3

def clean_line(line):
    # Cleanup incoming line
    return string.lstrip(line, '\0')

def insert_line_to_db(line, cursor):

    if (line == '\n'):
        return
    m = re.match(r'Station', line)

    # Footer?
    if (m is not None):
        return
    m = re.match(r'TYP', line)

    # Other footer?
    if (m is not None):
        return

    print "Line: " + line
    m = re.match(r'([\w/]*?)\s+?([\d\*]+?)\s+?(\d{5})\s+?[RING\s\.]*?([\d\-]+?)\s+?(\d*?)\s+?(\d\d):(\d\d)\s+?S=(\d+?)\s', line)
    print "Line: " + line
    if (m is None):
        return
    # Type field returned an empty string?
    if (not m.group(1)):
        type = 'RG'
    else:
        type = m.group(1)

    if (m.group(2) == '*****'):
        ext = 0
    else:
        ext = int(m.group(2))

    trunk = int(m.group(3))

    # Strip hyphens from phone number
    phone_number = int(m.group(4).replace('-', ''))

    if (m.group(5) is not ''):
        incoming_ext = int(m.group(5))
    else:
        incoming_ext = 0

    start_time_hh = int(m.group(6))
    start_time_mm = int(m.group(7))
    duration = int(m.group(8))

    start_time = datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(hour=start_time_hh, minute=start_time_mm))

    # Print record to console for debugging
    print "Type: "             + type
    print "Ext: "              + str(ext)
    print "Trunk: "            + str(trunk)
    print "Number and stuff: " + str(phone_number)
    #print "Incoming ext: "    + str(incoming_ext)
    print "Start time: "       + str(start_time)
    print "Duration: "         + str(duration)

    cursor.execute("INSERT INTO logviewer_phonerecord VALUES (NULL,'%s',%d,%d,%d,%d,'%s','%s')" % (type, ext, trunk, phone_number, incoming_ext, start_time, datetime.timedelta(seconds=duration)))

    return True


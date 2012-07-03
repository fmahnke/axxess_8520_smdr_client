import datetime
import logging
import re
import string
import sqlite3

def clean_line(line):
    """Clean any garbage characters from a line"""
    # Cleanup 'R' and null characters from beginning of line
    return string.lstrip(line, 'R\0')

def insert_line_to_db(line, cursor, record_date):

    logging.debug("Line: %s", line)

    if (line == '\n'):
        return False

    m = re.match(r'Station', line)

    # Footer?
    if (m is not None):
        return False

    m = re.match(r'TYP', line)

    # Other footer?
    if (m is not None):
        return False

    # Call Detail Record?
    logging.debug("Matching line against CDR regex")
    m = re.match(r'([\w/]*?)\s+?([\d\*]+?)\s+?(\d{5})\s+?[RING\s\.]*?([\d\-]+?)\s+?(\d*?)\s+?(\d\d):(\d\d)\s+?S=(\d+?)\s', line)
    if (m is None):
        logging.info('Line did not match CDR record')
        return False

    logging.info('Line matched CDR record')

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

    if (record_date is None):
        record_date = datetime.date.today()

    start_time = datetime.datetime.combine(
        record_date,
        datetime.time(hour=start_time_hh, minute=start_time_mm))

    # Log record
    logging.debug("Type: %s", type)
    logging.debug("Ext: %s", str(ext))
    logging.debug("Trunk: %s", str(trunk))
    logging.debug("Number: %s", str(phone_number))
    logging.debug("Incoming ext: %s", str(incoming_ext))
    logging.debug("Start time: %s", str(start_time))
    logging.debug("Duration: %s", str(duration))

    logging.debug("Executing query")
    cursor.execute("INSERT INTO logviewer_phonerecord VALUES (NULL,'%s',%d,%d,%d,%d,'%s','%s')" % (type, ext, trunk, phone_number, incoming_ext, start_time, datetime.timedelta(seconds=duration)))
    logging.debug("Cursor.rowcount holds %d", cursor.rowcount)

    return True


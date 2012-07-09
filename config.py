import logging

# Absolute path to sqlite database file e.g. sqdatabase.db
DATABASE_NAME = ''
# Quoted IP address of Axxess PBX system. Needed for TCP/IP client.
AXXESS_IP = ''
# TCP connection port. Needed for TCP/IP client.
AXXESS_PORT = 4000

# Absolute path of file to write log messages. Leave blank ('') for none.
LOG_FILE = 'testlog.log'

# If LOG_FILE is defined, define the format of the log messages to write.
if (LOG_FILE is not None):
    logging.basicConfig(format = '%(asctime)s %(message)s',
                        filename = LOG_FILE,
                        level = logging.DEBUG)


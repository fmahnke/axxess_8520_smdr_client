import logging

DATABASE_NAME = '' # sqlite database file
AXXESS_IP = ""
AXXESS_PORT = 4000

LOG_FILE = '' # file to write log messages

if (LOG_FILE is not None):
    logging.basicConfig(format = '%(asctime)s %(message)s',
                        filename = LOG_FILE,
                        level = logging.DEBUG)


import logging

DATABASE_NAME = '/home/fritz/django-pbx-smdr-accounting/sqdatabase.db' # sqlite database file
AXXESS_IP = "192.168.128.220"
AXXESS_PORT = 4000

LOG_FILE = 'testlog.log' # file to write log messages

if (LOG_FILE is not None):
    logging.basicConfig(format = '%(asctime)s %(message)s',
                        filename = LOG_FILE,
                        level = logging.DEBUG)


# Config.py: A module for parsing and writing to config files.

import getpass
import re
from os     import remove
from shutil import copy

class Config(object):
    def __init__(self):
        return

# read: parses through a given config file for information
#
# returns: array containing configuration data
# params:  filename - path for config.txt

    @staticmethod
    def read(filename, user = getpass.getuser()):
        f = open(filename, 'r')

        find_user = re.compile(r'.*:\n')

        content = dict()

        found = False
        line = f.readline()

        while not found and line:
            if find_user.match(line) and line.split(':')[0] == user:
                point = f.readline()
                while not found and point:
                    item = point.split('=')
                    val = item[1].strip()
                    try:
                        val = int(val)
                    except ValueError:
                        val = val.strip('\'')
                    content[item[0].strip()] = val
                    point = f.readline()
                    found = point == '\n'

            line = f.readline()

        f.close()

        return content

    @staticmethod
    def write(filename, key, val, user = getpass.getuser()):
        copy(filename, '.%s_temp' % filename)
        remove(filename)

        f_temp = open('.%s_temp' % filename, 'r')
        f_new  = open(filename, 'w')


        remove('.%s_temp' % filename)

# c = Config.write('config-example.txt', 'test', 3)

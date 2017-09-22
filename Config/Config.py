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
#          user     - user whose default parameters will be read

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
    def init(filename, user = getpass.getuser()):
        f = open(filename, 'w')
        f.close()

        f = open(filename, 'a')
        f.write('%s:\n' % user)
        f.close()

# write: parses through a given config file for information
#
# returns: array containing configuration data
# params:  filename - path for config.txt
#          key      - name of parameter to write
#          value    - value of parameter
#          user     - user whose default parameter will be written

    @staticmethod
    def write(filename, key, value, user = getpass.getuser()):
        copy(filename, '%s_temp' % filename)
        remove(filename)

        f_temp = open('%s_temp' % filename, 'r')
        f_new  = open(filename, 'w')

        find_user = re.compile(r'.*:\n')

        config = dict()

        found = False
        line = f_temp.readline()

        while line:
            found = False
            if find_user.match(line):
                u = line.split(':')[0]
                content = dict()
                point = f_temp.readline()
                while not found and point:
                    item = point.split('=')
                    val = item[1].strip()
                    try:
                        val = int(val)
                    except ValueError:
                        val = val.strip('\'')
                    content[item[0].strip()] = val
                    point = f_temp.readline()
                    found = point == '\n'

                config[u] = content
            line = f_temp.readline()

        config[user][key] = value

        for u in config:
            f_new.write('%s:\n' % u)
            for k in config[u]:
                try:
                    config[u][k] = int(config[u][k])
                    f_new.write('    %s = %s\n' % (k, config[u][k]))
                except ValueError:
                    f_new.write('    %s = \'%s\'\n' % (k, config[u][k]))
            f_new.write('\n')

        remove('%s_temp' % filename)

    @staticmethod
    def write_all(filename, defaults, user = getpass.getuser()):
        for key in defaults:
            Config.write(filename, key, defaults[key], user)

# Config.write('/Users/nick/cnbt/cnbt-repo/cnbt/Config/config-example.txt', 'key', 'spaghetti')

# import site
# print site.getsitepackages()

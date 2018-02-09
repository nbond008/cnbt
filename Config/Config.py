# Config.py: A module for parsing and writing to config files.

import getpass
import re

res = {
    'user_start'  : re.compile(r'.*<User '),
    'field_start' : re.compile(r'.*<Field '),
    'list_start'  : re.compile(r'.*<List '),
    'item_start'  : re.compile(r'.*<Item '),

    'name'        : re.compile(r'Name=\"[^\"]*\"'),
    'value'       : re.compile(r'Value=\"[^\"]*\"'),

    'quotes'      : re.compile(r'\" '),
    'end'         : re.compile(r'/.*>$')
}

const = {
    'user'  : 'User',
    'field' : 'Field',
    'list'  : 'List',
    'item'  : 'Item',

    'name'  : 'Name',
    'value' : 'Value',

    'tab'   : '    '
}

class Config(object):
    def __init__(self):
        return

# read: parses through a given config file for information
#
# returns: dict containing configuration data for a specific user
# params:  filename - path for config.xml
#          user     - user whose default parameters will be read

    @staticmethod
    def read(filename, user = getpass.getuser()):
        return Config.__read__(filename)[user]

    @staticmethod
    def init(filename, user = getpass.getuser()):
        f = open(filename, 'w')
        f.close()

        f = open(filename, 'a')
        textcontent = '<%s %s=\"%s\">\n' % (
            const['user'],
            const['name'],
            user
        )

        textcontent += '</%s>\n' % (
            const['user']
        )

        f.write(textcontent)
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
        content = Config.__read__(filename)

        try:
            content[user][key] = value
        except KeyError:
            content[user] = dict()
            content[user][key] = value

        textcontent = ''

        try:
            for u in content:
                textcontent += '<%s %s=\"%s\">\n' % (
                    const['user'],
                    const['name'],
                    u
                )
                for k in content[u]:
                    if isinstance(k, basestring):
                        textcontent += '%s<%s %s=\"%s\" %s=\"%s\"/>\n' % (
                            const['tab'],
                            const['field'],
                            const['name'],
                            k,
                            const['value'],
                            content[u][k]
                        )
                    else:
                        textcontent += '%s<%s %s=\"%s\">\n' % (
                            const['tab'],
                            const['list'],
                            const['name'],
                            content[u][k]
                        )
                        for item in k:
                            print 'p'

                        textcontent += '</%s>\n' % (
                            const['list']
                        )

                textcontent += '</%s>\n' % (
                    const['user']
                )
        except KeyError:
            return False

        f = open(filename, 'w')

        f.write(textcontent)

        f.close()

        return True

    @staticmethod
    def write_all(filename, defaults, user = getpass.getuser()):
        for key in defaults:
            Config.write(filename, key, defaults[key], user)
# __read__
#
# returns: dict containing configuration data for all users
# params:  filename - path for config.xml

    @staticmethod
    def __read__(filename):
        f = open(filename, 'r')

        content = dict()
        curruser = ''
        currlist = ''

        for line in f:
            if re.match(res['user_start'], line):
                user_str = re.match(res['name'], re.split(res['user_start'], line)[1]).group()
                curruser = user_str.split('\"')[1]
                content[curruser] = dict()
            elif re.match(res['field_start'], line):
                field = re.split(res['end'], re.split(res['field_start'], line)[1])[0]

                try:
                    name_str  = re.match(res['name'], field).group().strip()
                except AttributeError:
                    name_str  = re.split(res['value'], field)[1].strip()

                try:
                    value_str = re.match(res['value'], field).group().strip()
                except AttributeError:
                    value_str = re.split(res['name'], field)[1].strip()

                currname  = name_str.split('\"')[1]
                currvalue = value_str.split('\"')[1]

                try:
                    content[curruser][currname] = currvalue
                except Exception:
                    print 'not nice >:['
            elif re.match(res['list_start'], line):
                flist = re.split(res['end'], re.split(res['list_start'], line)[1])[0]
                name_str  = re.match(res['name'], flist).group().strip()
                currlist  = name_str.split('\"')[1]

                content[curruser][currlist] = list()
            elif re.match(res['item_start'], line):
                item = re.split(res['end'], re.split(res['item_start'], line)[1])[0]
                value_str = re.match(res['value'], item).group().strip()
                currvalue = value_str.split('\"')[1]

                try:
                    content[curruser][currlist].append(currvalue)
                except KeyError:
                    print 'List item without list!'

        f.close

        return content

p = Config.read('/Users/nickbond/research/cnbt/Config/config-example.xml')
print p

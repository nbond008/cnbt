from Config import Config
import re
import sys
from os import path
from os import remove as remove_file
from os import rename as rename_file

def read_color_data():
    configdir = '{}/config.xml'.format(path.dirname(path.realpath(__file__)))
    try:
        data = Config.read(configdir)
        print 'successfully read color data from {}\n'.format(configdir)
    except IOError:
        print 'failed to read color data.'
        print 'creating config.xml with default color values.\n'
        Config.init(configdir)

        data = {
            'A' : '0,0,255,255',
            'B' : '255,0,0,255',
            'C' : '0,255,0,255',
            'R' : '255,255,0,255'
        }

        Config.write_all(configdir, data)

    return data

def get_color_string(type, data):
    for key in data:
        if type == key:
            return data[key]

    raise IndexError('color for bead type \"{}\" not set. keeping original color.'.format(type))

def colorBARS_main(mtd_filename, timestep, remove = False):
    if timestep:
        new_filename = '{}_t{}.mtd'.format(re.split(r'\.mtd', mtd_filename)[0], timestep)
    else:
        new_filename = '{}_color.mtd'.format(re.split(r'\.mtd', mtd_filename)[0])

    mbt_start = re.compile(r'\s*(?=<MesoBeadType)')
    bead_name = re.compile(r'(?<=BeadName=\")[A-Z]*(?=\")')
    color_str = re.compile(r'(?<=Color=\")[0-9]+,[0-9]+,[0-9]+,[0-9]+(?=\")')

    old = open(mtd_filename, 'r')
    new = open(new_filename, 'w')

    color_data = read_color_data()

    for line in old:
        try:
            tab   = '\t' * len(mbt_start.search(line).group())
            type  = bead_name.search(line).group()[0]
            color = color_str.search(line).group()[0]

            print 'found bead of type {}'.format(type)

            try:
                color_string = get_color_string(type, color_data)
            except IndexError as e:
                print '    {}'.format(e)
                color_string = color

            new_line = '{}<MesoBeadType BeadName=\"{}\" Color=\"{}\"/>\r\n'.format(tab, type, color_string)
            new.write(new_line)
        except AttributeError:
            new.write(line)

    new.close()

    old.close()
    if remove and path.exists(mtd_filename):
        remove_file(mtd_filename)
        rename_file(new_filename, mtd_filename)

def colorBARS_config(beadtype):
    configdir = '{}/config.xml'.format(path.dirname(path.realpath(__file__)))
    print configdir
    try:
        Config.read(configdir)
    except IOError:
        Config.init(configdir)
        #set defaults
        data = {
            'A' : '0,0,255,255',
            'B' : '255,0,0,255',
            'C' : '0,255,0,255',
            'R' : '255,255,0,255'
        }
        Config.write_all(configdir, data)

    answer = raw_input('add color data for beadtype \"{}\"? (y/n)\n'.format(beadtype))
    if not (answer.lower() == 'y' or answer.lower() == 'yes'):
        return None

    color = [0, 0, 0, 255]

    try:
        color[0] = int(raw_input('R: ')) % 256
    except ValueError:
        return None

    try:
        color[1] = int(raw_input('G: ')) % 256
    except ValueError:
        return None

    try:
        color[2] = int(raw_input('B: ')) % 256
    except ValueError:
        return None

    color_str = '{},{},{},{}'.format(color[0], color[1], color[2], color[3])

    Config.write(configdir, beadtype, color_str)

    return color_str

def print_usage():
    print 'usage: python ColorBARS.py filename timestep OR'
    print '       python ColorBARS.py filename --remove OR'
    print '       python ColorBARS.py --define beadtype'

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print_usage()
        sys.exit(0)

    if sys.argv[1] == '--define' or sys.argv[1] == '-d':
        # try:
        result = colorBARS_config(sys.argv[2])
        if result:
            print 'successfully defined beadtype \"{}\" as color \"{}\"'.format(sys.argv[2], result)
        else:
            print 'cancelled'

        sys.exit(0)

    else:
        try:
            colorBARS_main(sys.argv[1], int(sys.argv[2]))
        except IOError:
            print 'invalid filename: \"{}\"'.format(sys.argv[1])
            print_usage()
            sys.exit(0)
        except ValueError:
            if sys.argv[2] == '--replace' or sys.argv[2] == '-r':
                try:
                    colorBARS_main(sys.argv[1], None, remove = True)
                except IOError:
                    print 'invalid filename: \"{}\"'.format(sys.argv[1])
                    print_usage()
                    sys.exit(0)
            else:
                print 'invalid timestep: \"{}\"'.format(sys.argv[2])
                print_usage()
            sys.exit(0)

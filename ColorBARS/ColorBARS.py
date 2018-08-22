import re
import sys
from os import path

def get_color_string(type):
    if type is 'A':
        return '0,0,255,255'
    if type is 'B':
        return '255,0,0,255'
    if type is 'C':
        return '0,255,0,255'
    if type is 'R':
        return '255,255,0,255'
    raise IndexError('color for bead type \"{}\" not set'.format(type))

def colorBARS_main(mtd_filename, timestep):
    new_filename = '{}_t{}.mtd'.format(re.split(r'\.mtd', mtd_filename)[0], timestep)

    mbt_start = re.compile(r'\s*(?=<MesoBeadType)')
    bead_name = re.compile(r'(?<=BeadName=\")[A-Z]*(?=\")')
    color_str = re.compile(r'(?<=Color=\")[0-9]+,[0-9]+,[0-9]+,[0-9]+(?=\")')

    old = open(mtd_filename, 'r')
    new = open(new_filename, 'w')

    for line in old:
        try:
            tab   = '\t' * len(mbt_start.search(line).group())
            type  = bead_name.search(line).group()[0]
            color = color_str.search(line).group()[0]

            print 'found bead of type {}!'.format(type)

            try:
                color_string = get_color_string(type)
            except IndexError as e:
                print '\t{}'.format(e)
                color_string = color

            new_line = '{}<MesoBeadType BeadName=\"{}\" Color=\"{}\"/>\r\n'.format(tab, type, color_string)
            new.write(new_line)
        except AttributeError:
            new.write(line)

    old.close()
    new.close()

if __name__ == '__main__':
    colorBARS_main('/Users/nickbond/research/dpd_shenanigans/Diblock2.mtd', 69)

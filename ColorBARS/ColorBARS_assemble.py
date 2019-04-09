from os import walk
from os.path import join
import xml.etree.ElementTree as ET
from shutil import move

a = 'aAaAa'
b = 'bBbBb'
c = 'cCcCc'
w = 'wWwWw'
 
def species_finder(directory):
    species = []
    for path, subs, files in walk(directory, topdown = True):
        for f in files:
            if f.endswith('.Dpd_par'):
                new_species = par_reader(path,f)
                for each in new_species:
                    if each not in species:
                        species.append(each)
                        print('   Added '+each+'...')
    return sorted(species)

def par_reader(p,f):
    s = []
    with open(join(p,f),'r') as pfile:
        for line in pfile:
            if ' name' in line:
                name = line.split()[-1]
                s.append(name)
            elif 'interaction' in line:
                break
    return s

def mtd_reader(directory, species={'A': a, 'B': b, 'C': c,'W': w}):
    print('Applying styles...')
    mtd_found = False
    for path, subs, files in walk(directory, topdown = True):
        for f in files:
            if f.endswith('.mtd'):
                mtd_found = True
                mtd_file = join(path,f)
                print('   Modifying '+mtd_file+'...')
                tree = ET.parse(mtd_file)
                root = tree.getroot()

                for elem in [['FloatField','Name'], ['MesoBeadType', 'BeadName']]:
##                    print('Looking in the '+elem[0]+' block')
                    for each in root.iter(elem[0]):
                        rawname = each.get(elem[1])
##                        print(rawname)
                        name = rawname.split()
                        if name[0] in species:
                            each.set('Color',species[name[0]])
                        else:
                            print('Species '+name[0]+' not found in species list. Some settings were not changed.')

                tree.write(join(path,f))
    if mtd_found == True:
        print('Done!\n')
    else:
        print('No .mtd files found.')

##                with open('out.mtd','r') as f:
##                    with open('temp.txt','w') as f2: 
##                        f2.write("<?xml version='1.0'?>\n<!DOCTYPE XSD []>\n")
##                        f2.write(f.read())
##                move('temp.txt','out.mtd')

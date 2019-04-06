import xml.etree.ElementTree as ET
from shutil import move

a = '0,0,255,255'
b = '255,0,0,255'
c = '0,255,0,255'
w = '0,255,255,255'

def mtd_reader(path='D:/colorbars/res1.mtd',species={'A': a, 'B': b, 'C': c,'W': w}):
    tree = ET.parse(path)
    root = tree.getroot()

    els = [['FloatField','Name'], ['MesoMoleculeSet', 'Name'], ['MesoBeadType', 'BeadName']]
    for i in range(3):
        print('Looking in the '+els[i][0]+' block')
        for each in root.iter(els[i][0]):
            rawname = each.get(els[i][1])
            print(rawname)
            name = rawname.split()
            if name[0] in species:
                each.set('Color',species[name[0]])


##    print('Looking in the FloatField block; these will be field value names')
##    for each in root.iter('FloatField'):
##        rawname = each.get('Name')
##        print(rawname)
##        name = rawname.split()
##        if name[0] in species:
##            each.set('Color',species[name[0]])
##
##    print('Looking in the MesoMoleculeSet block; these will be bead names')
##    for each in root.iter('MesoMoleculeSet'):
##        name = each.get('Name')
##        print(name)
##        if name in species:
##            each.set('Color',species[name[0]])
##
##    print('Looking in the MesoBeadType block; these will be bead names')
##    for each in root.iter('MesoBeadType'):
##        name = each.get('BeadName')
##        print(name)
##        name2 = name.split()
##        if name2[0] in species:
##            each.set('Color',species[name[0]])

##    root.insert(0, ET.Comment('DOCTYPE XSD []'))
    tree.write('out.mtd')

    with open('out.mtd','r') as f:
        with open('temp.txt','w') as f2: 
            f2.write("<?xml version='1.0'?>\n<!DOCTYPE XSD []>\n")
            f2.write(f.read())
    move('temp.txt','out.mtd')

mtd_reader()

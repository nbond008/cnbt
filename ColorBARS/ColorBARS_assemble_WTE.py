from os import walk
from os.path import join
import xml.etree.ElementTree as ET
##from shutil import move

def species_finder(directory):
    try:
        species = []
        mtd_found = False
        for path, subs, files in walk(directory):
            for f in files:
                if f.endswith('.Dpd_par'):
                    new_species = set(par_reader(path,f)) - set(species)
                    for each in new_species:
                        species.append(each)
                        print('   Added '+each+'...')
                elif f.endswith('.mtd'):
                    mtd_found = True
        return mtd_found, sorted(species)
    except:
        print('Tell Connor an error occurred in the species_finder function.')
        print('Please include all the exact steps you did to get this error.')
        print('If you can include steps to reliably reproduce it, that would be great.')

def par_reader(p,f):
    try:
        s = []
        with open(join(p,f),'r') as pfile:
            line = pfile.readline()
            done = False
            while line and not done:
                if 'name' in line:
                    name = line.split()[-1]
                    s.append(name)
                elif 'interaction' in line:
                    done = True
                line = pfile.readline()
        return s
    except:
        print('Tell Connor an error occurred in the par_reader function.')
        print('Please include all the exact steps you did to get this error.')
        print('If you can include steps to reliably reproduce it, that would be great.')

"""

General settings list contains:
    0. Path
    1. Species dictionary

Box settings list contains:
    0. Box visibility - if 0, need to set ShowBox="0" for all FloatField species
    1. Custom box color check
    2. Hide modified species check
    3. Box color in RGB

Field settings list contains:
    0. Field color mode, preformatted
    1. Field display style (Empty, Dots, or Volume), preformatted
    2. Dot quality, preformatted
    3. Dot size, preformatted
    4. Volume quality, preformatted
    5. Transparency value (alpha, to be concatenated with RGB values from species dictionary), preformatted

Mesoscale molecule settings list contains:
    0. Bead visibility
    1. Bond visibility
    2. Mesoscale molecule display style
    3. Dot size
    4. Line width
    5. Ball size
    6. Stick radius

Species dictionary definition:

species_dict[species_elem_list[i].get()] = [
                                                0. Mesoscale molecule visibility
                                                1. Preset color value (NOT NEEDED)
                                                2. RGB color value
                                                3. Hex color value (NOT NEEDED)
                                            ]

"""

def mtd_reader(generalsettings, boxsettings, fieldsettings, mmolsettings):
    try:
        directory = generalsettings[0]
        species = generalsettings[1]
        print('\nApplying styles...')
        for path, subs, files in walk(directory, topdown = True):
            for f in files:
                if f.endswith('.mtd'):
                    mtd_file = join(path,f)
                    print('   Modifying '+mtd_file+'...')
                    tree = ET.parse(mtd_file)
                    root = tree.getroot()

                    for each in root.iter('FloatField'):
                        rawname = each.get('Name')
                        name = rawname.split()
                        if name[0] in species:
                            each.set('ShowBox', str(boxsettings[0]))
                            if not fieldsettings[0] == 'species':
                                each.set('ColorMode', str(fieldsettings[0]))
                            elif 'ColorMode' in each:
                                del each['ColorMode']
                            each.set('DisplayStyle', str(fieldsettings[1]))
                            each.set('DotQuality', str(fieldsettings[2]))
                            each.set('DotSize', str(fieldsettings[3]))
                            each.set('VolumeQuality', str(fieldsettings[4]))
                            each.set('Color', str(species[name[0]][2] + fieldsettings[5]))
                        else:
                            print('Species '+name[0]+' not found in species list. Some settings were not changed.')
                    if boxsettings[1]:
                        each.set('Color', str(boxsettings[3] + fieldsettings[5]))
                        if boxsettings[2]:
                            each.set('DisplayStyle', 'Empty')

                    for each in root.iter('MesoMoleculeSet'):
                        each.set('ShowBeads', str(mmolsettings[0]))
                        each.set('ShowBonds', str(mmolsettings[1]))
                        each.set('ColorMode', '12289')
                        each.set('DisplayStyle', str(mmolsettings[2]))
                        each.set('DotSize', str(mmolsettings[3]))
                        each.set('LineWidth', str(mmolsettings[4]))
                        each.set('BallSize', str(mmolsettings[5]))
                        each.set('StickRadius', str(mmolsettings[6]))

                    for each in root.iter('MesoBeadType'):
                        name = each.get('BeadName')
                        if name in species:
                            each.set('Color', str(species[name][2] + ',255'))
                            each.set('Visible', str(species[name][0]))
                        else:
                            print('Species '+name+' not found in species list. Some settings were not changed.')

                    tree.write(join(path,'out.xml'))




    ##                with open('out.mtd','r') as f:
    ##                    with open('temp.txt','w') as f2: 
    ##                        f2.write("<?xml version='1.0'?>\n<!DOCTYPE XSD []>\n")
    ##                        f2.write(f.read())
    ##                move('temp.txt','out.mtd')
    
    except:
        print('Tell Connor an error occurred in the mtd_reader function.')
        print('Please include all the exact steps you did to get this error.')
        print('If you can include steps to reliably reproduce it, that would be great.')

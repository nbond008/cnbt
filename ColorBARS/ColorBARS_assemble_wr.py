from os import walk
from os.path import join
from time import time
from math import ceil
import xml.etree.cElementTree as ET

def species_finder(directory):
    species = []
    mtd_list = []
    for path, subs, files in walk(directory):
        for f in files:
            pfile = join(path,f)
            if pfile.endswith('.Dpd_par'):
                new_species = set(par_reader(pfile)) - set(species)
                for each in new_species:
                    species.append(each)
                    print('   Added '+each+'...')
            elif pfile.endswith('.mtd'):
                mtd_list.append(pfile)
    return sorted(species), mtd_list

def par_reader(f):
    s = []
    with open(f,'r') as pfile:
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

def mtd_reader(generalsettings, boxsettings, fieldsettings, mmolsettings, mtd_list):
    common_path = len(generalsettings[0])
    species = generalsettings[1]
    
    print('\n--- Applying styles to '+str(len(mtd_list))+' .mtd files... ---')
    progress = 0
    decade = 0
    t0 = time()
    error_files = []
    for f in mtd_list:
        print('   Modifying (...)'+f[common_path:]+'...')
        tree = ET.parse(f)

        floatfield_list = tree.findall('./MesoTreeRoot/FloatField')
        mesomoleculeset_list = tree.findall('./MesoTreeRoot/MesoMoleculeSet')

        if not (floatfield_list == [] or mesomoleculeset_list == []):
            for each in floatfield_list:
                rawname = each.get('Name')
                name = rawname.split()
                if name[0] in species:
                    each.set('ShowBox', str(boxsettings[0]))
                    if not fieldsettings[0] == 'species':
                        each.set('ColorMode', str(fieldsettings[0]))
                    elif not each.get('ColorMode') == None:
                        del each.attrib['ColorMode']
                    each.set('DisplayStyle', str(fieldsettings[1]))
                    each.set('DotQuality', str(fieldsettings[2]))
                    each.set('DotSize', str(fieldsettings[3]))
                    each.set('VolumeQuality', str(fieldsettings[4]))
                    each.set('Color', str(species[name[0]][3] + fieldsettings[5]))
                    each.set('Visible', str(species[name[0]][0]))
                else:
                    print('Species '+name[0]+' not found in species list. Some settings were not changed.')
            if boxsettings[1]:
                each.set('Color', str(boxsettings[3] + fieldsettings[5]))
                if boxsettings[2]:
                    each.set('Visible','1')
                    each.set('DisplayStyle', 'Empty')

            xcoords = []
            ycoords = []
            zcoords = []
            
            for each in mesomoleculeset_list:
                each.set('ShowBeads', str(mmolsettings[0]))
                each.set('ShowBonds', str(mmolsettings[1]))
                each.set('ColorMode', '12289')
                each.set('DisplayStyle', str(mmolsettings[2]))
                each.set('DotSize', str(mmolsettings[3]))
                each.set('LineWidth', str(mmolsettings[4]))
                each.set('BallSize', str(mmolsettings[5]))
                each.set('StickRadius', str(mmolsettings[6]))
                each.set('Visible',str(mmolsettings[0] or mmolsettings[1]))

                solvcheck = 0
                mesobeadtype_list = each.findall('./MesoBeadType')
                for eachtype in mesobeadtype_list:
                    name = eachtype.get('BeadName')
                    if name in species:
                        eachtype.set('Color', str(species[name][3] + ',255'))
                        eachtype.set('Visible', str(species[name][0]))
                        solvcheck += species[name][1]
                    else:
                        print('Species '+name+' not found in species list. Some settings were not changed.')

                if boxsettings[4] and solvcheck == 0:
                    xyz = getcoords(each)
                    xcoords.extend(xyz[0])
                    ycoords.extend(xyz[1])
                    zcoords.extend(xyz[2])
                
                elif boxsettings[4] and not solvcheck == int(each.get('NumberBeadTypes')):
                    print('Mesomolecule '+each.get('Name')+' has mixed solvent and non-solvent beads.')
                    print('This mesomolecule was not considered during rebracketing.')

            if not (xcoords == [] or ycoords == [] or zcoords == []):
                displayrange = rebracket(each, xcoords, ycoords, zcoords)
                for each in mesomoleculeset_list:
                    each.set('DisplayRange',displayrange)
            
            tree.write(f)

        else:
            error_files.append(f)

        progress += 1
        pProgress = float(progress)/len(mtd_list)
        dProgress = 10*int(progress/(0.1*len(mtd_list)))
        
        if dProgress > decade and not progress == len(mtd_list):
            decade = dProgress
            t = (time()-t0)/pProgress - (time()-t0)
            minutes = str(int(t//60))
            seconds = int(ceil(t%60))
            if seconds < 10:
                tens = '0'
            else:
                tens = ''
            print('\n--- Progress: ' + str(decade) + '% Estimated time remaining: ' + minutes + ':' + tens + str(seconds) + ' ---\n')

        elif progress == len(mtd_list):
            t = time()-t0
            minutes = str(int(t//60))
            seconds = int(ceil(t%60))
            if seconds < 10:
                tens = '0'
            else:
                tens = ''
            print('\n--- All files completed. Time elapsed: ' + str(minutes) + ':' + tens + str(seconds) + ' ---\n')
            if not error_files == []:
                if len(error_files)>1:
                    plural2 = 's were'
                else:
                    plural2 = ' was'
                print(' ** Warning: The following file' + plural2 + ' not modified.')
                for each in error_files:
                    print(' ** (...)' + each[common_path:])
                print('\n ** Before applying styles, all files must have been opened at least once.')
                print(' ** See the File Open Error section in Help for further information.\n')

def getcoords(mesomoleculeset):
    coords_list = mesomoleculeset.findall('./MesoMolecule')

    xdim = int(mesomoleculeset.get('XSize'))
    ydim = int(mesomoleculeset.get('YSize'))
    zdim = int(mesomoleculeset.get('ZSize'))

    x = []
    y = []
    z = []
    for m in coords_list:
        coords = m.get('Coords')
        coords = coords.split(':')
        for bead in coords:
            xyz = bead.split(',')
            x.append(float(xyz[0])/xdim)
            y.append(float(xyz[1])/ydim)
            z.append(float(xyz[2])/zdim)

    return [x,y,z]

def rebracket(mesomoleculeset, x, y, z):
    x.sort()
    y.sort()
    z.sort()

    divs = []
    
    for axis in x,y,z:
        count = 0
        mincount = 1000
        prog = 0.01
        i = 0
        while i < len(axis) and not mincount == 0:
            if axis[i] < prog:
                count += 1
            else:
                if count < mincount:
                    mincount = count
                    minprog = prog
                prog += 0.01
                count = 0
            i+=1
        if minprog > 0.5:
            minprog -= 1
        divs.append(round(minprog,2))

    return str(divs[0]) + ',' + str(divs[0]+1) + ',' + str(divs[1]) + ',' + str(divs[1]+1) + ',' + str(divs[2]) + ',' + str(divs[2]+1)

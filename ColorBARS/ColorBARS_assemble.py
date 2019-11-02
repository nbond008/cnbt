from os import walk
from os.path import join
from time import time
from math import ceil
import xml.etree.cElementTree as ET # cElementTree deprecated in 3.3 - use xml.etree.ElementTree in 3.3 or later if equivalent speed

def species_finder(directory):
    print('Detecting species and building .mtd list from '+directory+'...')
    print('(Depending on your directory size, this may take a little while.)')
    
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
    error_files2 = []
    for f in mtd_list:
        print('   Modifying (...)'+f[common_path:]+'...')
        tree = ET.parse(f)

        floatfield_list = tree.findall('./MesoTreeRoot/FloatField')
        mesomoleculeset_list = tree.findall('./MesoTreeRoot/MesoMoleculeSet')

        missing_species = []
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
                elif not (name[0] in species or name[0] in missing_species):
                    missing_species.append(name[0])
                    
            if boxsettings[0]:
                each.set('Visible','1')
            if boxsettings[1]:
                each.set('Color', str(boxsettings[3] + fieldsettings[5]))
                if boxsettings[2]:
                    each.set('DisplayStyle', 'Empty')

            brokenbond_list = [[0]*100, [0]*100, [0]*100]
            
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
                    elif not (name in species or name in missing_species):
                        missing_species.append(name)

                if boxsettings[4] and solvcheck == 0:
                    coords_analyzer(each, brokenbond_list)
                
                elif boxsettings[4] and not solvcheck == int(each.get('NumberBeadTypes')):
                    print('      Mesomolecule '+each.get('Name')+' has mixed solvent and non-solvent beads.')
                    print('      This mesomolecule was not considered during rebracketing.')

            if boxsettings[4]:
                displayrange = rebracket(brokenbond_list)
                for each in mesomoleculeset_list:
                    each.set('DisplayRange',displayrange)
            
            tree.write(f)
        
            if not missing_species == []:
                missing_species_string = missing_species[0]
                for name in missing_species[1:]:
                    missing_species_string += ', ' + name
                error_files2.append([f, missing_species_string])
        
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
        print('\n ** Before applying styles, all .mtd files must have been opened at least once.')
        print(' ** Click Help for further information.\n')

    if not error_files2 == []:
        if len(error_files2)>1:
            plural3 = 's'
        else:
            plural3 = ''
        print(' ** Warning: The following file' + plural3 + ' contained missing bead types.')
        for each in error_files2:
            print(' ** (...)' + each[0][common_path:] + '     (Missing species: ' + each[1] + ')')
        print('\n ** Each bead type must be present in the species list in order to be modified.\n')

def coords_analyzer(mesomoleculeset, brokenbond_list):
    mesomolecule_list = mesomoleculeset.findall('./MesoMolecule')
    architecture = bond_analyzer(topology_analyzer(mesomoleculeset.get('MesoMoleculeString')))

    xdim = int(mesomoleculeset.get('XSize'))
    ydim = int(mesomoleculeset.get('YSize'))
    zdim = int(mesomoleculeset.get('ZSize'))
    
    for mesomolecule in mesomolecule_list:
        xcoords = []
        ycoords = []
        zcoords = []
        
        coords = mesomolecule.get('Coords')
        coords = coords.split(':')
        
        for bead in range(len(coords)):
            xyz = coords[bead].split(',')
            x = float(xyz[0])/xdim
            y = float(xyz[1])/ydim
            z = float(xyz[2])/zdim
            xcoords.append(x)
            ycoords.append(y)
            zcoords.append(z)

            prev = architecture[bead][2]

            x1 = int(ceil(x*100))
            x2 = int(ceil(xcoords[prev]*100))
            y1 = int(ceil(y*100))
            y2 = int(ceil(ycoords[prev]*100))
            z1 = int(ceil(z*100))
            z2 = int(ceil(zcoords[prev]*100))
            
            comparisons = [[min(x1, x2), max(x1, x2)],
                           [min(y1, y2), max(y1, y2)],
                           [min(z1, z2), max(z1, z2)]]
            
            for i in range(3):
                lower = comparisons[i][0]
                upper = comparisons[i][1]
                if upper-lower > 100+lower-upper:
                    for j in range(upper, lower+100):
                        if j > 99:
                            j -= 100
                        brokenbond_list[i][j] += 1
                else:
                    for j in range(lower, upper):
                        brokenbond_list[i][j] += 1

def topology_analyzer(topology, architecture=[], mainlevel=1, branchpos=0):
    topology_list = topology.split()
    nestlist = []
    nest = 0

    for each in topology_list:
        nest += each.count('(') + each.count('[') - each.count(')') - each.count(']')
        nestlist.append(nest)

    i=0
    while i<len(nestlist):
        first = len(architecture)
        
        if nestlist[i] == 0:
            for j in range(int(topology_list[i+1])):
                if mainlevel:
                    branchpos = first+1

                architecture.append([topology_list[i], mainlevel])
            i+=2
        else:
            block = topology_list[i]
            i+=1
            while nestlist[i] > 0:
                block += ' '+topology_list[i]
                i+=1
            block += ' '+topology_list[i]
            block = block[1:-1].strip()
            
            if topology_list[i][-1] == ')':
                block += (int(topology_list[i+1])-1)*(' ' + block)
                topology_analyzer(block, architecture, mainlevel, branchpos)
                i+=1
                
            else:
                temp = architecture[branchpos:]
                del architecture[branchpos:]
                topology_analyzer(block, architecture, 0, branchpos)
                architecture.extend(temp)
            i+=1

    return architecture

def bond_analyzer(architecture):
    lastmain = 0
    
    for i in range(len(architecture)):
        if architecture[i][1]:
            architecture[i].append(lastmain)
            lastmain = i
        else:
            architecture[i].append(lastbranch)
        lastbranch = i
    
    return architecture

def rebracket(brokenbond_list):
    displayrange = ''
    
    for axis in brokenbond_list:
        minbonds = axis[0]
        minbonds_index = 0
        i = 0
        
        while i < len(axis) and not minbonds == 0:
            if axis[i] < minbonds:
                minbonds = axis[i]
                minbonds_index = i
            i+=1
        
        if minbonds_index > 50:
            minbonds_index -= 100
        minbonds_index /= 100.
        
        displayrange += str(minbonds_index) + ',' + str(minbonds_index + 1) + ','

    return displayrange[:-1]

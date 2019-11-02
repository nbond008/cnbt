import xml.etree.cElementTree as ET # cElementTree deprecated in 3.3 - use xml.etree.ElementTree

def load(username, config_file):
    all_species_dict = {}
    boxsettings_defs = [1, 0, 0, '0,0,0', '#000000', 1]
    fieldsettings_defs = ['fieldval', 'Empty', 'Medium', '3', 'Lowest', '75%']
    mmolsettings_defs = [1, 1, 'Dot and Line', '3', '3', '0.1', '0.1']
    try:
        tree = ET.parse(config_file)
        root = tree.getroot()
        user = root.find('./User[@Name="'+username+'"]')

        if user == None:
            print('No saved default settings found for this user.')
            print('Using standard settings.\n')

        else:
            species_elements = [['Name',0], ['Visible',1], ['Solvent',1], ['Preset',0], ['RGB',0], ['Hex',0]]
            all_species = user.findall('./Species/Bead')
            for bead in all_species:
                elem_list = []
                for each in range(len(species_elements)):
                    elem = bead.find('./[@' + species_elements[each][0] + ']')
                    if not elem == None:
                        val = elem.get(species_elements[each][0])
                        if species_elements[each][1]:
                            val = int(val)
                        elem_list.append(val)

                if len(elem_list) == len(species_elements):
                    all_species_dict[elem_list[0]] = elem_list[1:]

            box_elements = [['Visible',1], ['CustomColor',1], ['HideSpecies',1], ['RGB',0], ['Hex',0], ['Rebracket',1]]
            for each in range(len(box_elements)):
                elem = user.find('./Box[@' + box_elements[each][0] + ']')
                if not elem == None:
                    val = elem.get(box_elements[each][0])
                    if box_elements[each][1]:
                        val = int(val)
                    boxsettings_defs[each] = val

            field_elements = ['ColorMode', 'DisplayStyle', 'DotQuality', 'DotSize', 'VolumeQuality', 'Transparency']
            for each in range(len(field_elements)):
                elem = user.find('./Field[@' + field_elements[each] + ']')
                if not elem == None:
                    fieldsettings_defs[each] = elem.get(field_elements[each])

            mmol_elements = [['ShowBeads',1], ['ShowBonds',1], ['DisplayStyle',0], ['DotSize',0], ['LineWidth',0], ['BallRadius',0], ['StickRadius',0]]
            for each in range(len(mmol_elements)):
                elem = user.find('./MesoMolecule[@' + mmol_elements[each][0] + ']')
                if not elem == None:
                    val = elem.get(mmol_elements[each][0])
                    if mmol_elements[each][1]:
                        val = int(val)
                    mmolsettings_defs[each] = val

    except Exception as ex:
        if type(ex).__name__ == 'IOError':
            print('No configuration file was found.')
        elif type(ex).__name__ == 'ParseError':
            print('An error occurred in processing the configuration file.')
        else:
            print('An unexpected error occurred when processing the configuration file: '+type(ex).__name__)

        print('Use the Save Defaults button to rebuild the file.')
        print('Using standard settings.\n')

    return all_species_dict, boxsettings_defs, fieldsettings_defs, mmolsettings_defs

def save(username, config_file, species_dict, boxsettings, fieldsettings, mmolsettings):
    try:
        tree = ET.parse(config_file)
        root = tree.getroot()
    except Exception as ex:
        if type(ex).__name__ == 'ParseError':
            print('Warning: The ColorBARS configuration file was found to be corrupted.')
            print('The file will be deleted and replaced with a new configuration file.')
            print('It is not recommended to edit the configuration file manually.\n')

        with open(config_file, 'w') as f: pass
        root = ET.Element('ColorBARS')
        tree = ET.ElementTree(root)

    user = root.find('./User[@Name="'+username+'"]')
    if user == None:
        user = ET.SubElement(root, 'User', Name = username)

    species = user.find('./Species')
    if species == None:
        species = ET.SubElement(user, 'Species')

    for each in species_dict:
        bead = species.find('./Bead[@Name="'+each+'"]')
        if bead == None:
            bead = ET.SubElement(species, 'Bead')
            bead.set('Name', each)
        bead.set('Visible', str(species_dict[each][0]))
        bead.set('Solvent', str(species_dict[each][1]))
        bead.set('Preset', species_dict[each][2])
        bead.set('RGB', species_dict[each][3])
        bead.set('Hex', species_dict[each][4])

    box = user.find('./Box')
    if box == None:
        box = ET.SubElement(user, 'Box')
    box.set('Visible', str(boxsettings[0]))
    box.set('CustomColor', str(boxsettings[1]))
    box.set('HideSpecies', str(boxsettings[2]))
    box.set('RGB', boxsettings[3])
    box.set('Hex', boxsettings[4])
    if boxsettings[5]:
        box.set('Rebracket', str(boxsettings[6]))

    field = user.find('./Field')
    if field == None:
        field = ET.SubElement(user, 'Field')
    field.set('ColorMode', fieldsettings[0])
    field.set('DisplayStyle', fieldsettings[1])
    field.set('DotQuality', fieldsettings[2])
    field.set('DotSize', fieldsettings[3])
    field.set('VolumeQuality', fieldsettings[4])
    field.set('Transparency', fieldsettings[5])

    mmol = user.find('./MesoMolecule')
    if mmol == None:
        mmol = ET.SubElement(user, 'MesoMolecule')
    mmol.set('ShowBeads', str(mmolsettings[0]))
    mmol.set('ShowBonds', str(mmolsettings[1]))
    mmol.set('DisplayStyle', mmolsettings[2])
    mmol.set('DotSize', mmolsettings[3])
    mmol.set('LineWidth', mmolsettings[4])
    mmol.set('BallRadius', mmolsettings[5])
    mmol.set('StickRadius', mmolsettings[6])

    tree.write(config_file)

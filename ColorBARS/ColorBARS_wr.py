# -*- coding: cp1252 -*-
from Tkinter import *
from tkFileDialog import askdirectory
from tkColorChooser import askcolor
import ttk
import ColorBARS_assemble_wr
from os.path import normpath

def getdir():
    path_choice = normpath(askdirectory(initialdir=path.get()))
    if not (path_choice == '.' or path_choice == path.get()):
        path.set(path_choice)
        detect_species()

def detect_species():
    del species_list[:]
    del mtd_list[:]
    plural = 's'
    species_dict.clear()
    print('Detecting species and building .mtd list from '+path.get()+'...')
    print('(Depending on your directory size, this may take a little while.)')
    raw_species_list, raw_mtd_list = ColorBARS_assemble_wr.species_finder(path.get())
    for each in raw_species_list:
        species_list.append(each)
    for each in raw_mtd_list:
        mtd_list.append(each)

    if not species_list == [] and not mtd_list == []:
        species_string = species_list[0]
        for each in species_list[1:]:
            species_string += ', '+each
        species.set(species_string)
        if len(mtd_list) == 1:
            plural = ''
        print('Species list complete with ' + str(len(mtd_list)) + ' .mtd file' + plural + ' found.\n')
    elif species_list == []:
        print('No parameter (.Dpd_par) files found.\n')
        species.set('')
    else:
        print('No results (.mtd) files found. Clicking the Apply Styles button will have no effect.')
        print('Species list cleared.\n')
        species.set('')

def manage_species():
    if not species.get() == '':
        del species_elem_list[:]
        del vis_elem_list[:]
        del preset_elem_list[:]
        del rgb_elem_list[:]
        del hex_elem_list[:]
        del style_list[:]
        
        root_specmgr = Toplevel()
        root_specmgr.focus_force()
        root_specmgr.grab_set()
        root_specmgr.title('Species Manager')
        root_specmgr.resizable(False,False)
        root_specmgr.protocol('WM_DELETE_WINDOW', lambda: close_specmgr(root_specmgr))

        # Species manager header <LANDMARK> <specmgr>
        specmgr = ttk.Frame(root_specmgr)
        specmgr.grid(column=0, row=0, pady=(1,0), sticky=NSEW)

        color_label = ttk.Label(specmgr, text='Species Color')
        color_label_sep = ttk.Separator(specmgr, orient='horizontal')

        color_label.grid(column=3, row=0, columnspan=3)
        color_label_sep.grid(column=3, row=1, columnspan=3, sticky=EW)

        name_label = ttk.Label(specmgr, text='Name')
        visibility_label = ttk.Label(specmgr, text='Visible')
        solvent_label = ttk.Label(specmgr, text='Solvent')
        preset_label = ttk.Label(specmgr, text='Preset')
        rgb_label = ttk.Label(specmgr, text='RGB')
        preview_label = ttk.Label(specmgr, text='Preview')

        name_label.grid(column=0, row=2)
        visibility_label.grid(column=1, row=2)
        solvent_label.grid(column=2, row=2)
        preset_label.grid(column=3, row=2)
        rgb_label.grid(column=4, row=2)
        preview_label.grid(column=5, row=2)
        
        header_sep = ttk.Separator(specmgr, orient='horizontal')
        header_sep.grid(column=0, row=3, columnspan=6, ipady=2, sticky=EW)

        # Species manager rows <LANDMARK> <rows>
        rows = []
        for i in range(len(species_list)):
            species_elem_list.append(StringVar(value=species_list[i]))
            vis_elem_list.append(IntVar(value=1))
            solv_elem_list.append(IntVar())
            preset_elem_list.append(StringVar(value='Default'))
            rgb_elem_list.append(StringVar(value='240,240,240'))
            hex_elem_list.append(StringVar(value='#f0f0f0'))
            style_list.append(species_list[i]+'.TLabel')

            each = species_list[i]
            if each in species_dict:
                vis = species_dict[each][0]
                solv = species_dict[each][1]
                preset = species_dict[each][2]
                rgb_val = species_dict[each][3]
                hex_val = species_dict[each][4]
                
                vis_elem_list[i].set(vis)
                solv_elem_list[i].set(solv)
                preset_elem_list[i].set(preset)
                rgb_elem_list[i].set(rgb_val)
                hex_elem_list[i].set(hex_val)
            
            style.configure(style_list[i], background=hex_elem_list[i].get())

            species_elem = ttk.Entry(specmgr, textvariable=species_elem_list[i], width=14, state='readonly')
            vis_elem = ttk.Checkbutton(specmgr, variable=vis_elem_list[i])
            solv_elem = ttk.Checkbutton(specmgr, variable=solv_elem_list[i])
            preset_elem = ttk.Combobox(specmgr, textvariable=preset_elem_list[i], values=(
                                                                                            'White',
                                                                                            'Pink',
                                                                                            'Red',
                                                                                            'Orange',
                                                                                            'Yellow',
                                                                                            'Green',
                                                                                            'Cyan',
                                                                                            'Blue',
                                                                                            'Purple',
                                                                                            'Black'
                                                                                            ), width=9, state='readonly')
            preset_elem.bind('<<ComboboxSelected>>', preset_select)
            rgb_elem = ttk.Entry(specmgr, textvariable=rgb_elem_list[i], width=11, state='readonly')
            preview_elem = ttk.Label(specmgr, width=14, borderwidth=1, relief='solid', style=style_list[i])
            
            rows.append([
                species_elem,
                vis_elem,
                solv_elem,
                preset_elem,
                rgb_elem,
                preview_elem
            ])
        
        for j in range(len(rows)):
            rows[j][0].grid(column=0, row=j+4, sticky=W)
            rows[j][1].grid(column=1, row=j+4)
            rows[j][2].grid(column=2, row=j+4)
            rows[j][3].grid(column=3, row=j+4, sticky=W)
            rows[j][4].grid(column=4, row=j+4, sticky=W)
            rows[j][5].grid(column=5, row=j+4, sticky=NSEW)

        for child in specmgr.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

        specmgr_sep = ttk.Separator(root_specmgr, orient='horizontal')
        specmgr_sep.grid(column=0, row=1, padx=4, pady=(4,0), sticky=EW)

        # Customize species color <LANDMARK> <customize>
        customize = ttk.Frame(root_specmgr, padding='4 2 4 4')
        customize.grid(column=0, row=2, sticky=NSEW)

        customize_species_label = ttk.Label(customize, text='Customize species color:')
        customize_species_entry = ttk.Combobox(customize, textvariable=customize_species, values=species_list, width=14, state='readonly')
        choose_color_button = ttk.Button(customize, text='Choose Color', width=12, command=lambda: choose_color(root_specmgr))

        customize_species_label.grid(column=0, row=0)
        customize_species_entry.grid(column=1, row=0)
        choose_color_button.grid(column=2, row=0)

        for child in customize.winfo_children(): child.grid_configure(padx=4, pady=(1,0))

        # Species manager options <LANDMARK> <specmgropts>
        specmgropts = ttk.Frame(root_specmgr, padding='4 2 4 4')
        specmgropts.grid(column=0, row=3, sticky=NSEW)

        allvis_button = ttk.Button(specmgropts, text='Set All Visible', width=12, command=set_all_vis)
        nonevis_button = ttk.Button(specmgropts, text='Set None Visible', width=15, command=set_none_vis)
        done_button = ttk.Button(specmgropts, text='Done', width=5, command=lambda: close_specmgr(root_specmgr))

        allvis_button.grid(column=0, row=1)
        nonevis_button.grid(column=1, row=1)
        done_button.grid(column=2, row=1)

        for child in specmgropts.winfo_children(): child.grid_configure(padx=4, pady=(1,2))
    
    elif path.get() == '':
        print('Select a directory first.\n')

    else:
        print('Selected directory contains no species.\n')

def preset_select(event):
    for i in range(len(species_list)):
        each = preset_elem_list[i].get()
        if not each == 'Custom':
            rgb_elem_list[i].set(rgb_list[color_list.index(each)])
            hex_elem_list[i].set(hex_list[color_list.index(each)])
            style.configure(style_list[i], background=hex_elem_list[i].get())

def choose_color(root_specmgr):
    if not customize_species.get() == '':
        color = askcolor('#40bfbf')
        try:
            root_specmgr.focus_force()
            root_specmgr.grab_set()
            if not color == (None,None):
                i = species_list.index(customize_species.get())
                rgb = str(color[0][0])+','+str(color[0][1])+','+str(color[0][2])
                rgb_elem_list[i].set(rgb)
                hex_elem_list[i].set(color[1])
                style.configure(style_list[i], background=hex_elem_list[i].get())
                if rgb in rgb_list:
                    preset_elem_list[i].set(color_list[rgb_list.index(rgb)])
                else:
                    preset_elem_list[i].set('Custom')
        except:
            print('Warning: The species manager was closed improperly. As a result, some settings were not saved.')
            print('To avoid this, make sure to close all color selection windows before closing the species manager.\n')
    else:
        print('Select a species first.\n')

def close_customize(root_customize):
    root_specmgr.focus_set()
    root_specmgr.grab_set()
    root_customize.destroy()

def set_all_vis():
    for i in range(len(species_list)):
        vis_elem_list[i].set(1)

def set_none_vis():
    for i in range(len(species_list)):
        vis_elem_list[i].set(0)

def close_specmgr(root_specmgr):
    species_dict.clear()
    customize_species.set('')
    for i in range(len(species_list)):
        species_dict[species_elem_list[i].get()] = [vis_elem_list[i].get(), solv_elem_list[i].get(), preset_elem_list[i].get(), rgb_elem_list[i].get(), hex_elem_list[i].get()]

    solvcount = 0
    for each in species_dict:
        solvcount += species_dict[each][1]

    if solvcount == 0:
        tryrebracket_check.config(state='disabled')
        tryrebracket.set(0)
        print('No species are marked as solvents. Rebracketing is disabled.')

    elif solvcount == len(species_dict):
        tryrebracket_check.config(state='disabled')
        tryrebracket.set(0)
        print('All species are marked as solvents. Rebracketing is disabled.')

    else:
        tryrebracket_check.config(state='normal')

    root_specmgr.destroy()

def get_box_color():
    color = askcolor()
    if not color == (None,None):
        customboxcolor.set(1)
        boxvis.set(1)
        hidespecies.set(1)
        boxcolorrgb.set(str(color[0][0])+','+str(color[0][1])+','+str(color[0][2]))
        boxcolorhex.set(color[1])
        style.configure('Mine.TLabel', background=boxcolorhex.get())

def dots_select(event):
    fielddispstyle.set('Dots')

def vol_select(event):
    fielddispstyle.set('Volume')

def dotsize_select(event):
    mmoldispstyle.set('Dot and Line')
    if int(dotsize2.get()) < int(linewidth.get()):
        linewidth.set(dotsize2.get())

def linewidth_select(event):
    mmoldispstyle.set('Dot and Line')
    if int(linewidth.get()) > int(dotsize2.get()):
        dotsize2.set(linewidth.get())

def ballsize_select(event):
    mmoldispstyle.set('Ball and Stick')
    if float(ballsize.get()) < float(stickradius.get()):
        stickradius.set(ballsize.get())

def stickradius_select(event):
    mmoldispstyle.set('Ball and Stick')
    if float(stickradius.get()) > float(ballsize.get()):
        ballsize.set(stickradius.get())

def toggler1():
    if customboxcolor.get():
        boxvis.set(1)
        hidespecies.set(1)

def toggler2():
    if hidespecies.get():
        customboxcolor.set(1)
        boxvis.set(1)

def apply_styles():
    if not species_dict == {}:

        # Settings list builder <LANDMARK> <builder>
        if fieldcolormode.get() == 'fieldval':
            if fielddispstyle.get() == 'Volume':
                ms_fieldcolormode = '4097'
            else:
                ms_fieldcolormode = '12289'
        else:
            ms_fieldcolormode = 'species'

        ColorBARS_assemble_wr.mtd_reader(
            [path.get(), species_dict],
            [boxvis.get(), customboxcolor.get(), hidespecies.get(), boxcolorrgb.get(), tryrebracket.get()],
            [ms_fieldcolormode, fielddispstyle.get(), dotqual_dict[dotqual.get()], dotsize.get(), volqual_dict[volqual.get()], transparency_dict[transparency.get()]],
            [showbeads.get(), showbonds.get(), mmoldispstyle.get(), dotsize2.get(), linewidth.get(), ballsize.get(), stickradius.get()],
            mtd_list
        )

        print('Done!\n')
        
    else:
        print('All fields are required.')
        print('Make sure that the species list has been built by opening the species manager.\n')

def manage_defaults():
    print('This wasn\'t high enough of a priority to do yet.\nCheck back later.\n')
    pass

def program_help():
    print('Regarding the "Customize box color" option:')
    print('Materials Studio is weird, so there\'s not actually a box color attribute in the .mtd file.')
    print('The box color is controlled by the last visible species that does not have a ShowBox="0" attribute.')
    print('Because of this, this option requires overriding the field settings of the last species in each .mtd file.')
    print('That may or may not actually be the last species in the species list, by the way - it\'s complicated.')
    print('Since the settings of the last species will be overridden, I\'ve included an option to hide that species.')
    print('It\'s definitely weird, but I hope this clears things up in the short term before I find a better explanation.\n')
    print('The rest of the Help menu isn\'t written yet.')
    print('Ask me if you have any other questions on the program usage.\n')

def about_me():
    if 'About' not in pwindows:
        root_about = Toplevel()
        pwindows['About'] = root_about
        root_about.focus_force()
        root_about.title('About ColorBARS')
        root_about.resizable(False,False)
        root_about.protocol('WM_DELETE_WINDOW', lambda: close_passive('About'))
        
        about = ttk.Frame(root_about)
        about.grid(column=0, row=0, pady=(1,0), sticky=NSEW)

        about_label = ttk.Label(about, text=\
    '''ColorBARS is a member of the BARS Suite, which was developed by Connor Callaway, Vivian Bond, and SeungMin Lee as a part of the CNBT Laboratory under Seung Soon Jang.

The BARS Suite is a series of programs intended to offer extended functionality and/or quality-of-life improvements to various modules in Materials Studio (Accelrys/BIOVIA) and some in-house procedures as well. The suite was named in reference to the original program written for this project, the Blends Analysis/Refinement Script (BARS), and the associated script preparation utility, BARStool. From there, names were chosen almost entirely for the purpose of puns.

ColorBARS offers rapid and automated processing of DPD results files (.mtd filetype) created through Materials Studio. This processing includes species-based field particle and mesomolecule coloration, species visibility controls, and DPD box rebracketing based on mesomolecule species density. For more information, see Help.

We intend for users of this suite to find enhanced productivity through either deeper insights provided by programs in this suite or automation of monotonous tasks. Thank you for using the BARS Suite!''', wraplength=475)
        about_label.grid(column=0, row=0)

        for child in about.winfo_children(): child.grid_configure(padx=8, pady=(4,8))
        
    else:
        pwindows['About'].focus_force()

def close_passive(pw):
    pwindows[pw].destroy()
    del pwindows[pw]

root_main = Tk()
root_main.title('ColorBARS')

path = StringVar()
species = StringVar()
species_list = []
species_dict = {}
mtd_list = []
boxvis = IntVar(value=1)
customboxcolor = IntVar()
hidespecies = IntVar()
boxcolorrgb = StringVar(value='0,0,0')
boxcolorhex = StringVar(value='#000000')
style = ttk.Style()
style.configure('Mine.TLabel', background=boxcolorhex.get())
tryrebracket = IntVar()
fieldcolormode = StringVar(value='fieldval')
fielddispstyle = StringVar(value='Empty')
dotqual = StringVar(value='Medium')

dotqual_dict = {
    'Lowest':   '1',
    'Low':      '2',
    'Medium':   '4',
    'High':     '6',
    'Highest':  '8'
}

dotsize = StringVar(value='3')
volqual = StringVar(value='Medium')

volqual_dict = {
    'Lowest':   '25',
    'Low':      '50',
    'Medium':   '100',
    'High':     '200',
    'Highest':  '400'
}

transparency = StringVar(value='25%')

transparency_dict = {
    '0%':   ',255',
    '25%':  ',191',
    '50%':  ',127',
    '75%':  ',64',
    '100%': ',0'
}

showbeads = IntVar(value=1)
showbonds = IntVar(value=1)
mmoldispstyle = StringVar(value='Dot and Line')
dotsize2 = StringVar(value='3')
linewidth = StringVar(value='3')
ballsize = StringVar(value='0.1')
stickradius = StringVar(value='0.1')
species_elem_list = []
vis_elem_list = []
solv_elem_list = []
preset_elem_list = []
rgb_elem_list = []
hex_elem_list = []
style_list = []
customize_species = StringVar(value='')

color_list = [
    'Default',
    'Black',
    'Blue',
    'Cyan',
    'Green',
    'Orange',
    'Pink',
    'Purple',
    'Red',
    'White',
    'Yellow'
]

rgb_list = [
    '240,240,240',
    '0,0,0',
    '0,0,255',
    '0,255,255',
    '0,255,0',
    '255,128,0',
    '255,0,255',
    '128,0,255',
    '255,0,0',
    '255,255,255',
    '255,255,0'
]

hex_list = [
    '#F0F0F0',
    '#000000',
    '#0000FF',
    '#00FFFF',
    '#00FF00',
    '#FF8000',
    '#FF00FF',
    '#8000FF',
    '#FF0000',
    '#FFFFFF',
    '#FFFF00'
]
pwindows={}

root_main.columnconfigure(0,weight=1)

# General settings section <LANDMARK> <generalsettings>
generalsettings = ttk.Frame(root_main, padding='4 5 4 4')
generalsettings.grid(column=0, row=0, sticky=NSEW)

path_label = ttk.Label(generalsettings, text='Parent directory:')
path_button = ttk.Button(generalsettings, text='Open', width=8, command=getdir)
path_entry = ttk.Entry(generalsettings, textvariable=path, state='readonly')
notice1_label = ttk.Label(generalsettings, text='(Should be the folder containing all associated DPD files.)')
species_label = ttk.Label(generalsettings, text='Species:')
species_button = ttk.Button(generalsettings, text='Manage', width=8, command=manage_species)
species_entry = ttk.Entry(generalsettings, textvariable=species, state='readonly')

path_label.grid(column=0, row=0, sticky=W)
path_button.grid(column=1, row=0, sticky=W)
path_entry.grid(column=2, row=0, sticky=EW)
notice1_label.grid(column=0, row=1, columnspan=3, sticky=W)
species_label.grid(column=0, row=2, sticky=W)
species_button.grid(column=1, row=2, sticky=W)
species_entry.grid(column=2, row=2, sticky=EW)

generalsettings.columnconfigure(2,weight=1)

for child in generalsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep1 = ttk.Separator(root_main, orient='horizontal')
sep1.grid(column=0, row=1, padx=4, pady=(3,0), sticky=EW)

# Box settings <LANDMARK> <boxsettings>
boxsettings = ttk.Frame(root_main, padding='4 4 4 4')
boxsettings.grid(column=0, row=2, sticky=NSEW)

box_label = ttk.Label(boxsettings, text='Box settings', font='"Segoe UI" 9 bold')
boxvis_check = ttk.Checkbutton(boxsettings, text='Show box', variable=boxvis)
customboxcolor_check = ttk.Checkbutton(boxsettings, text='Custom color', variable=customboxcolor, command=toggler1)
chooseboxcolor_button = ttk.Button(boxsettings, text='Choose box color', command=get_box_color)
hidespecies_check = ttk.Checkbutton(boxsettings, text='Hide modified field species', variable=hidespecies, command=toggler2)
boxrgb_label = ttk.Label(boxsettings, text='RGB:')
boxrgb_entry = ttk.Entry(boxsettings, textvariable=boxcolorrgb, width=11, state='readonly')
showcolor_label = ttk.Label(boxsettings, width=14, borderwidth=1, relief='solid', style='Mine.TLabel')
notice2_label = ttk.Label(boxsettings, text='(Custom box color modifies some settings. For more information, click Help.)')
tryrebracket_check = ttk.Checkbutton(boxsettings, text='Attempt box rebracketing', variable=tryrebracket)
tryrebracket_check.config(state='disabled')

box_label.grid(column=0, row=0, columnspan=2, sticky=W)
boxvis_check.grid(column=0, row=1, sticky=W)
customboxcolor_check.grid(column=1, row=1, sticky=W)
chooseboxcolor_button.grid(column=1,row=2, sticky=W)
hidespecies_check.grid(column=2, row=1, columnspan=3, sticky=W)
boxrgb_label.grid(column=2, row=2, sticky=E)
boxrgb_entry.grid(column=3, row=2, sticky=W)
showcolor_label.grid(column=4, row=2, sticky=NSEW)
notice2_label.grid(column=0, row=3, columnspan=6, sticky=W)
tryrebracket_check.grid(column=0, row=4, columnspan=2, sticky=W)

for child in boxsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep2 = ttk.Separator(root_main, orient='horizontal')
sep2.grid(column=0, row=3, padx=4, pady=(3,0), sticky=EW)

# Field settings <LANDMARK> <fieldsettings>
fieldsettings = ttk.Frame(root_main, padding='4 4 4 4')
fieldsettings.grid(column=0, row=4, sticky=NSEW)

field_label = ttk.Label(fieldsettings, text='Field settings', font='"Segoe UI" 9 bold')
fieldcolor_label = ttk.Label(fieldsettings, text='Color by:')
species_radio = ttk.Radiobutton(fieldsettings, text='Species', variable=fieldcolormode, value='species')
fieldval_radio = ttk.Radiobutton(fieldsettings, text='Field values', variable=fieldcolormode, value='fieldval')
fielddispstyle_label = ttk.Label(fieldsettings, text='Display style:')
empty_radio = ttk.Radiobutton(fieldsettings, text='Empty', variable=fielddispstyle, value='Empty')
dots_radio = ttk.Radiobutton(fieldsettings, text='Dots', variable=fielddispstyle, value='Dots')
dotqual_label = ttk.Label(fieldsettings, text='Quality:')
dotqual_menu = ttk.Combobox(fieldsettings, textvariable=dotqual, values=('Lowest','Low','Medium','High','Highest'), width=8, state='readonly')
dotqual_menu.bind('<<ComboboxSelected>>', dots_select)
dotsize_label = ttk.Label(fieldsettings, text='Dot size:')
dotsize_menu = ttk.Combobox(fieldsettings, textvariable=dotsize, values=('1','2','3','4','5','6','7','8','9'), width=8, state='readonly')
dotsize_menu.bind('<<ComboboxSelected>>', dots_select)
volume_radio = ttk.Radiobutton(fieldsettings, text='Volume', variable=fielddispstyle, value='Volume')
volqual_label = ttk.Label(fieldsettings, text='Quality:')
volqual_menu = ttk.Combobox(fieldsettings, textvariable=volqual, values=('Lowest','Low','Medium','High','Highest'), width=8, state='readonly')
volqual_menu.bind('<<ComboboxSelected>>', vol_select)
transparency_label = ttk.Label(fieldsettings, text='Transparency:')
transparency_menu = ttk.Combobox(fieldsettings, textvariable=transparency, values=('0%','25%','50%','75%','100%'), width=8, state='readonly')
transparency_menu.bind('<<ComboboxSelected>>', vol_select)

field_label.grid(column=0, row=0, columnspan=2, sticky=W)
fieldcolor_label.grid(column=0, row=1, sticky=W)
species_radio.grid(column=1, row=1, sticky=W)
fieldval_radio.grid(column=2, row=1, sticky=W)
fielddispstyle_label.grid(column=0, row=2, sticky=W)
empty_radio.grid(column=0, row=3, sticky=W)
dots_radio.grid(column=0, row=4, sticky=W)
dotqual_label.grid(column=1, row=4, sticky=E)
dotqual_menu.grid(column=2, row=4, sticky=W)
dotsize_label.grid(column=3, row=4, sticky=E)
dotsize_menu.grid(column=4, row=4, sticky=W)
volume_radio.grid(column=0, row=5, sticky=W)
volqual_label.grid(column=1, row=5, sticky=E)
volqual_menu.grid(column=2, row=5, sticky=W)
transparency_label.grid(column=3, row=5, sticky=E)
transparency_menu.grid(column=4, row=5, sticky=W)

for child in fieldsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep3 = ttk.Separator(root_main, orient='horizontal')
sep3.grid(column=0, row=5, padx=4, pady=(3,0), sticky=EW)

# Mesoscale molecules settings <LANDMARK> <mmolsettings>
mmolsettings = ttk.Frame(root_main, padding='4 4 4 4')
mmolsettings.grid(column=0, row=6, sticky=NSEW)

mmol_label = ttk.Label(mmolsettings, text='Mesoscale molecule settings', font='"Segoe UI" 9 bold')
showbeads_check = ttk.Checkbutton(mmolsettings, text='Show beads', variable=showbeads)
showbonds_check = ttk.Checkbutton(mmolsettings, text='Show bonds', variable=showbonds)
mmoldispstyle_label = ttk.Label(mmolsettings, text='Display style:')
dotline_radio = ttk.Radiobutton(mmolsettings, text='Dot and line', variable=mmoldispstyle, value='Dot and Line')
dotsize2_label = ttk.Label(mmolsettings, text='Dot size:')
dotsize2_menu = ttk.Combobox(mmolsettings, textvariable=dotsize2, values=('1','2','3','4','5','6','7','8','9'), width=8, state='readonly')
dotsize2_menu.bind('<<ComboboxSelected>>', dotsize_select)
linewidth_label = ttk.Label(mmolsettings, text='Line width:')
linewidth_menu = ttk.Combobox(mmolsettings, textvariable=linewidth, values=('1','2','3','4','5','6','7','8','9'), width=8, state='readonly')
linewidth_menu.bind('<<ComboboxSelected>>', linewidth_select)
ballstick_radio = ttk.Radiobutton(mmolsettings, text='Ball and stick', variable=mmoldispstyle, value='Ball and Stick')
ballsize_label = ttk.Label(mmolsettings, text='Ball radius:')
ballsize_menu = ttk.Combobox(mmolsettings, textvariable=ballsize, values=('0.05','0.08','0.1','0.12','0.15'), width=8, state='readonly')
ballsize_menu.bind('<<ComboboxSelected>>', ballsize_select)
stickradius_label = ttk.Label(mmolsettings, text='Stick radius:')
stickradius_menu = ttk.Combobox(mmolsettings, textvariable=stickradius, values=('0.05','0.08','0.1','0.12','0.15'), width=8, state='readonly')
stickradius_menu.bind('<<ComboboxSelected>>', stickradius_select)
notice3_label = ttk.Label(mmolsettings, text='(Ball and stick style is higher quality, but renders more slowly while viewing.)')

mmol_label.grid(column=0, row=0, columnspan=2, sticky=W)
showbeads_check.grid(column=0, row=1, sticky=W)
showbonds_check.grid(column=1, row=1, sticky=W)
mmoldispstyle_label.grid(column=0, row=2, columnspan=2, sticky=W)
dotline_radio.grid(column=0, row=3, sticky=W)
dotsize2_label.grid(column=1, row=3, sticky=E)
dotsize2_menu.grid(column=2, row=3, sticky=W)
linewidth_label.grid(column=3, row=3, sticky=E)
linewidth_menu.grid(column=4, row=3, sticky=W)
ballstick_radio.grid(column=0, row=4, sticky=W)
ballsize_label.grid(column=1, row=4, sticky=E)
ballsize_menu.grid(column=2, row=4, sticky=W)
stickradius_label.grid(column=3, row=4, sticky=E)
stickradius_menu.grid(column=4, row=4, sticky=W)
notice3_label.grid(column=0, row=5, columnspan=5, sticky=W)

for child in mmolsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep4 = ttk.Separator(root_main, orient='horizontal')
sep4.grid(column=0, row=7, padx=4, pady=(3,0), sticky=EW)

# End options <LANDMARK> <endoptions>
endoptions = ttk.Frame(root_main, padding='4 2 4 4')
endoptions.grid(column=0, row=8, sticky=NSEW)

apply_button = ttk.Button(endoptions, text='Apply styles', width=11, command=apply_styles)
config_button = ttk.Button(endoptions, text='Save defaults', width=12, command=manage_defaults)
help_button = ttk.Button(endoptions, text='Help', width=5, command=program_help)
about_button = ttk.Button(endoptions, text='About', width=6, command=about_me)
quit_button = ttk.Button(endoptions, text='Quit', width=5, command=root_main.destroy)

apply_button.grid(column=0, row=0)
config_button.grid(column=1, row=0)
help_button.grid(column=2, row=0)
about_button.grid(column=3, row=0)
quit_button.grid(column=4, row=0)

for child in endoptions.winfo_children(): child.grid_configure(padx=4, pady=(3,2))

grip = ttk.Sizegrip(root_main)
grip.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

root_main.update()
root_main.minsize(root_main.winfo_width(), root_main.winfo_height())
root_main.maxsize(3*root_main.winfo_width(), root_main.winfo_height())

root_main.mainloop()

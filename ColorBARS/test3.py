from Tkinter import *
from tkFileDialog import askdirectory
from tkColorChooser import askcolor
import ttk
import ColorBARS_assemble
from os.path import normpath

def getdir():
    path_choice = normpath(askdirectory(initialdir=path.get()))
    if not (path_choice == '.' or path_choice == path.get()):
        path.set(path_choice)
        detect_species()

def detect_species():
    del species_list[:]
    species_dict.clear()
    print('Building species list from '+path.get()+'...')
    for each in ColorBARS_assemble.species_finder(path.get()):
        species_list.append(each)
    if not species_list == []:
        species_string = species_list[0]
        for each in species_list[1:]:
            species_string += ', '+each
        print('Species list complete.\n')
        species.set(species_string)
    else:
        print('No species found.\n')
        species.set('')

def manage_species():
    if not species.get() == '':
        del species_elem_list[:]
        del fieldvis_elem_list[:]
        del mmolvis_elem_list[:]
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

        # Species manager header <LANDMARK>
        specmgr = ttk.Frame(root_specmgr)
        specmgr.grid(column=0, row=0, pady=(1,0), sticky=NSEW)

        visibility_label = ttk.Label(specmgr, text='Visibility')
        color_label = ttk.Label(specmgr, text='Species Color')
        visibility_label_sep = ttk.Separator(specmgr, orient='horizontal')
        color_label_sep = ttk.Separator(specmgr, orient='horizontal')

        visibility_label.grid(column=1, row=0, columnspan=2)
        color_label.grid(column=3, row=0, columnspan=3)
        visibility_label_sep.grid(column=1, row=1, columnspan=2, sticky=EW)
        color_label_sep.grid(column=3, row=1, columnspan=3, sticky=EW)

        name_label = ttk.Label(specmgr, text='Name')
        fieldvis_label = ttk.Label(specmgr, text='Field')
        mmolvis_label = ttk.Label(specmgr, text='Bead')
        preset_label = ttk.Label(specmgr, text='Preset')
        rgb_label = ttk.Label(specmgr, text='RGB')
        preview_label = ttk.Label(specmgr, text='Preview')

        name_label.grid(column=0, row=2)
        fieldvis_label.grid(column=1, row=2)
        mmolvis_label.grid(column=2, row=2)
        preset_label.grid(column=3, row=2)
        rgb_label.grid(column=4, row=2)
        preview_label.grid(column=5, row=2)
        
        header_sep = ttk.Separator(specmgr, orient='horizontal')
        header_sep.grid(column=0, row=3, columnspan=6, ipady=2, sticky=EW)

        # Species manager rows <LANDMARK>
        rows = []
        for i in range(len(species_list)):
            species_elem_list.append(StringVar(value=species_list[i]))
            fieldvis_elem_list.append(IntVar())
            mmolvis_elem_list.append(IntVar(value=1))
            preset_elem_list.append(StringVar(value='Default'))
            rgb_elem_list.append(StringVar(value='240,240,240'))
            hex_elem_list.append(StringVar(value='#f0f0f0'))
            style_list.append(species_list[i]+'.TLabel')

            each = species_list[i]
            if each in species_dict:
                fieldvis = species_dict[each][0]
                mmolvis = species_dict[each][1]
                preset = species_dict[each][2]
                rgb_val = species_dict[each][3]
                hex_val = species_dict[each][4]
                
                fieldvis_elem_list[i].set(fieldvis)
                mmolvis_elem_list[i].set(mmolvis)
                preset_elem_list[i].set(preset)
                rgb_elem_list[i].set(rgb_val)
                hex_elem_list[i].set(hex_val)
            
            style.configure(style_list[i], background=hex_elem_list[i].get())

            species_elem = ttk.Entry(specmgr, textvariable=species_elem_list[i], state='readonly')
            fieldvis_elem = ttk.Checkbutton(specmgr, variable=fieldvis_elem_list[i])
            mmolvis_elem = ttk.Checkbutton(specmgr, variable=mmolvis_elem_list[i])
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
            rgb_elem = ttk.Entry(specmgr, textvariable=rgb_elem_list[i], width=10, state='readonly')
            preview_elem = ttk.Label(specmgr, width=15, style=style_list[i]) # Revisit later to get border width working
            
            rows.append([
                species_elem,
                fieldvis_elem,
                mmolvis_elem,
                preset_elem,
                rgb_elem,
                preview_elem
            ])
        
        for row_number in range(len(rows)):
            for column_number, each in enumerate(rows[row_number]):
                each.grid(column=column_number, row=row_number+4, sticky=E)

        for child in specmgr.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

        specmgr_sep = ttk.Separator(root_specmgr, orient='horizontal')
        specmgr_sep.grid(column=0, row=1, padx=4, pady=(4,0), sticky=EW)

        # Customize species color <LANDMARK>
        customize = ttk.Frame(root_specmgr, padding='4 2 4 4')
        customize.grid(column=0, row=2, sticky=NSEW)

        customize_species_label = ttk.Label(customize, text='Customize species color:')
        customize_species_entry = ttk.Combobox(customize, textvariable=customize_species, values=species_list, state='readonly')
        choose_color_button = ttk.Button(customize, text='Choose Color', width=12, command=lambda: choose_color(root_specmgr))

        customize_species_label.grid(column=0, row=0)
        customize_species_entry.grid(column=1, row=0)
        choose_color_button.grid(column=2, row=0)

        for child in customize.winfo_children(): child.grid_configure(padx=4, pady=(1,0))

        # Species manager options <LANDMARK>
        specmgr_opts = ttk.Frame(root_specmgr, padding='4 2 4 4')
        specmgr_opts.grid(column=0, row=3, sticky=NSEW)

        allvis_button = ttk.Button(specmgr_opts, text='Set All Visible', width=12, command=set_all_vis)
        nonevis_button = ttk.Button(specmgr_opts, text='Set None Visible', width=15, command=set_none_vis)
        done_button = ttk.Button(specmgr_opts, text='Done', width=5, command=lambda: close_specmgr(root_specmgr))

        allvis_button.grid(column=0, row=1)
        nonevis_button.grid(column=1, row=1)
        done_button.grid(column=2, row=1)

        for child in specmgr_opts.winfo_children(): child.grid_configure(padx=4, pady=(1,2))
    
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
        color = askcolor()
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
    else:
        print('Specify a species first.\n')

def close_customize(root_customize):
    root_specmgr.focus_set()
    root_specmgr.grab_set()
    root_customize.destroy()

def set_all_vis():
    for i in range(len(species_list)):
        fieldvis_elem_list[i].set(1)
        mmolvis_elem_list[i].set(1)

def set_none_vis():
    for i in range(len(species_list)):
        fieldvis_elem_list[i].set(0)
        mmolvis_elem_list[i].set(0)

def close_specmgr(root_specmgr):
    species_dict.clear()
    showfield_sum = 0
    showfield.set(0)
    customize_species.set('')
    for i in range(len(species_list)):
        species_dict[species_elem_list[i].get()] = [fieldvis_elem_list[i].get(), mmolvis_elem_list[i].get(), preset_elem_list[i].get(), rgb_elem_list[i].get(), hex_elem_list[i].get()]
        showfield_sum += fieldvis_elem_list[i].get()
    if not showfield_sum == 0:
        showfield.set(1)
    root_specmgr.destroy()

def get_box_color():
    color = askcolor()
    if not color == (None,None):
        boxvis.set(1)
        fieldcolor.set('species')
        customboxcolor.set(1)
        boxcolorrgb.set(str(color[0][0])+','+str(color[0][1])+','+str(color[0][2]))
        boxcolorhex.set(color[1])
        style.configure('Mine.TLabel', background=boxcolorhex.get())

def dots_select(event):
    fielddispstyle.set('dots')

def vol_select(event):
    fielddispstyle.set('volume')

def dotsize_select(event):
    mmoldispstyle.set('dotline')
    if int(dotsize2.get()) < int(linesize.get()):
        linesize.set(dotsize2.get())

def linesize_select(event):
    mmoldispstyle.set('dotline')
    if int(linesize.get()) > int(dotsize2.get()):
        dotsize2.set(linesize.get())

def ballsize_select(event):
    mmoldispstyle.set('ballstick')
    if float(ballsize.get()) < float(sticksize.get()):
        sticksize.set(ballsize.get())

def sticksize_select(event):
    mmoldispstyle.set('ballstick')
    if float(sticksize.get()) > float(ballsize.get()):
        ballsize.set(sticksize.get())

def toggler():
    if customboxcolor.get():
        boxvis.set(1)
        fieldcolor.set('species')

def apply_styles():
##    ColorBARS_assemble.mtd_reader('C:\\Users\\conno\\Desktop\\testing2')
    if not species_dict == {}: # Add checks to make sure all fields are filled
        print(species_dict)
        print('')
##        ColorBARS_assemble.mtd_reader(path.get())
    else:
        print('All fields are required.')
        print('Make sure that the species list has been built by opening the species manager.\n')

def manage_defaults():
    print('This wasn\'t high enough of a priority to do yet.\nCheck back later.\n')
    pass

def program_help():
    print('Not written yet.\nAsk Connor if you have any questions on the program usage.\n')

def about_me():
    print('Not written yet...check back later.\nShouldn\'t you know this part already, though?')

root_main = Tk()
root_main.title('ColorBARS')

path = StringVar()
species = StringVar()
species_list = []
species_dict = {}

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

boxvis = IntVar(value=1)
fieldcolor = StringVar(value='fieldval')
customboxcolor = IntVar()
boxcolor = StringVar()
boxcolorrgb = StringVar(value='240,240,240')
boxcolorhex = StringVar(value='#F0F0F0')
style = ttk.Style()
style.configure('Mine.TLabel', background='#F0F0F0')
showfield = IntVar(value=0)
fielddispstyle = StringVar(value='dots')
dotqual = StringVar(value='Medium')
dotsize = StringVar(value='3')
volqual = StringVar(value='Medium')
transparency = StringVar(value='25%')
beadvis = IntVar(value=1)
bondvis = IntVar(value=1)
mmoldispstyle = StringVar(value='dotline')
dotsize2 = StringVar(value='3')
linesize = StringVar(value='3')
ballsize = StringVar(value='0.1')
sticksize = StringVar(value='0.1')
species_elem_list = []
fieldvis_elem_list = []
mmolvis_elem_list = []
preset_elem_list = []
rgb_elem_list = []
hex_elem_list = []
style_list = []
customize_species = StringVar(value='')

root_main.columnconfigure(0,weight=1)

# General section <LANDMARK>
general = ttk.Frame(root_main, padding='4 5 4 4')
general.grid(column=0, row=0, sticky=NSEW)

path_label = ttk.Label(general, text='Parent directory:')
path_button = ttk.Button(general, text='Open', width=8, command=getdir)
path_entry = ttk.Entry(general, textvariable=path, state='readonly')
notice1_label = ttk.Label(general, text='(The parent directory should be the folder containing the DPD parameter and results files.)')
species_label = ttk.Label(general, text='Species:')
species_button = ttk.Button(general, text='Manage', width=8, command=manage_species)
species_entry = ttk.Entry(general, textvariable=species, state='readonly')

path_label.grid(column=0, row=0, sticky=W)
path_button.grid(column=1, row=0, sticky=W)
path_entry.grid(column=2, row=0, sticky=EW)
notice1_label.grid(column=0, row=1, columnspan=3, sticky=W)
species_label.grid(column=0, row=2, sticky=W)
species_button.grid(column=1, row=2, sticky=W)
species_entry.grid(column=2, row=2, sticky=EW)

general.columnconfigure(2,weight=1)

for child in general.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep1 = ttk.Separator(root_main, orient='horizontal')
sep1.grid(column=0, row=1, padx=4, pady=(3,0), sticky=EW)

# Box settings <LANDMARK>
boxsettings = ttk.Frame(root_main, padding='4 4 4 4')
boxsettings.grid(column=0, row=2, sticky=NSEW)

boxvis_check = ttk.Checkbutton(boxsettings, text='Show box', variable=boxvis)
customboxcolor_check = ttk.Checkbutton(boxsettings, text='Custom box color', variable=customboxcolor, command=toggler)
chooseboxcolor_button = ttk.Button(boxsettings, text='Choose color', width=12, command=get_box_color)
boxrgb_label = ttk.Label(boxsettings, text='RGB:')
boxrgb_entry = ttk.Entry(boxsettings, textvariable=boxcolorrgb, width=11, state='readonly')
showcolor_label = ttk.Label(boxsettings, width=10, style='Mine.TLabel') # Revisit later to get border width working
notice2_label = ttk.Label(boxsettings, text='(Requires coloring by Species and will change the field color of the last visible species.)')

boxvis_check.grid(column=0, row=0, sticky=W)
customboxcolor_check.grid(column=1, row=0, sticky=W)
chooseboxcolor_button.grid(column=2,row=0,sticky=W)
boxrgb_label.grid(column=3, row=0, sticky=E)
boxrgb_entry.grid(column=4, row=0, sticky=W)
showcolor_label.grid(column=5, row=0, sticky=W)
notice2_label.grid(column=0, row=2, columnspan=6, sticky=W)

for child in boxsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep2 = ttk.Separator(root_main, orient='horizontal')
sep2.grid(column=0, row=3, padx=4, pady=(3,0), sticky=EW)

# Field settings <LANDMARK>
fieldsettings = ttk.Frame(root_main, padding='4 4 4 4')
fieldsettings.grid(column=0, row=4, sticky=NSEW)

field_label = ttk.Label(fieldsettings, text='Field settings')
showfield_check = ttk.Checkbutton(fieldsettings, text='Show field species', variable=showfield)
fieldcolor_label = ttk.Label(fieldsettings, text='Color by:')
species_radio = ttk.Radiobutton(fieldsettings, text='Species', variable=fieldcolor, value='species')
fieldval_radio = ttk.Radiobutton(fieldsettings, text='Field values', variable=fieldcolor, value='fieldval')
fielddispstyle_label = ttk.Label(fieldsettings, text='Display style:')
dots_radio = ttk.Radiobutton(fieldsettings, text='Dots', variable=fielddispstyle, value='dots')
dotqual_label = ttk.Label(fieldsettings, text='Quality:')
dotqual_menu = ttk.Combobox(fieldsettings, textvariable=dotqual, values=('Lowest','Low','Medium','High','Highest'), width=8, state='readonly')
dotqual_menu.bind('<<ComboboxSelected>>', dots_select)
dotsize_label = ttk.Label(fieldsettings, text='Dot size:')
dotsize_menu = ttk.Combobox(fieldsettings, textvariable=dotsize, values=('1','2','3','4','5','6','7','8','9'), width=8, state='readonly')
dotsize_menu.bind('<<ComboboxSelected>>', dots_select)
volume_radio = ttk.Radiobutton(fieldsettings, text='Volume', variable=fielddispstyle, value='volume')
volqual_label = ttk.Label(fieldsettings, text='Quality:')
volqual_menu = ttk.Combobox(fieldsettings, textvariable=volqual, values=('Lowest','Low','Medium','High','Highest'), width=8, state='readonly')
volqual_menu.bind('<<ComboboxSelected>>', vol_select)
transparency_label = ttk.Label(fieldsettings, text='Transparency:')
transparency_menu = ttk.Combobox(fieldsettings, textvariable=transparency, values=('0%','25%','50%','75%','100%'), width=8, state='readonly')
transparency_menu.bind('<<ComboboxSelected>>', vol_select)

field_label.grid(column=0, row=0, columnspan=2, sticky=W)
showfield_check.grid(column=0, row=1, sticky=W)
fieldcolor_label.grid(column=2, row=1, sticky=E)
species_radio.grid(column=3, row=1, sticky=W)
fieldval_radio.grid(column=4, row=1, sticky=W)
fielddispstyle_label.grid(column=0, row=2, sticky=W)
dots_radio.grid(column=0, row=3, sticky=W)
dotqual_label.grid(column=1, row=3, sticky=E)
dotqual_menu.grid(column=2, row=3, sticky=W)
dotsize_label.grid(column=3, row=3, sticky=E)
dotsize_menu.grid(column=4, row=3, sticky=W)
volume_radio.grid(column=0, row=4, sticky=W)
volqual_label.grid(column=1, row=4, sticky=E)
volqual_menu.grid(column=2, row=4, sticky=W)
transparency_label.grid(column=3, row=4, sticky=E)
transparency_menu.grid(column=4, row=4, sticky=W)

for child in fieldsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep3 = ttk.Separator(root_main, orient='horizontal')
sep3.grid(column=0, row=5, padx=4, pady=(3,0), sticky=EW)

# Mesoscale molecules settings <LANDMARK>
mmolsettings = ttk.Frame(root_main, padding='4 4 4 4')
mmolsettings.grid(column=0, row=6, sticky=NSEW)

mmol_label = ttk.Label(mmolsettings, text='Mesoscale molecule settings')
beadvis_check = ttk.Checkbutton(mmolsettings, text='Show beads', variable=beadvis)
bondvis_check = ttk.Checkbutton(mmolsettings, text='Show bonds', variable=bondvis)
mmoldispstyle_label = ttk.Label(mmolsettings, text='Display style:')
dotline_radio = ttk.Radiobutton(mmolsettings, text='Dot and line', variable=mmoldispstyle, value='dotline')
dotsize2_label = ttk.Label(mmolsettings, text='Dot size:')
dotsize2_menu = ttk.Combobox(mmolsettings, textvariable=dotsize2, values=('1','2','3','4','5','6','7','8','9'), width=8, state='readonly')
dotsize2_menu.bind('<<ComboboxSelected>>', dotsize_select)
linesize_label = ttk.Label(mmolsettings, text='Line size:')
linesize_menu = ttk.Combobox(mmolsettings, textvariable=linesize, values=('1','2','3','4','5','6','7','8','9'), width=8, state='readonly')
linesize_menu.bind('<<ComboboxSelected>>', linesize_select)
ballstick_radio = ttk.Radiobutton(mmolsettings, text='Ball and stick', variable=mmoldispstyle, value='ballstick')
ballsize_label = ttk.Label(mmolsettings, text='Ball size:')
ballsize_menu = ttk.Combobox(mmolsettings, textvariable=ballsize, values=('0.05','0.08','0.1','0.12','0.15'), width=8, state='readonly')
ballsize_menu.bind('<<ComboboxSelected>>', ballsize_select)
sticksize_label = ttk.Label(mmolsettings, text='Stick size:')
sticksize_menu = ttk.Combobox(mmolsettings, textvariable=sticksize, values=('0.05','0.08','0.1','0.12','0.15'), width=8, state='readonly')
sticksize_menu.bind('<<ComboboxSelected>>', sticksize_select)
notice3_label = ttk.Label(mmolsettings, text='(Ball and stick style is higher quality, but renders more slowly while viewing.)')

mmol_label.grid(column=0, row=0, columnspan=2, sticky=W)
beadvis_check.grid(column=0, row=1, sticky=W)
bondvis_check.grid(column=1, row=1, sticky=W)
mmoldispstyle_label.grid(column=0, row=2, columnspan=2, sticky=W)
dotline_radio.grid(column=0, row=3, sticky=W)
dotsize2_label.grid(column=1, row=3, sticky=E)
dotsize2_menu.grid(column=2, row=3, sticky=W)
linesize_label.grid(column=3, row=3, sticky=E)
linesize_menu.grid(column=4, row=3, sticky=W)
ballstick_radio.grid(column=0, row=4, sticky=W)
ballsize_label.grid(column=1, row=4, sticky=E)
ballsize_menu.grid(column=2, row=4, sticky=W)
sticksize_label.grid(column=3, row=4, sticky=E)
sticksize_menu.grid(column=4, row=4, sticky=W)
notice3_label.grid(column=0, row=5, columnspan=5, sticky=W)

for child in mmolsettings.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep4 = ttk.Separator(root_main, orient='horizontal')
sep4.grid(column=0, row=7, padx=4, pady=(3,0), sticky=EW)

# End options <LANDMARK>
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

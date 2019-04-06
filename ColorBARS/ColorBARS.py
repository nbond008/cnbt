from Tkinter import *
from tkFileDialog import askdirectory
from tkColorChooser import askcolor
import ttk
import ColorBARS_assemble

def getdir():
    path_choice = askdirectory(initialdir=path.get())
    if not path_choice == '':
        path.set(path_choice)
        print('Directory has been changed to '+path.get()+'.\n')

def getcolor():
    color = askcolor()
    if not color == (None,None):
        boxvis.set(1)
        fieldcolor.set('fieldcustom')
        customboxcolor.set(1)
        boxcolorrgb.set('RGB: '+str(color[0][0])+','+str(color[0][1])+','+str(color[0][2]))
        boxcolorhex.set(color[1])
        style = ttk.Style()
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

def toggler1():
    if customboxcolor.get():
        boxvis.set(1)
        fieldcolor.set('fieldcustom')

##def is_integer(val):
##    is_int = False
##    try:
##        if int(val)>=1 and int(val)<=9:
##            is_int = True
##    except:
##        pass
##    if not is_int:
##    return is_int

def manage_species():
    if not path.get() == '':
        print('Rebuilding species list...')
        species_list = ColorBARS_assemble.species_finder(path.get(), True)
        if not species_list == []:
            species_string = species_list[0]
            for spec in species_list[1:]:
                species_string += ', ' + spec
            print('Rebuilding complete.\n')
            species.set(species_string)
        else:
            print('No species found!\n')
            species.set('')
    else:
        print('Choose a directory first.\n')
        species.set('')

def apply_styles():
    pass

def manage_defaults():
    pass

def program_help():
    pass

def about_me():
    pass

root = Tk()
root.title('ColorBARS')
root.resizable(True,False)

path = StringVar()
species = StringVar()
boxvis = IntVar(value=1)
fieldcolor = StringVar(value='fieldval')
customboxcolor = IntVar()
boxcolorrgb = StringVar()
boxcolorhex = StringVar()
fielddispstyle = StringVar(value='empty')
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

# General section <LANDMARK>
general = ttk.Frame(root, padding='4 5 4 4')
general.grid(column=0, row=0, sticky=NSEW)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

path_label = ttk.Label(general, text='Parent directory:')
path_button = ttk.Button(general, text='Open', width=8, command=getdir)
path_entry = ttk.Entry(general, textvariable=path, width=50, state='readonly')
notice1_label = ttk.Label(general, text='(The parent directory should be the folder containing the DPD parameter and results files.)')
species_label = ttk.Label(general, text='Species:')
species_button = ttk.Button(general, text='Manage', width=8, command=manage_species)
species_entry = ttk.Entry(general, textvariable=species, width=50, state='readonly')

path_label.grid(column=0, row=0, sticky=W)
path_button.grid(column=1, row=0, sticky=W)
path_entry.grid(column=2, row=0, sticky=EW)
notice1_label.grid(column=0, row=1, columnspan=3, sticky=W)
species_label.grid(column=0, row=2, sticky=W)
species_button.grid(column=1, row=2, sticky=W)
species_entry.grid(column=2, row=2, sticky=EW)

general.columnconfigure(2,weight=1)

for child in general.winfo_children(): child.grid_configure(padx=4, pady=(0,2))

sep1 = ttk.Separator(root, orient='horizontal')
sep1.grid(column=0, row=1, padx=4, pady=(3,0), sticky=EW)

# Field settings section <LANDMARK>
fieldsettings = ttk.Frame(root, padding='4 4 4 4')
fieldsettings.grid(column=0, row=2, sticky=NSEW)

field_label = ttk.Label(fieldsettings, text='Field settings')
boxvis_check = ttk.Checkbutton(fieldsettings, text='Show box', variable=boxvis)
fieldcolor_label = ttk.Label(fieldsettings, text='Coloring:')
fieldcustom_radio = ttk.Radiobutton(fieldsettings, text='Custom', variable=fieldcolor, value='fieldcustom')
fieldval_radio = ttk.Radiobutton(fieldsettings, text='Field values', variable=fieldcolor, value='fieldval')
customboxcolor_check = ttk.Checkbutton(fieldsettings, text='Customize box color', variable=customboxcolor, command=toggler1)
chooseboxcolor_button = ttk.Button(fieldsettings, text='Choose color', width=12, command=getcolor)
rgb_entry = ttk.Entry(fieldsettings, textvariable=boxcolorrgb, width=15, state='readonly')
showcolor_label = ttk.Label(fieldsettings, style='Mine.TLabel') # Revisit later to get border width working
notice2_label = ttk.Label(fieldsettings, text='(Note: This setting requires coloring by Custom and will change the field color of the last visible species.)')
fielddispstyle_label = ttk.Label(fieldsettings, text='Display style:')
empty_radio = ttk.Radiobutton(fieldsettings, text='Empty', variable=fielddispstyle, value='empty')
dots_radio = ttk.Radiobutton(fieldsettings, text='Dots', variable=fielddispstyle, value='dots')
dotqual_label = ttk.Label(fieldsettings, text='Quality:')
dotqual_menu = ttk.Combobox(fieldsettings, textvariable=dotqual, values=('Lowest','Low','Medium','High','Highest'), state='readonly')
dotqual_menu.bind('<<ComboboxSelected>>', dots_select)
dotsize_label = ttk.Label(fieldsettings, text='Dot size:')

##entry_is_int = fieldsettings.register(is_integer)
##dotsize_menu = ttk.Entry(fieldsettings, textvariable=dotsize, validate='focusout', validatecommand=(entry_is_int,'%P'))    # Revisit this later to get validation working
dotsize_menu = ttk.Combobox(fieldsettings, textvariable=dotsize, values=('1','2','3','4','5','6','7','8','9'), state='readonly')
dotsize_menu.bind('<<ComboboxSelected>>', dots_select)

volume_radio = ttk.Radiobutton(fieldsettings, text='Volume', variable=fielddispstyle, value='volume')
volqual_label = ttk.Label(fieldsettings, text='Quality:')
volqual_menu = ttk.Combobox(fieldsettings, textvariable=volqual, values=('Lowest','Low','Medium','High','Highest'), state='readonly')
volqual_menu.bind('<<ComboboxSelected>>', vol_select)
transparency_label = ttk.Label(fieldsettings, text='Transparency:')

# Revisit the below line later to get slider bar working
transparency_menu = ttk.Combobox(fieldsettings, textvariable=transparency, values=('0%','25%','50%','75%','100%'), state='readonly')
transparency_menu.bind('<<ComboboxSelected>>', vol_select)

field_label.grid(column=0, row=0, columnspan=2, sticky=W)
boxvis_check.grid(column=0, row=1, ipadx=7, sticky=W)
fieldcolor_label.grid(column=2, row=1, sticky=E)
fieldcustom_radio.grid(column=3, row=1, sticky=W)
fieldval_radio.grid(column=4, row=1, sticky=W)
customboxcolor_check.grid(column=0, row=2, columnspan=2, sticky=W)
chooseboxcolor_button.grid(column=2,row=2,sticky=W)
rgb_entry.grid(column=3, row=2, sticky=W)
showcolor_label.grid(column=4, row=2, sticky=EW)
notice2_label.grid(column=0, row=3, columnspan=5, sticky=W)
fielddispstyle_label.grid(column=0, row=4, columnspan=2, sticky=W)
empty_radio.grid(column=0, row=5, sticky=W)
dots_radio.grid(column=0, row=6, sticky=W)
dotqual_label.grid(column=1, row=6, sticky=E)
dotqual_menu.grid(column=2, row=6, sticky=W)
dotsize_label.grid(column=3, row=6, sticky=E)
dotsize_menu.grid(column=4, row=6, sticky=W)
volume_radio.grid(column=0, row=7, sticky=W)
volqual_label.grid(column=1, row=7, sticky=E)
volqual_menu.grid(column=2, row=7, sticky=W)
transparency_label.grid(column=3, row=7, sticky=E)
transparency_menu.grid(column=4, row=7, sticky=W)

for child in fieldsettings.winfo_children(): child.grid_configure(padx=3, pady=(0,2))

sep2 = ttk.Separator(root, orient='horizontal')
sep2.grid(column=0, row=3, padx=4, pady=(3,0), sticky=EW)

# Mesoscale molecules settings section <LANDMARK>
mmolsettings = ttk.Frame(root, padding='4 4 4 4')
mmolsettings.grid(column=0, row=4, sticky=NSEW)

mmol_label = ttk.Label(mmolsettings, text='Mesoscale molecule settings')
beadvis_check = ttk.Checkbutton(mmolsettings, text='Show beads', variable=beadvis)
bondvis_check = ttk.Checkbutton(mmolsettings, text='Show bonds', variable=bondvis)
mmoldispstyle_label = ttk.Label(mmolsettings, text='Display style:')
dotline_radio = ttk.Radiobutton(mmolsettings, text='Dot and line', variable=mmoldispstyle, value='dotline')
dotsize2_label = ttk.Label(mmolsettings, text='Dot size:')
dotsize2_menu = ttk.Combobox(mmolsettings, textvariable=dotsize2, values=('1','2','3','4','5','6','7','8','9'), state='readonly')
dotsize2_menu.bind('<<ComboboxSelected>>', dotsize_select)
linesize_label = ttk.Label(mmolsettings, text='Line size:')
linesize_menu = ttk.Combobox(mmolsettings, textvariable=linesize, values=('1','2','3','4','5','6','7','8','9'), state='readonly')
linesize_menu.bind('<<ComboboxSelected>>', linesize_select)
ballstick_radio = ttk.Radiobutton(mmolsettings, text='Ball and stick', variable=mmoldispstyle, value='ballstick')
ballsize_label = ttk.Label(mmolsettings, text='Ball size:')
ballsize_menu = ttk.Combobox(mmolsettings, textvariable=ballsize, values=('0.05','0.08','0.1','0.12','0.15'), state='readonly')
ballsize_menu.bind('<<ComboboxSelected>>', ballsize_select)
sticksize_label = ttk.Label(mmolsettings, text='Stick size:')
sticksize_menu = ttk.Combobox(mmolsettings, textvariable=sticksize, values=('0.05','0.08','0.1','0.12','0.15'), state='readonly')
sticksize_menu.bind('<<ComboboxSelected>>', sticksize_select)
notice3_label = ttk.Label(mmolsettings, text='(Note: The ball and stick display style is higher quality, but renders more slowly while viewing.)')

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

for child in mmolsettings.winfo_children(): child.grid_configure(padx=3, pady=(0,2))

sep3 = ttk.Separator(root, orient='horizontal')
sep3.grid(column=0, row=5, padx=4, pady=(3,0), sticky=EW)

# End section <LANDMARK>
endsettings = ttk.Frame(root, padding='4 4 4 4')
endsettings.grid(column=0, row=6, sticky=NSEW)

apply_button = ttk.Button(endsettings, text='Apply styles', width=11, command=apply_styles)
config_button = ttk.Button(endsettings, text='Save defaults', width=12, command=manage_defaults)
help_button = ttk.Button(endsettings, text='Help', width=5, command=program_help)
about_button = ttk.Button(endsettings, text='About', width=6, command=about_me)
quit_button = ttk.Button(endsettings, text='Quit', width=5, command=root.destroy)

apply_button.grid(column=0, row=0)
config_button.grid(column=1, row=0)
help_button.grid(column=2, row=0)
about_button.grid(column=3, row=0)
quit_button.grid(column=4, row=0)

grip = ttk.Sizegrip(root)
grip.grid(row=6, sticky=SE)

for child in endsettings.winfo_children(): child.grid_configure(padx=2, pady=(3,2))

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()

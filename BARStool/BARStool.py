import Tkinter as tk
import tkFont
import tkFileDialog
import tkMessageBox
import ttk
import sys
import shutil
from os import chdir,mkdir
import getpass
user=getpass.getuser()
print("Hi, "+user+"!")
if user=='cnbt02':
    user=user+'_new'
localdir = 'C:/Users/%s/Documents/BARStool/' % user
configdir = '%sconfig.txt' % localdir

txtFile = open(configdir,"r")
config = txtFile.read()
p = config.split("\n")

paths = []
for each in p:
    paths.append(each.replace('\r', ''))

userLoc = paths.index(user)
txtFile.close()

print("Your current default directory is:\n%s\n") % paths[userLoc+1]

class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.localdir = 'C:/Users/%s/Documents/BARStool/' % user
        self.configdir = '%sconfig.txt' % localdir

    def create_widgets(self):
        self.prep_text_path   = tk.StringVar()
        self.prep_num_runs    = tk.IntVar()
        self.prep_text_m1     = tk.StringVar()
        self.prep_text_m2     = tk.StringVar()
        self.prep_text_ff     = tk.StringVar()
        self.prep_num_frames  = tk.StringVar()
        self.prep_temperature = tk.StringVar()
        self.prep_text_path.set(paths[userLoc+1])
        self.prep_num_frames.set(1000)
        self.prep_temperature.set(298)

        self.collect_source_path    = tk.StringVar()
        self.collect_dest_path      = tk.StringVar()
        self.collect_num_runs       = tk.IntVar()
        self.collect_text_m1        = tk.StringVar()
        self.collect_text_m2        = tk.StringVar()
        self.collect_check_std      = tk.IntVar()
        self.collect_check_out      = tk.IntVar()
        self.collect_check_settings = tk.IntVar()
        self.collect_check_BARS     = tk.IntVar()
        self.collect_source_path.set(paths[userLoc+1])

        self.prep_text_ff.set('Dreiding')
        self.collect_check_std.set(1)
        self.collect_check_out.set(1)

        barstool_style = ttk.Style()
        barstool_style.configure('My.TFrame', background = 'grey94')

        self.tabs = ttk.Notebook(self)

        frame_prepare = ttk.Frame(self.tabs, style = 'My.TFrame')
        frame_collect = ttk.Frame(self.tabs, style = 'My.TFrame')

        self.tabs.add(frame_prepare, text = 'Prepare')
        self.tabs.add(frame_collect, text = 'Collect')

        self.tabs.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)

        #Prepare tab

        self.prep_path_label = tk.Label(
            frame_prepare,
            text = 'Destination file path:'
        )

        self.prep_path_path = tk.Button(
            frame_prepare,
            text = 'Open',
            command = self.open_prep_path
        )

        self.prep_path_label.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_path_path.grid(row = 1, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.prep_path_box = tk.Entry(
            frame_prepare,
            textvariable = self.prep_text_path,
            width = 40
        )

        self.prep_path_box.grid(row = 1, column = 2, padx = 6, pady = 4)

        self.prep_path_label2 = tk.Label(
            frame_prepare,
            text = '(Should be the folder containing all the Blends runs.)'
        )

        self.prep_path_label2.grid(row = 2, column = 0, columnspan = 3, padx = 6, pady = 4, sticky = tk.W)

        self.prep_num_label = tk.Label(
            frame_prepare,
            text = 'Number of runs:'
        )

        self.prep_num_path = tk.Scale(
            frame_prepare,
            from_        = 1,
            to           = 10,
            orient       = tk.HORIZONTAL,
            length       = 200,
            variable     = self.prep_num_runs
        )

        self.prep_num_label.grid(row = 3, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_num_path.grid(row = 3, column = 1, columnspan = 2, padx = 0, pady = 4, sticky = tk.W)

        self.prep_m1_label = tk.Label(
            frame_prepare,
            text = 'Base molecule name:'
        )

        self.prep_m2_label = tk.Label(
            frame_prepare,
            text = 'Screen molecule name:'
        )

        self.prep_m1_box = tk.Entry(
            frame_prepare,
            textvariable = self.prep_text_m1,
            width = 16
        )

        self.prep_m2_box = tk.Entry(
            frame_prepare,
            textvariable = self.prep_text_m2,
            width = 16
        )

        self.prep_m1_label.grid(row = 4, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_m1_box.grid(row = 4, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.prep_m2_label.grid(row = 5, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_m2_box.grid(row = 5, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.prep_ff_label = tk.Label(
            frame_prepare,
            text = 'Forcefield:'
        )

        self.prep_ff_menu = tk.OptionMenu(
            frame_prepare,
            self.prep_text_ff,
            'Dreiding',
            'Dreiding_Dielectric_Const_78',
            'Universal'
        )

        self.prep_ff_label.grid(row = 6, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_ff_menu.grid(row = 6, column = 1, columnspan = 2, padx = 0, pady = 4, sticky = tk.W)

        self.prep_num_frames_label = tk.Label(
            frame_prepare,
            text = 'Number of frames:'
        )

        self.prep_num_frames_box = tk.Entry(
            frame_prepare,
            textvariable = self.prep_num_frames,
            width = 4
        )

        self.prep_num_frames_label.grid(row = 7, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_num_frames_box.grid(row = 7, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.prep_temperature_label = tk.Label(
            frame_prepare,
            text = 'Temperature:'
        )

        self.prep_temperature_box = tk.Entry(
            frame_prepare,
            textvariable = self.prep_temperature,
            width = 4
        )

        self.prep_temperature_label.grid(row = 8, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_temperature_box.grid(row = 8, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.prepare_button = tk.Button(
            frame_prepare,
            text    = 'Prepare',
            command = self.prepare_main
        )

        self.prepare_button.grid(row = 9, column = 0, padx = 0, pady = 15)

        self.quit_button1 = tk.Button(
            frame_prepare,
            text    = 'Quit',
            command = self.quit
        )

        self.quit_button1.grid(row = 9, column = 2, padx = 0, pady = 15)

        self.default_button1 = tk.Button(
            frame_prepare,
            text    = 'Change Default Directory',
            command = self.change_default
        )

        self.default_button1.grid(row = 9, column = 1, padx = 0, pady = 15)

        #Copy tab

        self.collect_source_path_label = tk.Label(
            frame_collect,
            text = 'Source file path:'
        )

        self.collect_source_path_path = tk.Button(
            frame_collect,
            text = 'Open',
            command = self.open_source_path
        )

        self.collect_source_path_label.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.collect_source_path_path.grid(row = 1, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.collect_source_path_box = tk.Entry(
            frame_collect,
            textvariable = self.collect_source_path,
            width = 40
        )

        self.collect_source_path_box.grid(row = 1, column = 2, padx = 6, pady = 4)

        self.collect_source_path_label2 = tk.Label(
            frame_collect,
            text = '(Should be the folder containing all the Blends runs.)'
        )

        self.collect_source_path_label2.grid(row = 2, column = 0, columnspan = 3, padx = 6, pady = 4, sticky = tk.W)

        self.collect_dest_path_label = tk.Label(
            frame_collect,
            text = 'Destination file path:'
        )

        self.collect_dest_path_path = tk.Button(
            frame_collect,
            text = 'Open',
            command = self.open_dest_path
        )

        self.collect_dest_path_label.grid(row = 3, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.collect_dest_path_path.grid(row = 3, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.collect_dest_path_box = tk.Entry(
            frame_collect,
            textvariable = self.collect_dest_path,
            width = 40
        )

        self.collect_dest_path_box.grid(row = 3, column = 2, padx = 6, pady = 4)

        self.collect_num_label = tk.Label(
            frame_collect,
            text = 'Number of runs:'
        )

        self.collect_num_path = tk.Scale(
            frame_collect,
            from_        = 1,
            to           = 10,
            orient       = tk.HORIZONTAL,
            length       = 200,
            variable     = self.collect_num_runs
        )

        self.collect_num_label.grid(row = 4, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.collect_num_path.grid(row = 4, column = 1, columnspan = 2, padx = 0, pady = 4, sticky = tk.W)

        self.collect_m1_label = tk.Label(
            frame_collect,
            text = 'Base molecule name:'
        )

        self.collect_m2_label = tk.Label(
            frame_collect,
            text = 'Screen molecule name:'
        )

        self.collect_m1_box = tk.Entry(
            frame_collect,
            textvariable = self.collect_text_m1,
            width = 16
        )

        self.collect_m2_box = tk.Entry(
            frame_collect,
            textvariable = self.collect_text_m2,
            width = 16
        )

        self.collect_m1_label.grid(row = 5, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.collect_m1_box.grid(row = 5, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.collect_m2_label.grid(row = 6, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.collect_m2_box.grid(row = 6, column = 1, padx = 0, pady = 4, sticky = tk.W)

        subframe_to_copy = tk.Frame(frame_collect)

        self.to_copy_label = tk.Label(
            subframe_to_copy,
            text = 'Files to copy:'
        )

        self.to_copy_label.grid(row = 0, column = 0, columnspan = 8, padx = 6, pady = 4, sticky = tk.W)

        self.to_copy_std_label = tk.Label(
            subframe_to_copy,
            text = '.std'
        )

        self.to_copy_std_box = tk.Checkbutton(
            subframe_to_copy,
            variable = self.collect_check_std
        )

        self.to_copy_out_label = tk.Label(
            subframe_to_copy,
            text = 'Results'
        )

        self.to_copy_out_box = tk.Checkbutton(
            subframe_to_copy,
            variable = self.collect_check_out
        )

        self.to_copy_settings_label = tk.Label(
            subframe_to_copy,
            text = 'Settings'
        )

        self.to_copy_settings_box = tk.Checkbutton(
            subframe_to_copy,
            variable = self.collect_check_settings
        )

        self.to_copy_BARS_label = tk.Label(
            subframe_to_copy,
            text = 'BARS.pl'
        )

        self.to_copy_BARS_box = tk.Checkbutton(
            subframe_to_copy,
            variable = self.collect_check_BARS
        )

        self.to_copy_std_label.grid(row = 1, column = 0, padx = 3, pady = 4, sticky = tk.W)
        self.to_copy_std_box.grid(row = 1, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_out_label.grid(row = 1, column = 2, padx = 3, pady = 4, sticky = tk.W)
        self.to_copy_out_box.grid(row = 1, column = 3, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_settings_label.grid(row = 1, column = 4, padx = 3, pady = 4, sticky = tk.W)
        self.to_copy_settings_box.grid(row = 1, column = 5, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_BARS_label.grid(row = 1, column = 6, padx = 3, pady = 4, sticky = tk.W)
        self.to_copy_BARS_box.grid(row = 1, column = 7, padx = 0, pady = 4, sticky = tk.W)

        subframe_to_copy.grid(row = 7, column = 0, columnspan = 3, padx = 3, pady = 4, sticky = tk.W)

        self.copy_button = tk.Button(
            frame_collect,
            text    = 'Copy',
            command = self.collect_main
        )

        self.copy_button.grid(row = 9, column = 0, padx = 0, pady = 8)

        self.quit_button2 = tk.Button(
            frame_collect,
            text    = 'Quit',
            command = self.quit
        )

        self.quit_button2.grid(row = 9, column = 2, padx = 0, pady = 8)

        self.default_button2 = tk.Button(
            frame_collect,
            text    = 'Change Default Directory',
            command = self.change_default
        )

        self.default_button2.grid(row = 9, column = 1, padx = 0, pady = 8)

    def open_prep_path(self):
        self.prep_text_path.set(tkFileDialog.askdirectory(initialdir = paths[userLoc+1]))
        self.collect_source_path.set(self.prep_text_path.get())

    def open_source_path(self):
        self.collect_source_path.set(tkFileDialog.askdirectory(initialdir = paths[userLoc+1]))

    def open_dest_path(self):
        self.collect_dest_path.set(tkFileDialog.askdirectory(initialdir = paths[userLoc+1]))

    def prepare_main(self):
        if (self.prep_text_path is None or self.prep_num_runs is None
                or self.prep_text_m1 is None or self.prep_text_m2 is None
                or self.prep_text_ff is None or self.prep_num_frames is None
                or self.prep_temperature is None) \
            or (self.prep_text_path.get() == '' or self.prep_text_m1.get() == ''
                or self.prep_text_m2.get() == '' or self.prep_text_ff.get() == ''
                or self.prep_num_frames.get() == '' or self.prep_temperature.get() == ''):

            tkMessageBox.showerror('BARStool', 'All inputs are required.')
            return

        print 'Preparing...'
##        bars_top    = open(localdir+'bars_top.txt', 'r')
##        bars_bottom = open(localdir+'bars_bottom.txt', 'r')
##        top    = bars_top.read()
##        bottom = bars_bottom.read()

        f = self.prep_text_path.get()
        pathchar = '/'

        path = ''
        for st in self.prep_text_path.get().split(pathchar)[1:len(self.prep_text_path.get().split(pathchar))]:
            path += pathchar + st
        path = 'C:%s/%s Blends Mixing' % (path, self.prep_text_m1.get())
        full = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' % (
            top,
            'my $dir = \'%s%sLowest Energies\';' % (path, pathchar),
            'my $monomer1 = "%s";' % self.prep_text_m1.get(),
            'my $monomer2 = "%s";' % self.prep_text_m2.get(),
            'my $forcefield = "%s";' % self.prep_text_ff.get(),
            'my $numframes = "%d";' % int(self.prep_num_frames.get()),
            'my $temperature = "%d";' % int(self.prep_temperature.get()),
            bottom
        )
        print '\nSaving to %s%sLowest Energies...' % (path, pathchar)

        try:
            bars = open('%s%sLowest Energies%sBARS.pl' % (path, pathchar, pathchar), 'w')
            bars.write(full)
        except IOError:
            print 'Path not found: %s%sLowest Energies' % (path, pathchar)

        if self.prep_num_runs.get() > 1:
            for run in range(2, self.prep_num_runs.get() + 1):
                full = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' % (
                    top,
                    'my $dir = \'%s (%d)%sLowest Energies\';' % (path, run, pathchar),
                    'my $monomer1 = "%s";' % self.prep_text_m1.get(),
                    'my $monomer2 = "%s";' % self.prep_text_m2.get(),
                    'my $forcefield = "%s";' % self.prep_text_ff.get(),
                    'my $numframes = "%d";' % int(self.prep_num_frames.get()),
                    'my $temperature = "%d";' % int(self.prep_temperature.get()),
                    bottom
                )

                print '\nSaving to %s (%d)%sLowest Energies...' % (path, run, pathchar)

                try:
                    bars = open('%s (%d)%sLowest Energies%sBARS.pl' % (path, run, pathchar, pathchar), 'w')
                    bars.write(full)
                except IOError:
                    print 'Path not found: %s (%d)%sLowest Energies' % (path, run, pathchar)

        print '\nDone!\n'

    def collect_main(self):
        if (self.collect_source_path is None or self.collect_dest_path is None
                or self.collect_num_runs is None or self.collect_text_m1 is None
                or self.collect_text_m2 is None) \
            or (self.collect_source_path.get() == '' or self.collect_dest_path.get() == ''
                or self.collect_text_m1.get() == '' or self.collect_text_m2.get() == ''):

            tkMessageBox.showerror('BARStool', 'All inputs are required.')
            return

        if self.collect_source_path.get() == self.collect_dest_path.get():
            tkMessageBox.showerror('BARStool', 'Source and destination cannot be the same.')
            return

        print 'Collecting...'

        pathchar = '/'
        hostFolder = '%s/%s' % (self.collect_dest_path.get(), self.collect_source_path.get().split(pathchar)[-1])
        try:
            mkdir(hostFolder)
        except OSError:
            print 'Directory %s already exists.' % hostFolder

        source_path = '%s%s%s Blends Mixing' % (self.collect_source_path.get(), pathchar, self.collect_text_m1.get())
        dest_path   = '%s%s%s Blends Mixing' % (hostFolder, pathchar, self.collect_text_m1.get())
        try:
            print 'Creating directory %s...' % dest_path
            mkdir(dest_path)
        except OSError:
            print 'Directory %s already exists.' % dest_path

        if self.collect_check_std.get():
            std_source = '%s%s%s.std' % (source_path, pathchar, self.collect_text_m1.get())
            std_dest   = '%s%s%s.std' % (dest_path, pathchar, self.collect_text_m1.get())

            try:
                print 'Copying %s to %s...\n' % (std_source, std_dest)
                shutil.copy(std_source, std_dest)
            except IOError:
                print 'Directory not found: %s' % std_source

        if self.collect_check_out.get():
            out_path = '%s%sLowest Energies' % (source_path, pathchar)
            print out_path

            outfile1_source = '%s%s%s %s.txt' % (out_path, pathchar, self.collect_text_m1.get(), self.collect_text_m1.get())
            outfile2_source = '%s%s%s %s.txt' % (out_path, pathchar, self.collect_text_m1.get(), self.collect_text_m2.get())
            outfile3_source = '%s%s%s %s.txt' % (out_path, pathchar, self.collect_text_m2.get(), self.collect_text_m2.get())

            outfile1_dest = '%s%s%s %s.txt' % (dest_path, pathchar, self.collect_text_m1.get(), self.collect_text_m1.get())
            outfile2_dest = '%s%s%s %s.txt' % (dest_path, pathchar, self.collect_text_m1.get(), self.collect_text_m2.get())
            outfile3_dest = '%s%s%s %s.txt' % (dest_path, pathchar, self.collect_text_m2.get(), self.collect_text_m2.get())

            try:
                print 'Copying %s to %s...\n' % (outfile1_source, outfile1_dest)
                shutil.copy(outfile1_source, outfile1_dest)
            except IOError:
                print 'Directory not found: %s' % outfile1_source

            try:
                print 'Copying %s to %s...\n' % (outfile2_source, outfile2_dest)
                shutil.copy(outfile2_source, outfile2_dest)
            except IOError:
                print 'Directory not found: %s' % outfile2_source

            try:
                print 'Copying %s to %s...\n' % (outfile3_source, outfile3_dest)
                shutil.copy(outfile3_source, outfile3_dest)
            except IOError:
                print 'Directory not found: %s' % outfile3_source

        if self.collect_check_settings.get():
            settings_source = '%s%s%s.txt' % (source_path, pathchar, self.collect_text_m1.get())
            settings_dest   = '%s%s%s.txt' % (dest_path, pathchar, self.collect_text_m1.get())

            try:
                print 'Copying %s to %s...\n' % (settings_source, settings_dest)
                shutil.copy(settings_source, settings_dest)
            except IOError:
                print 'Directory not found: %s' % settings_source

        if self.collect_check_BARS.get():
            BARS_source = '%s%sbars.pl' % (out_path, pathchar)
            BARS_dest   = '%s%sbars.pl' % (dest_path, pathchar)

            try:
                print 'Copying %s to %s...\n' % (BARS_source, BARS_dest)
                shutil.copy(BARS_source, BARS_dest)
            except IOError:
                print 'Directory not found: %s' % BARS_source

        if self.collect_num_runs.get() > 1:
            for run in range(2, self.collect_num_runs.get() + 1):

                source_path = '%s%s%s Blends Mixing (%d)' % (self.collect_source_path.get(), pathchar, self.collect_text_m1.get(), run)
                dest_path   = '%s%s%s Blends Mixing (%d)' % (hostFolder, pathchar, self.collect_text_m1.get(), run)
                try:
                    print 'Creating directory %s...' % dest_path
                    mkdir(dest_path)
                except OSError:
                    print 'Directory %s already exists.' % dest_path

                if self.collect_check_std.get():
                    std_source = '%s%s%s.std' % (source_path, pathchar, self.collect_text_m1.get())
                    std_dest   = '%s%s%s.std' % (dest_path, pathchar, self.collect_text_m1.get())

                    try:
                        print 'Copying %s to %s...\n' % (std_source, std_dest)
                        shutil.copy(std_source, std_dest)
                    except IOError:
                        print 'Directory not found: %s' % std_source

                if self.collect_check_out.get():
                    out_path = '%s%sLowest Energies' % (source_path, pathchar)
                    print out_path

                    outfile1_source = '%s%s%s %s.txt' % (out_path, pathchar, self.collect_text_m1.get(), self.collect_text_m1.get())
                    outfile2_source = '%s%s%s %s.txt' % (out_path, pathchar, self.collect_text_m1.get(), self.collect_text_m2.get())
                    outfile3_source = '%s%s%s %s.txt' % (out_path, pathchar, self.collect_text_m2.get(), self.collect_text_m2.get())

                    outfile1_dest = '%s%s%s %s.txt' % (dest_path, pathchar, self.collect_text_m1.get(), self.collect_text_m1.get())
                    outfile2_dest = '%s%s%s %s.txt' % (dest_path, pathchar, self.collect_text_m1.get(), self.collect_text_m2.get())
                    outfile3_dest = '%s%s%s %s.txt' % (dest_path, pathchar, self.collect_text_m2.get(), self.collect_text_m2.get())

                    try:
                        print 'Copying %s to %s...\n' % (outfile1_source, outfile1_dest)
                        shutil.copy(outfile1_source, outfile1_dest)
                    except IOError:
                        print 'Directory not found: %s' % outfile1_source

                    try:
                        print 'Copying %s to %s...\n' % (outfile2_source, outfile2_dest)
                        shutil.copy(outfile2_source, outfile2_dest)
                    except IOError:
                        print 'Directory not found: %s' % outfile2_source

                    try:
                        print 'Copying %s to %s...\n' % (outfile3_source, outfile3_dest)
                        shutil.copy(outfile3_source, outfile3_dest)
                    except IOError:
                        print 'Directory not found: %s' % outfile3_source

                if self.collect_check_settings.get():
                    settings_source = '%s%s%s.txt' % (source_path, pathchar, self.collect_text_m1.get())
                    settings_dest   = '%s%s%s.txt' % (dest_path, pathchar, self.collect_text_m1.get())

                    try:
                        print 'Copying %s to %s...\n' % (settings_source, settings_dest)
                        shutil.copy(settings_source, settings_dest)
                    except IOError:
                        print 'Directory not found: %s' % settings_source

                if self.collect_check_BARS.get():
                    BARS_source = '%s%sbars.pl' % (out_path, pathchar)
                    BARS_dest   = '%s%sbars.pl' % (dest_path, pathchar)

                    try:
                        print 'Copying %s to %s...\n' % (BARS_source, BARS_dest)
                        shutil.copy(BARS_source, BARS_dest)
                    except IOError:
                        print 'Directory not found: %s' % BARS_source

        print 'Done!'

    def change_default(self):
        ## This block will overwrite the default BARStool directory if the user selects
        ## the "Change default directory..." option
        newDefault = tkFileDialog.askdirectory(initialdir = paths[userLoc+1])
        if not newDefault == '':
            paths[userLoc+1] = newDefault
            txtFile = open(self.configdir,"w")
            for line in paths:
                txtFile.write(line+"\n")
            txtFile.close()
            self.prep_text_path.set(paths[userLoc+1])
            self.collect_source_path.set(paths[userLoc+1])
            print("Your new default directory is:\n"+paths[userLoc+1]+"\n")
        return;

top =\
'''###############################################################################################################
#                                                                                                             #
#                                888888b.         d8888 8888888b.   .d8888b.                                  #
#                                888  "88b       d88888 888   Y88b d88P  Y88b                                 #
#                                888  .88P      d88P888 888    888 Y88b.                                      #
#                                8888888K.     d88P 888 888   d88P  "Y888b.                                   #
#                                888  "Y88b   d88P  888 8888888P"      "Y88b.                                 #
#                                888    888  d88P   888 888 T88b         "888                                 #
#                                888   d88P d8888888888 888  T88b  Y88b  d88P                                 #
#                                8888888P" d88P     888 888   T88b  "Y8888P"                                  #
#                                                                                                             #
#                                      BLENDS ANALYSIS/REFINEMENT SCRIPT                                      #
#                                                                                                             #
#      This Perl script performs geometry optimization and Connolly volume measurements on each individual    #
#  fragment and pair of fragments in each frame of the .xtd trajectory files output by the Blends module. It  #
#  outputs three .txt files that can be used as inputs to the STX processing script.                          #
#                                                                                                             #
#      To use this script, copy it into the "Lowest energies" folder of the Blends run under consideration.   #
#  Provide the requested information in the "Required input parameters" block below. Note that the variables  #
#  $monomer1 and $monomer2 refer to the names of the files as they were input into Blends (i.e., the output   #
#  .xtd trajectory files from Forcite). The forcefields commonly used are:                                    #
#          (1) "Dreiding"                                                                                     #
#          (2) "Dreiding_Dielectric_Const_78.4"                                                               #
#          (3) "Universal"                                                                                    #
#  The same forcefield that was used in Forcite/Blends should be used here.                                   #
#                                                                                                             #
#      Principal credit for the development of this script goes to Parveen Sood, a now-graduated student of   #
#  CNBT Lab at the Georgia Institute of Technology under Seung Soon Jang. Additional credit goes to Nicholas  #
#  Bond, an undergraduate researcher in CNBT Lab, for extensive script functionality improvements.            #
#                                                                                                             #
#  Copyright 2016 CNBT Lab. All rights reserved. Please use only with permission. If you believe you were     #
#  sent this file in error, please delete it and contact the sender.                                          #
#                                                                                                             #
###############################################################################################################

# Required input parameters:'''

bottom =\
'''
# Optional: The naming convention of the output files can be customized:
my $outfile1 = "$dir/$monomer1 $monomer1.txt";
my $outfile2 = "$dir/$monomer1 $monomer2.txt";
my $outfile3 = "$dir/$monomer2 $monomer2.txt";

use strict;
use MaterialsScript qw(:all);
my $doc=$Documents{"$monomer1 $monomer1.xtd"};
my $trajectory = $Documents{"$monomer1 $monomer1.xtd"}->Trajectory;
my $fh;
for (my $i=1; $i<=1000; $i=$i+1){
    $trajectory->CurrentFrame = $i;
    my $copyDoc_Pair=$doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
    my $copyDoc_Frag_1=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
    my $copyDoc_Frag_2=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");
    my $Atom_Of_Frag_1 = $copyDoc_Frag_1->Atoms("Frag_1");
    my $fragment_1 = $Atom_Of_Frag_1->Fragment;
    my $Atom_Of_Frag_2 = $copyDoc_Frag_2->Atoms("Frag_2");
    my $fragment_2 = $Atom_Of_Frag_2->Fragment;
    $fragment_1->Delete;
    $fragment_2->Delete;
    my $Frag_2_Only=$copyDoc_Frag_1->SaveAs("./Frag_2_Only_Frame_$i.xsd");
    my $Frag_1_Only=$copyDoc_Frag_2->SaveAs("./Frag_1_Only_Frame_$i.xsd");

     my $forcite_Pair= Modules->Forcite;
     $forcite_Pair->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,
     WriteLevel => "Silent"]);

    my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair); #Settings is optional parameter for run function

    my $Etot_Pair=$copyDoc_Pair->PotentialEnergy;

    my $avField_Pair= Tools->AtomVolumesSurfaces->Connolly->Calculate($copyDoc_Pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Pair->IsVisible = "No";
    my $Iso_Surface_Pair=   $avField_Pair->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Pair=$Iso_Surface_Pair->EnclosedVolume;

     my $forcite_Frag_1= Modules->Forcite;
     $forcite_Frag_1->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);


    my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($Frag_1_Only); #Settings is optional parameter for run function


    my $Etot_Frag_1=$Frag_1_Only->PotentialEnergy;

    my $avField_Frag_1= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_1_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Frag_1->IsVisible = "No";
    my $Iso_Surface_Frag_1=   $avField_Frag_1->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_1=$Iso_Surface_Frag_1->EnclosedVolume;

     my $forcite_Frag_2= Modules->Forcite;
     $forcite_Frag_2->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);

    my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($Frag_2_Only); #Settings is optional parameter for run function

    #Extract the result: Need to write functionality to print it to a file
    my $Etot_Frag_2=$Frag_2_Only->PotentialEnergy;

    my $avField_Frag_2= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_2_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Frag_2->IsVisible = "No";
    my $Iso_Surface_Frag_2=   $avField_Frag_2->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_2=$Iso_Surface_Frag_2->EnclosedVolume;

  if ($i == 1) {
  open($fh, '>', $outfile1) or die "File not opened";

  printf $fh  "%%22s %%22s %%22s %%22s %%22s %%22s %%22s\\n", "E_Pair (kcal/mol),","E_Frag_1 (kcal/mol),","E_Frag_2 (kcal/mol),","Del_E (kcal/mol),","CV_Pair (A^3),","CV_Frag_1 (A^3),","CV_Frag_2 (A^3)";

    }

    my $Del_E=$Etot_Pair-($Etot_Frag_1+$Etot_Frag_2);
    printf $fh "%%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f, %22.5f, %22.5f\\n", $Etot_Pair,$Etot_Frag_1,$Etot_Frag_2,$Del_E,$Connolly_Vol_Pair,$Connolly_Vol_Frag_1,$Connolly_Vol_Frag_2;

    $copyDoc_Pair->Delete;
    $copyDoc_Frag_1->Delete;
    $copyDoc_Frag_2->Delete;
    $Frag_1_Only->Delete;
    $Frag_2_Only->Delete;
}

use strict;
use MaterialsScript qw(:all);
my $doc=$Documents{"$monomer1 $monomer2.xtd"};
my $trajectory = $Documents{"$monomer1 $monomer2.xtd"}->Trajectory;
my $fh;
for (my $i=1; $i<=1000; $i=$i+1){
    $trajectory->CurrentFrame = $i;
    my $copyDoc_Pair=$doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
    my $copyDoc_Frag_1=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
    my $copyDoc_Frag_2=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");
    my $Atom_Of_Frag_1 = $copyDoc_Frag_1->Atoms("Frag_1");
    my $fragment_1 = $Atom_Of_Frag_1->Fragment;
    my $Atom_Of_Frag_2 = $copyDoc_Frag_2->Atoms("Frag_2");
    my $fragment_2 = $Atom_Of_Frag_2->Fragment;
    $fragment_1->Delete;
    $fragment_2->Delete;
    my $Frag_2_Only=$copyDoc_Frag_1->SaveAs("./Frag_2_Only_Frame_$i.xsd");
    my $Frag_1_Only=$copyDoc_Frag_2->SaveAs("./Frag_1_Only_Frame_$i.xsd");

     my $forcite_Pair= Modules->Forcite;
     $forcite_Pair->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,
     WriteLevel => "Silent"]);

    my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair); #Settings is optional parameter for run function

    my $Etot_Pair=$copyDoc_Pair->PotentialEnergy;

    my $avField_Pair= Tools->AtomVolumesSurfaces->Connolly->Calculate($copyDoc_Pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Pair->IsVisible = "No";
    my $Iso_Surface_Pair=   $avField_Pair->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Pair=$Iso_Surface_Pair->EnclosedVolume;

     my $forcite_Frag_1= Modules->Forcite;
     $forcite_Frag_1->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);


    my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($Frag_1_Only); #Settings is optional parameter for run function


    my $Etot_Frag_1=$Frag_1_Only->PotentialEnergy;

    my $avField_Frag_1= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_1_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Frag_1->IsVisible = "No";
    my $Iso_Surface_Frag_1=   $avField_Frag_1->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_1=$Iso_Surface_Frag_1->EnclosedVolume;

     my $forcite_Frag_2= Modules->Forcite;
     $forcite_Frag_2->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);

    my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($Frag_2_Only); #Settings is optional parameter for run function

    #Extract the result: Need to write functionality to print it to a file
    my $Etot_Frag_2=$Frag_2_Only->PotentialEnergy;

    my $avField_Frag_2= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_2_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Frag_2->IsVisible = "No";
    my $Iso_Surface_Frag_2=   $avField_Frag_2->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_2=$Iso_Surface_Frag_2->EnclosedVolume;

  if ($i == 1) {
  open($fh, '>', $outfile2) or die "File not opened";

  printf $fh  "%%22s %%22s %%22s %%22s %%22s %%22s %%22s\\n", "E_Pair (kcal/mol),","E_Frag_1 (kcal/mol),","E_Frag_2 (kcal/mol),","Del_E (kcal/mol),","CV_Pair (A^3),","CV_Frag_1 (A^3),","CV_Frag_2 (A^3)";

    }

    my $Del_E=$Etot_Pair-($Etot_Frag_1+$Etot_Frag_2);
    printf $fh "%%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f\\n", $Etot_Pair,$Etot_Frag_1,$Etot_Frag_2,$Del_E,$Connolly_Vol_Pair,$Connolly_Vol_Frag_1,$Connolly_Vol_Frag_2;

    $copyDoc_Pair->Delete;
    $copyDoc_Frag_1->Delete;
    $copyDoc_Frag_2->Delete;
    $Frag_1_Only->Delete;
    $Frag_2_Only->Delete;
}

use strict;
use MaterialsScript qw(:all);
my $doc=$Documents{"$monomer2 $monomer2.xtd"};
my $trajectory = $Documents{"$monomer2 $monomer2.xtd"}->Trajectory;
my $fh;
for (my $i=1; $i<=1000; $i=$i+1){
    $trajectory->CurrentFrame = $i;
    my $copyDoc_Pair=$doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
    my $copyDoc_Frag_1=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
    my $copyDoc_Frag_2=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");
    my $Atom_Of_Frag_1 = $copyDoc_Frag_1->Atoms("Frag_1");
    my $fragment_1 = $Atom_Of_Frag_1->Fragment;
    my $Atom_Of_Frag_2 = $copyDoc_Frag_2->Atoms("Frag_2");
    my $fragment_2 = $Atom_Of_Frag_2->Fragment;
    $fragment_1->Delete;
    $fragment_2->Delete;
    my $Frag_2_Only=$copyDoc_Frag_1->SaveAs("./Frag_2_Only_Frame_$i.xsd");
    my $Frag_1_Only=$copyDoc_Frag_2->SaveAs("./Frag_1_Only_Frame_$i.xsd");

     my $forcite_Pair= Modules->Forcite;
     $forcite_Pair->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,
     WriteLevel => "Silent"]);

    my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair); #Settings is optional parameter for run function

    my $Etot_Pair=$copyDoc_Pair->PotentialEnergy;

    my $avField_Pair= Tools->AtomVolumesSurfaces->Connolly->Calculate($copyDoc_Pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Pair->IsVisible = "No";
    my $Iso_Surface_Pair=   $avField_Pair->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Pair=$Iso_Surface_Pair->EnclosedVolume;

     my $forcite_Frag_1= Modules->Forcite;
     $forcite_Frag_1->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);


    my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($Frag_1_Only); #Settings is optional parameter for run function


    my $Etot_Frag_1=$Frag_1_Only->PotentialEnergy;

    my $avField_Frag_1= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_1_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Frag_1->IsVisible = "No";
    my $Iso_Surface_Frag_1=   $avField_Frag_1->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_1=$Iso_Surface_Frag_1->EnclosedVolume;

     my $forcite_Frag_2= Modules->Forcite;
     $forcite_Frag_2->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);

    my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($Frag_2_Only); #Settings is optional parameter for run function

    #Extract the result: Need to write functionality to print it to a file
    my $Etot_Frag_2=$Frag_2_Only->PotentialEnergy;

    my $avField_Frag_2= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_2_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));

       $avField_Frag_2->IsVisible = "No";
    my $Iso_Surface_Frag_2=   $avField_Frag_2->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_2=$Iso_Surface_Frag_2->EnclosedVolume;

  if ($i == 1) {
  open($fh, '>', $outfile3) or die "File not opened";

  printf $fh  "%%22s %%22s %%22s %%22s %%22s %%22s %%22s\\n", "E_Pair (kcal/mol),","E_Frag_1 (kcal/mol),","E_Frag_2 (kcal/mol),","Del_E (kcal/mol),","CV_Pair (A^3),","CV_Frag_1 (A^3),","CV_Frag_2 (A^3)";

    }

    my $Del_E=$Etot_Pair-($Etot_Frag_1+$Etot_Frag_2);
    printf $fh "%%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f, %%22.5f\\n", $Etot_Pair,$Etot_Frag_1,$Etot_Frag_2,$Del_E,$Connolly_Vol_Pair,$Connolly_Vol_Frag_1,$Connolly_Vol_Frag_2;

    $copyDoc_Pair->Delete;
    $copyDoc_Frag_1->Delete;
    $copyDoc_Frag_2->Delete;
    $Frag_1_Only->Delete;
    $Frag_2_Only->Delete;
}'''

app = Application()
app.master.title('BARStool')
app.mainloop()

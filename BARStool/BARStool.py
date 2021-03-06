import Tkinter as tk
import tkFont
import tkFileDialog
import tkMessageBox
import ttk
from sys import platform
import shutil
from os import chdir, mkdir, path

import BARStool_assemble
from Config import Config

const = {
    'manage' : 'Manage...',
    'ffpath' : path.dirname('C:\Program Files (x86)\Accelrys\Materials Studio 5.0\share\Resources\Simulation\ClassicalEnergy\FORCEFIELDS\Standard')
}

FILEOPENOPTIONS = {
    'defaultextension' : '.off',
    'filetypes'        : [('All files', '*.*'), ('Force Field files', '*.off')]
}

class Application(tk.Frame):
    configdir = '%s/config.xml' % path.dirname(path.realpath(__file__))

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.prep_text_path   = tk.StringVar()
        self.prep_num_runs    = tk.IntVar()
        self.prep_text_m1     = tk.StringVar()
        self.prep_text_m2     = tk.StringVar()
        self.prep_text_ff     = tk.StringVar()
        self.prep_list_ff     = []
        self.prep_num_frames  = tk.StringVar()
        self.prep_temperature = tk.StringVar()

        self.collect_source_path    = tk.StringVar()
        self.collect_dest_path      = tk.StringVar()
        self.collect_num_runs       = tk.IntVar()
        self.collect_text_m1        = tk.StringVar()
        self.collect_text_m2        = tk.StringVar()
        self.collect_check_std      = tk.IntVar()
        self.collect_check_out      = tk.IntVar()
        self.collect_check_settings = tk.IntVar()
        self.collect_check_BARS     = tk.IntVar()

        self.label_text_path = tk.StringVar()
        self.label_num_runs  = tk.IntVar()
        self.label_text_m1   = tk.StringVar()
        self.label_text_m2   = tk.StringVar()

        self.set_defaults()

        barstool_style = ttk.Style()
        barstool_style.configure('My.TFrame', background = 'white')

        self.tabs = ttk.Notebook(self)

        frame_prepare = ttk.Frame(self.tabs, style = 'My.TFrame')
        frame_label   = ttk.Frame(self.tabs, style = 'My.TFrame')
        frame_collect = ttk.Frame(self.tabs, style = 'My.TFrame')

        self.tabs.add(frame_prepare, text = 'Prepare')
        self.tabs.add(frame_label  , text = 'Label')
        self.tabs.add(frame_collect, text = 'Collect')

        self.tabs.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)

        #Prepare tab <LANDMARK>

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
            *self.prep_list_ff,
            command = self.manage_ff_list
        )

        self.prep_ff_label.grid(row = 6, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.prep_ff_menu.grid(row = 6, column = 1, columnspan = 1, padx = 0, pady = 4, sticky = tk.EW)

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

        self.prepare_button.grid(row = 9, column = 0, padx = 6, pady = 25)

        self.default_button1 = tk.Button(
            frame_prepare,
            text    = 'Set All as Default',
            command = self.change_default_prep
        )

        self.default_button1.grid(row = 9, column = 1, padx = 6, pady = 10)

        self.quit_button1 = tk.Button(
            frame_prepare,
            text    = 'Quit',
            command = self.quit
        )

        self.quit_button1.grid(row = 9, column = 2, padx = 6, pady = 25)

        #Label tab <LANDMARK>

        self.label_path_label = tk.Label(
            frame_label,
            text = 'Destination file path:'
        )

        self.label_path_path = tk.Button(
            frame_label,
            text = 'Open',
            command = self.open_label_path
        )

        self.label_path_label.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.label_path_path.grid(row = 1, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.label_path_box = tk.Entry(
            frame_label,
            textvariable = self.label_text_path,
            width = 40
        )

        self.label_path_box.grid(row = 1, column = 2, padx = 6, pady = 4)

        self.label_path_label2 = tk.Label(
            frame_label,
            text = '(Should be the folder containing all the Blends runs.)'
        )

        self.label_path_label2.grid(row = 2, column = 0, columnspan = 3, padx = 6, pady = 4, sticky = tk.W)

        self.label_num_label = tk.Label(
            frame_label,
            text = 'Number of runs:'
        )

        self.label_num_path = tk.Scale(
            frame_label,
            from_        = 1,
            to           = 10,
            orient       = tk.HORIZONTAL,
            length       = 200,
            variable     = self.label_num_runs
        )

        self.label_num_label.grid(row = 3, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.label_num_path.grid(row = 3, column = 1, columnspan = 2, padx = 0, pady = 4, sticky = tk.W)

        self.label_m1_label = tk.Label(
            frame_label,
            text = 'Base molecule name:'
        )

        self.label_m2_label = tk.Label(
            frame_label,
            text = 'Screen molecule name:'
        )

        self.label_m1_box = tk.Entry(
            frame_label,
            textvariable = self.label_text_m1,
            width = 16
        )

        self.label_m2_box = tk.Entry(
            frame_label,
            textvariable = self.label_text_m2,
            width = 16
        )

        self.label_m1_label.grid(row = 4, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.label_m1_box.grid(row = 4, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.label_m2_label.grid(row = 5, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.label_m2_box.grid(row = 5, column = 1, padx = 0, pady = 4, sticky = tk.W)

        # self.label_bigspace = tk.Label(
        #     frame_label
        # )
        #
        # self.label_bigspace.grid(row = 2, column = 0, rowspan = 7, padx = 6, pady = 120, sticky = tk.W)

        self.label_button = tk.Button(
            frame_label,
            text    = 'Label',
            command = self.label_main
        )

        self.label_button.grid(row = 9, column = 0, padx = 6, pady = 25)

        self.default_button2 = tk.Button(
            frame_label,
            text    = 'Set All as Default',
            command = self.change_default_label
        )

        self.default_button2.grid(row = 9, column = 1, padx = 6, pady = 10)

        self.quit_button2 = tk.Button(
            frame_label,
            text    = 'Quit',
            command = self.quit
        )

        self.quit_button2.grid(row = 9, column = 2, padx = 6, pady = 25)

        self.unlabel_button = tk.Button(
            frame_label,
            text    = 'Unlabel',
            command = self.unlabel_main
        )

        self.unlabel_button.grid(row = 10, column = 0, padx = 6, pady = 25)

        #Copy tab <LANDMARK>

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

        self.to_copy_label.grid(row = 0, column = 0, columnspan = 8, padx = 0, pady = 4, sticky = tk.W)

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

        self.to_copy_std_label.grid(row = 1, column = 0, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_std_box.grid(row = 1, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_out_label.grid(row = 1, column = 2, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_out_box.grid(row = 1, column = 3, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_settings_label.grid(row = 1, column = 4, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_settings_box.grid(row = 1, column = 5, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_BARS_label.grid(row = 1, column = 6, padx = 0, pady = 4, sticky = tk.W)
        self.to_copy_BARS_box.grid(row = 1, column = 7, padx = 0, pady = 4, sticky = tk.W)

        subframe_to_copy.grid(row = 7, column = 0, columnspan = 3, padx = 0, pady = 4, sticky = tk.W)

        self.copy_button = tk.Button(
            frame_collect,
            text    = 'Copy',
            command = self.collect_main
        )

        self.copy_button.grid(row = 9, column = 0, padx = 6, pady = 25)

        self.default_button3 = tk.Button(
            frame_collect,
            text    = 'Set All as Defaults',
            command = self.change_default_copy
        )

        self.default_button3.grid(row = 9, column = 1, padx = 6, pady = 10)

        self.quit_button3 = tk.Button(
            frame_collect,
            text    = 'Quit',
            command = self.quit
        )

        self.quit_button3.grid(row = 9, column = 2, padx = 6, pady = 25)

    def open_prep_path(self):
        self.prep_text_path.set(tkFileDialog.askdirectory(initialdir = self.prep_text_path.get()))
        self.label_text_path.set(self.prep_text_path.get())
        self.collect_source_path.set(self.prep_text_path.get())

    def open_label_path(self):
        self.label_text_path.set(tkFileDialog.askdirectory(initialdir = self.label_text_path.get()))

    def open_source_path(self):
        self.collect_source_path.set(tkFileDialog.askdirectory(initialdir = self.collect_source_path.get()))

    def open_dest_path(self):
        self.collect_dest_path.set(tkFileDialog.askdirectory(initialdir = self.collect_dest_path.get()))

    #manage ff list <LANDMARK>
    def manage_ff_list(self, text):
        if text != const['manage']:
            return 0

        top = tk.Toplevel(self)
        mgr = FFManager(top)
        mgr.set_list_ff(self.prep_list_ff)

    def set_list_ff(self, list_ff):
        self.prep_list_ff = list_ff
        self.prep_list_ff.append(const['manage'])

        frame = self.prep_ff_menu.master

        self.prep_ff_menu.destroy()

        self.prep_ff_menu = tk.OptionMenu(
            frame,
            self.prep_text_ff,
            *self.prep_list_ff,
            command = self.manage_ff_list
        )

        self.prep_text_ff.set(self.prep_list_ff[0])

        self.prep_ff_menu.grid(row = 6, column = 1, columnspan = 1, padx = 0, pady = 4, sticky = tk.EW)

        self.change_default_prep()

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

        index   = 1
        success = True

        while success and (index < self.prep_num_runs.get() + 1):
            success = BARStool_assemble.BS_prepare(
                self.prep_text_path.get(),
                index,
                self.prep_text_m1.get(),
                self.prep_text_m2.get(),
                self.prep_text_ff.get(),
                int(self.prep_num_frames.get()),
                int(self.prep_temperature.get())
            )

            index += 1

        print '\nDone!\n'

    def label_main(self):
        if (self.label_text_path is None or self.label_num_runs is None
                or self.label_text_m1 is None or self.label_text_m2 is None) \
            or (self.label_text_path.get() == '' or self.label_text_m1.get() == ''
                or self.label_text_m2.get() == ''):

            tkMessageBox.showerror('BARStool', 'All inputs are required.')
            return

        print 'Labeling...'

        index   = 1
        success = True

        while success and (index < self.label_num_runs.get() + 1):
            success = BARStool_assemble.BS_label(
                self.label_text_path.get(),
                index,
                self.label_text_m1.get(),
                self.label_text_m2.get()
            )

            index += 1

        print '\nDone!\n'

    def unlabel_main(self):
        if (self.label_text_path is None or self.label_num_runs is None
                or self.label_text_m1 is None or self.label_text_m2 is None) \
            or (self.label_text_path.get() == '' or self.label_text_m1.get() == ''
                or self.label_text_m2.get() == ''):

            tkMessageBox.showerror('BARStool', 'All inputs are required.')
            return

        print 'Unlabeling...'

        index   = 1
        success = True

        while success and (index < self.label_num_runs.get() + 1):
            success = BARStool_assemble.BS_unlabel(
                self.label_text_path.get(),
                index,
                self.label_text_m1.get(),
                self.label_text_m2.get()
            )

            index += 1

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

        print 'Copying...'

        pathchar = '/'

        index = 1

        index   = 1
        success = True

        while success and (index < self.collect_num_runs.get() + 1):
            success = BARStool_assemble.BS_collect(
                self.collect_dest_path.get(),
                self.collect_source_path.get(),
                index,
                self.collect_text_m1.get(),
                self.collect_text_m2.get(),
                self.collect_check_std.get(),
                self.collect_check_out.get(),
                self.collect_check_settings.get(),
                self.collect_check_BARS.get()
            )

            index += 1

        print '\nDone!\n'

    def set_defaults(self):
        try:
            defaults = Config.read(self.configdir)
        except IOError:
            Config.init(self.configdir)
            defaults = dict()
        except KeyError:
            Config.init(self.configdir)
            defaults = dict()

        try:
            self.prep_text_path.set(defaults['prep_text_path'])
        except KeyError:
            self.prep_text_path.set('')
            pass

        try:
            self.prep_num_runs.set(defaults['prep_num_runs'])
        except KeyError:
            self.prep_num_runs.set(1)
            pass

        try:
            self.prep_text_m1.set(defaults['prep_text_m1'])
        except KeyError:
            self.prep_text_m1.set('')
            pass

        try:
            self.prep_text_m2.set(defaults['prep_text_m2'])
        except KeyError:
            self.prep_text_m2.set('')
            pass

        try:
            self.prep_text_ff.set(defaults['prep_text_ff'])
        except KeyError:
            self.prep_text_ff.set('')
            pass

        try:
            self.prep_list_ff = defaults['prep_list_ff']
        except KeyError:
            self.prep_list_ff = [
                'Dreiding',
                'Dreiding_Dielectric_Const_78.4',
                'Universal',
                'F3C',
                'F3C_Dielectric_Const_78.4'
            ]
            pass
        self.prep_list_ff.append(const['manage'])

        try:
            self.prep_num_frames.set(defaults['prep_num_frames'])
        except KeyError:
            self.prep_num_frames.set(1000)
            pass

        try:
            self.prep_temperature.set(defaults['prep_temperature'])
        except KeyError:
            self.prep_temperature.set(298)
            pass

        try:
            self.label_text_path.set(defaults['label_text_path'])
        except KeyError:
            self.label_text_path.set('')
            pass

        try:
            self.label_num_runs.set(defaults['label_num_runs'])
        except KeyError:
            self.label_num_runs.set(1)
            pass

        try:
            self.label_text_m1.set(defaults['label_text_m1'])
        except KeyError:
            self.label_text_m1.set('')
            pass

        try:
            self.label_text_m2.set(defaults['label_text_m2'])
        except KeyError:
            self.label_text_m2.set('')
            pass

        try:
            self.collect_source_path.set(defaults['collect_source_path'])
        except KeyError:
            self.collect_source_path.set('')
            pass

        try:
            self.collect_dest_path.set(defaults['collect_dest_path'])
        except KeyError:
            self.collect_dest_path.set('')
            pass

        try:
            self.collect_num_runs.set(defaults['collect_num_runs'])
        except KeyError:
            self.collect_num_runs.set(1)
            pass

        try:
            self.collect_text_m1.set(defaults['collect_text_m1'])
        except KeyError:
            self.collect_text_m1.set('')
            pass

        try:
            self.collect_text_m2.set(defaults['collect_text_m2'])
        except KeyError:
            self.collect_text_m2.set('')
            pass

        try:
            self.collect_check_std.set(defaults['collect_check_std'])
        except KeyError:
            self.collect_check_std.set(1)
            pass

        try:
            self.collect_check_out.set(defaults['collect_check_out'])
        except KeyError:
            self.collect_check_out.set(1)
            pass

        try:
            self.collect_check_settings.set(defaults['collect_check_settings'])
        except KeyError:
            self.collect_check_settings.set(0)
            pass

        try:
            self.collect_check_BARS.set(defaults['collect_check_BARS'])
        except KeyError:
            self.collect_check_BARS.set(0)
            pass

        return

    def change_default_prep(self):
        ## This block will overwrite the default BARStool directory if the user selects
        ## the "Set All as Defaults" option

        defaults = dict()

        defaults['prep_text_path']   = self.prep_text_path.get()
        defaults['prep_num_runs']    = self.prep_num_runs.get()
        defaults['prep_text_m1']     = self.prep_text_m1.get()
        defaults['prep_text_m2']     = self.prep_text_m2.get()
        defaults['prep_text_ff']     = self.prep_text_ff.get()
        defaults['prep_num_frames']  = self.prep_num_frames.get()
        defaults['prep_temperature'] = self.prep_temperature.get()

        defaults['prep_list_ff']     = []
        for each in self.prep_list_ff:
            if each != const['manage']:
                defaults['prep_list_ff'].append(each)

        try:
            Config.write_all(self.configdir, defaults)
        except IOError:
            Config.init(self.configdir)
            Config.write_all(self.configdir, defaults)

        print 'Prepare tab defaults saved.'
        return

    def change_default_label(self):
        ## This block will overwrite the default BARStool directory if the user selects
        ## the "Set All as Defaults" option

        defaults = dict()

        defaults['label_text_path'] = self.label_text_path.get()
        defaults['label_num_runs']  = self.label_num_runs.get()
        defaults['label_text_m1']   = self.label_text_m1.get()
        defaults['label_text_m2']   = self.label_text_m2.get()

        try:
            Config.write_all(self.configdir, defaults)
        except IOError:
            Config.init(self.configdir)
            Config.write_all(self.configdir, defaults)

        print 'Label tab defaults saved.'
        return

    def change_default_copy(self):
        ## This block will overwrite the default BARStool directory if the user selects
        ## the "Set All as Defaults" option

        defaults = dict()

        defaults['collect_source_path']    = self.collect_source_path.get()
        defaults['collect_dest_path']      = self.collect_dest_path.get()
        defaults['collect_num_runs']       = self.collect_num_runs.get()
        defaults['collect_text_m1']        = self.collect_text_m1.get()
        defaults['collect_text_m2']        = self.collect_text_m2.get()
        defaults['collect_check_std']      = self.collect_check_std.get()
        defaults['collect_check_out']      = self.collect_check_out.get()
        defaults['collect_check_settings'] = self.collect_check_settings.get()
        defaults['collect_check_BARS']     = self.collect_check_BARS.get()

        try:
            Config.write_all(self.configdir, defaults)
        except IOError:
            Config.init(self.configdir)
            Config.write_all(self.configdir, defaults)

        print 'Copy tab defaults saved.'
        return

class FFManager(tk.Frame):
    list_ff = []

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.list_ff = []

    def set_list_ff(self, list_ff):
        self.list_ff = list_ff[:-1]

        try:
            self.ff_listbox.delete(0, tk.END)
            for item in self.list_ff:
                self.ff_listbox.insert(tk.END, item)
        except AttributeError:
            print 'self.ff_listbox does not exist yet!'

    def create_widgets(self):
        barstool_style = ttk.Style()
        barstool_style.configure('My.TFrame', background = 'white')

        # self.selected = tk.StringVar()

        self.ff_label = tk.Label(
            self,
            text = 'Manage Force Fields...'
        )

        self.ff_label.grid(row = 0, column = 0, columnspan = 3, padx = 6, pady = 4, sticky = tk.W)

        self.ff_listbox = tk.Listbox(
            self
        )

        self.ff_listbox.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 4, sticky = tk.EW)

        self.add_button = tk.Button(
            self,
            text = 'Add',
            command = self.add_ff
        )

        self.add_button.grid(row = 2, column = 0, padx = 6, pady = 4, sticky = tk.W)

        self.remove_button = tk.Button(
            self,
            text = 'Remove',
            command = self.remove_ff
        )

        self.remove_button.grid(row = 2, column = 1, padx = 6, pady = 4, sticky = tk.W)

        self.submit_button = tk.Button(
            self,
            text = 'Done',
            command = self.submit_ff
        )

        self.submit_button.grid(row = 2, column = 2, padx = 6, pady = 4, sticky = tk.W)

    def add_ff(self):
        ff_new = ''

        try:
            ff_file = tkFileDialog.askopenfile(initialdir = const['ffpath'], **FILEOPENOPTIONS)
        except AttributeError:
            ff_file = tkFileDialog.askopenfile(**FILEOPENOPTIONS)

        try:
            ff_new = ff_file.name
            ff_file.close()
        except AttributeError:
            return 0
        except IOError:
            pass

        name = BARStool_assemble.BS_get_ff_name(ff_new)

        if name:
            self.list_ff.append(name)
            self.list_ff.append(const['manage'])
            self.set_list_ff(self.list_ff)
            print 'Added %s to the Force Field list.' % name
            return 1

        return 0


    def remove_ff(self):
        try:
            name = self.list_ff[map(int, self.ff_listbox.curselection())[0]]
            print 'Removed %s from the Force Field list.' % name
            del self.list_ff[map(int, self.ff_listbox.curselection())[0]]
            self.list_ff.append('')
            self.set_list_ff(self.list_ff)
        except IndexError:
            print 'No item selected to remove.'

    def submit_ff(self):
        self.master.master.set_list_ff(self.list_ff)
        self.master.destroy()

app = Application()
app.master.title('BARStool')
app.mainloop()

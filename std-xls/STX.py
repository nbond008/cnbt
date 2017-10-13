import Tkinter as tk
import tkFont
import tkFileDialog
import tkMessageBox
import std_to_xls
import xls_compile
import getpass
from os import path
from Config import Config

# user=getpass.getuser()
# print("Hi, "+user+"!")
# if user=='cnbt02':
#     user=user+'_new'
# localdir = '/Users/%s/cnbt/cnbt-repo/cnbt/std-xls/' % user
# configdir = '%sconfig.txt' % localdir
#
# txtFile = open(configdir,"r")
# config = txtFile.read()
# p = config.split("\n")
#
# paths = []
# for each in p:
#     paths.append(each.replace('\r', ''))
#
# userLoc = paths.index(user)
# txtFile.close()

# print("Your current default directory is:\n%s\n") % paths[userLoc+1]

class Application(tk.Frame):
    configdir = '%s/config.txt' % path.dirname(path.realpath(__file__))

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        #self.localdir = '/Users/%s/cnbt/cnbt-repo/cnbt/std-xls/' % 'spaghetti'
        #self.configdir = '%sconfig.txt' % self.localdir

    def create_widgets(self):
        self.text_path  = tk.StringVar()
        self.num_runs   = tk.IntVar()
        self.text_m1    = tk.StringVar()
        self.text_m2    = tk.StringVar()
        self.num_frames = tk.StringVar()
        self.check_cvn = tk.IntVar()
        self.check_dpn = tk.IntVar()
        self.text_dpn1 = tk.StringVar()
        self.text_dpn2 = tk.StringVar()
        self.text_mds  = tk.StringVar()
        self.check_mds = tk.IntVar()

        self.set_defaults()

        # self.text_path.set(paths[userLoc + 1])
        # self.num_frames.set(1000)
        # self.text_dpn1.set('1')
        # self.text_dpn2.set('1')
        # self.check_mds.set(1)

        self.path_label = tk.Label(
            self,
            text = 'Destination directory:'
        )

        self.path_path = tk.Button(
            self,
            text = 'Open',
            command = lambda: self.text_path.set(tkFileDialog.askdirectory())# initialdir = paths[userLoc + 1])

        )

        self.path_label.grid(row = 0, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.path_path.grid(row = 0, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.path_box = tk.Entry(
            self,
            textvariable = self.text_path,
            width = 40
        )

        self.path_box.grid(row = 0, column = 2, padx = 6, pady = 4)

        self.num_label = tk.Label(
            self,
            text = 'Number of runs:'
        )

        self.num_path = tk.Scale(
            self,
            from_        = 1,
            to           = 10,
            orient       = tk.HORIZONTAL,
            length       = 200,
            variable     = self.num_runs
        )

        self.num_label.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.num_path.grid(row = 1, column = 1, columnspan = 2, padx = 0, pady = 4, sticky = tk.W)

        self.m1_label = tk.Label(
            self,
            text = 'Base molecule name:'
        )

        self.m2_label = tk.Label(
            self,
            text = 'Screen molecule name:'
        )

        self.m1_box = tk.Entry(
            self,
            textvariable = self.text_m1,
            width = 16
        )

        self.m2_box = tk.Entry(
            self,
            textvariable = self.text_m2,
            width = 16
        )

        self.m1_label.grid(row = 2, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.m1_box.grid(row = 2, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.m2_label.grid(row = 3, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.m2_box.grid(row = 3, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.num_frames_label = tk.Label(
            self,
            text = 'Number of frames:'
        )

        self.num_frames_box = tk.Entry(
            self,
            textvariable = self.num_frames,
            width = 4
        )

        self.num_frames_label.grid(row = 4, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.num_frames_box.grid(row = 4, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.cvn_label = tk.Label(
            self,
            text = 'Using CVN?'
        )

        self.cvn_checkbox = tk.Checkbutton(
            self,
            variable = self.check_cvn,
            command  = self.set_cvn
        )

        self.cvn_label.grid(row = 5, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.cvn_checkbox.grid(row = 5, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.dpn_label = tk.Label(
            self,
            text = 'Using DPN?'
        )

        self.dpn_checkbox = tk.Checkbutton(
            self,
            variable = self.check_dpn,
            command  = self.set_dpn,
            state = tk.DISABLED
        )

        if self.check_cvn.get():
            self.dpn_checkbox.config(state = tk.NORMAL)

        self.dpn_label.grid(row = 6, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.dpn_checkbox.grid(row = 6, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.text_dpn1_label = tk.Label(
            self,
            text = 'n1'
        )

        self.text_dpn1_box = tk.Entry(
            self,
            textvariable = self.text_dpn1,
            width = 2,
            state = tk.DISABLED
        )

        self.text_dpn2_label = tk.Label(
            self,
            text = 'n2'
        )

        self.text_dpn2_box = tk.Entry(
            self,
            textvariable = self.text_dpn2,
            width = 2,
            state = tk.DISABLED
        )

        if self.check_dpn.get():
            self.text_dpn1_box.config(state = tk.NORMAL)
            self.text_dpn2_box.config(state = tk.NORMAL)

        self.text_dpn1_label.grid(row = 7, column = 0, padx = 12, pady = 4, sticky = tk.E)
        self.text_dpn1_box.grid(row = 7, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.text_dpn2_label.grid(row = 8, column = 0, padx = 12, pady = 4, sticky = tk.E)
        self.text_dpn2_box.grid(row = 8, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.mds_label = tk.Label(
            self,
            text = 'Create master data sheet?'
        )

        self.mds_checkbox = tk.Checkbutton(
            self,
            variable = self.check_mds
        )

        self.mds_label.grid(row = 9, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.mds_checkbox.grid(row = 9, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.run_button = tk.Button(
            self,
            text    = 'Run',
            command = self.run_main
        )

        self.default_button = tk.Button(
            self,
            text    = 'Set All as Defaults',
            command = self.change_default
        )

        self.quit_button = tk.Button(
            self,
            text    = 'Quit',
            command = self.quit
        )

        self.run_button.grid(row = 10, column = 0, padx = 6, pady = 25)
        self.default_button.grid(row = 10, column = 1, padx = 0, pady = 8)
        self.quit_button.grid(row = 10, column = 2, padx = 6, pady = 25)

    def set_cvn(self):
        if self.check_cvn.get():
            self.dpn_checkbox.config(state = tk.NORMAL)
            if self.check_dpn.get():
                self.text_dpn1_box.config(state = tk.NORMAL)
                self.text_dpn2_box.config(state = tk.NORMAL)
        else:
            self.dpn_checkbox.config(state = tk.DISABLED)
            self.text_dpn1_box.config(state = tk.DISABLED)
            self.text_dpn2_box.config(state = tk.DISABLED)

    def set_dpn(self):
        if self.check_cvn.get() and self.check_dpn.get():
            self.text_dpn1_box.config(state = tk.NORMAL)
            self.text_dpn2_box.config(state = tk.NORMAL)
        else:
            self.text_dpn1_box.config(state = tk.DISABLED)
            self.text_dpn2_box.config(state = tk.DISABLED)

    def default(self):
        return ''

    def run_main(self):

        if (self.text_path is None or self.text_m1 is None or self.text_m2 is None) \
            or (self.text_path.get() == '' or self.text_m1.get() == '' or self.text_m2.get() == ''):

            tkMessageBox.showerror('STX', 'All inputs are required.')
            return

        pathchar = '/'

        base = '%s%s%s Blends Mixing' % (self.text_path.get(), pathchar, self.text_m1.get())
        wb_paths = ['%s%s%s %s (1).xlsx' % (base, pathchar, self.text_m1.get(), self.text_m2.get())]

        if self.num_runs.get() > 1:
            print('\n------ Starting run 1 ------\n')

        std_to_xls.main(
            self.check_cvn.get(),
            '%s%s%s.std'    % (base, pathchar, self.text_m1.get()),
            '%s%s%s %s.txt' % (base, pathchar, self.text_m1.get(), self.text_m1.get()),
            '%s%s%s %s.txt' % (base, pathchar, self.text_m1.get(), self.text_m2.get()),
            '%s%s%s %s.txt' % (base, pathchar, self.text_m2.get(), self.text_m2.get()),
            wb_paths[0],
            int(self.text_dpn1.get()),
            int(self.text_dpn2.get()),
            int(self.num_frames.get())
        )

        if self.num_runs.get() > 1:
            print('\n\tCurrent progress: %d%%' % (100 / self.num_runs.get()))

            for i in range(2,self.num_runs.get() + 1):
                print('\n------ Starting run %d ------\n' % (i))
                try:
                    wb_paths.append('%s (%d)%s%s %s (%d).xlsx' % (base, i, pathchar, self.text_m1.get(), self.text_m2.get(), i))

                    std_to_xls.main(
                        self.check_cvn.get(),
                        '%s (%d)%s%s.std'    % (base, i, pathchar, self.text_m1.get()),
                        '%s (%d)%s%s %s.txt' % (base, i, pathchar, self.text_m1.get(), self.text_m1.get()),
                        '%s (%d)%s%s %s.txt' % (base, i, pathchar, self.text_m1.get(), self.text_m2.get()),
                        '%s (%d)%s%s %s.txt' % (base, i, pathchar, self.text_m2.get(), self.text_m2.get()),
                        wb_paths[i - 1],
                        int(self.text_dpn1.get()),
                        int(self.text_dpn2.get())
                    )

                    if i < self.num_runs.get():
                        print('\n\tCurrent progress: %d%%' % (i * (100 / self.num_runs.get())))

                except IOError:
                    tkMessageBox.showerror(
                        'STX',
                        'Invalid path: %s (%d)' % (base, i)
                    )

            print('\n\tCurrent progress: 100%')

            if self.check_mds.get():
                print('\n------ Master Data Sheet ------\n')

                xls_compile.main(
                    self.check_cvn.get(),
                    wb_paths,
                    '%s%s%s %s.xlsx' % (base, pathchar, self.text_m1.get(), self.text_m2.get()),
                    pathchar
                )

        print('\nDone!\n')

    def set_defaults(self):
        try:
            defaults = Config.read(self.configdir)
        except IOError:
            Config.init(self.configdir)
            defaults = dict([])

        try:
            self.text_path.set(defaults['text_path'])
        except KeyError:
            self.text_path.set('')
            pass

        try:
            self.num_runs.set(defaults['num_runs'])
        except KeyError:
            self.num_runs.set('')
            pass

        try:
            self.check_cvn.set(defaults['check_cvn'])
        except KeyError:
            self.check_cvn.set(0)
            pass

        try:
            self.check_dpn.set(defaults['check_dpn'])
        except KeyError:
            self.check_dpn.set(0)
            pass

        try:
            self.text_m1.set(defaults['text_m1'])
        except KeyError:
            self.text_m1.set('')
            pass

        try:
            self.text_m2.set(defaults['text_m2'])
        except KeyError:
            self.text_m2.set('')
            pass

        try:
            self.num_frames.set(defaults['num_frames'])
        except KeyError:
            self.num_frames.set('')
            pass

        try:
            self.text_dpn1.set(defaults['text_dpn1'])
        except KeyError:
            self.text_dpn1.set('1')
            pass

        try:
            self.text_dpn2.set(defaults['text_dpn2'])
        except KeyError:
            self.text_dpn2.set('1')
            pass

        try:
            self.text_mds.set(defaults['text_mds'])
        except KeyError:
            self.text_mds.set('')
            pass

        try:
            self.check_mds.set(defaults['check_mds'])
        except KeyError:
            self.check_mds.set(1)
            pass

        #self.set_cvn()
        #self.set_dpn()

        return

    def change_default(self):
        defaults = dict()

        defaults['text_path']  = self.text_path.get()
        defaults['num_runs']   = self.num_runs.get()
        defaults['text_m1']    = self.text_m1.get()
        defaults['text_m2']    = self.text_m2.get()
        defaults['num_frames'] = self.num_frames.get()
        defaults['check_cvn']  = self.check_cvn.get()
        defaults['check_dpn']  = self.check_dpn.get()
        defaults['text_dpn1']  = self.text_dpn1.get()
        defaults['text_dpn2']  = self.text_dpn2.get()
        defaults['text_mds']   = self.text_mds.get()
        defaults['check_mds']  = self.check_mds.get()

        try:
            Config.write_all(self.configdir, defaults)
        except IOError:
            Config.init(self.configdir)
            Config.write_all(self.configdir, defaults)

        print 'Defaults saved.'

        return

app = Application()
app.master.title('STD to XLSX')
app.mainloop()

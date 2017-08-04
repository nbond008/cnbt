import Tkinter as tk
import tkFont
import tkFileDialog
import tkMessageBox
import std_to_xls
import xls_compile
import getpass

user=getpass.getuser()
print("Hi, "+user+"!")
if user=='cnbt02':
    user=user+'_new'
localdir = '/Users/%s/cnbt/cnbt-repo/cnbt/std-xls/' % user
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
        self.localdir = '/Users/%s/cnbt/cnbt-repo/cnbt/std-xls/' % user
        self.configdir = '%sconfig.txt' % self.localdir

    def create_widgets(self):
        self.text_path  = tk.StringVar()
        self.num_runs   = tk.IntVar()
        self.text_m1    = tk.StringVar()
        self.text_m2    = tk.StringVar()
        self.num_frames = tk.StringVar()

        self.check_cvn = tk.IntVar()

        self.check_dpm = tk.IntVar()
        self.text_dpm1 = tk.StringVar()
        self.text_dpm2 = tk.StringVar()

        self.text_mds  = tk.StringVar()
        self.check_mds = tk.IntVar()

        self.text_path.set(paths[userLoc + 1])
        self.num_frames.set(1000)
        self.text_dpm1.set('1')
        self.text_dpm2.set('1')
        self.check_mds.set(1)

        self.path_label = tk.Label(
            self,
            text = 'Destination directory:'
        )

        self.path_path = tk.Button(
            self,
            text = 'Open',
            command = lambda: self.text_path.set(tkFileDialog.askdirectory(initialdir = paths[userLoc + 1]))

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

        self.dpm_label = tk.Label(
            self,
            text = 'Using DPM?'
        )

        self.dpm_checkbox = tk.Checkbutton(
            self,
            variable = self.check_dpm,
            command  = self.set_dpm,
            state = tk.DISABLED
        )

        self.dpm_label.grid(row = 6, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.dpm_checkbox.grid(row = 6, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.text_dpm1_label = tk.Label(
            self,
            text = 'n1'
        )

        self.text_dpm1_box = tk.Entry(
            self,
            textvariable = self.text_dpm1,
            width = 2,
            state = tk.DISABLED
        )

        self.text_dpm2_label = tk.Label(
            self,
            text = 'n2'
        )

        self.text_dpm2_box = tk.Entry(
            self,
            textvariable = self.text_dpm2,
            width = 2,
            state = tk.DISABLED
        )

        self.text_dpm1_label.grid(row = 7, column = 0, padx = 12, pady = 4, sticky = tk.E)
        self.text_dpm1_box.grid(row = 7, column = 1, padx = 0, pady = 4, sticky = tk.W)
        self.text_dpm2_label.grid(row = 8, column = 0, padx = 12, pady = 4, sticky = tk.E)
        self.text_dpm2_box.grid(row = 8, column = 1, padx = 0, pady = 4, sticky = tk.W)

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
            text    = 'Change Default Directory',
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
            self.dpm_checkbox.config(state = tk.NORMAL)
            if self.check_dpm.get():
                self.text_dpm1_box.config(state = tk.NORMAL)
                self.text_dpm2_box.config(state = tk.NORMAL)
        else:
            self.dpm_checkbox.config(state = tk.DISABLED)
            self.text_dpm1_box.config(state = tk.DISABLED)
            self.text_dpm2_box.config(state = tk.DISABLED)

    def set_dpm(self):
        if self.check_cvn.get() and self.check_dpm.get():
            self.text_dpm1_box.config(state = tk.NORMAL)
            self.text_dpm2_box.config(state = tk.NORMAL)
        else:
            self.text_dpm1_box.config(state = tk.DISABLED)
            self.text_dpm2_box.config(state = tk.DISABLED)

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
            int(self.text_dpm1.get()),
            int(self.text_dpm2.get()),
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
                        int(self.text_dpm1.get()),
                        int(self.text_dpm2.get())
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
            self.text_path.set(paths[userLoc+1])
            print("Your new default directory is:\n"+paths[userLoc+1]+"\n")
        return;

app = Application()
app.master.title('STD to XLSX')
app.mainloop()

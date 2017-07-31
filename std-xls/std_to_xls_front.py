import Tkinter as tk
import tkFont
import tkFileDialog
import tkMessageBox
import std_to_xls
import xls_compile
from sys import platform
import os

class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.text_std  = tk.StringVar()
        self.text_bb   = tk.StringVar()
        self.text_bs   = tk.StringVar()
        self.text_ss   = tk.StringVar()
        self.text_wb   = tk.StringVar()
        self.check_cvn = tk.IntVar()
        self.check_dpm = tk.IntVar()
        self.text_dpm1 = tk.StringVar()
        self.text_dpm2 = tk.StringVar()
        self.num_runs  = tk.IntVar()
        self.text_comp = tk.StringVar()
        self.check_mds = tk.IntVar() #master data sheet

        self.main_label = tk.Label(
            self,
            text = 'STD to XLSX',
            font = tkFont.Font(
                family = 'Helvetica',
                size   = 16,
                weight = 'bold'
            )
        )

        self.main_label.grid(row = 0, column = 0, columnspan = 3, pady = 14)

        self.std_label = tk.Label(
            self,
            text = 'STD file path:'
        )

        self.std_path = tk.Button(
            self,
            text = 'Open',
            command = self.open_std
        )

        self.std_label.grid(row = 1, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.std_path.grid(row = 1, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.std_box = tk.Entry(
            self,
            textvariable = self.text_std,
            width = 40
        )

        self.std_box.grid(row = 1, column = 2, padx = 6, pady = 4)

        self.bb_label = tk.Label(
            self,
            text = 'Base-base file path:'
        )

        self.bb_path = tk.Button(
            self,
            text = 'Open',
            command = self.open_bb
        )

        self.bb_label.grid(row = 2, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.bb_path.grid(row = 2, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.bb_box = tk.Entry(
            self,
            textvariable = self.text_bb,
            width = 40
        )

        self.bb_box.grid(row = 2, column = 2, padx = 6, pady = 4)

        self.bs_label = tk.Label(
            self,
            text = 'Base-screen file path:'
        )

        self.bs_path = tk.Button(
            self,
            text = 'Open',
            command = self.open_bs
        )

        self.bs_label.grid(row = 4, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.bs_path.grid(row = 4, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.bs_box = tk.Entry(
            self,
            textvariable = self.text_bs,
            width = 40
        )

        self.bs_box.grid(row = 4, column = 2, padx = 6, pady = 4)

        self.ss_label = tk.Label(
            self,
            text = 'Screen-screen file path:'
        )

        self.ss_path = tk.Button(
            self,
            text = 'Open',
            command = self.open_ss
        )

        self.ss_label.grid(row = 5, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.ss_path.grid(row = 5, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.ss_box = tk.Entry(
            self,
            textvariable = self.text_ss,
            width = 40
        )

        self.ss_box.grid(row = 5, column = 2, padx = 6, pady = 4)

        self.wb_label = tk.Label(
            self,
            text = 'Workbook file path:'
        )

        self.wb_path = tk.Button(
            self,
            text = 'Open',
            command = self.open_wb
        )

        self.wb_label.grid(row = 6, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.wb_path.grid(row = 6, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.wb_box = tk.Entry(
            self,
            textvariable = self.text_wb,
            width = 40
        )

        self.wb_box.grid(row = 6, column = 2, padx = 6, pady = 4)

        self.divider = tk.Canvas(
            self,
            height = 24
        )

        self.divider.create_line(
            4, 12, 480, 12,
            fill = '#ccc'
        )

        self.divider.grid(row = 7, column = 0, columnspan = 3)

        self.cvn_label = tk.Label(
            self,
            text = 'Using CVN?'
        )

        self.cvn_checkbox = tk.Checkbutton(
            self,
            variable = self.check_cvn,
            command  = self.set_cvn
        )

        self.cvn_label.grid(row = 8, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.cvn_checkbox.grid(row = 8, column = 1, padx = 0, pady = 4, sticky = tk.W)

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

        self.dpm_label.grid(row = 9, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.dpm_checkbox.grid(row = 9, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.text_dpm1.set('1')
        self.text_dpm2.set('1')

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

        self.text_dpm1_label.grid(row = 10, column = 1, padx = 6, pady = 4, sticky = tk.W)
        self.text_dpm1_box.grid(row = 10, column = 2, padx = 0, pady = 4, sticky = tk.W)
        self.text_dpm2_label.grid(row = 11, column = 1, padx = 6, pady = 4, sticky = tk.W)
        self.text_dpm2_box.grid(row = 11, column = 2, padx = 0, pady = 4, sticky = tk.W)

        self.divider2 = tk.Canvas(
            self,
            height = 24
        )

        self.divider2.create_line(
            4, 12, 480, 12,
            fill = '#ccc'
        )

        self.divider2.grid(row = 12, column = 0, columnspan = 3)

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
            variable     = self.num_runs,
            command      = self.update_mds
        )

        self.num_label.grid(row = 13, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.num_path.grid(row = 13, column = 1, columnspan = 2, padx = 0, pady = 4, sticky = tk.W)

        self.check_mds.set(1)

        self.mds_label = tk.Label(
            self,
            text = 'Create master data sheet?'
        )

        self.mds_checkbox = tk.Checkbutton(
            self,
            variable = self.check_mds,
            command  = self.set_mds
        )

        self.mds_label.grid(row = 14, column = 0, padx = 6, pady = 4, sticky = tk.W)
        self.mds_checkbox.grid(row = 14, column = 1, padx = 0, pady = 4, sticky = tk.W)

        self.divider3 = tk.Canvas(
            self,
            height = 24
        )

        self.divider3.create_line(
            4, 12, 480, 12,
            fill = '#ccc'
        )

        self.divider3.grid(row = 15, column = 0, columnspan = 3)

        self.run_button = tk.Button(
            self,
            text    = 'Run',
            command = self.run_main
        )

        self.quit_button = tk.Button(
            self,
            text    = 'Quit',
            command = self.quit
        )


        self.run_button.grid(row = 16, column = 0, padx = 6, pady = 25)
        self.quit_button.grid(row = 16, column = 2, padx = 6, pady = 25)

    def open_std(self):
        self.text_std.set(tkFileDialog.askopenfilename())

    def open_bb(self):
        self.text_bb.set(tkFileDialog.askopenfilename())

    def open_bs(self):
        fn_bs = tkFileDialog.askopenfilename()
        self.text_bs.set(fn_bs)
        self.text_wb.set('%s.xlsx' % fn_bs[:len(fn_bs) - 4])

    def open_ss(self):
        self.text_ss.set(tkFileDialog.askopenfilename())

    def open_wb(self):
        self.text_wb.set(tkFileDialog.askopenfilename())

    def set_cvn(self):
        self.is_cvn = self.check_cvn.get()
        self.is_dpm = self.check_dpm.get()
        if self.is_cvn:
            self.dpm_checkbox.config(state = tk.NORMAL)
            if self.is_dpm:
                self.text_dpm1_box.config(state = tk.NORMAL)
                self.text_dpm2_box.config(state = tk.NORMAL)
        else:
            self.dpm_checkbox.config(state = tk.DISABLED)
            self.text_dpm1_box.config(state = tk.DISABLED)
            self.text_dpm2_box.config(state = tk.DISABLED)

    def set_dpm(self):
        self.is_dpm = self.check_dpm.get()
        if self.is_dpm and self.is_cvn:
            self.text_dpm1_box.config(state = tk.NORMAL)
            self.text_dpm2_box.config(state = tk.NORMAL)
        else:
            self.text_dpm1_box.config(state = tk.DISABLED)
            self.text_dpm2_box.config(state = tk.DISABLED)

    def set_mds(self):
        self.is_mds = self.check_mds.get()

    # def open_comp(self):
    #     self.text_comp.set(tkFileDialog.askopenfilename())

    def update_mds(self, runs):
        if int(runs) > 1:
            self.mds_checkbox.config(state = tk.NORMAL)
        else:
            self.mds_checkbox.config(state = tk.DISABLED)
            #self.check_mds.set(0)

    def run_main(self):

        if ((self.text_std is None) or (self.text_bb is None) or (self.text_bs is None)
            or (self.text_ss is None) or (self.text_wb is None)
            or (self.text_std.get() == '') or (self.text_bb.get() == '') or (self.text_bs.get() == '')
            or (self.text_ss.get() == '') or (self.text_wb.get() == '')):

            tkMessageBox.showerror('STD to XLSX', 'Invalid filename(s).')

        else:
            if self.num_runs.get() > 1:
                print('\n------ Starting run 1 ------\n')

            std_to_xls.main(
                self.check_cvn.get(),
                self.text_std.get(),
                self.text_bb.get(),
                self.text_bs.get(),
                self.text_ss.get(),
                self.text_wb.get(),
                int(self.text_dpm1.get()),
                int(self.text_dpm2.get())
            )

            if (platform != 'linux' and platform != 'linux2'
                and platform != 'darwin' and platform != 'win32'):

                print('Multiple runs not supported.')

            if self.num_runs.get() > 1:
                wb_paths = [self.text_wb.get()]
                print('\n\tCurrent progress: %d%%' % (100 / self.num_runs.get()))
                pathchar = '/'

                stdbase = ''
                for st in self.text_std.get().split(pathchar)[1:len(self.text_std.get().split(pathchar)) - 1]:
                    stdbase += pathchar + st

                bbbase = ''
                for st in self.text_bb.get().split(pathchar)[1:len(self.text_bb.get().split(pathchar)) - 1]:
                    bbbase += pathchar + st

                bsbase = ''
                for st in self.text_bs.get().split(pathchar)[1:len(self.text_bs.get().split(pathchar)) - 1]:
                    bsbase += pathchar + st

                ssbase = ''
                for st in self.text_ss.get().split(pathchar)[1:len(self.text_ss.get().split(pathchar)) - 1]:
                    ssbase += pathchar + st

                wbbase = ''
                for st in self.text_wb.get().split(pathchar)[1:len(self.text_wb.get().split(pathchar)) - 1]:
                    wbbase += pathchar + st

                for i in range(2,self.num_runs.get() + 1):
                    print('\n------ Starting run %d ------\n' % i)
                    try:
                        wb_noext = self.text_wb.get().split(pathchar)[-1].split('.xlsx')[0]

                        std_to_xls.main(
                            self.check_cvn.get(),
                            '%s (%d)%s%s' % (stdbase, i, pathchar, self.text_std.get().split(pathchar)[-1]),
                            '%s (%d)%s%s' % (bbbase, i, pathchar, self.text_bb.get().split(pathchar)[-1]),
                            '%s (%d)%s%s' % (bsbase, i, pathchar, self.text_bs.get().split(pathchar)[-1]),
                            '%s (%d)%s%s' % (ssbase, i, pathchar, self.text_ss.get().split(pathchar)[-1]),
                            '%s (%d)%s%s-%d.xlsx' % (wbbase, i, pathchar, wb_noext, i),
                            int(self.text_dpm1.get()),
                            int(self.text_dpm2.get())
                        )
                        wb_paths.append('%s (%d)%s%s-%d.xlsx' % (wbbase, i, pathchar, wb_noext, i))
                        if i < self.num_runs.get():
                            print('\n\tCurrent progress: %d%%' % (i * (100 / self.num_runs.get())))
                    except IOError:
                        tkMessageBox.showerror(
                            'STD to XLSX',
                            'Invalid path: %s (%d)' % (stdbase, i)
                        )
                print('\n\tCurrent progress: 100%')

            if self.num_runs.get() > 1 and self.check_mds.get():
                print('\n------ Master Data Sheet ------\n')

                mds_path = ''
                for st in wbbase.split(pathchar)[1:len(wbbase.split(pathchar)) - 1]:
                    mds_path += pathchar + st
                mds_path += pathchar + self.text_wb.get().split(pathchar)[-1].split('.xlsx')[0] + '-mds.xlsx'

                xls_paths = [self.text_wb.get()]
                for i in range(2,self.num_runs.get() + 1):
                    wb_noext = self.text_wb.get().split(pathchar)[-1].split('.xlsx')[0]
                    xls_paths.append('%s (%d)%s%s-%d.xlsx' % (wbbase, i, pathchar, wb_noext, i))

                xls_compile.main(self.check_cvn.get(), xls_paths, mds_path, pathchar)

            print('\nDone!\n')


app = Application()
app.master.title('STD to XLSX')
app.mainloop()

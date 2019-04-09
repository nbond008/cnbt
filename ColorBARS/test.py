from Tkinter import *
import ttk
import time

root = Tk()
master = ttk.Frame(root)
master.grid(column=0, row=0)

label_list = []

def add_new_data():
    label_list.insert(-1, ttk.Label(master, text=str(time.time())))

    for widget in master.children.values():
        widget.grid_forget() 

    for ndex, i in enumerate(label_list):
        i.grid(row=ndex)
    print(label_list)

for i in range(2):
    label_list.append(ttk.Label(master, text="Some Data"))
    label_list[i].grid(row=i)

label_list.append(ttk.Button(master, text="Add new data", command=add_new_data))
label_list[-1].grid(row=2)

print(label_list)

root.mainloop()


##import Tkinter as tk
##import tkFileDialog
##
##class SampleApp(tk.Tk):
##    def __init__(self, *args, **kwargs):
##        tk.Tk.__init__(self, *args, **kwargs)
##        self.button = tk.Button(text="Pick a file!", command=self.pick_file)
##        self.button.pack()
##        self.entry_frame = tk.Frame(self)
##        self.entry_frame.pack(side="top", fill="both", expand=True)
##        self.entry_frame.grid_columnconfigure(0, weight=1)
##
##    def pick_file(self):
##        file = tkFileDialog.askopenfile(title="pick a file!")
##        if file is not None:
##            entry = tk.Entry(self)
##            entry.insert(0, file.name)
##            entry.grid(in_=self.entry_frame, sticky="ew")
##            self.button.configure(text="Pick another file!")
##
##app = SampleApp()
##app.mainloop()

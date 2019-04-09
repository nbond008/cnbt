from Tkinter import *
import ttk
from  time import sleep

def update_list(manager, rows):
    species_list = ['A','B','C','D']
    del rows[1:]

##    global species_elem_list
    species_elem_list = []
    for i, each in enumerate(species_list):

        ## Here I attempt to create a dynamic list of StringVars to attach to the Entry fields below, based on the contents of the species list.
        species_elem_list.append(StringVar())

        ## Here I initialize the values of the elements of the Entry fields by setting the StringVar of each.
        species_elem_list[i].set(each)

        ## I tried to attach the value of the StringVar (from the species list) to the Entry below, but when the program is run, the Entry does not stay populated.
        temp_name = ttk.Entry(manager, textvariable=species_elem_list[i], state='readonly')
        temp_color = ttk.Label(manager, text='data')
        temp_row = [temp_name, temp_color]
        rows.append(temp_row)

    for row_number in range(len(rows)):
        for column_number, each in enumerate(rows[row_number]):
            each.grid(column=column_number, row=row_number)
        each.grid()

    manager.update()
##    sleep(3) ## Included so that the population of the fields can be observed before they depopulate.

    ## After this point, the update_list function terminates.
    ## When that happens, the Entry fields depopulate. How can I get them to persist after the function terminates?

root = Tk()

manager = ttk.Frame(root)
manager.grid()

name_label = ttk.Label(manager, text='Name')
color_label = ttk.Label(manager, text='RGB')

rows = [[name_label, color_label]]

options = ttk.Frame(root)
options.grid(sticky=NSEW)

detect_button = ttk.Button(options, text='Auto-Detect', command=lambda: update_list(manager,rows))
done_button = ttk.Button(options, text='Done', command=root.destroy)

detect_button.grid(column=0, row=0)
done_button.grid(column=1, row=0)

root.mainloop()

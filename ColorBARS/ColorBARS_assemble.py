from os import walk
 
def species_finder(directory = 'D:/colorbars/testing', deep=True):
    species = []
    for path, subs, files in walk(directory, topdown = True):
        for f in files:
            if f.endswith('.Dpd_par'):
                new_species = par_reader(path,f)
                for each in new_species:
                    if each not in species:
                        species.append(each)
                        print('   Added '+each+'...')
                if not deep:
                    subs[:]=[]
                    files[:]=[]
    return species

def par_reader(p,f):
    s = []
    if p[-1] != '\\':
        p += '\\'
    fileLoc = p+f
    with open(fileLoc,'r') as pfile:
        for line in pfile:
            if ' name' in line:
                name = line.split()[-1]
                s.append(name)
            elif 'interaction' in line:
                break
    return s

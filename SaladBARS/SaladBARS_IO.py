import SaladBARS
import re
import sys
from os import path

init_path   = '/Users/nickbond/research/dpd_shenanigans/db2_init.txt'
init_folder = path.dirname(path.realpath(init_path))

step_start = re.compile(r'[0-9]*(?=\ *:)')
mtd_start  = re.compile(r'(?<=\').*(?=\.mtd\')')

init_file = open(init_path)

concs = [.95, .97, .99, 1.00]

step = 0
mtd  = ''

for line in init_file:
    try:
        step = int(step_start.search(line).group())
        mtd  = mtd_start.search(line).group()

        out = SaladBARS.saladBARS_main(
            '%s/%s.mtd' % (init_folder, mtd),
            '%s/%s_hist.mtd' % (init_folder, mtd),
            '%s/%s_xy.mtd' % (init_folder, mtd),
            '%s/%s_log.txt' % (init_folder, mtd),
            '%s/%s.txt' % (init_folder, mtd),
            concs,
            'timestep %d' % step,
            suppress = True
        )

        print '\ntimestep %d:\n%s\n' % (step, out)

        # print '\ntimestep %d:'
        #
        # for i in range(len(concs)):
        #     print '%d%%: %d inside, %d outside' % (int(concs[i] * 100),
        #                                            R_percent_counts[i],
        #                                            len(R) - R_percent_counts[i])

    except AttributeError:
        pass #ignore these

init_file.close()
sys.exit(0)
# # db2_init =
#
# print SaladBARS.saladBARS_main()

import SaladBARS
import re
import sys
from os import path

init_path   = '/Users/nickbond/research/dpd_shenanigans/C1k_10k/C_init.txt'
init_folder = path.dirname(path.realpath(init_path))

summ_path = '%s/C_summary.csv' % (init_folder)

step_start = re.compile(r'[0-9]*(?=\ *:)')
mtd_start  = re.compile(r'(?<=\').*(?=\.mtd\')')

init_file = open(init_path)

concs = [.95, .97, .99, 1.00]

step = 0
mtd  = ''

summ_file = open(summ_path, 'w')
summ_file.write('step, %d%% radius, %d%% radius, %d%% count, %d%% count, %d%% ABC radius, %d%% ABC radius, %d%% ABC count, %d%% ABC count\n' % (
    int(concs[0] * 100),
    int(concs[1] * 100),
    int(concs[0] * 100),
    int(concs[1] * 100),
    int(concs[0] * 100),
    int(concs[1] * 100),
    int(concs[0] * 100),
    int(concs[1] * 100)
))

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

        new_radius_C     = out['radius_C']
        new_radius_ABC   = out['radius_ABC']
        new_count_C      = out['count_C']
        new_count_ABC    = out['count_ABC']

        summ_file.write('%d, %0.4f, %0.4f, %d, %d, %0.4f, %0.4f, %d, %d\n' % (
            step,
            new_radius_C[0],
            new_radius_C[1],
            new_count_C[0],
            new_count_C[1],
            new_radius_ABC[0],
            new_radius_ABC[1],
            new_count_ABC[0],
            new_count_ABC[1]
        ))

    except AttributeError:
        pass #ignore these
    except ValueError:
        pass #yeah comment

init_file.close()
summ_file.close()
sys.exit(0)
# # db2_init =
#
# print SaladBARS.saladBARS_main()

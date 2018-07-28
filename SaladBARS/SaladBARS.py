import re
import sys
import math
from os import path
import copy

# adding the flag -d displays a little debug text.

def distance(a, b):
    return math.sqrt(
        math.pow(a[0] - b[0], 2) +
        math.pow(a[1] - b[1], 2) +
        math.pow(a[2] - b[2], 2)
    )

def get_offset(tup, size, offset_magnitude):
    offset = [0, 0, 0]

    if float(tup[0]) > offset_magnitude[0]:
        offset[0] = -size[0]
    # # elif float(tup[0]) < -size[0] + offset_magnitude[0]:
    # #     offset[0] = size[0]
    #
    if float(tup[1]) > offset_magnitude[1]:
        offset[1] = -size[1]
    # # elif float(tup[1]) < -size[1] + offset_magnitude[1]:
    # #     offset[1] = size[1]
    #
    if float(tup[2]) > offset_magnitude[2]:
        offset[2] = -size[2]
    # # elif float(tup[2]) < -size[2] + offset_magnitude[2]:
    # #     offset[2] = size[2]

    return offset

def saladBARS_main(mtd_filename, hist_filename, xy_filename, log_filename, coords_filename, concs, comment = '', diagnostic = False, suppress = False):
    if diagnostic:
        suppress = False

    A = []
    B = []
    C = []
    R = []

    mms_start      = re.compile(r'<MesoMoleculeSet')
    mm_start       = re.compile(r'<MesoMolecule')

    id_start     = re.compile(r'(?<=ID=\")\d*(?=\")')
    coords_start = re.compile(r'(?<=Coords=\").*(?=\")')

    dispr_start = re.compile(r'(?<=DisplayRange=\")[-,\.0-9]*(?=\")')
    xsize_start = re.compile(r'(?<=XSize=\")[0-9]*(?=\")')
    ysize_start = re.compile(r'(?<=YSize=\")[0-9]*(?=\")')
    zsize_start = re.compile(r'(?<=ZSize=\")[0-9]*(?=\")')
    mmstring_start = re.compile(r'(?<=MesoMoleculeString=\")[A-C0-9 ]*(?=\")')

    dispr = [0, 0, 0]
    size  = [30, 30, 30]

    try:
        fi = open(mtd_filename, 'r')
    except IOError:
        print 'invalid filename: %s\nusage: python SaladBARS.py [-d] filename...' % mtd_filename
        sys.exit(0)

    p = 0

    # log_string = ''
    f_log = open(log_filename, 'w')

    for line in fi:
        if mms_start.search(line):
            p = int(id_start.search(line).group())
            if diagnostic:
                print '\nID = %d' % p
                f_log.write('ID = %d\n' % p)

            try:
                dispr_temp = dispr_start.search(line).group().split(',')
                dispr = [float(dispr_temp[0]),
                         float(dispr_temp[2]),
                         float(dispr_temp[4])]

                for i in range(3):
                    while dispr[i] > 1:
                        dispr[i] -= 1
                    while dispr[i] < 0:
                        dispr[i] += 1

                if diagnostic:
                    print 'display range: %s' % dispr
                    f_log.write('display range: %s\n' % dispr)

                size = [int(xsize_start.search(line).group()),
                        int(ysize_start.search(line).group()),
                        int(zsize_start.search(line).group())]

                if diagnostic:
                    print 'size: %s' % size
                    f_log.write('size: %s\n\n' % size)

                offset_magnitude = (dispr[0] * float(size[0]),
                                    dispr[1] * float(size[1]),
                                    dispr[2] * float(size[2]))

            except AttributeError:
                pass

            if p == 7:
                try:
                    mmstring = mmstring_start.search(line).group().split(' ')
                    numblocks = len(mmstring) / 2
                    if numblocks > 3:
                        print 'warning: only considering first 3 bead types'
                        f_log.write('warning: only considering first 3 bead types')

                    startbead = 0
                    for i in range(3):
                        if mmstring[2 * i] == 'A':
                            rangeA = range(startbead, startbead + int(mmstring[2 * i + 1]))
                        elif mmstring[2 * i] == 'B':
                            rangeB = range(startbead, startbead + int(mmstring[2 * i + 1]))
                        startbead += int(mmstring[2 * i + 1])

                except AttributeError:
                    pass

        if p == 7:
            if mm_start.search(line):
                try:
                    cs = coords_start.search(line).group()
                    ca = cs.split(':')

                    try:
                        for i in range(len(ca)):
                            tup = ca[i].split(',')

                            offset = get_offset(tup, size, offset_magnitude)

                            if i in rangeA:
                                A.append((
                                    float(tup[0]) + offset[0],
                                    float(tup[1]) + offset[1],
                                    float(tup[2]) + offset[2]
                                ))
                            elif i in rangeB:
                                B.append((
                                    float(tup[0]) + offset[0],
                                    float(tup[1]) + offset[1],
                                    float(tup[2]) + offset[2]
                                ))
                            else:
                                C.append((
                                    float(tup[0]) + offset[0],
                                    float(tup[1]) + offset[1],
                                    float(tup[2]) + offset[2]
                                ))
                    except IndexError:
                        print 'error code 11 - please contact nick'
                except AttributeError:
                    # print ca
                    pass

        elif p == 9:
            if mm_start.search(line):
                try:
                    cs = coords_start.search(line).group()
                    tup = cs.split(',')

                    offset = get_offset(tup, size, offset_magnitude)

                    R.append((
                        float(tup[0]) + offset[0],
                        float(tup[1]) + offset[1],
                        float(tup[2]) + offset[2]
                    ))

                except AttributeError:
                    pass

    fi.close()

    # if diagnostic:
    f_coords = open(coords_filename, 'w')

    f_coords.write('%d\n%s\n' % (len(A) + len(B) + len(C) + len(R), comment))

    for a in A:
        f_coords.write('A\t%0.5f\t%0.5f\t%0.5f\n' % (a[0], a[1], a[2]))

    for a in B:
        f_coords.write('B\t%0.5f\t%0.5f\t%0.5f\n' % (a[0], a[1], a[2]))

    for a in C:
        f_coords.write('C\t%0.5f\t%0.5f\t%0.5f\n' % (a[0], a[1], a[2]))

    for a in R:
        f_coords.write('R\t%0.5f\t%0.5f\t%0.5f\n' % (a[0], a[1], a[2]))

    f_coords.close()

    origin_temp = [0, 0, 0]

    for c in C:
        origin_temp[0] += (c[0] / len(C))
        origin_temp[1] += (c[1] / len(C))
        origin_temp[2] += (c[2] / len(C))

    origin = tuple(origin_temp)
    if diagnostic:
        print '\norigin at [%0.3f, %0.3f, %0.3f]\n' % origin
        f_log.write('origin at [%0.3f, %0.3f, %0.3f]\n\n' % origin)

    A_dist = [0 for i in range(len(A))]
    B_dist = [0 for i in range(len(B))]
    C_dist = [0 for i in range(len(C))]

    R_dist = [0 for i in range(len(R))]

    for i in range(len(A)):
        A_dist[i] = distance(A[i], origin)

    for i in range(len(B)):
        B_dist[i] = distance(B[i], origin)

    C_high = [0 for i in range(100)]

    C_avg = 0

    for i in range(len(C)):
        C_dist[i] = distance(C[i], origin)
        C_avg += (C_dist[i] / len(C))

    C_max_radius = max(C_dist)

    C_sorted = copy.deepcopy(C_dist)
    C_sorted.sort()
    #concs   = [.95, .97, .99, 1.00]
    indices = [int(i * len(C_dist) - 1) for i in concs]

    C_percent_radius = [C_sorted[i] for i in indices]

    for i in range(len(R)):
        R_dist[i] = distance(R[i], origin)

    total_dist = [0 for i in range(len(A) + len(B) + len(C))]
    for i in range(len(A)):
        total_dist[i] = A_dist[i]
    for i in range(len(B)):
        total_dist[i + len(A)] = B_dist[i]
    for i in range(len(C)):
        total_dist[i + len(A) + len(B)] = C_dist[i]

    total_dist.sort()

    indices_tot = [int(i * len(total_dist) - 1) for i in concs]
    total_percent_radius = [total_dist[i] for i in indices_tot]

    A_hist = []
    B_hist = []
    C_hist = []
    R_hist = []
    rs = []

    # the important part

    dr = 0.1
    r = dr

    while r < size[0] and (A_dist or B_dist or C_dist):
        temp_h = []

        for p in A_dist:
            if p < r + dr:
                temp_h.append(p)
                A_dist.remove(p)

        A_hist.append(len(temp_h))

        temp_h = []

        for p in B_dist:
            if p < r + dr:
                temp_h.append(p)
                B_dist.remove(p)

        B_hist.append(len(temp_h))

        temp_h = []

        for p in C_dist:
            if p < r + dr:
                temp_h.append(p)
                C_dist.remove(p)

        C_hist.append(len(temp_h))

        temp_h = []
        try:
            for p in R_dist:
                if p < r + dr:
                    temp_h.append(p)
                    R_dist.remove(p)

            R_hist.append(len(temp_h))
        except IndexError:
            pass

        rs.append(r)
        r += dr

    l = min(len(A_hist), len(B_hist), len(C_hist), len(rs))

    C_peak_radius = rs[C_hist.index(max(C_hist))]

    R_peak_count = 0
    R_percent_counts = [0 for i in concs]
    R_total_percent_counts = [0 for i in concs]

    # R_max_count = 0
    for i in range(len(R)):
        R_peak_count += (distance(R[i], origin) <= C_peak_radius)
        for index in range(len(C_percent_radius)):
            R_percent_counts[index] += (distance(R[i], origin) <= C_percent_radius[index])

        for index in range(len(total_percent_radius)):
            R_total_percent_counts[index] += (distance(R[i], origin) <= total_percent_radius[index])

    if not suppress:
        print 'C peak radius: %0.3f' % (C_peak_radius)
        print '%d inside peak, %d outside peak\n' % (R_peak_count, len(R) - R_peak_count)

    f_log.write('C peak radius: %0.3f\n' % (C_peak_radius))
    f_log.write('%d inside peak, %d outside peak\n\n' % (R_peak_count, len(R) - R_peak_count))

    inner_volume = math.pi * 4 / 3 * math.pow(C_peak_radius, 3)
    box_volume = size[0] * size[1] * size[2]

    percent_volumes = [math.pi * 4 / 3 * math.pow(r, 3) for r in C_percent_radius]

    inner_density = R_peak_count / inner_volume
    # total_density = R_peak_count / total_volume
    box_density = len(R) / box_volume

    percent_densities = [R_percent_counts[i] / percent_volumes[i] for i in range(len(percent_volumes))]

    # if not suppress:
    #     print '%0.6f R/u^3 inside peak\n%0.6f R/u^3 total\n' % (inner_density, box_density)
    # f_log.write('%0.6f R/u^3 inside peak\n%0.6f R/u^3 total\n\n------\n\n' % (inner_density, box_density))

    if not suppress:
        print '------\n'

    for i in range(4):
        if not suppress:
            print 'radius at %d%% (%d) = %0.5f' % (int(concs[i] * 100), indices[i], C_percent_radius[i])
        f_log.write('radius at %d%% (%d) = %0.5f\n' % (int(concs[i] * 100), indices[i], C_percent_radius[i]))

    if not suppress:
        print ''
    f_log.write('\n')

    for i in range(4):
        if not suppress:
            print '%d%%: %d inside, %d outside' % (int(concs[i] * 100),
                                               R_percent_counts[i],
                                               len(R) - R_percent_counts[i])
        f_log.write('%d%%: %d inside, %d outside\n' % (int(concs[i] * 100),
                                                     R_percent_counts[i],
                                                     len(R) - R_percent_counts[i]))

    if not suppress:
        print ''
    f_log.write('\n')

    for i in range(4):
        if not suppress:
            print '%d%%: %0.6f R/u^3' % (int(concs[i] * 100), percent_densities[i])
        f_log.write('%d%%: %0.6f R/u^3\n' % (int(concs[i] * 100), percent_densities[i]))

    fi = open(hist_filename, 'w')

    fi.write('i, r, A, B, C, Reactant\n')

    for i in range(l):
        if A_hist[i] != 0 or B_hist[i] != 0 or C_hist[i] != 0:
            fi.write('%d, %0.2f, %0.4f, %0.4f, %0.4f, %0.4f\n' % (
                i,
                rs[i],
                A_hist[i],
                B_hist[i],
                C_hist[i],
                R_hist[i]
            ))

    fi.close()

    fi = open(xy_filename, 'w')

    fi.write('i, Ax, Ay, Bx, By, Cx, Cy, Rx, Ry\n')

    for i in range(len(A)):
        try:
            fi.write('%d, %0.4f, %0.4f, %0.4f, %0.4f, %0.4f, %0.4f, %0.4f, %0.4f\n' % (
                i,
                A[i][0],
                A[i][1],
                B[i][0],
                B[i][1],
                C[i][0],
                C[i][1],
                R[i][0],
                R[i][1]
            ))
        except IndexError:
            fi.write('%d, %0.4f, %0.4f, %0.4f, %0.4f, %0.4f, %0.4f\n' % (
                i,
                A[i][0],
                A[i][1],
                B[i][0],
                B[i][1],
                C[i][0],
                C[i][1]
            ))

    fi.close()

    f_log.write('\ntotals:\n\n%d A beads\n%d B beads\n%d C beads\n%d R beads\n' % (len(A),
                                                                             len(B),
                                                                             len(C),
                                                                             len(R)))

    f_log.write('mesomolecule string: \"{} {} {} {} {} {}\"'.format(*mmstring))
    f_log.close()

    if diagnostic:
        print '\n------\n\ntotals:\n\n%d A beads\n%d B beads\n%d C beads\n%d R beads\n\n' % (len(A),
                                                                                             len(B),
                                                                                             len(C),
                                                                                             len(R))

        print 'mesomolecule string: \"{} {} {} {} {} {}\"'.format(*mmstring)

    return {
        'conc'       : concs,
        'radius_C'   : C_percent_radius,
        'radius_ABC' : total_percent_radius,
        'volume'     : percent_volumes,
        'count_C'    : R_percent_counts,
        'count_ABC'  : R_total_percent_counts,
        'density'    : percent_densities
    }

if __name__ == '__main__':
    concs = [.95, .97, .99, 1.00]
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print  'usage: python SaladBARS.py [-d] filename...'
            sys.exit(0)

        mtd_filename = path.realpath(sys.argv[1])

        hist_filename = '%s_hist.csv' % mtd_filename.split('.mtd')[0]
        xy_filename   = '%s_xy.csv' % mtd_filename.split('.mtd')[0]
        log_filename  = '%s.txt' % mtd_filename.split('.mtd')[0]

        coords_filename = '%s_coords.txt' % mtd_filename.split('.mtd')[0]

        saladBARS_main(mtd_filename, hist_filename, xy_filename, log_filename, coords_filename, concs, 'timestep 0')
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            mtd_filename = path.realpath(sys.argv[2])

            hist_filename = '%s_hist.csv' % mtd_filename.split('.mtd')[0]
            xy_filename   = '%s_xy.csv' % mtd_filename.split('.mtd')[0]
            log_filename  = '%s.txt' % mtd_filename.split('.mtd')[0]

            coords_filename = '%s_coords.txt' % mtd_filename.split('.mtd')[0]

        elif sys.argv[2] == '-d':
            mtd_filename = path.realpath(sys.argv[1])

            hist_filename = '%s_hist.csv' % mtd_filename.split('.mtd')[0]
            xy_filename   = '%s_xy.csv' % mtd_filename.split('.mtd')[0]
            log_filename  = '%s.txt' % mtd_filename.split('.mtd')[0]

            coords_filename = '%s_coords.txt' % mtd_filename.split('.mtd')[0]

        else:
            print 'usage: python SaladBARS.py [-d] filename...'
            sys.exit(0)

        saladBARS_main(mtd_filename, hist_filename, xy_filename, log_filename, coords_filename, concs, 'timestep 0', True)
    else:
        print 'usage: python SaladBARS.py [-d] filename...'
        sys.exit(0)

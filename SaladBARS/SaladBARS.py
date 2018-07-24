import re
import sys
import math
from os import path

# adding the flag -d displays a little debug text.

def distance(a, b):
    return math.sqrt(
        math.pow(a[0] - b[0], 2) +
        math.pow(a[1] - b[1], 2) +
        math.pow(a[2] - b[2], 2)
    )

def saladBARS_main(mtd_filename, histogram_filename, xy_filename, diagnostic = False):
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
        print 'invalid filename: %s\nusage: python rdf.py filename...' % mtd_filename
        sys.exit(0)

    p = 0

    for line in fi:
        if mms_start.search(line):
            p = int(id_start.search(line).group())
            if diagnostic:
                print '\nID = %d' % p

            try:
                dispr_temp = dispr_start.search(line).group().split(',')
                dispr = [float(dispr_temp[0]) + (float(dispr_temp[0]) < 0),
                         float(dispr_temp[2]) + (float(dispr_temp[0]) < 0),
                         float(dispr_temp[4]) + (float(dispr_temp[0]) < 0)]

                if diagnostic:
                    print 'display range: %s' % dispr

                size = [int(xsize_start.search(line).group()),
                        int(ysize_start.search(line).group()),
                        int(zsize_start.search(line).group())]

                if diagnostic:
                    print 'size: %s' % size

                offset_magnitude = [dispr[0] * float(size[0]),
                                    dispr[1] * float(size[1]),
                                    dispr[2] * float(size[2])]

            except AttributeError:
                pass

            if p == 7:
                try:
                    mmstring = mmstring_start.search(line).group().split(' ')
                    numblocks = len(mmstring) / 2
                    if numblocks > 3:
                        print 'warning: only considering first 3 bead types'

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

                            offset = [0, 0, 0]#offset_magnitude

                            if float(tup[0]) > offset_magnitude[0]:
                                offset[0] = -size[0]
                            elif float(tup[0]) < -size[0] + offset_magnitude[0]:
                                offset[0] = size[0]

                            if float(tup[1]) > offset_magnitude[1]:
                                offset[1] = -size[1]
                            elif float(tup[1]) < -size[1] + offset_magnitude[1]:
                                offset[1] = size[1]

                            if float(tup[2]) > offset_magnitude[2]:
                                offset[2] = -size[2]
                            elif float(tup[2]) < -size[2] + offset_magnitude[2]:
                                offset[2] = size[2]

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

                    offset = [0, 0, 0]#offset_magnitude

                    if float(tup[0]) > offset_magnitude[0]:
                        offset[0] = -size[0]
                    elif float(tup[0]) < -size[0] + offset_magnitude[0]:
                        offset[0] = size[0]

                    if float(tup[1]) > offset_magnitude[1]:
                        offset[1] = -size[1]
                    elif float(tup[1]) < -size[1] + offset_magnitude[1]:
                        offset[1] = size[1]

                    if float(tup[2]) > offset_magnitude[2]:
                        offset[2] = -size[2]
                    elif float(tup[2]) < -size[2] + offset_magnitude[2]:
                        offset[2] = size[2]

                    R.append((
                        float(tup[0]) + offset[0],
                        float(tup[1]) + offset[1],
                        float(tup[2]) + offset[2]
                    ))

                except AttributeError:
                    pass

    fi.close()

    origin_temp = [0, 0, 0]

    for c in C:
        origin_temp[0] += (c[0] / len(C))
        origin_temp[1] += (c[1] / len(C))
        origin_temp[2] += (c[2] / len(C))

    origin = tuple(origin_temp)

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

    for i in range(len(R)):
        R_dist[i] = distance(R[i], origin)

    A_hist = []
    B_hist = []
    C_hist = []
    R_hist = []
    rs = []

    # the important part

    dr = 0.2
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
    R_max_count = 0
    for i in range(len(R)):
        R_peak_count += (distance(R[i], origin) <= C_peak_radius)
        R_max_count  += (distance(R[i], origin) <= C_max_radius)

    print '\nC peak radius: %0.3f\nC max radius: %0.3f\n' % (C_peak_radius, C_max_radius)

    print '%d inside peak, %d outside peak' % (R_peak_count, len(R) - R_peak_count)
    print '%d inside max, %d outside max\n' % (R_max_count, len(R) - R_max_count)

    inner_volume = math.pi * 4 / 3 * math.pow(C_peak_radius, 3)
    mid_volume   = math.pi * 4 / 3 * math.pow(C_max_radius, 3)
    total_volume = size[0] * size[1] * size[2]

    inner_density = R_peak_count / inner_volume
    mid_density   = R_max_count / mid_volume
    total_density = len(R) / total_volume

    print '%0.6f R/u^3 inside peak\n%0.6f R/u^3 inside max\n%0.6f R/u^3 total' % (inner_density, mid_density, total_density)

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

    if diagnostic:
        print '\ntotals:\n\n%d A beads\n%d B beads\n%d C beads\n%d R beads\n' % (len(A),
                                                                                 len(B),
                                                                                 len(C),
                                                                                 len(R))

        print 'mesomolecule string: \"{} {} {} {} {} {}\"'.format(*mmstring)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print 'usage: python SaladBARS.py filename...'
            sys.exit(0)

        mtd_filename = path.realpath(sys.argv[1])

        hist_filename = '%s hist.csv' % mtd_filename.split('.mtd')[0]
        xy_filename   = '%s_xy.csv' % mtd_filename.split('.mtd')[0]

        saladBARS_main(mtd_filename, hist_filename, xy_filename)
    elif len(sys.argv) == 3:
        if sys.argv[1] == '-d':
            mtd_filename = path.realpath(sys.argv[2])

            hist_filename = '%s hist.csv' % mtd_filename.split('.mtd')[0]
            xy_filename   = '%s_xy.csv' % mtd_filename.split('.mtd')[0]
        elif sys.argv[2] == '-d':
            mtd_filename = path.realpath(sys.argv[1])

            hist_filename = '%s hist.csv' % mtd_filename.split('.mtd')[0]
            xy_filename   = '%s_xy.csv' % mtd_filename.split('.mtd')[0]
        else:
            print 'usage: python SaladBARS.py [-d] filename...'
            sys.exit(0)

        saladBARS_main(mtd_filename, hist_filename, xy_filename, True)
    else:
        print 'usage: python SaladBARS.py [-d] filename...'
        sys.exit(0)

from sys import platform
from sys import exit
import shutil
from os import chdir, mkdir, path, error
from Config import Config
import re

pathchar = '/'

def BS_prepare(text_path, index, m1, m2, ff, num_frames, temp):
    path = ''
    for st in text_path.split(pathchar)[1:len(text_path.split(pathchar))]:
        path += pathchar + st

    index_paren = ''

    if index > 1:
        index_paren = ' (%d)' % index

    path += '%s%s Blends Mixing%s' % (pathchar, m1, index_paren)

    full = '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n' % (
        top,
        'my $dir = \'%s%sLowest Energies\';' % (path, pathchar),
        'my $monomer1 = "%s";' % m1,
        'my $monomer2 = "%s";' % m2,
        'my $forcefield = "%s";' % ff,
        'my $numframes = %d;' % num_frames,
        'my $temperature = %d;' % temp,
        bottom
    )

    print '\nSaving to %s%sLowest Energies...' % (path, pathchar)

    try:
        bars = open('%s%sLowest Energies%sBARS.pl' % (path, pathchar, pathchar), 'w')
        bars.write(full)
    except IOError:
        print 'Path not found: %s%sLowest Energies' % (path, pathchar)
        return False

    return True

def BS_label(text_path, index, m1, m2):
    path = ''
    for st in text_path.split(pathchar)[1:len(text_path.split(pathchar))]:
        path += pathchar + st

    index_paren = ''

    if index > 1:
        index_paren = ' (%d)' % index

    path += '%s%s Blends Mixing%s%sLowest Energies' % (pathchar, m1, index_paren, pathchar)

    try:
        __label__(path, m1, m2)
    except IOError:
        print 'Path not found: %s' % path
        return False

    return True

def BS_unlabel(text_path, index, m1, m2):
    path = ''
    for st in text_path.split(pathchar)[1:len(text_path.split(pathchar))]:
        path += pathchar + st

    index_paren = ''

    if index > 1:
        index_paren = ' (%d)' % index

    path += '%s%s Blends Mixing%s%sLowest Energies' % (pathchar, m1, index_paren, pathchar)

    try:
        __unlabel__(path, m1, m2)
    except IOError:
        print 'Path not found: %s' % path
        return False

    return True

def BS_collect(dest, src, index, m1, m2, c_std, c_out, c_set, c_bar):
    dest_folder = '%s%s%s' % (dest, pathchar, src.split(pathchar)[-1])

    index_paren = ''

    if index == 1:
        try:
            print 'Creating directory %s...' % dest_folder
            mkdir(dest_folder)
        except OSError:
            print 'Directory \"%s\" already exists.' % dest_folder
    else:
        index_paren = ' (%d)' % index

    source_path = '%s%s%s Blends Mixing%s' % (src, pathchar, m1, index_paren)
    dest_path   = '%s%s%s Blends Mixing%s' % (dest_folder, pathchar, m1, index_paren)

    try:
        print 'Creating directory %s...' % dest_path
        mkdir(dest_path)
    except OSError:
        print 'Directory \"%s\" already exists.' % dest_path

    if c_std:
        std_source = '%s%s%s.std' % (source_path, pathchar, m1)
        std_dest   = '%s%s%s.std' % (dest_path, pathchar, m1)

        try:
            print 'Copying %s to %s...\n' % (std_source, std_dest)
            shutil.copy(std_source, std_dest)
        except IOError:
            print 'File not found: %s' % std_source
            # return False

    if c_out:
        out_path = '%s%sLowest Energies' % (source_path, pathchar)

        pair     = [(m1, m1), (m1, m2), (m2, m2)]
        out_src  = ['', '', '']
        out_dest = ['', '', '']

        for i in range(3):
            out_src[i]  = '%s%s%s %s.txt' % (out_path,  pathchar, pair[i][0], pair[i][1])
            out_dest[i] = '%s%s%s %s.txt' % (dest_path, pathchar, pair[i][0], pair[i][1])

            try:
                print 'Copying %s to %s...\n' % (out_src[i], out_dest[i])
                shutil.copy(out_src[i], out_dest[i])
            except IOError:
                print 'File not found: %s\n' % out_src[i]
                # return False

    if c_set:
        settings_source = '%s%s%s.txt' % (source_path, pathchar, m1)
        settings_dest   = '%s%s%s.txt' % (dest_path, pathchar, m1)

        try:
            print 'Copying %s to %s...\n' % (settings_source, settings_dest)
            shutil.copy(settings_source, settings_dest)
        except IOError:
            print 'File not found: %s' % settings_source
            # return False

    if c_bar:
        bars_source = '%s%sLowest Energies%sBARS.pl' % (source_path, pathchar, pathchar)
        bars_dest   = '%s%sBARS.pl' % (dest_path, pathchar, pathchar)

        try:
            print 'Copying %s to %s...\n' % (bars_source, bars_dest)
            shutil.copy(bars_source, bars_dest)
        except IOError:
            print 'File not found: %s' % ('%s%sLowest Energies%sBARS.pl' % (source_path, pathchar, pathchar))
            # return False

    return True

# TODO: come up with a more robust regex solution to this
def BS_get_ff_name(ff):
    res = {
        'isolate' : re.compile(r'[^/]*\.off$')
    }

    try:
        # print re.search(res['isolate'], ff).group().split('.')[0]
        return re.search(res['isolate'], ff).group().split('.')[0]
    except AttributeError:
        return None

    return None

# __label__ <LANDMARK> : the behind-the-scenes for the behind-the-scenes

def __label__(path, m1, m2):
    pairs = [
        '%s%s%s %s.xtd' % (path, pathchar, m1, m1),
        '%s%s%s %s.xtd' % (path, pathchar, m1, m2),
        '%s%s%s %s.xtd' % (path, pathchar, m2, m2)
    ]

    print '\nSaving to %s...' % path

    for pair in pairs:
        bonds = __get_bonds__(pair)

        index = 0
        contents = ''
        f = open(pair, 'r')
        for line in f:

            contents += __edit__(line, __get_fn__(line, bonds))
            index += 1

        f.close()

        f2 = open(pair, 'w')

        f2.write(contents)
        f2.close()

    return 1

def __edit__(line, fn):
    res = {
        'atom' : re.compile(r'\w*<Atom3d '),
        'bond' : re.compile(r'\w*<Bond '),
        'name' : re.compile(r'Name=\"[^\"]*\"'),
        'end'  : re.compile(r'>')
    }

    newname = ''

    if fn > 0:
        newname = 'Name=\"Frag_%d\"' % fn

    if re.search(res['atom'], line):
        split_start = re.split(res['atom'], line)

        if re.search(res['name'], line):
            split_name = re.split(res['name'], split_start[1])

            return '%s<Atom3d %s%s%s' % (
                split_start[0],
                split_name[0],
                newname,
                split_name[1]
            )

        return '%s<Atom3d %s%s' % (
            split_start[0],
            newname,
            split_start[1]
        )

    elif re.search(res['bond'], line):
        split_start = re.split(res['bond'], line)

        if re.search(res['name'], line):
            split_name = re.split(res['name'], split_start[1])

            return '%s<Bond %s%s%s' % (
                split_start[0],
                split_name[0],
                newname,
                split_name[1]
            )

        return '%s<Bond %s%s' % (
            split_start[0],
            newname,
            split_start[1]
        )

    return line

def __get_fn__(line, bonds):
    res = {
        'start' : re.compile(r'\s*<\w* '),
        'id'    : re.compile(r'ID=\"[^\"]*\"'),
        'nums'  : re.compile(r'[0-9]+')
    }

    try:
        if re.search(res['start'], line):
            idstr = re.search(res['id'], line).group()

            num = int(re.search(res['nums'], idstr).group())

            if num in bonds[0]:
                return 1

            if num in bonds[1]:
                return 2

            if num != 1:
                return 0
                # print 'Item %d matches neither molecule.' % num

    except AttributeError:
        pass

    return -1

def __get_bonds__(path):
    res = {
        'start' : re.compile(r'\w*<Bond '),
        'conn'  : re.compile(r'Connects=\"[^\"]*\"'),
        'id'    : re.compile(r'ID=\"[^\"]*\"'),
        'isol'  : re.compile(r'\"|\,'),
        'pair'  : re.compile(r'\"[0-9]+,[0-9]+\"'),
        'nums'  : re.compile(r'[0-9]+')
    }

    bonds = []
    frag_1 = set()
    frag_2 = set()

    f = open(path, 'r')

    i = 0

    for line in f:
        try:
            if re.search(res['start'], line):
                connstr = re.search(res['conn'], line).group()
                pair = re.split(res['isol'], re.search(res['pair'], connstr).group())

                idstr = re.search(res['id'], line).group()

                num = int(re.search(res['nums'], idstr).group())

                bonds.append(set())
                bonds[i].add(int(pair[1]))
                bonds[i].add(int(pair[2]))
                bonds[i].add(int(num))

                i += 1
        except AttributeError:
            pass

    frag_1 = frag_1.union(bonds[0])

    for i in range(1, len(bonds)):
        neither = False
        for b in bonds[i]:
            if b not in frag_1:
                neither = True
            else:
                neither = False
                frag_1 = frag_1.union(bonds[i])

        if neither:
            frag_2.add(b)

    for i in range(1, len(bonds)):
        for b in bonds[i]:
            if b in frag_2:
                frag_2 = frag_2.union(bonds[i])

    f.close()

    return (frag_1, frag_2)

def __unlabel__(path, m1, m2):
    pairs = [
        '%s%s%s %s.xtd' % (path, pathchar, m1, m1),
        '%s%s%s %s.xtd' % (path, pathchar, m1, m2),
        '%s%s%s %s.xtd' % (path, pathchar, m2, m2)
    ]

    print '\nSaving to %s...' % path

    for pair in pairs:
        bonds = __get_bonds__(pair)

        index = 0
        contents = ''
        f = open(pair, 'r')
        for line in f:

            contents += __edit__(line, -1)
            index += 1

        f.close()

        f2 = open(pair, 'w')

        f2.write(contents)
        f2.close()

    return 1

top =\
'''###############################################################################################################
#                                                                                                             #
#                                888888b.         d8888 8888888b.   .d8888b.                                  #
#                                888  "88b       d88888 888   Y88b d88P  Y88b                                 #
#                                888  .88P      d88P888 888    888 Y88b.                                      #
#                                8888888K.     d88P 888 888   d88P  "Y888b.                                   #
#                                888  "Y88b   d88P  888 8888888P"      "Y88b.                                 #
#                                888    888  d88P   888 888 T88b         "888                                 #
#                                888   d88P d8888888888 888  T88b  Y88b  d88P                                 #
#                                8888888P" d88P     888 888   T88b  "Y8888P"                                  #
#                                                                                                             #
#                                      BLENDS ANALYSIS/REFINEMENT SCRIPT                                      #
#                                                                                                             #
#      This Perl script performs geometry optimization and Connolly volume measurements on each individual    #
#  fragment and pair of fragments in each frame of the .xtd trajectory files output by the Blends module. It  #
#  outputs three .txt files that can be used as inputs to the STX processing script.                          #
#                                                                                                             #
#      To use this script, copy it into the "Lowest energies" folder of the Blends run under consideration.   #
#  Provide the requested information in the "Required input parameters" block below. Note that the variables  #
#  $monomer1 and $monomer2 refer to the names of the files as they were input into Blends (i.e., the output   #
#  .xtd trajectory files from Forcite). The forcefields commonly used are:                                    #
#          (1) "Dreiding"                                                                                     #
#          (2) "Dreiding_Dielectric_Const_78.4"                                                               #
#          (3) "Universal"                                                                                    #
#  The same forcefield that was used in Forcite/Blends should be used here.                                   #
#                                                                                                             #
#      Principal credit for the development of this script goes to Parveen Sood, a now-graduated student of   #
#  CNBT Lab at the Georgia Institute of Technology under Seung Soon Jang. Additional credit goes to Nicholas  #
#  Bond, an undergraduate researcher in CNBT Lab, for extensive script functionality improvements.            #
#                                                                                                             #
#  Copyright 2016 CNBT Lab. All rights reserved. Please use only with permission. If you believe you were     #
#  sent this file in error, please delete it and contact the sender.                                          #
#                                                                                                             #
###############################################################################################################

use strict;
use MaterialsScript qw(:all);

# Required input parameters:
'''

bottom =\
'''
# Optional: The naming convention of the output files can be customized:
my $outfile1 = "$dir/$monomer1 $monomer1.txt";
my $outfile2 = "$dir/$monomer1 $monomer2.txt";
my $outfile3 = "$dir/$monomer2 $monomer2.txt";
use strict;
use MaterialsScript qw(:all);
my $doc=$Documents{"$monomer1 $monomer1.xtd"};
my $trajectory = $Documents{"$monomer1 $monomer1.xtd"}->Trajectory;
my $fh;
for (my $i=1; $i<=$numframes; $i=$i+1){
    $trajectory->CurrentFrame = $i;
    my $copyDoc_Pair=$doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
    my $copyDoc_Frag_1=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
    my $copyDoc_Frag_2=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");
    my $Atom_Of_Frag_1 = $copyDoc_Frag_1->Atoms("Frag_1");
    my $fragment_1 = $Atom_Of_Frag_1->Fragment;
    my $Atom_Of_Frag_2 = $copyDoc_Frag_2->Atoms("Frag_2");
    my $fragment_2 = $Atom_Of_Frag_2->Fragment;
    $fragment_1->Delete;
    $fragment_2->Delete;
    my $Frag_2_Only=$copyDoc_Frag_1->SaveAs("./Frag_2_Only_Frame_$i.xsd");
    my $Frag_1_Only=$copyDoc_Frag_2->SaveAs("./Frag_1_Only_Frame_$i.xsd");
     my $forcite_Pair= Modules->Forcite;
     $forcite_Pair->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,
     WriteLevel => "Silent"]);
    my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair); #Settings is optional parameter for run function
    my $Etot_Pair=$copyDoc_Pair->PotentialEnergy;
    my $avField_Pair= Tools->AtomVolumesSurfaces->Connolly->Calculate($copyDoc_Pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Pair->IsVisible = "No";
    my $Iso_Surface_Pair=   $avField_Pair->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Pair=$Iso_Surface_Pair->EnclosedVolume;
     my $forcite_Frag_1= Modules->Forcite;
     $forcite_Frag_1->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);
    my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($Frag_1_Only); #Settings is optional parameter for run function
    my $Etot_Frag_1=$Frag_1_Only->PotentialEnergy;
    my $avField_Frag_1= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_1_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Frag_1->IsVisible = "No";
    my $Iso_Surface_Frag_1=   $avField_Frag_1->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_1=$Iso_Surface_Frag_1->EnclosedVolume;
     my $forcite_Frag_2= Modules->Forcite;
     $forcite_Frag_2->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);
    my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($Frag_2_Only); #Settings is optional parameter for run function
    #Extract the result: Need to write functionality to print it to a file
    my $Etot_Frag_2=$Frag_2_Only->PotentialEnergy;
    my $avField_Frag_2= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_2_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Frag_2->IsVisible = "No";
    my $Iso_Surface_Frag_2=   $avField_Frag_2->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_2=$Iso_Surface_Frag_2->EnclosedVolume;
  if ($i == 1) {
  open($fh, '>', $outfile1) or die "File not opened";
  printf $fh  "%22s %22s %22s %22s %22s %22s %22s\\n", "E_Pair (kcal/mol),","E_Frag_1 (kcal/mol),","E_Frag_2 (kcal/mol),","Del_E (kcal/mol),","CV_Pair (A^3),","CV_Frag_1 (A^3),","CV_Frag_2 (A^3)";
    }
    my $Del_E=$Etot_Pair-($Etot_Frag_1+$Etot_Frag_2);
    printf $fh "%22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f\\n", $Etot_Pair,$Etot_Frag_1,$Etot_Frag_2,$Del_E,$Connolly_Vol_Pair,$Connolly_Vol_Frag_1,$Connolly_Vol_Frag_2;
    $copyDoc_Pair->Delete;
    $copyDoc_Frag_1->Delete;
    $copyDoc_Frag_2->Delete;
    $Frag_1_Only->Delete;
    $Frag_2_Only->Delete;
}
my $doc=$Documents{"$monomer1 $monomer2.xtd"};
my $trajectory = $Documents{"$monomer1 $monomer2.xtd"}->Trajectory;
my $fh;
for (my $i=1; $i<=$numframes; $i=$i+1){
    $trajectory->CurrentFrame = $i;
    my $copyDoc_Pair=$doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
    my $copyDoc_Frag_1=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
    my $copyDoc_Frag_2=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");
    my $Atom_Of_Frag_1 = $copyDoc_Frag_1->Atoms("Frag_1");
    my $fragment_1 = $Atom_Of_Frag_1->Fragment;
    my $Atom_Of_Frag_2 = $copyDoc_Frag_2->Atoms("Frag_2");
    my $fragment_2 = $Atom_Of_Frag_2->Fragment;
    $fragment_1->Delete;
    $fragment_2->Delete;
    my $Frag_2_Only=$copyDoc_Frag_1->SaveAs("./Frag_2_Only_Frame_$i.xsd");
    my $Frag_1_Only=$copyDoc_Frag_2->SaveAs("./Frag_1_Only_Frame_$i.xsd");
     my $forcite_Pair= Modules->Forcite;
     $forcite_Pair->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,
     WriteLevel => "Silent"]);
    my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair); #Settings is optional parameter for run function
    my $Etot_Pair=$copyDoc_Pair->PotentialEnergy;
    my $avField_Pair= Tools->AtomVolumesSurfaces->Connolly->Calculate($copyDoc_Pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Pair->IsVisible = "No";
    my $Iso_Surface_Pair=   $avField_Pair->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Pair=$Iso_Surface_Pair->EnclosedVolume;
     my $forcite_Frag_1= Modules->Forcite;
     $forcite_Frag_1->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);
    my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($Frag_1_Only); #Settings is optional parameter for run function
    my $Etot_Frag_1=$Frag_1_Only->PotentialEnergy;
    my $avField_Frag_1= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_1_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Frag_1->IsVisible = "No";
    my $Iso_Surface_Frag_1=   $avField_Frag_1->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_1=$Iso_Surface_Frag_1->EnclosedVolume;
     my $forcite_Frag_2= Modules->Forcite;
     $forcite_Frag_2->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);
    my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($Frag_2_Only); #Settings is optional parameter for run function
    #Extract the result: Need to write functionality to print it to a file
    my $Etot_Frag_2=$Frag_2_Only->PotentialEnergy;
    my $avField_Frag_2= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_2_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Frag_2->IsVisible = "No";
    my $Iso_Surface_Frag_2=   $avField_Frag_2->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_2=$Iso_Surface_Frag_2->EnclosedVolume;
  if ($i == 1) {
  open($fh, '>', $outfile2) or die "File not opened";
  printf $fh  "%22s %22s %22s %22s %22s %22s %22s\\n", "E_Pair (kcal/mol),","E_Frag_1 (kcal/mol),","E_Frag_2 (kcal/mol),","Del_E (kcal/mol),","CV_Pair (A^3),","CV_Frag_1 (A^3),","CV_Frag_2 (A^3)";
    }
    my $Del_E=$Etot_Pair-($Etot_Frag_1+$Etot_Frag_2);
    printf $fh "%22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f\\n", $Etot_Pair,$Etot_Frag_1,$Etot_Frag_2,$Del_E,$Connolly_Vol_Pair,$Connolly_Vol_Frag_1,$Connolly_Vol_Frag_2;
    $copyDoc_Pair->Delete;
    $copyDoc_Frag_1->Delete;
    $copyDoc_Frag_2->Delete;
    $Frag_1_Only->Delete;
    $Frag_2_Only->Delete;
}
my $doc=$Documents{"$monomer2 $monomer2.xtd"};
my $trajectory = $Documents{"$monomer2 $monomer2.xtd"}->Trajectory;
my $fh;
for (my $i=1; $i<=$numframes; $i=$i+1){
    $trajectory->CurrentFrame = $i;
    my $copyDoc_Pair=$doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
    my $copyDoc_Frag_1=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
    my $copyDoc_Frag_2=$doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");
    my $Atom_Of_Frag_1 = $copyDoc_Frag_1->Atoms("Frag_1");
    my $fragment_1 = $Atom_Of_Frag_1->Fragment;
    my $Atom_Of_Frag_2 = $copyDoc_Frag_2->Atoms("Frag_2");
    my $fragment_2 = $Atom_Of_Frag_2->Fragment;
    $fragment_1->Delete;
    $fragment_2->Delete;
    my $Frag_2_Only=$copyDoc_Frag_1->SaveAs("./Frag_2_Only_Frame_$i.xsd");
    my $Frag_1_Only=$copyDoc_Frag_2->SaveAs("./Frag_1_Only_Frame_$i.xsd");
     my $forcite_Pair= Modules->Forcite;
     $forcite_Pair->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,
     WriteLevel => "Silent"]);
    my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair); #Settings is optional parameter for run function
    my $Etot_Pair=$copyDoc_Pair->PotentialEnergy;
    my $avField_Pair= Tools->AtomVolumesSurfaces->Connolly->Calculate($copyDoc_Pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Pair->IsVisible = "No";
    my $Iso_Surface_Pair=   $avField_Pair->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Pair=$Iso_Surface_Pair->EnclosedVolume;
     my $forcite_Frag_1= Modules->Forcite;
     $forcite_Frag_1->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);
    my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($Frag_1_Only); #Settings is optional parameter for run function
    my $Etot_Frag_1=$Frag_1_Only->PotentialEnergy;
    my $avField_Frag_1= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_1_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Frag_1->IsVisible = "No";
    my $Iso_Surface_Frag_1=   $avField_Frag_1->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_1=$Iso_Surface_Frag_1->EnclosedVolume;
     my $forcite_Frag_2= Modules->Forcite;
     $forcite_Frag_2->ChangeSettings([
     Quality => "Fine",
     CurrentForcefield => "$forcefield",
     ChargeAssignment => "Use current",MaxIterations=> 5000,WriteLevel => "Silent"]);
    my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($Frag_2_Only); #Settings is optional parameter for run function
    #Extract the result: Need to write functionality to print it to a file
    my $Etot_Frag_2=$Frag_2_Only->PotentialEnergy;
    my $avField_Frag_2= Tools->AtomVolumesSurfaces->Connolly->Calculate($Frag_2_Only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
       $avField_Frag_2->IsVisible = "No";
    my $Iso_Surface_Frag_2=   $avField_Frag_2->CreateIsosurface([IsoValue => 0,
                            HasFlippedNormals => "No"]);
    my $Connolly_Vol_Frag_2=$Iso_Surface_Frag_2->EnclosedVolume;
  if ($i == 1) {
  open($fh, '>', $outfile3) or die "File not opened";
  printf $fh  "%22s %22s %22s %22s %22s %22s %22s\\n", "E_Pair (kcal/mol),","E_Frag_1 (kcal/mol),","E_Frag_2 (kcal/mol),","Del_E (kcal/mol),","CV_Pair (A^3),","CV_Frag_1 (A^3),","CV_Frag_2 (A^3)";
    }
    my $Del_E=$Etot_Pair-($Etot_Frag_1+$Etot_Frag_2);
    printf $fh "%22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f\\n", $Etot_Pair,$Etot_Frag_1,$Etot_Frag_2,$Del_E,$Connolly_Vol_Pair,$Connolly_Vol_Frag_1,$Connolly_Vol_Frag_2;
    $copyDoc_Pair->Delete;
    $copyDoc_Frag_1->Delete;
    $copyDoc_Frag_2->Delete;
    $Frag_1_Only->Delete;
    $Frag_2_Only->Delete;
}
'''

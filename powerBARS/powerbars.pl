###############################################################################################################
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
#                                       �������������������������������                                       #
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
#  Copyright � 2016 CNBT Lab. All rights reserved. Please use only with permission. If you believe you were   #
#  sent this file in error, please delete it and contact the sender.                                          #
#                                                                                                             #
###############################################################################################################

use strict;
use MaterialsScript qw(:all);

# Required input parameters:

my $dir = '/Users/nick/cnbt/fall 2017/bars';
my $monomer1 = "A";
my $monomer2 = "B";
my $forcefield = "Dreiding";
my $numframes = 1000;
my $temperature = 298;

my @infile = (
    "$monomer1 $monomer1.xtd",
    "$monomer1 $monomer2.xtd",
    "$monomer2 $monomer2.xtd"
);

# Optional: The naming convention of the output files can be customized:

my @outfile = (
    "$dir\\$monomer1 $monomer1.txt",
    "$dir\\$monomer1 $monomer2.txt",
    "$dir\\$monomer2 $monomer2.txt"
);

my $fh;

for (my $fIndex = 0; $fIndex < scalar @infile; $fIndex++) {
    my $in  = $infile[$fIndex];
    my $out = $outfile[$fIndex];

    my $doc = $Documents{$in};
    my $trajectory = $Documents{$in}->Trajectory;

    open ($fh, '>', $out) or die "File not opened";
    printf $fh "%22s %22s %22s %22s %22s %22s %22s\n",
               "E_Pair (kcal/mol),",
               "E_Frag_1 (kcal/mol),",
               "E_Frag_2 (kcal/mol),",
               "Del_E (kcal/mol),",
               "CV_Pair (A^3),",
               "CV_Frag_1 (A^3),",
               "CV_Frag_2 (A^3)";

    for (my $i = 1; $i < $numframes + 1; $i++) {
        $trajectory->CurrentFrame = $i;

        my $copyDoc_Pair   = $doc->SaveAs("./Blends_Traj_Perl_Trial_Pair_Frame_$i.xsd");
        my $copyDoc_Frag_1 = $doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_1_Frame_$i.xsd");
        my $copyDoc_Frag_2 = $doc->SaveAs("./Blends_Traj_Perl_Trial_Frag_2_Frame_$i.xsd");

        $copyDoc_Frag_1->Atoms('Frag_1')->Fragment->Delete;
        $copyDoc_Frag_2->Atoms('Frag_2')->Fragment->Delete;

        my $copyDoc_Frag_1_Only = $copyDoc_Frag_2->SaveAs("./Frag_2_Only_Frame_$i.xsd");
        my $copyDoc_Frag_2_Only = $copyDoc_Frag_1->SaveAs("./Frag_1_Only_Frame_$i.xsd");

        #Pair

        my $forcite_Pair = Modules->Forcite;
        $forcite_Pair->ChangeSettings([
            Quality           => 'Fine',
            CurrentForcefield => "$forcefield",
            ChargeAssignment  => 'Use current',
            MaxIterations     => 5000,
            WriteLevel        => 'Silent',
            Temperature       => $temperature
        ]);

        my $results_Pair = $forcite_Pair->GeometryOptimization->Run($copyDoc_Pair);

        my $Etot_Pair = $copyDoc_Pair->PotentialEnergy;

        my $avField_Pair = Tools->AtomVolumesSurfaces->Connolly->Calculate(
            $copyDoc_Pair, Settings(
                ConnollyRadius => 1.0,
                GridInterval => 0.25
            )
        );
        $avField_Pair->IsVisible = 'No';

        my $Connolly_Vol_Pair = $avField_Pair->CreateIsosurface([
            IsoValue => 0,
            HasFlippedNormals => 'No'
        ])->EnclosedVolume;

        #Frag_1 only

        my $forcite_Frag_1 = Modules->Forcite;
        $forcite_Frag_1->ChangeSettings([
            Quality           => 'Fine',
            CurrentForcefield => "$forcefield",
            ChargeAssignment  => 'Use current',
            MaxIterations     => 5000,
            WriteLevel        => 'Silent',
            Temperature       => $temperature
        ]);

        my $results_Frag_1 = $forcite_Frag_1->GeometryOptimization->Run($copyDoc_Frag_1);

        my $Etot_Frag_1 = $copyDoc_Frag_1->PotentialEnergy;

        my $avField_Frag_1 = Tools->AtomVolumesSurfaces->Connolly->Calculate(
            $copyDoc_Frag_1, Settings(
                ConnollyRadius => 1.0,
                GridInterval => 0.25
            )
        );
        $avField_Frag_1->IsVisible = 'No';

        my $Connolly_Vol_Frag_1 = $avField_Frag_1->CreateIsosurface([
            IsoValue => 0,
            HasFlippedNormals => 'No'
        ])->EnclosedVolume;

        #Frag_2 only

        my $forcite_Frag_2 = Modules->Forcite;
        $forcite_Frag_2->ChangeSettings([
            Quality           => 'Fine',
            CurrentForcefield => "$forcefield",
            ChargeAssignment  => 'Use current',
            MaxIterations     => 5000,
            WriteLevel        => 'Silent',
            Temperature       => $temperature
        ]);

        my $results_Frag_2 = $forcite_Frag_2->GeometryOptimization->Run($copyDoc_Frag_2);

        my $Etot_Frag_2 = $copyDoc_Frag_2->PotentialEnergy;

        my $avField_Frag_2 = Tools->AtomVolumesSurfaces->Connolly->Calculate(
            $copyDoc_Frag_2, Settings(
                ConnollyRadius => 1.0,
                GridInterval => 0.25
            )
        );
        $avField_Frag_2->IsVisible = 'No';

        my $Connolly_Vol_Frag_2 = $avField_Frag_2->CreateIsosurface([
            IsoValue => 0,
            HasFlippedNormals => 'No'
        ])->EnclosedVolume;

        my $del_E = $Etot_Pair - ($Etot_Frag_1 + $Etot_Frag_2);

        print $fh "%22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f, %22.5f\n",
                  $Etot_Pair,
                  $Etot_Frag_1,
                  $Etot_Frag_2,
                  $Del_E,
                  $Connolly_Vol_Pair,
                  $Connolly_Vol_Frag_1,
                  $Connolly_Vol_Frag_2;

        $copyDoc_Pair->Delete;
        $copyDoc_Frag_1->Delete;
        $copyDoc_Frag_2->Delete;
        $Frag_1_Only->Delete;
        $Frag_2_Only->Delete;
    }
}

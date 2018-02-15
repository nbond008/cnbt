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
my $monomer1 = "4tbs-1";
my $monomer2 = "pi-1";
my $forcefield = "Dreiding";
my $numframes = 1000;
my $temperature = 298;

my @pairs = (
    "$monomer1 $monomer1",
    "$monomer1 $monomer2",
    "$monomer2 $monomer2"
);

for my $pair (@pairs) {
    my $current = $Documents{"$pair.xtd"};
    my $traj    = $Documents{"$pair.xtd"}->Trajectory;

    my $out = Documents->New("$pair.txt");
    $out->ClearContent;
    $out->Append(
        sprintf "%22s, %22s, %22s, %22s, %22s, %22s, %22s\n",
        "E_Pair (kcal/mol)",
        "E_Frag_1 (kcal/mol)",
        "E_Frag_2 (kcal/mol)",
        "Del_E (kcal/mol)",
        "CV_Pair (A^3)",
        "CV_Frag_1 (A^3)",
        "CV_Frag_2 (A^3)"
    );

    for (my $i = 1; $i <= $numframes; $i++) {
        $traj->CurrentFrame = $i;

        my $copy_pair   = $current->SaveAs("./blends_temp_pair_$i.xsd");
        my $copy_frag_1 = $current->SaveAs("./blends_temp_frag_1_$i.xsd");
        my $copy_frag_2 = $current->SaveAs("./blends_temp_frag_2_$i.xsd");

        eval {
            $copy_frag_1->Atoms("Frag_1")->Fragment->Delete;
            $copy_frag_2->Atoms("Frag_2")->Fragment->Delete;
        }; if ($@) {
            print "$pair.xtd has not been renamed.\n";
            next;
        }

        my $frag_2_only = $copy_frag_1->SaveAs("./frag_2_only_$i.xsd");
        my $frag_1_only = $copy_frag_2->SaveAs("./frag_1_only_$i.xsd");

        $copy_frag_1->Close;
        $copy_frag_1->Delete;
        $copy_frag_2->Close;
        $copy_frag_2->Delete;

        my $forcite_pair = Modules->Forcite;
        $forcite_pair->ChangeSettings([
            Quality => "Fine",
            CurrentForcefield => "$forcefield",
            ChargeAssignment => "Use current",
            MaxIterations=> 5000,
            WriteLevel => "Silent"
        ]);

        my $results_pair      = $forcite_pair->GeometryOptimization->Run($copy_pair);
        my $Etot_pair         = $copy_pair->PotentialEnergy;
        my $avfield_pair      = Tools->AtomVolumesSurfaces->Connolly->Calculate($copy_pair, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
        $avfield_pair->IsVisible = "No";

        my $iso_surface_pair  = $avfield_pair->CreateIsosurface([IsoValue => 0, HasFlippedNormals => "No"]);
        my $connolly_vol_pair = $iso_surface_pair->EnclosedVolume;

        $copy_pair->Close;
        $copy_pair->Delete;

        my $forcite_frag_1 = Modules->Forcite;
        $forcite_frag_1->ChangeSettings([
            Quality => "Fine",
            CurrentForcefield => "$forcefield",
            ChargeAssignment => "Use current",
            MaxIterations=> 5000,
            WriteLevel => "Silent"
        ]);

        my $results_frag_1      = $forcite_frag_1->GeometryOptimization->Run($frag_1_only);
        my $Etot_frag_1         = $frag_1_only->PotentialEnergy;
        my $avfield_frag_1      = Tools->AtomVolumesSurfaces->Connolly->Calculate($frag_1_only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
        $avfield_frag_1->IsVisible = "No";

        my $iso_surface_frag_1  = $avfield_frag_1->CreateIsosurface([IsoValue => 0, HasFlippedNormals => "No"]);
        my $connolly_vol_frag_1 = $iso_surface_frag_1->EnclosedVolume;

        $frag_1_only->Close;
        $frag_1_only->Delete;

        my $forcite_frag_2 = Modules->Forcite;
        $forcite_frag_2->ChangeSettings([
            Quality => "Fine",
            CurrentForcefield => "$forcefield",
            ChargeAssignment => "Use current",
            MaxIterations=> 5000,
            WriteLevel => "Silent"
        ]);

        my $results_frag_2      = $forcite_frag_2->GeometryOptimization->Run($frag_2_only);
        my $Etot_frag_2         = $frag_2_only->PotentialEnergy;
        my $avfield_frag_2      = Tools->AtomVolumesSurfaces->Connolly->Calculate($frag_2_only, Settings(ConnollyRadius => 1.0, GridInterval => 0.25));
        $avfield_frag_2->IsVisible = "No";

        my $iso_surface_frag_2  = $avfield_frag_2->CreateIsosurface([IsoValue => 0, HasFlippedNormals => "No"]);
        my $connolly_vol_frag_2 = $iso_surface_frag_2->EnclosedVolume;

        $frag_2_only->Close;
        $frag_2_only->Delete;

        $out->Append(
            sprintf "%22s, %22s, %22s, %22s, %22s, %22s, %22s\n",
            $Etot_pair,
            $Etot_frag_1,
            $Etot_frag_2,
            $Etot_pair - ($Etot_frag_1 + $Etot_frag_2),
            $connolly_vol_pair,
            $connolly_vol_frag_1,
            $connolly_vol_frag_2
        );
    }

    $out->Close;
}

exit(0);

use strict;
use warnings;
#use MaterialsScript qw(:all);

my $dir_blends       = '/Users/nick/cnbt/fall 2017/shaker-test';
my $dir_forcite      = '/Users/nick/cnbt/fall 2017';
my $experiment_group = '1_Baseline';

my $base   = '4tbs-1';
my $screen = 'pi-1';

my $forcefield           = 'Dreiding';
my $energy_samples       = 1000000;
my $lowest_energy_frames = 1000;
my $temperature          = 298;

my $num_runs = 5;

print "Creating directory $dir_blends/$experiment_group...\n";

eval {
    if (-e "$dir_blends/$experiment_group") {
        print "Directory already exists.\n";
    } else {
        mkdir "$dir_blends/$experiment_group";
        print "Successfully created directory.\n"
    }
};
die "Failed to create directory. Aborting...\n" if $@;

my $run_paren = "";

BLENDS_LOOP:
for (my $run = 1; $run < $num_runs + 1; $run++) {
    if ($run > 1) {
        $run_paren = " ($run)";
    }

    my $temp = "$dir_blends/$experiment_group/$base Blends Mixing$run_paren";

    print "Creating directory $temp...\n";

    eval {
        if (-e "$temp") {
            print "Directory already exists.\n";
        } else {
            mkdir "$temp";
            print "Successfully created directory.\n"
        }
    };
    if ($@) {
        print "Failed to create directory. Aborting...\n";
        next BLENDS_LOOP;
    }
}

#!/usr/bin/env perl

use strict;
use warnings;

use File::Find;
use File::Spec;
use File::Basename;

my $Usage = <<"EOT";
Usage: $0 top_dir

For every review in top_dir, add the stars from the 'info' file to the
'features' file, add normalized sentiment features to the 'features' file
and add a binary judgement to the 'features' file.
EOT

if ( scalar @ARGV == 0 ) {
    print "$Usage" and exit;
}

my $top_dir = $ARGV[0];

# $dir is the directory this script resides in.
my $dir = dirname($0);

# These three scripts must reside in $dir.
our $stars_to_features = File::Spec->rel2abs("$dir/stars_to_features.sh");
our $normalize_features = File::Spec->rel2abs("$dir/normalize_features.sh");
our $add_binary_judgement = File::Spec->rel2abs("$dir/add_binary_judgement.sh");

sub features {
    if ($_ eq 'features') {
        system($stars_to_features, "info", $_);
        system($normalize_features, $_);
        system($add_binary_judgement, $_);
    }
}

find({ wanted => \&features, follow_fast => 1} , $top_dir);

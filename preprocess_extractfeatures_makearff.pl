#!/usr/bin/env perl

use strict;
use warnings;

use File::Find;
use File::Basename;
use Getopt::Long;
use autodie qw(:all);

our $chunk_dir = '';
our $sentiws = 'SentiWS.txt';
our $verbose = 0;
our $help = 0;

my $Usage = <<"EOT";
Usage: $0 [OPTIONS] top-dir arff-name

Preprocess Amazon reviews residing in top-dir, extract features from them,
arrange them in balanced and randomized chunks and create an ARFF file from
them, which is called arff-name.

OPTIONS
    -c, --chunk-dir
        The name of the directory that is created as the top level directory
            for the review chunks.
    -s, --sentiws
        The name of the SentiWS file used for computing sentiment features.
            The default is a file named 'SentiWS.txt' in the current
            working directory.
    -v, --verbose
        Print some information about what is currently done.
    -h, --help
        Print this help message.
EOT

GetOptions(
    'chunk-dir|c=s' => \$chunk_dir,
    'sentiws|s=s' => \$sentiws,
    'verbose|v' => \$verbose,
    'help|h' => \$help
) or die "$Usage";

if ( $help or scalar @ARGV == 0 ) {
    print "$Usage" and exit;
}

# $dir is the directory this script resides in.
my $dir = dirname($0);

# Scripts that are needed.
our $preprocess = "$dir/preprocessing/preprocess.sh";
our $chunk = "$dir/review_chunking/make_chunks.pl";
our $extract_features = "$dir/feature_extraction/write_features.sh";
our $add_features = "$dir/feature_extraction/add_additional_features.pl";
our $create_arff = "$dir/feature_extraction/arff_data.py";

# These features will be in the resulting arff file.
our @features = qw(
    normalized_overall_sentiment
    normalized_verb_sentiment
    normalized_noun_sentiment
    normalized_adjective_sentiment
    token_number
    stars
);

sub main {
    my $top_dir = shift;
    my $arff_name = shift;
    $chunk_dir = "${top_dir}_chunks" unless $chunk_dir;
    
    # Preprocess the review content.
    $verbose && print "Preprocessing the review content ...\n";
    `$preprocess $top_dir content 2>&1 1>/dev/null`;

    # Arrange reviews in chunks.
    $verbose && print "Chunking the reviews ...\n";
    system('perl', $chunk,
        '--housing-dir', 'reviews',
        '--chunk-size', '50',
        '--balance',
        $top_dir,
        $chunk_dir);

    # Extract features from preprocessed content.
    $verbose && print "Extracting features ...\n";
    system($extract_features, 'overwrite', $sentiws, $chunk_dir);

    # Add additional features.
    $verbose && print "Adding more features ...\n";
    system($add_features, $chunk_dir);

    # Create arff file from 'features' files.
    $verbose && print "Creating arff file ...\n";
    system($create_arff, $chunk_dir, $arff_name, @features);
}

main @ARGV;

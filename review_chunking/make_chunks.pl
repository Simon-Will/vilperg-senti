#!/usr/bin/env perl

use strict;
use warnings;

use File::Find;
use File::Basename;
use Getopt::Long;
use Set::Scalar;

our $without = '';
our $housing_dir = '';
our $chunk_size = 0;
my $help = 0;

my $Usage = <<"EOT";
Usage: $0 [OPTIONS] top-dir out-dir

Create links to files in housing-dir under top-dir and randomly put them into
directories under out-dir.

OPTIONS
    -d, --housing-dir
        The name of the directories that house the files to which symbolic
            links are to be created.
    -w, --without
        A file containing the full path to files that are to be ignored by
            this script.
    -c, --chunk-size
        The number of links that are to be grouped together in one directory.
    -h, --help
        Print this help message.
EOT

GetOptions(
    'housing-dir|d=s' => \$housing_dir,
    'without|w=s' => \$without,
    'chunk-size|c=i' => \$chunk_size,
    'help|h'             => \$help
) or die "$Usage";

if ( $help or scalar @ARGV == 0 ) {
    print "$Usage" and exit;
}

sub main {
    my $top_dir = shift;
    my $out_dir = shift;

    # The files that are to be excluded.
    my $without_files = Set::Scalar->new();
    if ($without) {
        open my $fh, '<', $without or die "Could not read file: $without ($!)";
        $without_files->insert(map {chomp; $_} <$fh>);
        close $fh;
    }

    # The files that are to be written in chunks.
    my @files;

    if ($housing_dir) {
        # The directories the files that are to be written in chunks live in.
        my @housing_dirs;
        find({ wanted => sub { push @housing_dirs, $File::Find::fullname if -d and $_ eq $housing_dir }, follow_fast => 1 }, $top_dir);
        for my $hd (@housing_dirs) {
            # Pushing files to the @files array.
            find_files(\@files, $without_files, $hd);
        }
    }
    else {
        # Pushing files to the @files array.
        find_files(\@files, $without_files, $top_dir);
    }

    # Dividing the files into chunks.
    my @chunks;

    while (scalar @files > $chunk_size) {
        my @chunk  = random_sublist(\@files, $chunk_size);
        push @chunks, \@chunk;
    }
    push @chunks, \@files;

    mkdir $out_dir unless -d $out_dir;
    # Create symlinks.
    for (my $i = 0; $i < scalar @chunks; ++$i) {
        my $chunk_dir = "$out_dir/$i";
        mkdir $chunk_dir unless -d $chunk_dir;
        for my $f (@{$chunks[$i]}) {
            my $b = basename($f);
            #print "Make link: $chunk_dir/$b\n";
            symlink($f, "$chunk_dir/$b");
        }
    }
}

sub find_files {
    my $files = shift;
    my $without_files = shift;
    my $top_dir = shift;
    opendir(my $dh, $top_dir);
    push @$files, map {"$top_dir/$_"} (grep { my $f = File::Spec->rel2abs($_); not $_ =~ /^\.{1,2}$/ or $without_files->has($f) } readdir $dh);
}

sub random_sublist {
    my $list = shift;
    my $size = shift;

    if (scalar $list <= $size) {
        return $list 
    }
    else {
        my @range = reverse (@$list - $size .. @$list-1);
        return map {splice @$list, rand($_), 1} @range;
    }
}

main @ARGV;

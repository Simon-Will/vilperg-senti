#!/usr/bin/env perl

use strict;
use warnings;

use File::Find;
use File::Basename;
use Getopt::Long;
use Set::Scalar;
use POSIX qw(strftime);
use List::Util qw(shuffle);

our $without = '';
our $housing_dir = '';
our $chunk_size = 0;
our $balance = 0;
our $star_line = 3;
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
    -b, --balance
        With this switch, the reviews are balanced with respect to their
            star number. This means that in every chunk directory, there are
            chunk-size/5 files of each star number.
    -s, --star-line
        The line number of the line containing the stars in the info file.
    -h, --help
        Print this help message.
EOT

GetOptions(
    'housing-dir|d=s' => \$housing_dir,
    'without|w=s' => \$without,
    'chunk-size|c=i' => \$chunk_size,
    'star-line|s=i' => \$star_line,
    'balance|b' => \$balance,
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

    # Randomize files.
    my @rand_files = shuffle(@files);

    # Dividing the files into chunks.
    my @chunks;
    if ($balance) {
        my %star_files = get_star_files(\@rand_files, $star_line);
        while (@{$star_files{1}}) {
            my @chunk;
            for (keys %star_files) {
                push @chunk, splice(@{$star_files{$_}}, 0, $chunk_size/5);
            }
            push @chunks, \@chunk;
        }
    }
    else {
        while (@rand_files) {
            my @chunk = splice(@rand_files, 0, $chunk_size);
            push @chunks, \@chunk;
        }
    }

    #print "Chunks: ", join("\n", @chunks), "\n";
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
    # top_dir shuould be an absoulute path
    opendir(my $dh, $top_dir);
    push @$files, map {"$top_dir/$_"} (grep { my $f = "$top_dir/$_"; print "$f\n"; not ($_ =~ /^\.{1,2}$/ or $without_files->has($f)) } readdir $dh);
}

sub random_sublist {
    my $list = shift;
    my $size = shift;

    if ((scalar @$list) <= $size) {
        return @$list;
    }
    else {
        my @range = reverse (@$list - $size .. @$list-1);
        return map {splice @$list, rand($_), 1} @range;
    }
}

sub get_star_files {
    my $files = shift;
    my $info_line = shift;
    my $total = scalar @$files;

    # Hash mapping star number to their frequencies.
    my %stars = (
        1 => 0,
        2 => 0,
        3 => 0,
        4 => 0,
        5 => 0
    );

    # Build hash mapping star number to the respective files.
    my @files1;
    my @files2;
    my @files3;
    my @files4;
    my @files5;
    my %star_files = (
        1 => \@files1,
        2 => \@files2,
        3 => \@files3,
        4 => \@files4,
        5 => \@files5
    );
    # Fill the hash.
    for my $f (@$files) {
        open my $fh, '<', "$f/info";
        my @lines = map {chomp; $_} <$fh>;
        close $fh;
        my $star_number = int($lines[$info_line-1]) or
            print "Error in star conversion in review $f ($!)";
        ++$stars{$star_number};
        push @{$star_files{$star_number}}, $f;
    }

    if ( my @invalid = grep {my $key = $_; not grep {$_ == $key} (1,2,3,4,5)}
        keys %stars ) {
        die "Invalid keys in star hash (@invalid)";
    }

    my $min_stars = $stars{1};
    $min_stars = $stars{$_} < $min_stars ? $stars{$_} : $min_stars for keys %stars;

    # Cut the lists to the same size.
    while (my ($star_num, $file_list) = each %star_files) {
        my $len = scalar @$file_list;
        splice(@$file_list, $min_stars - 1, $len - $min_stars);
    }

    return %star_files;
}

sub printHash {
    my $h = shift;
    for (keys %$h) {
        print "$_: $h->{$_}\n";
    }
}

main @ARGV;

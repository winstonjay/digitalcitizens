#!/usr/bin/env perl
=pod
newpost.pl:
Create a new jekyl post with front matter in `_posts/` or `_drafts/`.
USE:
        $ perl newpost.pl
    Then follow the prompted instructions. Blank values ok but
=cut
use strict;
use warnings;
use Time::Piece;

# Set date as the local now.
my $fulldate = localtime->strftime('%Y-%m-%d %T %z');

# Get input values...
print "Title: "; chomp(my $title = <STDIN>);
print "Draft?(y/n): "; my $dir = <STDIN> eq "y\n" ? "_drafts" : "_posts";

# Format title, replace spaces with dashes but you still cant be silly
# and put stuff that would be nightmare filenames.
(my $filename = lc "$dir/".((split ' ', $fulldate)[0])."-$title.md") =~ s/\s+/-/g;

# Write info to file...
open(my $fn, '>', $filename) or die "Couldn't open file '$filename' $!";
print $fn <<"CONTENT";
---
layout: post
title:  "$title"
date:   $fulldate
---
Content goes here...
CONTENT
close $fn;

# We done...give some encouragement for the future.
print "Created:\n\t$filename\n\nGood luck with your new post!\n";
#!/usr/bin/env perl
=pod
newpost.pl:
Create a new jekyl post with front matter in `_posts/` or `_drafts/`.
USE:
        $ perl newpost.pl
    Then follow the prompted instructions. Blank values ok.
    Try to keep filenames short. You can update them later in the post.
=cut
use strict;
use warnings;
use Time::Piece;

# Set date as the local now.
my $fulldate = localtime->strftime('%Y-%m-%d %T %z');

# Get input values...
print "Title: "; chomp(my $title = <STDIN>);
print "Draft?(y/n): "; my $dir = <STDIN> eq "y\n" ? "_drafts" : "_posts";

# Format title, replace spaces with dashes and remove any non alpha numeric
(my $cleanedtitle = lc $title) =~ s/\s+/-/g;
$cleanedtitle =~ s/[^a-zA-Z0-9-_]+//g;

# create a directory for the posts img/media assets to go into.

my $assetdir = 'assets/imgs/'.$cleanedtitle;
if (! -e $assetdir) {
    unless(mkdir $assetdir) {
        die "Unable to create $assetdir\n";
    }
}

# make the full file path for the post template to go into and write the info
# into the file.
my $filename = "$dir/" . ((split ' ', $fulldate)[0]) . "-$cleanedtitle.md";

open(my $fn, '>', $filename) or die "Couldn't open file '$filename' $!";
print $fn <<"CONTENT";
---
layout: post
title:  "$title"
date:   $fulldate
---
**TODO:** Post intro goes here...

{% assign static_path = "$assetdir" | absolute_url %}

**TODO:** Post body goes here..
CONTENT
close $fn;

# say what we did then we are done...
# give some encouragement for the future.
print "Created...\n\ttitle: $title\n\tfile:  $filename\n\tdir:   $assetdir/\n";
print "Good luck with your new post!\n";
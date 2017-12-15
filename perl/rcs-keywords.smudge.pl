#!/usr/bin/perl
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$

# @brief  Git filter to implement rcs keyword expansion as seen in cvs and svn.
# @author Martin Turon

# Copyright (c) 2009-2011 Turon Technologies, Inc.  All rights reserved.
# Modified by David Rotthoff, vAuto, Inc.

# Impacted during checkout of new files by not having the commit data
# readily available during the smudge operation (so git log returns a
# null string).  Adding HEAD to the git log command to see if it will
# correctly identify the relevant commit point.

# Look at possibly using a post-checkout or post-merge hook instead!

use MIME::Base64;

$filter_debug = 0;

# Base64 encoded keyword strings.print STDERR "Started RCS smudge";
$id_decode=decode_base64('SWQ=');
$date_decode=decode_base64('RGF0ZQ==');
$author_decode=decode_base64('QXV0aG9y');
$source_decode=decode_base64('U291cmNl');
$file_decode=decode_base64('RmlsZQ==');
$revision_decode=decode_base64('UmV2aXNpb24=');
$rev_decode=decode_base64('UmV2');
$hash_decode=decode_base64('SGFzaA==');

#if ($filter_debug) {
#  print STDERR "Filter debug: $filter_debug\n";
#  print STDERR "id_decode: $id_decode\n";
#  print STDERR "date_decode: $date_decode\n";
#  print STDERR "author_decode: $author_decode\n";
#  print STDERR "source_decode: $source_decode\n";
#  print STDERR "file_decode: $file_decode\n";
#  print STDERR "revision_decode: $revision_decode\n";
#  print STDERR "rev_decode: $rev_decode\n";
#  print STDERR "hash_decode: $hash_decode\n";
#}

# Capture the source file name and path
$path = shift;
$path =~ /.*\/(.*)/;
$filename = $1;
if (0 == length($filename)) {
	$filename = $path;
}

print STDERR "Started RCS smudge of $filename\n";

# If debugging, list the local branches available
if ($filter_debug) {
  $branch = `git branch --list`;
  print STDERR "Return code: ${^CHILD_ERROR_NATIVE}\n";
  print STDERR "Local branch: $branch\n";
}

# Calculate the rcs keyword values from git log
#$rev = `git log --date=iso8601 -- $path | head -n 3`;
$rev = `git log --date=iso8601 --max-count=1 -- $path`;
if ($rev eq '') {
  if ($filter_debug) {
    print STDERR "Return code: $?\n";
    print STDERR "Return code: ${^CHILD_ERROR_NATIVE}\n";
    print STDERR "Rev: $rev\n";
    print STDERR "String rev is empty\n";
    $rev = `git log --date=iso8601 --max-count=5 --`;
    print STDERR "Rev: $rev\n";
  }
  $rev = `git log --date=iso8601 --max-count=1 --`;
}

if ($filter_debug) {
  $rev = `git log --date=iso8601 --max-count=1 --`;
  print STDERR "Return code: $?\n";
  print STDERR "Return code: ${^CHILD_ERROR_NATIVE}\n";
  print STDERR "Rev: $rev\n";
}

$rev =~ /^Author:\s*(.*)\s*$/m;
$author = $1;
$author =~ /\s*(.*)\s*<.*/;
$name = $1;
$rev =~ /^Date:\s*(.*)\s*$/m;
$date = $1;
$rev =~ /^commit (.*)$/m;
$ident = $1;

if ($filter_debug) {
  print STDERR "Filename: $filename\n";
  print STDERR "Path: $path\n";
  print STDERR "Date: $date\n";
  print STDERR "Author: $author\n";
  print STDERR "Name: $name\n";
  print STDERR "Ident: $ident\n";
}

# Process each line from STDIN to insert the defined substitutions
while (<STDIN>) {
    s/\$$date_decode\$/\$$date_decode:     $date \$/;
    s/\$$author_decode\$/\$$author_decode:   $author \$/;
    s/\$$id_decode\$/\$$id_decode:       $filename | $date | $name \$/;
    s/\$$file_decode\$/\$$file_decode:     $filename \$/;
    s/\$$source_decode\$/\$$source_decode:   $path \$/;
    s/\$$revision_decode\$/\$$revision_decode: $date \$/;
    s/\$$rev_decode\$/\$$rev_decode:      $date \$/;
    s/\$$hash_decode\$/\$$hash_decode:     $ident \$/;
} continue {
    print or die "-p destination: $!\n";
}

print STDERR "Completed RCS smudge of $filename\n\n";

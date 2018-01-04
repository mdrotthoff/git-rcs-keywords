#!/usr/bin/perl
# $Author$
# $Date$
# $File$
# $Rev$
# $Source$
# $Hash$
# $Id$

# @brief  Git filter to implement rcs keyword expansion as seen in cvs and svn.
# @author Martin Turon

# Copyright (c) 2009-2011 Turon Technologies, Inc.  All rights reserved.
# Modified by David Rotthoff, vAuto, Inc.

use MIME::Base64;

print STDERR "Started RCS clean\n";

#$filter_debug = 0;

# Base64 encoded keyword strings.
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

# Process each line from STDIN to remove the defined substitutions
while (<STDIN>) {
  s/\$$id_decode:[^\$]*\$/\$$id_decode\$/;
  s/\$$date_decode:[^\$]*\$/\$$date_decode\$/;
  s/\$$author_decode:[^\$]*\$/\$$author_decode\$/;
  s/\$$source_decode:[^\$]*\$/\$$source_decode\$/;
  s/\$$file_decode:[^\$]*\$/\$$file_decode\$/;
  s/\$$revision_decode:[^\$]*\$/\$$revision_decode\$/;
  s/\$$rev_decode:[^\$]*\$/\$$rev_decode\$/;
  s/\$$hash_decode:[^\$]*\$/\$$hash_decode\$/;
} continue {
    print or die "-p destination: $!\n";
}

print STDERR "Completed RCS clean\n";

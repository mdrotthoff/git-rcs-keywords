#!/usr/bin/perl
# $Author$
# $Date$
# $File$
# $Rev$
# $Source$
# $Hash$
# $Id$
#
# @brief  Simple perl program to generate variables from base64 encoded strings for use with
#         rcs-keyword expansion filters.

# @author David Rotthoff

use MIME::Base64;

$id_str=encode_base64('Id');
chomp($id_str);
print "\$id_decode=decode_base64('$id_str');\n";

$date_str=encode_base64('Date');
chomp($date_str);
print "\$date_decode=decode_base64('$date_str');\n";

$author_str=encode_base64('Author');
chomp($author_str);
print "\$author_decode=decode_base64('$author_str');\n";

$source_str=encode_base64('Source');
chomp($source_str);
print "\$source_decode=decode_base64('$source_str');\n";

$file_str=encode_base64('File');
chomp($file_str);
print "\$file_decode=decode_base64('$file_str');\n";

$revision_str=encode_base64('Revision');
chomp($revision_str);
print "\$revision_decode=decode_base64('$revision_str');\n";

$rev_str=encode_base64('Rev');
chomp($rev_str);
print "\$rev_decode=decode_base64('$rev_str');\n";

$hash_str=encode_base64('Hash');
chomp($hash_str);
print "\$hash_decode=decode_base64('$hash_str');\n";

print "\n";

# Decode the hash values
$id_decode=decode_base64('SWQ=');
$date_decode=decode_base64('RGF0ZQ==');
$author_decode=decode_base64('QXV0aG9y');
$source_decode=decode_base64('U291cmNl');
$file_decode=decode_base64('RmlsZQ==');
$revision_decode=decode_base64('UmV2aXNpb24=');
$hash_decode=decode_base64('SGFzaA==');

# Print the hash values
print "ID: $id_decode\n";
print "Date: $date_decode\n";
print "Author: $author_decode\n";
print "Source: $source_decode\n";
print "File: $file_decode\n";
print "Revision: $revision_decode\n";
print "Hash: $hash_decode\n";

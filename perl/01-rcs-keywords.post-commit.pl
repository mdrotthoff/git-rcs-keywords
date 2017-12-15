#!/usr/bin/perl

# git configuration script
#	 $Id$
#	 $Date$
#	 $File$
#	 $Author$
#	 $Rev$
#	 $Source$

print "***** POST-COMMIT hook started *****\n";

@file_list=`git diff-tree HEAD~1 HEAD --name-only -r --diff-filter=ACMRT`;

foreach my $file (@file_list) {
  chomp(my $source = $file);
  print STDERR "Starting commit of file $file\n";
  if ( !-e "$source") {
    die "File $source not found!\n";
  }

# Skip any source that is a directory (we can't remove it)
  if ( -d $source ) {
  	print STDERR "Directory $source skipped";
  } else {
    unlink "$source" or warn "Could not remove file $source -- error: $!";
    if ( -e "$source") {
      die "File $source was NOT removed\n"
    }

    system("git checkout -- $source");
    if ( $? == -1 ) {
      die "git checkout command failed\n";
    } elsif (($? >> 8) != 0) {
      die "Command exited with status code %d\n", $? >> 8;
    }
    if ( !-e "$source") {
      die "File $source was NOT restored\n";
    }
    print STDERR "Competed commit of file %$file\n";
  }
}

print "***** POST-COMMIT hook complete *****\n";

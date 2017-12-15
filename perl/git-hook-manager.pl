#!/usr/bin/perl
# $Author$
# $Date$
# $File$
# $Rev$
# $Source$
# $Hash$
# $Id$

use File::Basename;

# Determine what hook we were called as
$prog_name=$0;
print STDERR "Full program name: $prog_name\n";
$hook_name=basename($prog_name);
print STDERR "Base hook name: $hook_name\n";
$curr_dir="$ENV{'PWD'}";
print STDERR "Current directory: $curr_dir\n";
### NOTE:  The environment variable GIT_DIR is not always set for all hooks!!!!

# get total arg passed to this script
my $total = $#ARGV + 1;
my $counter = 1;

# Use loop to print all args stored in an array called @ARGV
foreach my $a(@ARGV) {
	print STDERR "Param$counter: $a\n";
	$counter++;
}

# If no directory for the hooks, then print a message and exit
print STDERR "git-hook-manager running $hook_name hooks\n";
$hook_dir="$ENV{'GIT_DIR'}/hooks/$hook_name.d";
if ( !-d "$hook_dir") {
  print "No directory $hook_dir found\n";
  $hook_dir=dirname($0);
  $hook_dir="${hook_dir}/${hook_name}.d";
  print "Alternate hook directory is $hook_dir\n";
  if ( !-d "$hook_dir") {
    print "No alternate directory $hook_dir found\n";
    system("/usr/bin/env");
    exit(0)
  }
}
print STDERR "Hook directory name: $hook_dir\n";

opendir(my $dir_handle, $hook_dir) || die "Can't open hook directory $hook_dir\n";
@files = sort { $a cmp $b } readdir($dir_handle);

while (my $file =  shift @files) {
  print STDERR "Evaluating hook $hook_dir/$file\n";
# We only want executable files
  next unless (-x "$hook_dir/$file");
# Use a regular expression to ignore files the standard dot files
  next if ($file =~ m/^\.[\.]*/);

# Execute the defined hook
  print STDERR "Executing: $hook_dir/$file\n";
  system("$hook_dir/$file");
  if ( $? == -1 ) {
    die "git post-commit command failed for $file\n";
  } elsif (($? >> 8) != 0) {
    die "Command exited with status code %d on file $file\n", $? >> 8;
  }
}

closedir($dir_handle);

print STDERR "git-hook-manager completed $hook_name hooks\n";
print STDERR "\n";

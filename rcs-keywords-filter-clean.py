#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$

import sys
import os
import re
import subprocess
import time

# Set the debugging flag
summary_flag = bool(True)
verbose_flag = bool(True)
timing_flag = bool(False)
debug_flag = bool(False)
if debug_flag:
    timing_flag = bool(True)
if timing_flag:
    verbose_flag = bool(True)
if verbose_flag:
    summary_flag = bool(True)

# Set the start time for calculating elapsed time
if timing_flag:
    start_time = time.clock()

# Parameter processing
program_name = str(sys.argv[0])
(hook_path, hook_name) = os.path.split(program_name)
if debug_flag:
    sys.stderr.write('************ START **************\n')
    sys.stderr.write('Filter program: %s\n' % str(program_name))
    sys.stderr.write('Hook path: %s\n' % str(hook_path))
    sys.stderr.write('Hook name: %s\n' % str(hook_name))
    sys.stderr.write('*********************************\n')
        
# Calculate the source file being cleaned (if provided)
if len(sys.argv) > 1:
    file_full_name = sys.argv[1]
    (file_path, file_name) = os.path.split(file_full_name)
else:
    file_full_name = 'Not provided'
    file_path = 'Not provided'
    file_name= 'Not provided'

# Output the program name start
if summary_flag:
    sys.stderr.write('Start program name: %s file: %s\n' % (str(program_name), str(file_full_name)))

# List the provided parameters
if verbose_flag:
    sys.stderr.write("  Parameter list\n")
    param_num = 0
    for param in sys.argv:
        sys.stderr.write('    Param[%d]: %s\n' % (param_num, sys.argv[param_num]))
        param_num = param_num + 1

# Show the OS environment variables
if debug_flag:
    sys.stderr.write('  Environment variables defined\n')
    for key, value in sorted(os.environ.items()):
        sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
    sys.stderr.write("\n")
        
# Display the name of the file being cleaned
if verbose_flag:
    sys.stderr.write('  Clean file full name: %s\n' % str(file_full_name))
if debug_flag:
    sys.stderr.write('  Clean file path: %s\n' % str(file_path))
    sys.stderr.write('  Clean file name: %s\n' % str(file_name))
    sys.stderr.write("\n")

# Define the various substitution regular expressions 
author_regex = re.compile("\$Author: +[.\w@<> ]+ +\$|\$Author\$", re.IGNORECASE)
id_regex = re.compile("\$Id: +.+ \| [-:\d ]+ \| .+ +\$|\$Id\$", re.IGNORECASE)
date_regex = re.compile("\$Date: +[-:\d ]+ +\$|\$Date\$", re.IGNORECASE)
source_regex = re.compile("\$Source: .+[.].+ \$|\$Source\$", re.IGNORECASE)
file_regex = re.compile("\$File: .+[.].+ \$|\$File\$", re.IGNORECASE)
revision_regex = re.compile("\$Revision: +[-:\d ]+ +\$|\$Revision\$", re.IGNORECASE)
rev_regex = re.compile("\$Rev: +[-:\d ]+ +\$|\$Rev\$", re.IGNORECASE)
hash_regex = re.compile("\$Hash: +\w+ +\$|\$Hash\$", re.IGNORECASE)
     
# Calculate empty strings based on the keyword
git_hash = '$%s$' % 'Hash'
git_author = '$%s$' % 'Author'
git_date = '$%s$' % 'Date'
git_rev = '$%s$' % 'Rev'
git_revision = '$%s$' % 'Revision'
git_file = '$%s$' % 'File'
git_source = '$%s$' % 'Source'
git_id = '$%s$' % 'Id'
     
# Display the cleaning values (debugging)
if debug_flag:
    sys.stderr.write('git hash:     %s\n' % git_hash)
    sys.stderr.write('git author:   %s\n' % git_author)
    sys.stderr.write('git date:     %s\n' % git_date)
    sys.stderr.write('git rev:      %s\n' % git_rev)
    sys.stderr.write('git revision: %s\n' % git_revision)
    sys.stderr.write('git file:     %s\n' % git_file)
    sys.stderr.write('git source:   %s\n' % git_source)
    sys.stderr.write('git id:       %s\n' % git_id)
    sys.stderr.write("\n")

# Calculate the setup elapsed time
if timing_flag:
    setup_time = time.clock()

# Process each of the rows found on stdin
line_count = 0
for line in sys.stdin:
    line_count = line_count + 1
    line = author_regex.sub(git_author, line)
    line = id_regex.sub(git_id, line)
    line = date_regex.sub(git_date, line)
    line = source_regex.sub(git_source, line)
    line = file_regex.sub(git_file, line)
    line = revision_regex.sub(git_revision, line)
    line = rev_regex.sub(git_rev, line)
    line = hash_regex.sub(git_hash, line)
    sys.stdout.write(line)
    if debug_flag:
        sys.stderr.write(line)


# Calculate the elapsed times
if timing_flag:
    end_time = time.clock()
    sys.stderr.write('  Setup elapsed time: %s\n' % str(setup_time - start_time))
    sys.stderr.write('  Execution elapsed time: %s\n' % str(end_time - setup_time))
    sys.stderr.write('  Total elapsed time: %s\n' % str(end_time - start_time))

# Display a processing summary
if verbose_flag:
    sys.stderr.write('  Total lines processed: %s\n' % str(line_count))

# Output the program end
if summary_flag:
    sys.stderr.write('End program name: %s\n' % str(program_name))
    sys.stderr.write("\n")
elif debug_flag:
    sys.stderr.write('************ END ****************\n')
    sys.stderr.write('Hook path: %s\n' % str(hook_path))
    sys.stderr.write('Hook name: %s\n' % str(hook_name))
    sys.stderr.write('*********************************\n')
    sys.stderr.write("\n")
    sys.stderr.write("\n")
    sys.stderr.write("\n")

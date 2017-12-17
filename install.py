#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$

git_hook    = 'git-hook.py'

git_dirs    = {'filter_dir': '.git/filters',
               'event_dir': '.git/hooks'}

git_hooks   = [{'git_event': 'post_commit', 'event_code': 'rcs-keywords-hook-post-commit.py'},
               {'git_event': 'post_checkout', 'event_code': 'rcs-keywords-hook-post-checkout.py'},
               {'git_event': 'post_merge', 'event_code': 'rcs-keywords-hook-post-merge.py'}]

git_filters = ['rcs-keywords-filter-clean.py',
               'rcs-keywords-filter-smudge.py']

import sys
import os
import time
from shutil import copy2
import errno

# Set the debugging flag
summary_flag = bool(True)
verbose_flag = bool(True)
timing_flag = bool(False)
debug_flag = bool(True)
if debug_flag:
    timing_flag = bool(True)
if timing_flag:
    verbose_flag = bool(True)
if verbose_flag:
    summary_flag = bool(True)

def validatedirexists (dirname):
    # Steps:
    # 1) Verify destfile does not exit
    # 1.1) If destfile exists check whether or not it is a duplicate of source, if so ignore the file
    # 2) check if source file exists
    # 3) Copy srcfile to destfile using shutil.copyfile
    dir_exists = os.path.isdir(dirname)
    if debug_flag:
        sys.stderr.write('  Validate directory %s exists: %s\n' % (dirname, str(dir_exists)))
    return dir_exists;

def createdir (dirname):
    # Steps:
    # 1) Verify destfile does not exit
    # 1.1) If destfile exists check whether or not it is a duplicate of source, if so ignore the file
    # 2) check if source file exists
    # 3) Copy srcfile to destfile using shutil.copyfile
    if validatedirexists(dirname = dirname):
        if debug_flag:
            sys.stderr.write('  Directory %s already exists\n' % dirname)
        return;
    os.makedirs(dirname)
    if summary_flag:
        sys.stderr.write('  Directory %s created\n' % dirname)
    return;

def copyfile (srcfile, destfile):
    # Steps:
    # 1) Verify destfile does not exit
    # 1.1) If destfile exists check whether or not it is a duplicate of source, if so ignore the file
    # 2) check if source file exists
    # 3) Copy srcfile to destfile using shutil.copyfile   
    if debug_flag:
        sys.stderr.write('  Copy source file: %s\n' % srcfile)
        sys.stderr.write('  Copy destination file: %s\n' % destfile)

    # If the file already exists, throw the appropriate exception
    if os.path.exists(destfile):
        sys.stderr.write('  Destination file already exist\n')
#        raise OSError(errno.EEXIST, 'File %s already exists' % destfile)
    # Copy the source file to the destination file
    else:
        copy2(srcfile, destfile)
        if summary_flag:
            sys.stderr.write('  Copied file  %s to %s\n' % (srcfile, destfile))
    return;

def registergitevent (eventname, eventcode):
    if debug_flag:
        sys.stderr.write('  git event name: %s\n' % eventname)
        sys.stderr.write('  event code: %s\n' % eventcode)
    event_dir = os.path.join(target_dir, git_dirs['event_dir'], '%s.d' % eventname)
    createdir(dirname = event_dir)
    copyfile(srcfile = os.path.join(program_path, eventcode), destfile = os.path.join(event_dir, eventcode))
    os.symlink(os.path.join(git_hook), os.path.join(target_dir, git_dirs['event_dir'], eventname))
    return;

# Set the start time for calculating elapsed time
if timing_flag:
    start_time = time.clock()

# Parameter processing
program_name = str(sys.argv[0])
(program_path, program_executable) = os.path.split(program_name)
if debug_flag:
    sys.stderr.write('************ START **************\n')
    sys.stderr.write('Program: %s\n' % str(program_name))
    sys.stderr.write('Program path: %s\n' % str(program_path))
    sys.stderr.write('Program executable: %s\n' % str(program_executable))
    sys.stderr.write('*********************************\n')

# Output the program name start
if summary_flag:
    program_name = str(sys.argv[0])
    sys.stderr.write('Start program name: %s\n' % str(program_name))

# Set the installation target
if len(sys.argv) > 1:
    target_dir = sys.argv[1]
    sys.stderr.write('  Target from parameter: %s\n' % target_dir)
else:
    target_dir = '.'
    sys.stderr.write('  Target default: %s\n' % target_dir)
if summary_flag:
    sys.stderr.write('  Target directory: %s\n' % target_dir)

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

# Show the embedded variables
if debug_flag:
    sys.stderr.write('  git hook manager: %s\n' % git_hook)
    sys.stderr.write('  git dirs: ')
    sys.stderr.write(str(git_dirs))
    sys.stderr.write('\n  git hooks: ')
    sys.stderr.write(str(git_hooks))
    sys.stderr.write('\n  git filters: ')
    sys.stderr.write(str(git_filters))
    sys.stderr.write('\n')


# Save the setup time
if timing_flag:
    setup_time = time.clock()

# Validate that the installation target has a .git directory
if not validatedirexists(dirname = os.path.join(target_dir, '.git')):
    sys.stderr.write('Target installation directory %s is not a git repository\n' % target_dir)
    sys.stderr.write('Aborting installation!\n')
    exit(1)

# Create the core directories
createdir(dirname = os.path.join(target_dir, git_dirs['filter_dir']))
createdir(dirname = os.path.join(target_dir, git_dirs['event_dir']))

# Copy the filter programs into place
for filter_name in git_filters:
    copyfile(srcfile = os.path.join(program_path, filter_name), destfile = os.path.join(target_dir, git_dirs['filter_dir'], filter_name))


# Need to add registering the filters
# Need to register the file patterns to the filters in the attributes files

# Copy the git event manager
copyfile(srcfile = os.path.join(program_path, git_hook), destfile = os.path.join(target_dir, git_dirs['event_dir'], git_hook))

# Register the git event hooks
for event_name in git_hooks:
    registergitevent(eventname = event_name['git_event'], eventcode = event_name['event_code'])


# Calculate the elapsed times
if timing_flag:
    end_time = time.clock()
    sys.stderr.write('  Setup elapsed time: %s\n' % str(setup_time - start_time))
    sys.stderr.write('  Execution elapsed time: %s\n' % str(end_time - setup_time))
    sys.stderr.write('  Total elapsed time: %s\n' % str(end_time - start_time))
    sys.stderr.write("\n")

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

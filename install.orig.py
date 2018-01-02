#! /usr/bin/env python
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$

git_hook = 'git-hook.py'

git_dirs = {'filter_dir': 'filters', 'event_dir': 'hooks'}

git_hooks = [{'event_name': 'post-commit', 'event_code': 'rcs-keywords-hook-post-commit.py'},
             {'event_name': 'post-checkout', 'event_code': 'rcs-keywords-hook-post-checkout.py'},
             {'event_name': 'post-merge', 'event_code': 'rcs-keywords-hook-post-merge.py'}]

git_filters = [{'filter_type': 'clean', 'filter_name': 'rcs-keywords-filter-clean.py'},
               {'filter_type': 'smudge', 'filter_name': 'rcs-keywords-filter-smudge.py'}]

git_file_pattern = ['*.sql', '*.ora', '*.txt', '*.md', '*.yml', '*.yaml', '*.hosts', '*.xml',
                    '*.jsn', '*.json', '*.pl', '*.py', '*.sh' ]

import sys
import os
import time
from shutil import copy2
import subprocess
import re
#import errno

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
        sys.stderr.write('  Destination file already exist -- OVERWRITTING!!!!\n')
#        raise OSError(errno.EEXIST, 'File %s already exists' % destfile)
    # Copy the source file to the destination file
    # TODO:  Make sure it is overwritting as planned!!!!
    copy2(srcfile, destfile)
    if summary_flag:
        sys.stderr.write('  Copied file  %s to %s\n' % (srcfile, destfile))
    return;


def registergitevent (eventdir, eventname, eventcode):
    if debug_flag:
        sys.stderr.write('  git event dir: %s\n' % eventdir)
        sys.stderr.write('  git event name: %s\n' % eventname)
        sys.stderr.write('  git event code: %s\n' % eventcode)
    event_code_dir = os.path.join(eventdir, '%s.d' % eventname)
    if debug_flag:
        sys.stderr.write('  git event code dir: %s\n' % event_code_dir)
    createdir(dirname = event_code_dir)
    copyfile(srcfile = os.path.join(program_path, eventcode), destfile = os.path.join(event_code_dir, eventcode))
    event_link = os.path.join(eventdir, eventname)
    if os.path.islink(event_link):
        if debug_flag:
            sys.stderr.write('  Removed event link: %s\n' % event_link)
        os.remove(event_link)
    os.symlink(git_hook, event_link)
    if debug_flag:
        sys.stderr.write('  Created event link: %s\n' % event_link)
    return;


def installgitkeywords (git_dir, repo_dir):
#    target_dir = None
#
    if debug_flag:
        sys.stderr.write('  Target git directory: %s\n' % git_dir)
        sys.stderr.write('  Repository directory: %s\n' % repo_dir)

    # Validate that the installation target has a .git directory
    if not validatedirexists(dirname = git_dir):
        sys.stderr.write('  Target git directory %s is not a git repository\n' % git_dir)
        sys.stderr.write('  Aborting installation!\n')
        exit(1)

    # Create the core directories
    filter_dir = os.path.join(git_dir, git_dirs['filter_dir'])
    createdir(dirname = filter_dir)
    event_dir = os.path.join(git_dir, git_dirs['event_dir'])
    createdir(dirname = event_dir)

    # Set up the filter programs for use
    for filter_def in git_filters:
        # Gather the filter name & type for each filter processed
        filter_name = filter_def['filter_name']
        filter_type = filter_def['filter_type']
        if debug_flag:
            sys.stderr.write('  Copying filter: %s\n' % filter_name)

        # Copy the filter program to the target directory
        copyfile(srcfile = os.path.join(program_path, filter_name), destfile = os.path.join(filter_dir, filter_name))
        if debug_flag:
            sys.stderr.write('  Registering filter: %s\n' % filter_name)

        # Register the filter program to rcs-keywords filter
        git_cmd = 'git config --local filter.rcs-keywords.%s "%s %s"' % (filter_type, os.path.join(filter_dir, filter_name), '%f')
        if debug_flag:
            sys.stderr.write('  git_cmd: %s\n' % git_cmd)
        git_return = subprocess.Popen([git_cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (git_stdout, git_stderr) = git_return.communicate()
        if debug_flag:
            sys.stderr.write('    git exit code: %s\n' % str(git_return.returncode))
            sys.stderr.write('    stdout length: %s\n' % str(len(git_stdout)))
            sys.stderr.write('    stderr length: %s\n' % str(len(git_stderr)))


    # Register the defined file patterns to the filters in the attributes files
    attribute_file = os.path.join(git_dir, 'info', 'attributes')
    attribute_backup = os.path.join(git_dir, 'info', 'attributes~')

    # If the attribute file already exists, rename the file and re-create it 
    if os.path.exists(attribute_file):
        os.rename(attribute_file, attribute_backup)
        keyword_regex = re.compile("rcs-keywords", re.IGNORECASE)
        source = open(attribute_backup, "r")
        destination = open(attribute_file, "w")
        for line in source:
            if not keyword_regex.search(line):
                destination.write(line)
        source.close()
    else:
        destination = open(attribute_file, "w")

    # Write the appropriate file patterns for the filter usage
    max_len = len(max(git_file_pattern, key=len))
    sys.stderr.write('  max file pattern length: %d\n' % max_len)
    for file_pattern in git_file_pattern:
        destination.write('%s filter=rcs-keywords\n' % file_pattern.ljust(max_len))
    destination.close() 
             
    # Copy the git event manager
    copyfile(srcfile = os.path.join(program_path, git_hook), destfile = os.path.join(event_dir, git_hook))

    # Register the git event hooks
    for git_event in git_hooks:
        # Gather the filter name & type for each filter processed
        event_name = git_event['event_name']
        event_code = git_event['event_code']
        if debug_flag:
            sys.stderr.write('  Registering event %s\n' % event_name)
        registergitevent(eventdir = event_dir, eventname = event_name, eventcode = event_code)
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
    if debug_flag:
        sys.stderr.write('  Target from parameter: %s\n' % target_dir)
else:
    target_dir = ''
    if debug_flag:
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
    sys.stderr.write('\n  git file_pattern: ')
    sys.stderr.write(str(git_file_pattern))
    sys.stderr.write('\n')


# Save the setup time
if timing_flag:
    setup_time = time.clock()

installgitkeywords (git_dir = os.path.join(target_dir, '.git'), repo_dir = target_dir)



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
    sys.stderr.write('Program path: %s\n' % str(program_path))
    sys.stderr.write('Program executable: %s\n' % str(program_executable))
    sys.stderr.write('*********************************\n')
    sys.stderr.write("\n")
    sys.stderr.write("\n")
    sys.stderr.write("\n")

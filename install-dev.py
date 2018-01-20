#! /usr/bin/env python3
# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash$
# $Id$

"""Install

This module installs the RCS keyword functionality into an
existing git repository.
"""


import sys
import os
import time
from shutil import copy2
import subprocess
import re


GIT_HOOK = 'git-hook.py'

GIT_DIRS = {'filter_dir': 'filters', 'event_dir': 'hooks'}

GIT_HOOKS = [{'event_name': 'post-commit',
              'event_code': 'rcs-post-commit.py'},
             {'event_name': 'post-checkout',
              'event_code': 'rcs-post-checkout.py'},
             {'event_name': 'post-merge',
              'event_code': 'rcs-post-merge.py'},
             {'event_name': 'post-rewrite',
              'event_code': 'rcs-post-rewrite.py'}]

UNUSED_HOOKS = [{'event_name': 'applypatch-msg'},
                {'event_name': 'pre-applypatch'},
                {'event_name': 'post-applypatch'},
                {'event_name': 'pre-commit'},
                {'event_name': 'prepare-commit-msg'},
                {'event_name': 'commit-msg'},
                {'event_name': 'pre-rebase'},
                {'event_name': 'pre-push'},
                {'event_name': 'ore-receive'},
                {'event_name': 'update'},
                {'event_name': 'post-receive'},
                {'event_name': 'post-update'},
                {'event_name': 'push-to-checkout'},
                {'event_name': 'pre-auto-gc'},
                {'event_name': 'sendemail-validate'}]

GIT_FILTERS = [{'filter_type': 'clean',
                'filter_name': 'rcs-filter-clean.py'},
               {'filter_type': 'smudge',
                'filter_name': 'rcs-filter-smudge.py'}]

GIT_FILE_PATTERN = ['*.sql', '*.ora', '*.txt', '*.md', '*.yml',
                    '*.yaml', '*.hosts', '*.xml', '*.jsn',
                    '*.json', '*.pl', '*.py', '*.sh']


# Set the debugging flag
DEBUG_FLAG = bool(True)
TIMING_FLAG = bool(True)
VERBOSE_FLAG = bool(True)
SUMMARY_FLAG = bool(True)


def check_for_cmd(cmd):
    """Make sure that a program necessary for using this script is
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Nothing
    """
    function_name = 'check_for_cmd'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)
        sys.stderr.write('    Validating command is available\n')

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        shutdown_message(return_code=1)

    # Execute the command
    try:
        execute_cmd(cmd)

    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        print("CalledProcessError - Program '{}' not found! -- Exiting."
              .format(cmd))
        shutdown_message(return_code=err.returncode)
    except OSError as err:
        print("OSError - Required program '{}' not found! -- Exiting."
              .format(cmd))
        shutdown_message(return_code=err.errno)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def validatedirexists(dirname):
    """Validate whether or not an OS directory exists

    Arguments:
        dirname: Name of the subdirectory to verify

    Returns:
        Bool
    """

    function_name = 'validatedir'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    dir_exists = os.path.isdir(dirname)
    if DEBUG_FLAG:
        sys.stderr.write('  Validate directory %s exists: %s\n'
                         % (dirname, str(dir_exists)))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return dir_exists


def createdir(dirname):
    """Create an OS directory

    Arguments:
        dirname: Name of the subdirectory to create

    Returns:
        None
    """

    function_name = 'createdir'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    if validatedirexists(dirname=dirname):
        if DEBUG_FLAG:
            sys.stderr.write('  Directory %s already exists\n' % dirname)
        return
    os.makedirs(dirname)
    if SUMMARY_FLAG:
        sys.stderr.write('  Directory %s created\n' % dirname)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def copyfile(srcfile, destfile):
    """Copy an existing source file to a target file name

    Arguments:
        srcfile: Source file for use with the copy
        destfile: Destination file for use with the copy

    Returns:
        None
    """
    function_name = 'copyfile'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    if DEBUG_FLAG:
        sys.stderr.write('  Copy source file: %s\n' % srcfile)
        sys.stderr.write('  Copy destination file: %s\n' % destfile)

    # If the file already exists, throw the appropriate exception
    if os.path.exists(destfile):
        sys.stderr.write('  Destination file exists -- OVERWRITTING!!!!\n')
    # Copy the source file to the destination file
    copy2(srcfile, destfile)
    if SUMMARY_FLAG:
        sys.stderr.write('  Copied file  %s to %s\n' % (srcfile, destfile))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def execute_cmd(cmd):
    """Execute the supplied program
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Process Popen handle
        Process stdout file handle
        Process stderr file handle
    """
    function_name = 'execute_cmd'
    if DEBUG_FLAG:
        sys.stderr.write('    Entered module %s\n' % function_name)
        sys.stderr.write('      cmd: %s\n' % str(cmd))

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        shutdown_message(return_code=1)

    # Execute the command
    sys.stderr.flush()
    cmd_handle = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
    if DEBUG_FLAG:
        sys.stderr.write('        cmd return code: %d\n'
                         % cmd_handle.returncode)
        sys.stderr.write('        stdout length: %d\n'
                         % len(cmd_stdout))
        sys.stderr.write('        stderr length: %s\n'
                         % len(cmd_stderr))
        dump_file_stream(stream_handle=cmd_stdout,
                         stream_description='STDOUT from check_for_cmd')
        dump_file_stream(stream_handle=cmd_stderr,
                         stream_description='STDERR from check_for_cmd')

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('    Leaving module %s\n' % function_name)
    return cmd_stdout


def registergitevent(eventdir, eventname, eventcode):
    """Register a git event in the .git/hooks folder

    Arguments:
        eventdir: Source file for use with the copy
        eventname: Destination file for use with the copy
        eventcode: Source program to be copied into the hook directory

    Returns:
        None
    """
    function_name = 'registergitevent'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    event_code_dir = os.path.join(eventdir, '%s.d' % eventname)
    if DEBUG_FLAG:
        sys.stderr.write('  git event dir: %s\n' % eventdir)
        sys.stderr.write('  git event name: %s\n' % eventname)
        sys.stderr.write('  git event code: %s\n' % eventcode)
        sys.stderr.write('  git event code dir: %s\n' % event_code_dir)

    # If an event handler is defined, create the event subdiectory
    # and copy the code to it
    if eventcode:
        createdir(dirname=event_code_dir)
        copyfile(srcfile=os.path.join(PROGRAM_PATH, eventcode),
                 destfile=os.path.join(event_code_dir, eventcode))

    # Register the handler with git event
    event_link = os.path.join(eventdir, eventname)
    if os.path.islink(event_link):
        if DEBUG_FLAG:
            sys.stderr.write('  Removed event link: %s\n' % event_link)
        os.remove(event_link)
    if SUMMARY_FLAG:
        sys.stderr.write('  Registered event: %s\n' % event_link)
    os.symlink(GIT_HOOK, event_link)
    if DEBUG_FLAG:
        sys.stderr.write('  Created event link: %s\n' % event_link)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def registerfilter(filter_dir, filter_type, filter_name):
    """Register a git filter for rcs-keywords functionality

    Arguments:
        filter_dir: Directory to hold the filter program
        filter_type: Type of the filter program
        filter_name: Source program of the filter to be copied

    Returns:
        None
    """
    function_name = 'registerfilter'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    if DEBUG_FLAG:
        sys.stderr.write('  Copying filter: %s\n' % filter_name)
        sys.stderr.write('  Filter dir: %s\n' % filter_dir)
        sys.stderr.write('  Filter type: %s\n' % filter_type)

    # Register the filter program to rcs-keywords filter
    cmd = ['git',
           'config',
           '--local',
           'filter.rcs-keywords.%s' % filter_type,
           '%s %s' % (os.path.join(filter_dir, filter_name), '%f')]
    execute_cmd(cmd=cmd)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def registerfilepattern(git_dir):
    """Register the relevant file patterns for rcs-keywords functionality

    Arguments:
        filter_dir: Directory to hold the filter program
        filter_type: Type of the filter program
        filter_name: Source program of the filter to be copied

    Returns:
        None
    """
    function_name = 'registerfilepattern'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Register the defined file patterns to the filters in the attributes files
    attribute_file = os.path.join(git_dir, 'info', 'attributes')
    attribute_backup = os.path.join(git_dir, 'info', 'attributes~')

    # If the attribute file already exists, rename the file and re-create it
    # without the rcs file patterns defined
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
    max_len = len(max(GIT_FILE_PATTERN, key=len))
    if DEBUG_FLAG:
        sys.stderr.write('  max file pattern length: %d\n' % max_len)
    for file_pattern in GIT_FILE_PATTERN:
        destination.write('%s filter=rcs-keywords\n'
                          % file_pattern.ljust(max_len))
    destination.close()

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def validategitrepo(repo_dir, git_dir='.git'):
    """Validate that the supplied directory is a git repository

    Arguments:
        repo_dir: Source git repository folder
        git_dir:  Name of the git configuration subfolder

    Returns:
        None
    """
    function_name = 'validategitrepo'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)
        sys.stderr.write('  Repository directory: %s\n' % repo_dir)
        sys.stderr.write('  Target git directory: %s\n' % git_dir)
#    git_dir=os.path.join(repo_dir, '.git')
#    git_dir='.git'

    # Validate that the installation target has a .git directory
#    sys.stderr.write('Current directory %s\n' % os.getcwd())
    if not validatedirexists(dirname=os.path.join(repo_dir, git_dir)):
        sys.stderr.write('  Target directory %s is not a git repository\n'
                         % repo_dir)
        sys.stderr.write('  Aborting installation!\n')
        raise Exception('Target git directory %s is not a git repository'
                        % repo_dir)

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def installgitkeywords(repo_dir, git_dir='.git'):
    """Register a git event in the .git/hooks folder

    Arguments:
        eventdir: Source file for use with the copy
        eventname: Destination file for use with the copy
        eventcode: Source program to be copied into the hook directory

    Returns:
        None
    """
    function_name = 'installgitkeywords'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

#    git_dir=os.path.join(repo_dir, '.git')
#    git_dir='.git'
    if DEBUG_FLAG:
        sys.stderr.write('  Repository directory: %s\n' % repo_dir)
        sys.stderr.write('  Target git directory: %s\n' % git_dir)
        sys.stderr.write('Current directory %s\n' % os.getcwd())

    # Create the core directories
    filter_dir = os.path.join(git_dir, GIT_DIRS['filter_dir'])
    createdir(dirname=filter_dir)
    event_dir = os.path.join(git_dir, GIT_DIRS['event_dir'])
    createdir(dirname=event_dir)

    # Register the defined file patterns to the filters in the attributes files
    registerfilepattern(git_dir)

    # Copy the git event manager
    copyfile(srcfile=os.path.join(PROGRAM_PATH, GIT_HOOK),
             destfile=os.path.join(event_dir, GIT_HOOK))

    # Register the git event hooks
    for git_event in GIT_HOOKS:
        registergitevent(eventdir=event_dir,
                         eventname=git_event['event_name'],
                         eventcode=git_event['event_code'])

    # Register the unsued git event hooks
    for git_event in UNUSED_HOOKS:
        registergitevent(eventdir=event_dir,
                         eventname=git_event['event_name'],
                         eventcode=None)

    # Set up the filter programs for use
    for filter_def in GIT_FILTERS:
        copyfile(srcfile=os.path.join(PROGRAM_PATH, filter_def['filter_name']),
                 destfile=os.path.join(filter_dir, filter_def['filter_name']))

    # Change to the repository directory and de-register the
    # rcs-keywords filter
    local_dir = os.getcwd()
    os.chdir(os.path.abspath(repo_dir))
#    sys.stderr.write('Current directory %s\n' % os.getcwd())
    cmd = ['git',
           'config',
           '--local',
           '--remove-section',
           'filter.rcs-keywords']
    execute_cmd(cmd=cmd)

    # Set up the filter programs for use
    filter_dir = os.path.join(git_dir, GIT_DIRS['filter_dir'])
    for filter_def in GIT_FILTERS:
        # Register the defined filter program
        registerfilter(filter_dir=os.path.join('$GIT_DIR',
                                               GIT_DIRS['filter_dir']),
                       filter_type=filter_def['filter_type'],
                       filter_name=filter_def['filter_name'])
    os.chdir(local_dir)
#    sys.stderr.write('Current directory %s\n' % os.getcwd())

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def display_timing(start_clock=None, setup_clock=None):
    """Function displays the elapsed time for various stages of the
    the program.

    Arguments:
        start_clock -- Time the program started
        setup_clock -- Time the setup stage of the program completed

    Returns:
        Nothing
    """
    function_name = 'display_timing'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Calculate the elapsed times
    if TIMING_FLAG:
        end_clock = time.clock()
        if setup_clock is None:
            setup_clock = end_clock
        if start_clock is None:
            start_clock = end_clock
        sys.stderr.write('    Setup elapsed time: %s\n'
                         % str(setup_clock - start_clock))
        sys.stderr.write('    Execution elapsed time: %s\n'
                         % str(end_clock - setup_clock))
        sys.stderr.write('    Total elapsed time: %s\n'
                         % str(end_clock - start_clock))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def startup_message():
    """Function display any startup messages

    Arguments:
        argv -- Command line parameters

    Returns:
        Nothing
    """
    function_name = 'startup_message'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Display source executable information
    if DEBUG_FLAG:
        sys.stderr.write('************ START **************\n')
        sys.stderr.write('Program name: %s\n' % str(PROGRAM_NAME))
        sys.stderr.write('Program path: %s\n' % str(PROGRAM_PATH))
        sys.stderr.write('Program executable: %s\n' % str(PROGRAM_EXECUTABLE))
        sys.stderr.write('*********************************\n')

    # Output the program name start
    if VERBOSE_FLAG:
        sys.stderr.write('Start program name: %s\n' % str(PROGRAM_NAME))

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


def shutdown_message(return_code=0):
    """Function display any shutdown messages and
    the program.

    Arguments:
        argv -- Command line parameters
        files_processed -- The number of files checked out
                           by the hook
        return_code - the return code to be used when the
                      program s

    Returns:
        Nothing
    """
    function_name = 'shutdown_message'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    # Output the program end
    if VERBOSE_FLAG:
        sys.stderr.write('End program name: %s\n' % PROGRAM_NAME)
        sys.stderr.write("\n")

    if DEBUG_FLAG:
        sys.stderr.write('************ END ****************\n')
        sys.stderr.write('Program name: %s\n' % str(PROGRAM_NAME))
        sys.stderr.write('Program path: %s\n' % str(PROGRAM_PATH))
        sys.stderr.write('Program executable: %s\n' % str(PROGRAM_EXECUTABLE))
        sys.stderr.write('Return code: %d\n' % return_code)
        sys.stderr.write('*********************************\n')
        sys.stderr.write("\n")
        sys.stderr.write("\n")
        sys.stderr.write("\n")

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    exit(return_code)


def dump_file_stream(stream_handle, stream_description):
    """Function to dump the byte stream handle from Popen
    to STDERR.

    Arguments:
        steam_handle -- a stream handle returned by the Popen
                        communicate function.
        stream_descrition -- a text description of the stream handle

    Returns:
        Nothing
    """
    function_name = 'dump_file_stream'
    if DEBUG_FLAG:
        sys.stderr.write('      Entered module %s\n' % function_name)

    # Output the stream handle description
    sys.stderr.write('        %s\n' % stream_description)

    # Output the contents of the stream handle if any exists
    if stream_handle:
        sys.stderr.write(stream_handle.strip().decode("utf-8"))
        sys.stderr.write("\n")

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('      Leaving module %s\n' % function_name)
    return


def dump_list(list_values, list_description, list_message):
    """Function to dump the byte stream handle from Popen
    to STDERR.

    Arguments:
        list_values -- a list of files to be output
        list_descrition -- a text description of the file being output

    Returns:
        Nothing
    """
    function_name = 'dump_list'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)

    sys.stderr.write("    %s\n" % list_message)
    list_num = 0
    for list_value in list_values:
        sys.stderr.write('      %s[%d]: %s\n'
                         % (list_description, list_num, list_value))
        list_num = list_num + 1

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return


# def findsubmodules(repo_dir):
def findsubmodules():
    """Function to find the relevent configuration files for any
    submodules associated with the master repository.  Leave the
    parameter blank if the current working directory is holds
    the master repository

    Arguments:
        dirname -- OS folder holding the master repository.
        subdirname -- Subdirectory name within dirname to search
        filename -- Name of the file to find

    Returns:
        List of file names
    """
    function_name = 'findsubmodules'
    if DEBUG_FLAG:
        sys.stderr.write('  Entered module %s\n' % function_name)
        sys.stderr.write('Current dir: %s\n' % os.getcwd())

    dirmodule = os.path.join('.git', 'modules')
    field_name = ['gitdir', 'repodir']

    submodule_list = [dict(zip(field_name, (dirpath,
                                            os.path.relpath(dirpath,
                                                            dirmodule))))
                      for (dirpath, _, filenames) in os.walk(dirmodule)
                      for name in filenames if name == 'config']

    # Return from the function
    if DEBUG_FLAG:
        sys.stderr.write('  Leaving module %s\n' % function_name)
    return submodule_list


######
# Main
######
# Set the start time for calculating elapsed time
START_TIME = time.clock()

# Parameter processing
PROGRAM_NAME = os.path.abspath(sys.argv[0])
(PROGRAM_PATH, PROGRAM_EXECUTABLE) = os.path.split(PROGRAM_NAME)
if SUMMARY_FLAG or DEBUG_FLAG:
    startup_message()

# Set the installation target
if len(sys.argv) > 1:
    TARGET_DIR = sys.argv[1]
    if DEBUG_FLAG:
        sys.stderr.write('  Target from parameter: %s\n' % TARGET_DIR)
else:
    TARGET_DIR = ''
    if DEBUG_FLAG:
        sys.stderr.write('  Target default: %s\n' % TARGET_DIR)

if SUMMARY_FLAG:
    sys.stderr.write('  Target directory: %s\n' % TARGET_DIR)

# Save the current working directory
current_dir = os.getcwd()

if VERBOSE_FLAG:
    dump_list(list_values=sys.argv,
              list_description='Param',
              list_message='Parameter list')

# Show the OS environment variables
if DEBUG_FLAG:
    sys.stderr.write('  Environment variables defined\n')
    for key, value in sorted(os.environ.items()):
        sys.stderr.write('    Key: %s  Value: %s\n' % (key, value))
    sys.stderr.write("\n")

# Show the embedded variables
if DEBUG_FLAG:
    sys.stderr.write('  git hook manager: %s\n' % GIT_HOOK)
    sys.stderr.write('  git dirs: ')
    sys.stderr.write(str(GIT_DIRS))
    sys.stderr.write('\n  git hooks: ')
    sys.stderr.write(str(GIT_HOOKS))
    sys.stderr.write('\n  git filters: ')
    sys.stderr.write(str(GIT_FILTERS))
    sys.stderr.write('\n  git file_pattern: ')
    sys.stderr.write(str(GIT_FILE_PATTERN))
    sys.stderr.write('\n')

# Check if git is available.
check_for_cmd(cmd=['git', '--version'])

# Save the setup time
SETUP_TIME = time.clock()

# Install the keyword support
try:
    # Validate that a git repository was supplied
    validategitrepo(repo_dir=TARGET_DIR)
    # Change to the repository directory
    os.chdir(os.path.abspath(TARGET_DIR))
    if DEBUG_FLAG:
        sys.stderr.write('Current directory %s\n' % os.getcwd())
    # Install rcs keywords support in the repo
    installgitkeywords(repo_dir='')
#    submodules = findsubmodules(repo_dir=TARGET_DIR)
    submodules = findsubmodules()
    if DEBUG_FLAG:
        sys.stderr.write('  Submodule count: %d\n' % len(submodules))
    for module in submodules:
        if DEBUG_FLAG:
            sys.stderr.write('    Found submodule %s\n' % str(module))
            sys.stderr.write('Repo dir: %s\n' % module['repodir'])
            sys.stderr.write('git dir: %s\n' % module['gitdir'])
        installgitkeywords(repo_dir=module['repodir'],
                           git_dir=module['gitdir'])

except:
    sys.stderr.write('Exception caught\n')
    raise

# Return to the initial working directory
os.chdir(current_dir)

# Calculate the elapsed times
if TIMING_FLAG:
    display_timing(start_clock=START_TIME,
                   setup_clock=SETUP_TIME)

shutdown_message(return_code=0)
exit(0)

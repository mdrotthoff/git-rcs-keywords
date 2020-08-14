#! /usr/bin/env python
# # -*- coding: utf-8 -*

# $Author$
# $Date$
# $File$
# $Rev$
# $Rev$
# $Source$
# $Hash:     "ce6f6d53540aa85c30264deab1a47016232ff0e8 $

"""
rcs-keywords-post-merge

This module provides code to act as an event hook for the git
post-merge event.  It detects which files have been changed
and forces the file to be checked back out within the
repository once the commit data is available.
"""

import sys
import os
import errno
import subprocess
import time


__author__ "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-0.9.5"
__date__ = "2018-06-11 09:10:44"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__credits__ = []
__status__ = "Development"
# __license__ = "Python"


# Set the debugging flag
CALL_GRAPH = False
TIMING_FLAG = False
VERBOSE_FLAG = False
SUMMARY_FLAG = False


if CALL_GRAPH:
    from pycallgraph import PyCallGraph
    from pycallgraph.output import GraphvizOutput


def shutdown_message(return_code=0, files_processed=0):
    """Function display any provided messages and exit the program.

    Arguments:
        return_code - the return code to be used when the
                      program exits
        files_processed -- The number of files checked out
                           by the hook

    Returns:
        Nothing
    """
    # Display a processing summary
    if SUMMARY_FLAG:
        sys.stderr.write('  Files processed: %d\n' % files_processed)
        sys.stderr.write('End program name: %s\n' % sys.argv[0])

    # Return from the function
    exit(return_code)


def display_timing(start_time=None, setup_time=None):
    """Function displays the elapsed time for various stages of the
    the program.

    Arguments:
        start_time -- Time the program started
        setup_time -- Time the setup stage of the program completed

    Returns:
        Nothing
    """
    # Calculate the elapsed times
    end_time = time.clock()
    if setup_time is None:
        setup_time = end_time
    if start_time is None:
        start_time = end_time
    sys.stderr.write('    Setup elapsed time: %s\n'
                     % str(setup_time - start_time))
    sys.stderr.write('    Execution elapsed time: %s\n'
                     % str(end_time - setup_time))
    sys.stderr.write('    Total elapsed time: %s\n'
                     % str(end_time - start_time))

    # Return from the function
    return


def dump_list(list_values, list_description, list_message):
    """Function to dump a list of values to STDERR.

    Arguments:
        list_values -- a list of files to be output
        list_descrition -- a text description of the values being output
        list_message -- a text description of the value list

    Returns:
        Nothing
    """
    sys.stderr.write("    %s\n" % list_message)
    list_num = 0
    for value in list_values:
        sys.stderr.write('      %s[%d]: %s\n'
                         % (list_description, list_num, value))
        list_num += 1

    # Return from the function
    return


def execute_cmd(cmd, cmd_source=None):
    """Execute the supplied program.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.
        cmd_source -- The function requesting the program execution
                      Default value of None.

    Returns:
        Process stdout file handle
    """
    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        shutdown_message(return_code=1,
                         files_processed=0)

    # Execute the command
    try:
        cmd_handle = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
        if cmd_stderr:
            for line in cmd_stderr.strip().decode("utf-8").splitlines():
                sys.stderr.write("%s\n" % line)
    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        sys.stderr.write("CalledProcessError - Program {0} called by {1} not found! -- Exiting."
                         .format(str(cmd), str(cmd_source)))
        raise
#        shutdown_message(return_code=err.returncode,
#                         files_processed=0)
    except OSError as err:
        sys.stderr.write("OSError - Program {0} called by {1} not found! -- Exiting."
                         .format(str(cmd), str(cmd_source)))
        raise
#        shutdown_message(return_code=err.errno,
#                         files_processed=0)

    # Return from the function
    return cmd_stdout

'''
    # Execute the command
    cmd_handle = subprocess.Popen(cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
    if cmd_stderr:
        for line in cmd_stderr.strip().decode("utf-8").splitlines():
            sys.stderr.write("%s\n" % line)

    # Return from the function
    return cmd_stdout
'''


def check_for_cmd(cmd):
    """Make sure that a program necessary for using this script is
    available.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.

    Returns:
        Nothing
    """
    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        shutdown_message(return_code=1,
                         files_processed=0)

    # Execute the command
    execute_cmd(cmd=cmd, cmd_source='check_for_cmd')

    # Return from the function
    return

'''
    # Execute the command
    try:
        execute_cmd(cmd)

    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        print("CalledProcessError - Program '{}' not found! -- Exiting."
              .format(cmd))
        shutdown_message(return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        print("OSError - Required program '{}' not found! -- Exiting."
              .format(cmd))
        shutdown_message(return_code=err.errno,
                         files_processed=0)

    # Return from the function
    return
'''


def git_ls_files():
    """Find files that are relevant based on all files for the
       repository branch.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    cmd = ['git', 'ls-files']

    # Get a list of all files in the current repository branch
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='git_ls_files')

    # Return from the function
    return cmd_stdout

'''
    # Get a list of all files in the current repository branch
    try:
        cmd_stdout = execute_cmd(cmd)

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError as err:
        shutdown_message(return_code=err.returncode,
                         files_processed=0)

    # Return from the function
    return cmd_stdout
'''


def get_modified_files():
    """Find files that were modified by the merge.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    modified_file_list = []
    cmd = ['git', 'diff-tree', 'ORIG_HEAD', 'HEAD', '--name-only', '-r',
           '--diff-filter=ACMRT']

    # Fetch the list of files modified by the last commit
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='get_modified_files')

    # Convert the stdout stream to a list of files
    modified_file_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if modified_file_list and modified_file_list[0] == 'clean':
        shutdown_message(return_code=0,
                         files_processed=0)

    # Only return regular files.
    modified_file_list = [i for i in modified_file_list if os.path.isfile(i)]
    if VERBOSE_FLAG:
        sys.stderr.write('  %d modified files found for processing\n'
                         % len(modified_file_list))

    # Return from the function
    return modified_file_list

'''
    # Fetch the list of files modified by the last commit
    try:
        cmd_stdout = execute_cmd(cmd)

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError as err:
        # This is a new repository, so get a list of all files
        if err.returncode == 128:  # new repository
            cmd_stdout = git_ls_files()
        else:
            shutdown_message(return_code=err.returncode,
                             files_processed=0)

    # Convert the stdout stream to a list of files
    modified_file_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if modified_file_list and modified_file_list[0] == 'clean':
        shutdown_message(return_code=0,
                         files_processed=0)

    # Only return regular files.
    modified_file_list = [i for i in modified_file_list if os.path.isfile(i)]
    if VERBOSE_FLAG:
        sys.stderr.write('  %d modified files found for processing\n'
                         % len(modified_file_list))

    # Return from the function
    return modified_file_list
'''


def remove_modified_files(files):
    """Filter the found files to eliminate any that have changes that have
       not been checked in.

    Arguments:
        files - list of files to checkout

    Returns:
        A list of files to checkout that do not have pending changes.
    """
    cmd = ['git', 'status', '-s']

    # Get the list of files that are modified but not checked in
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='remove_modified_files')

    # Convert the stream output to a list of output lines
    modified_files_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if not modified_files_list:
        return files

    # Pull the file name (second field) of the output line and
    # remove any double quotes
    modified_files_list = [l.split(None, 1)[-1].strip('"')
                           for l in modified_files_list]

    # Remove any modified files from the list of files to process
    if modified_files_list:
        files = [f for f in files if f not in modified_files_list]

    # Return from the function
    return files

'''
    # Get the list of files that are modified but not checked in
    try:
        cmd_stdout = execute_cmd(cmd)

    # if an exception occurs, raise it to the caller
    except subprocess.CalledProcessError as err:
        sys.stderr.write('  CalledProcessError in git_not_checked_id\n')
        shutdown_message(return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        sys.stderr.write('  OSError in git_not_checked_id\n')
        shutdown_message(return_code=err.errno,
                         files_processed=0)

    # Convert the stream output to a list of output lines
    modified_files_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if not modified_files_list:
        return files

    # Pull the file name (second field) of the output line and
    # remove any double quotes
    modified_files_list = [l.split(None, 1)[-1].strip('"')
                           for l in modified_files_list]

    # Remove any modified files from the list of files to process
    if modified_files_list:
        files = [f for f in files if f not in modified_files_list]

    # Return from the function
    return files
'''


def check_out_file(file_name):
    """Checkout file that was been modified by the latest merge.

    Arguments:
        file_name -- the file name to be checked out for smudging

    Returns:
        Nothing.
    """
    # Remove the file if it currently exists
    try:
        os.remove(file_name)
    except OSError as err:
        # Ignore a file not found error, it was being removed anyway
        if err.errno != errno.ENOENT:
            shutdown_message(return_code=err.errno,
                             files_processed=0)

    cmd = ['git', 'checkout', '-f', '%s' % file_name]

    # Check out the file so that it is smudged
    execute_cmd(cmd=cmd, cmd_source='check_out_files')

    # Return from the function
    return

'''
    # Check out the file so that it is smudged
    try:
        execute_cmd(cmd)
    except subprocess.CalledProcessError as err:
        sys.stderr.write('  CalledProcessError in check_out_file\n')
        shutdown_message(return_code=err.returncode,
                         files_processed=0)
    except OSError as err:
        sys.stderr.write('  OSError in check_out_file\n')
        shutdown_message(return_code=err.errno,
                         files_processed=0)

    # Return from the function
    return
'''


def main():
    """Main program.

    Arguments:
        None

    Returns:
        Nothing
    """
    # Set the start time for calculating elapsed time
    start_time = time.clock()
    setup_time = None

    # Display the startup message
    if SUMMARY_FLAG:
        sys.stderr.write('Start program name: %s\n' % sys.argv[0])

    # List the provided parameters
    if VERBOSE_FLAG:
        dump_list(list_values=sys.argv,
                  list_description='Param',
                  list_message='Parameter list')

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of modified files
    files = get_modified_files()
    if VERBOSE_FLAG:
        dump_list(list_values=files,
                  list_description='File',
                  list_message='Files not checked in')

    # Filter the list of modified files to exclude those modified since
    # the commit
    files = remove_modified_files(files=files)

    # Calculate the setup elapsed time
    setup_time = time.clock()

    # Process the remaining file list
    files_processed = 0
    if files:
        files.sort()
        for file_name in files:
            check_out_file(file_name=file_name)
            files_processed += 1

    # Calculate the elapsed times
    if TIMING_FLAG:
        display_timing(start_time=start_time,
                       setup_time=setup_time)

    # Return from the function
    shutdown_message(files_processed=files_processed,
                     return_code=0)


def call_graph():
    """Call_graph execution

    Arguments:
        None

    Returns:
        Nothing
    """
    graphviz = GraphvizOutput()
    graphviz.output_type = 'pdf'
    graphviz.output_file = (os.path.splitext(os.path.basename(sys.argv[0]))[0]
                            + '-' + time.strftime("%Y%m%d-%H%M%S")
                            + '.' + graphviz.output_type)
    with PyCallGraph(output=graphviz):
        main()


# Execute the main function
if __name__ == '__main__':
    if CALL_GRAPH:
        call_graph()
    else:
        main()

#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
rcs-keywords-post-commit

This module provides code to act as an event hook for the git
post-commit event.  It detects which files have been changed
and forces the file to be checked back out within the
repository.
"""

import sys
import os
import errno
import subprocess
# import time

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-04 09:10:44"
__copyright__ = "Copyright (c) 2018 David Rotthoff"
__credits__ = []
__status__ = "Production"
# __license__ = "Python"


def shutdown_message(return_code=0):
    """Function display any provided messages and exit the program.

    Arguments:
        return_code - the return code to be used when the
                      program exits
        files_processed -- The number of files checked out
                           by the hook

    Returns:
        Nothing
    """
    exit(return_code)


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
        shutdown_message(return_code=1)

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
        sys.stderr.write(
            "{0} - Program {1} called by {2} not found! -- Exiting."
            .format(str(err), str(cmd), str(cmd_source))
        )
        raise
    except OSError as err:
        sys.stderr.write(
            "{0} - Program {1} called by {2} not found! -- Exiting."
            .format(str(err), str(cmd), str(cmd_source))
        )
        raise

    # Return from the function
    return cmd_stdout


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
        shutdown_message(return_code=1)

    # Execute the command
    execute_cmd(cmd=cmd, cmd_source='check_for_cmd')

    # Return from the function
    return


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


def get_modified_files():
    """Find files that were modified by the commit.

    Arguments:
        None

    Returns:
        A list of filenames.
    """
    modified_file_list = []
    cmd = ['git', 'diff-tree', 'HEAD~1', 'HEAD', '--name-only', '-r',
           '--diff-filter=ACMRT']

    # Fetch the list of files modified by the last commit
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='get_modified_files')

    # Convert the stdout stream to a list of files
    modified_file_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if modified_file_list and modified_file_list[0] == 'clean':
        shutdown_message(return_code=0)

    # Only return regular files.
    modified_file_list = [i for i in modified_file_list if os.path.isfile(i)]

    # Return from the function
    return modified_file_list


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


def check_out_file(file_name):
    """Checkout file that was been modified by the latest commit.

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
            shutdown_message(return_code=err.errno)
    cmd = ['git', 'checkout', '-f', '%s' % file_name]

    # Check out the file so that it is smudged
    execute_cmd(cmd=cmd, cmd_source='check_out_file')

    # Return from the function
    return


def main():
    """Main program.

    Arguments:
        None

    Returns:
        Nothing
    """
    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of modified files
    files = get_modified_files()

    # Filter the list of modified files to exclude those modified since
    # the commit
    files = remove_modified_files(files=files)

    # Force a checkout of the remaining file list
    # Process the remaining file list
    files_processed = 0
    if files:
        files.sort()
        for file_name in files:
            check_out_file(file_name=file_name)
            files_processed += 1

    # Return from the function
    shutdown_message(return_code=0)


# Execute the main function
if __name__ == '__main__':
    main()

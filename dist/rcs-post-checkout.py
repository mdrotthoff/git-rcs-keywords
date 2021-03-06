#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
rcs-keywords-post-checkout

This module provides code to act as an event hook for the git
post-checkout event.  It detects which files have been changed
and forces the files to be checked back out within the
repository.  If the checkout event is  a file based event, the
hook exits without doing any work.  If the event is a branch
based event, the files are checked again after the the commit
information is available after the merge has completed.
"""

import sys
import os
import errno
import subprocess

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"


def execute_cmd(cmd, cmd_source=None):
    """Execute the supplied program.

    Arguments:
        cmd -- string or list of strings of commands. A single string may
               not contain spaces.
        cmd_source -- The function requesting the program execution.
                      Default value of None.

    Returns:
        Process stdout file handle
    """
    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        exit(1)

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
        exit(1)

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


def get_checkout_files(first_hash, second_hash):
    """Find files that have been modified over the range of the supplied
       commit hashes.

    Arguments:
        first_hash - The starting hash of the range
        second_hash - The ending hash of the range

    Returns:
        A list of filenames.
    """
    file_list = []

    # Get the list of files impacted.  If argv[1] and argv[2] are the same
    # commit, then pass the value only once otherwise the file list is not
    # returned
    if first_hash == second_hash:
        cmd = ['git',
               'diff-tree',
               '-r',
               '--name-only',
               '--no-commit-id',
               '--diff-filter=ACMRT',
               first_hash]
    else:
        cmd = ['git',
               'diff-tree',
               '-r',
               '--name-only',
               '--no-commit-id',
               '--diff-filter=ACMRT',
               first_hash,
               second_hash]

    # Fetch the list of files modified by the last commit
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='get_checkout_files')

    # Convert the stdout stream to a list of files
    file_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if file_list and file_list[0] == 'clean':
        exit(0)

    # Only return regular files.
    file_list = [i for i in file_list if os.path.isfile(i)]
    # if VERBOSE_FLAG:
    #     sys.stderr.write('  %d real files found for processing\n'
    #                      % len(file_list))

    # Return from the function
    return file_list


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
    """Checkout file that was been modified by the latest branch checkout.

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
            exit(err.errno)

    cmd = ['git', 'checkout', '-f', '%s' % file_name]

    # Check out the file so that it is smudged
    execute_cmd(cmd=cmd, cmd_source='check_out_files')

    # Return from the function
    return


def main():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """
    # If argv[3] is zero (file checkout rather than branch checkout),
    # then exit the hook as there is no need to re-smudge the file.
    # (The commit info was already available)
    if sys.argv[3] == '0':
        exit(0)

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of files impacted.
    files = get_checkout_files(first_hash=sys.argv[1], second_hash=sys.argv[2])

    # Filter the list of modified files to exclude those modified since
    # the commit
    files = remove_modified_files(files=files)

    # Force a checkout of the remaining file list
    files_processed = 0
    if files:
        files.sort()
        for file_name in files:
            check_out_file(file_name=file_name)
            files_processed += 1


# Execute the main function
if __name__ == '__main__':
    main()

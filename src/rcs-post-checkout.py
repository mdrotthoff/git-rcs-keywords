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
import logging

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"

LOGGING_LEVEL = None
LOGGING_LEVEL = logging.DEBUG
# LOGGING_LEVEL = logging.INFO
# LOGGING_LEVEL = logging.WARNING
# LOGGING_LEVEL = logging.ERROR

# Conditionally map a time function for performance measurement
# depending on the version of Python used
if LOGGING_LEVEL:
    if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
        from time import perf_counter as get_clock
    else:
        from time import clock as get_clock
else:
    def get_clock():
        """Dummy get_clock function for when the timing flag is not set"""
        pass


def configure_logging():
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format='%(asctime)s:%(levelname)s: %(message)s',
        filename='.git-hook.post-checkout.log',
        datefmt='%Y-%m-%d %H:%M:%S.%f',
    )


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

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('cmd: %s' % cmd)
        logging.debug('cmd_source: %s' % cmd_source)

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        logging.error('Embedded space in command')
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
        logging.error(
            "%s - Program %s called by %s not found! -- Exiting."
            % (str(err), str(cmd[0]), str(' '.join(cmd)))
        )
        raise
    except OSError as err:
        logging.error(
            "%s - Program %s called by %s not found! -- Exiting."
            % (str(err), str(cmd[0]), str(' '.join(cmd)))
        )
        raise

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))
        # logging.debug('cmd_stdout: %s' % cmd_stdout)

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

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('cmd: %s' % cmd)

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        logging.error('Embedded space in command')
        exit(1)

    # Execute the command
    execute_cmd(cmd=cmd, cmd_source='check_for_cmd')

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))


def git_ls_files():
    """Find files that are relevant based on all files for the
       repository branch.

    Arguments:
        None

    Returns:
        A list of filenames.
    """

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)

    cmd = ['git', 'ls-files']

    # Get a list of all files in the current repository branch
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='git_ls_files')

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))

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

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('First hash: %s' % first_hash)
        logging.debug('Second hash: %s' % second_hash)

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
        if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
            logging.debug('No files to process')
        exit(0)

    # Only return regular files.
    file_list = [i for i in file_list if os.path.isfile(i)]

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))
        logging.debug('Returning file list to process %s' % file_list)

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

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('files: %s' % files)

    cmd = ['git', 'status', '-s']

    # Get the list of files that are modified but not checked in
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='remove_modified_files')

    # Convert the stream output to a list of output lines
    modified_files_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if not modified_files_list:
        # Display input parameters
        if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
            logging.debug('No modified files found')
        return files

    # Pull the file name (second field) of the output line and
    # remove any double quotes
    modified_files_list = [l.split(None, 1)[-1].strip('"')
                           for l in modified_files_list]

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        logging.debug('Modified files list: %s' % modified_files_list)

    # Remove any modified files from the list of files to process
    if modified_files_list:
        files = [f for f in files if f not in modified_files_list]

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))
        logging.debug('Modified file list %s' % files)

    # Return from the function
    return files


def check_out_file(file_name):
    """Checkout file that was been modified by the latest branch checkout.

    Arguments:
        file_name -- the file name to be checked out for smudging

    Returns:
        Nothing.
    """

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('File_name: %s' % file_name)

    # Remove the file if it currently exists
    try:
        os.remove(file_name)
    except OSError as err:
        # Ignore a file not found error, it was being removed anyway
        if err.errno != errno.ENOENT:
            logging.error('Unable to remove file %s for re-checkout' % file_name)
            exit(err.errno)

    cmd = ['git', 'checkout', '-f', '%s' % file_name]

    # Check out the file so that it is smudged
    execute_cmd(cmd=cmd, cmd_source='check_out_files')

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))


def post_checkout():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """

    # Display input parameters
    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        start_time = get_clock()
        logging.debug('')
        logging.debug('Function: %s' % sys._getframe().f_code.co_name)
        logging.debug('sys.argv: %s' % sys.argv)

    # If argv[3] is zero (file checkout rather than branch checkout),
    # then exit the hook as there is no need to re-smudge the file.
    # (The commit info was already available)
    if sys.argv[3] == '0':
        if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
            logging.debug('File checkout - no work required')
        exit(0)

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of files impacted.
    files = get_checkout_files(first_hash=sys.argv[1], second_hash=sys.argv[2])

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        logging.debug('Files to checkout: %s' % files)

    # Filter the list of modified files to exclude those modified since
    # the commit
    files = remove_modified_files(files=files)

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        logging.debug('Non-modified files: %s' % files)

    # Force a checkout of the remaining file list
    files_processed = 0
    if files:
        files.sort()
        for file_name in files:
            check_out_file(file_name=file_name)
            files_processed += 1

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s'
                     % (sys._getframe().f_code.co_name,
                        end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    # Initialize logging
    if LOGGING_LEVEL:
        if LOGGING_LEVEL <= logging.INFO:
            start_time = get_clock()
        configure_logging()
        logging.debug('')
        logging.debug('')
        logging.debug('Executing: %s' % sys.argv[0])

    post_checkout()

    if LOGGING_LEVEL and LOGGING_LEVEL <= logging.INFO:
        end_time = get_clock()
        logging.info('Elapsed for %s: %s' % (sys.argv[0], end_time - start_time))

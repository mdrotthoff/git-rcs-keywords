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
__project__ = "git-rcs-keywords"
__version__ = "1.2.0-dev1-19"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"

# LOGGING_CONSOLE_LEVEL = None
# LOGGING_CONSOLE_LEVEL = logging.DEBUG
# LOGGING_CONSOLE_LEVEL = logging.INFO
# LOGGING_CONSOLE_LEVEL = logging.WARNING
LOGGING_CONSOLE_LEVEL = logging.ERROR
# LOGGING_CONSOLE_LEVEL = logging.CRITICAL
LOGGING_CONSOLE_MSG_FORMAT = \
    '%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(lineno)s: %(message)s'
LOGGING_CONSOLE_DATE_FORMAT = '%Y-%m-%d %H.%M.%S'

# LOGGING_FILE_LEVEL = None
# LOGGING_FILE_LEVEL = logging.DEBUG
LOGGING_FILE_LEVEL = logging.INFO
# LOGGING_FILE_LEVEL = logging.WARNING
# LOGGING_FILE_LEVEL = logging.ERROR
# LOGGING_FILE_LEVEL = logging.CRITICAL
LOGGING_FILE_MSG_FORMAT = LOGGING_CONSOLE_MSG_FORMAT
LOGGING_FILE_DATE_FORMAT = LOGGING_CONSOLE_DATE_FORMAT
# LOGGING_FILE_NAME = '.git-hook.post-checkout.log'
LOGGING_FILE_NAME = '.git-hook.log'

# Conditionally map a time function for performance measurement
# depending on the version of Python used
if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
    from time import perf_counter as get_clock
else:
    from time import clock as get_clock


def dump_environment():
    """Dump the execution environment"""
    logging.debug('Start environment variables')
    for key in sorted(os.environ.keys()):
        logging.debug('%s: %s' % (key, os.environ[key]))
    logging.debug('End environment variables')

    logging.debug('Start command parameters')
    logging.debug('Argument count: %d' % len(sys.argv))
    for cnt, argument in enumerate(sys.argv):
        logging.debug('Argument %d: %s' % (cnt, argument))
    logging.debug('End command parameters')


def configure_logging():
    """Configure the logging service"""
    # Configure the console logger
    if LOGGING_CONSOLE_LEVEL:
        console = logging.StreamHandler()
        console.setLevel(LOGGING_CONSOLE_LEVEL)
        console_formatter = logging.Formatter(
            fmt=LOGGING_CONSOLE_MSG_FORMAT,
            datefmt=LOGGING_CONSOLE_DATE_FORMAT,
        )
        console.setFormatter(console_formatter)

    # Create an file based logger if a LOGGING_FILE_LEVEL is defined
    if LOGGING_FILE_LEVEL:
        logging.basicConfig(
            level=LOGGING_FILE_LEVEL,
            format=LOGGING_FILE_MSG_FORMAT,
            datefmt=LOGGING_FILE_DATE_FORMAT,
            filename=LOGGING_FILE_NAME,
        )

    # Basic logger configuration
    if LOGGING_CONSOLE_LEVEL or LOGGING_FILE_LEVEL:
        logger = logging.getLogger('')
        if LOGGING_CONSOLE_LEVEL:
            # Add the console logger to default logger
            logger.addHandler(console)


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
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('cmd: %s', cmd)
    logging.debug('cmd_source: %s', cmd_source)

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        end_time = get_clock()
        logging.error('Exiting - embedded space in command')
        logging.info('Elapsed time: %f', (end_time - start_time))
        exit(1)

    # Execute the command
    try:
        cmd_handle = subprocess.Popen(cmd,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
        logging.info('Command %s successfully executed', cmd)
        if cmd_stderr:
            for line in cmd_stderr.strip().decode("utf-8").splitlines():
                logging.info("stderr line: %s", line)
    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        end_time = get_clock()
        logging.info(
            "Program %s call failed! -- Exiting.", cmd,
            exc_info=True
        )
        logging.error(
            "Program %s call failed! -- Exiting.", cmd
        )
        logging.info('Elapsed time: %f', (end_time - start_time))
        raise
    except OSError as err:
        end_time = get_clock()
        logging.info(
            "Program %s caused on OS error! -- Exiting.",
            cmd,
            exc_info=True
        )
        logging.error(
            "Program %s caused OS error %s! -- Exiting.",
            cmd, err.errno
        )
        logging.info('Elapsed time: %f', (end_time - start_time))
        raise

    end_time = get_clock()
    logging.info('Elapsed time: %f', (end_time - start_time))

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
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('cmd: %s', cmd)

    # Ensure there are no embedded spaces in a string command
    if isinstance(cmd, str) and ' ' in cmd:
        end_time = get_clock()
        logging.error('Exiting - embedded space in command')
        logging.info('Elapsed time: %f', (end_time - start_time))
        exit(1)

    # Execute the command
    execute_cmd(cmd=cmd, cmd_source='check_for_cmd')

    end_time = get_clock()
    logging.info('Elapsed time: %f', (end_time - start_time))


def git_ls_files():
    """Find files that are relevant based on all files for the
       repository branch.

    Arguments:
        None

    Returns:
        A list of filenames.
    """

    # Display input parameters
    start_time = get_clock()
    logging.debug('Entered function')

    cmd = ['git', 'ls-files']

    # Get a list of all files in the current repository branch
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='git_ls_files')

    end_time = get_clock()
    logging.info('Elapsed time: %f', (end_time - start_time))

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
    start_time = get_clock()
    logging.debug('Entered function')
    logging.debug('First hash: %s', first_hash)
    logging.debug('Second hash: %s', second_hash)

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
        end_time = get_clock()
        logging.info('No files to process')
        logging.info('Elapsed time: %f', (end_time - start_time))
        exit(0)

    # Only return regular files.
    file_list = [i for i in file_list if os.path.isfile(i)]

    end_time = get_clock()
    logging.debug('Returning file list to process %s', file_list)
    logging.info('Elapsed time: %f', (end_time - start_time))

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
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('files: %s', files)

    cmd = ['git', 'status', '-s']

    # Get the list of files that are modified but not checked in
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='remove_modified_files')

    # Convert the stream output to a list of output lines
    modified_files_list = cmd_stdout.decode('utf8').splitlines()

    # Deal with unmodified repositories
    if not modified_files_list:
        end_time = get_clock()
        logging.info('No modified files found')
        logging.info('Elapsed time: %f', (end_time - start_time))
        return files

    # Pull the file name (second field) of the output line and
    # remove any double quotes
    modified_files_list = [l.split(None, 1)[-1].strip('"')
                           for l in modified_files_list]
    logging.debug('Modified files list: %s', modified_files_list)

    # Remove any modified files from the list of files to process
    if modified_files_list:
        files = [f for f in files if f not in modified_files_list]

    end_time = get_clock()
    logging.debug('Modified file list %s', files)
    logging.info('Elapsed time: %f', (end_time - start_time))

    # Return from the function
    return files


# def check_out_file(file_name):
#     """Checkout file that was been modified by the latest branch checkout.
#
#     Arguments:
#         file_name -- the file name to be checked out for smudging
#
#     Returns:
#         Nothing.
#     """
#
#     # Display input parameters
#     start_time = get_clock()
#     logging.info('Entered function')
#     logging.debug('File_name: %s', file_name)
#
#     # Remove the file if it currently exists
#     try:
#         os.remove(file_name)
#         logging.info('Removed file %s', file_name)
#     except OSError as err:
#         # Ignore a file not found error, it was being removed anyway
#         if err.errno != errno.ENOENT:
#             end_time = get_clock()
#             logging.error('Unable to remove file %s for re-checkout',
#                           file_name)
#             logging.info('Elapsed time: %f', (end_time - start_time))
#             exit(err.errno)
#         else:
#             logging.info('File %s not found to remove', file_name)
#
#     cmd = ['git', 'checkout', '-f', '%s' % file_name]
#
#     # Check out the file so that it is smudged
#     execute_cmd(cmd=cmd, cmd_source='check_out_files')
#     logging.info('Checked out file %s', file_name)
#
#     end_time = get_clock()
#     logging.info('Elapsed time: %f', (end_time - start_time))


def post_checkout():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """

    # Display input parameters
    start_time = get_clock()
    logging.info('Entered function')
    logging.info('sys.argv: %s', sys.argv)

    # If argv[3] is zero (file checkout rather than branch checkout),
    # then exit the hook as there is no need to re-smudge the file.
    # (The commit info was already available)  If the vallue is 1, then
    # this is a branch checkout and commit info was not available at the
    # time the file was checkted out.
    if sys.argv[3] == '0':
        end_time = get_clock()
        logging.debug('File checkout - no work required')
        logging.info('Elapsed time: %f', (end_time - start_time))
        exit(0)

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of files impacted.
    files = get_checkout_files(first_hash=sys.argv[1], second_hash=sys.argv[2])
    logging.debug('Files to checkout: %s', files)

    # Filter the list of modified files to exclude those modified since
    # the commit
    files = remove_modified_files(files=files)
    logging.debug('Non-modified files: %s', files)

    # Force a checkout of the remaining file list
    files_processed = 0
    if files:
        files.sort()
        for file_name in files:
            # logging.info('Checking out file %s', file_name)
            # check_out_file(file_name=file_name)
            # sys.stderr.write('Smudged file %s\n' % file_name)
            logging.info('Checked out file %s', file_name)
            files_processed += 1

    end_time = get_clock()
    logging.info('Elapsed time: %f', (end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    configure_logging()

    START_TIME = get_clock()
    logging.debug('Entered module')

    if LOGGING_FILE_LEVEL and LOGGING_FILE_LEVEL <= logging.DEBUG:
        dump_environment()

    post_checkout()

    END_TIME = get_clock()
    logging.info('Elapsed time: %f', (END_TIME - START_TIME))

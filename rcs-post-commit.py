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
import logging

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__project__ = "git-rcs-keywords"
__version__ = "1.1.1-dev1-3"
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
LOGGING_FILE_LEVEL = logging.DEBUG
# LOGGING_FILE_LEVEL = logging.INFO
# LOGGING_FILE_LEVEL = logging.WARNING
# LOGGING_FILE_LEVEL = logging.ERROR
# LOGGING_FILE_LEVEL = logging.CRITICAL
LOGGING_FILE_MSG_FORMAT = LOGGING_CONSOLE_MSG_FORMAT
LOGGING_FILE_DATE_FORMAT = LOGGING_CONSOLE_DATE_FORMAT
# LOGGING_FILE_NAME = '.git-hook.post-commit.log'
LOGGING_FILE_NAME = '.git-hook.log'

# Conditionally map a time function for performance measurement
# depending on the version of Python used
if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
    from time import perf_counter as get_clock
else:
    from time import clock as get_clock


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
        logger.setLevel(logging.DEBUG)
        if LOGGING_CONSOLE_LEVEL:
            # Add the console logger to default logger
            logger.addHandler(console)


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
        if cmd_stderr:
            for line in cmd_stderr.strip().decode("utf-8").splitlines():
                logging.info("stderr line: %s", line)

    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        end_time = get_clock()
        logging.info(
            "Program %s called by %s failed! -- Exiting.",
            cmd,
            cmd_source,
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
            "Program %s called by %s caused on OS error %s! -- Exiting.",
            cmd,
            cmd_source,
            err.errno,
            exc_info=True
        )
        logging.error(
            "Program %s caused OS error %s! -- Exiting.",
            cmd,
            err.errno
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
    logging.info('Entered function')

    cmd = ['git', 'ls-files']

    # Get a list of all files in the current repository branch
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='git_ls_files')

    end_time = get_clock()
    logging.info('Elapsed time: %f', (end_time - start_time))

    # Return from the function
    return cmd_stdout


def get_modified_files():
    """Find files that were modified by the commit.

    Arguments:
        None

    Returns:
        A list of filenames.
    """

    # Display input parameters
    start_time = get_clock()
    logging.debug('Entered function')

    modified_file_list = []
    cmd = ['git', 'diff-tree', 'HEAD~1', 'HEAD', '--name-only', '-r',
           '--diff-filter=ACMRT']

    # Fetch the list of files modified by the last commit
    cmd_stdout = execute_cmd(cmd=cmd, cmd_source='get_modified_files')

    # Convert the stdout stream to a list of files
    modified_file_list = cmd_stdout.decode('utf8').splitlines()
    logging.debug('modified_file_list: %s', cmd)

    # Deal with unmodified repositories
    if modified_file_list and modified_file_list[0] == 'clean':
        end_time = get_clock()
        logging.info('No modified files found')
        logging.info('Elapsed time: %f', (end_time - start_time))
        exit(0)

    # Only return regular files.
    modified_file_list = [i for i in modified_file_list if os.path.isfile(i)]

    end_time = get_clock()
    logging.debug('modified_file_list: %s', cmd)
    logging.info('Elapsed time: %f', (end_time - start_time))

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
    logging.debug('files: %s', files)
    logging.info('Elapsed time: %f', (end_time - start_time))

    # Return from the function
    return files


def check_out_file(file_name):
    """Checkout file that was been modified by the latest commit.

    Arguments:
        file_name -- the file name to be checked out for smudging

    Returns:
        Nothing.
    """

    # Display input parameters
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('file_name: %s', file_name)

    # Remove the file if it currently exists
    try:
        os.remove(file_name)
    except OSError as err:
        # Ignore a file not found error, it was being removed anyway
        if err.errno != errno.ENOENT:
            end_time = get_clock()
            logging.info(
                "File removal of %s caused on OS error %d! -- Exiting.",
                file_name,
                err.errno,
                exc_info=True
            )
            logging.error(
                "File removal %s caused OS error %d! -- Exiting.",
                file_name,
                err.errno
            )
            logging.info('Elapsed time: %f', (end_time - start_time))
            exit(err.errno)

    cmd = ['git', 'checkout', '-f', '%s' % file_name]

    # Check out the file so that it is smudged
    execute_cmd(cmd=cmd, cmd_source='check_out_file')

    end_time = get_clock()
    logging.info('Elapsed time: %f', (end_time - start_time))


def post_commit():
    """Main program.

    Arguments:
        None

    Returns:
        Nothing
    """

    # Display input parameters
    start_time = get_clock()
    logging.info('Entered function')

    # Check if git is available.
    check_for_cmd(cmd=['git', '--version'])

    # Get the list of modified files
    committed_files = get_modified_files()
    logging.debug('committed_files: %s', committed_files)

    # Filter the list of modified files to exclude those modified since
    # the commit
    committed_files = remove_modified_files(files=committed_files)
    logging.debug('committed_files: %s', committed_files)

    # Force a checkout of the remaining file list
    # Process the remaining file list
    files_processed = 0
    if committed_files:
        committed_files.sort()
        for file_name in committed_files:
            check_out_file(file_name=file_name)
            files_processed += 1

    end_time = get_clock()
    logging.debug('files processed: %s', files_processed)
    logging.info('Elapsed time: %f', (end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    configure_logging()

    START_TIME = get_clock()
    logging.debug('Entered module')

    post_commit()

    END_TIME = get_clock()
    logging.info('Elapsed time: %f', (END_TIME - START_TIME))

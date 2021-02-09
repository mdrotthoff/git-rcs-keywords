#! /usr/bin/env python
# # -*- coding: utf-8 -*

"""
rcs-keywords-filter-smudge

This module provides the code to smudge the local copy of the
file retreived from the git repository performing the various
keyword substitutions.
"""

import sys
import re
import subprocess
import logging

__author__ = "David Rotthoff"
__email__ = "drotthoff@gmail.com"
__version__ = "git-rcs-keywords-1.1.0"
__date__ = "2021-02-07 10:51:24"
__credits__ = []
__status__ = "Production"

# LOGGING_CONSOLE_LEVEL = None
# LOGGING_CONSOLE_LEVEL = logging.DEBUG
# LOGGING_CONSOLE_LEVEL = logging.INFO
# LOGGING_CONSOLE_LEVEL = logging.WARNING
LOGGING_CONSOLE_LEVEL = logging.ERROR
# LOGGING_CONSOLE_LEVEL = logging.CRITICAL
LOGGING_CONSOLE_MSG_FORMAT = '%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(lineno)s: %(message)s'
LOGGING_CONSOLE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

LOGGING_FILE_LEVEL = None
# LOGGING_FILE_LEVEL = logging.DEBUG
# LOGGING_FILE_LEVEL = logging.INFO
# LOGGING_FILE_LEVEL = logging.WARNING
# LOGGING_FILE_LEVEL = logging.ERROR
# LOGGING_FILE_LEVEL = logging.CRITICAL
LOGGING_FILE_MSG_FORMAT = LOGGING_CONSOLE_MSG_FORMAT
LOGGING_FILE_DATE_FORMAT = LOGGING_CONSOLE_DATE_FORMAT
LOGGING_FILE_NAME = '.git-hook.smudge.log'

# Conditionally map a time function for performance measurement
# depending on the version of Python used
if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
    from time import perf_counter as get_clock
else:
    from time import clock as get_clock


def configure_logging():
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


def git_log_attributes(git_field_log, file_name, git_field_name):
    """Function to dump the git log associated with the provided
    file name.

    Arguments:
        git_field_log -- a list of git log fields to capture
        file_name -- The full file name to be examined
        git_field_name -- Name of the attributes fields for the dictionary

    Returns:
        git_log -- List of defined attribute dictionaries
    """

    # Display input parameters
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('git_field_log %s' % git_field_log)
    logging.debug('file_name: %s' % file_name)
    logging.debug('git_field_name: %s' % git_field_name)

    # Format the git log command
    git_field_format = '%x1f'.join(git_field_log) + '%x1e'
    cmd = ['git',
           'log',
           '--date=iso8601',
           '--max-count=1',
           '--format=%s' % git_field_format,
           '--',
           str(file_name)]
    logging.debug('cmd: %s' % cmd)

    # Process the git log command
    try:
        cmd_handle = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        (cmd_stdout, cmd_stderr) = cmd_handle.communicate()
        if cmd_stderr:
            for line in cmd_stderr.strip().decode("utf-8").splitlines():
                sys.stderr.write("%s\n" % line)
    # If the command fails, notify the user and exit immediately
    except subprocess.CalledProcessError as err:
        # sys.stderr.write(
        #     "{0} - Program {1} called by {2} not found! -- Exiting."
        #     .format(str(err), str(cmd[0]), str(' '.join(cmd)))
        # )
        logging.info(
            "Program %s call failed! -- Exiting." % cmd,
            exc_info=True
        )
        logging.error(
            "Program %s call failed! -- Exiting." % cmd
        )
        exit(err.returncode)
    except OSError as err:
        logging.info(
            "Program %s caused on OS error! -- Exiting."
            % cmd,
            exc_info=True
        )
        logging.error(
            "Program %s caused OS error %s! -- Exiting."
            % (cmd, err.errno)
        )
        exit(err.errno)

    # If an error occurred, display the command output and exit
    # with the returned exit code
    if cmd_handle.returncode != 0:
        logging.info(
            "Exiting -- git log return error code: %d" % cmd_handle.returncode,
            exc_info=True
        )
        logging.error(
            "Exiting -- git log return error code: %d" % cmd_handle.returncode
        )
        logging.info(
            "Output text: %s"
            % cmd_stdout.strip().decode("utf-8")
        )
        exit(cmd_handle.returncode)

    # Calculate replacement strings based on the git log results
    if cmd_stdout:
        # Convert returned values to a list of dictionaries
        git_output = cmd_stdout.strip().decode("utf-8")
        git_log = git_output.strip().split("\x1e")
        git_log = [row.strip().split("\x1f") for row in git_log]
        git_log = [dict(zip(git_field_name, row)) for row in git_log]
    else:
        git_log = []

    if not git_log:
        logging.error('No git attributes returned')
        exit(4)

    if len(git_log) > 1:
        logging.error('More than one row of git attributes returned')
        exit(3)

    # Log the results of the git log operation
    end_time = get_clock()
    logging.debug('git_log: %s' % git_log)
    logging.info('Elapsed time: %f' % (end_time - start_time))

    # Return from the function
    return git_log


def build_regex_dict(git_field_log, file_name, git_field_name):
    """Function to converts a 1 row list of git log attributes into
    dictionary of regex expressions.

    Arguments:
        git_field_log -- a list of git log fields to capture
        file_name -- The full file name to be examined
        git_field_name -- Name of the attributes fields for the dictionary

    Returns:
        regex_dict -- Array of defined attribute dictionaries
    """

    # Display input parameters
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('git_field_log %s' % git_field_log)
    logging.debug('file_name: %s' % file_name)
    logging.debug('git_field_name: %s' % git_field_name)

    # Format the git log command
    git_log = git_log_attributes(git_field_log=git_field_log,
                                 file_name=file_name,
                                 git_field_name=git_field_name)

    logging.debug('git_log %s' % git_log)

    regex_dict = {}
    if git_log:
        logging.debug('Calculating regex dictionary')
        # Calculate the replacement strings based on the git log results
        # Deal with values in author name that have a Windows domain name
        if '\\' in git_log[0]['author_name']:
            git_log[0]['author_name'] = git_log[0]['author_name'].split('\\')[-1]

        regex_dict['git_hash'] = '$Hash:     %s $' % str(git_log[0]['hash'])
        regex_dict['git_short_hash'] = '$Short Hash:     %s $' % str(git_log[0]['short_hash'])
        regex_dict['git_author'] = '$Author:   %s <%s> $' % (str(git_log[0]['author_name']),
                                                             str(git_log[0]['author_email']))
        regex_dict['git_date'] = '$Date:     %s $' % str(git_log[0]['commit_date'])
        regex_dict['git_rev'] = '$Rev:      %s $' % str(git_log[0]['commit_date'])
        regex_dict['git_revision'] = '$Revision: %s $' % str(git_log[0]['commit_date'])
        regex_dict['git_file'] = '$File:     %s $' % str(file_name)
        regex_dict['git_source'] = '$Source:   %s $' % str(file_name)
        regex_dict['git_id'] = '$Id:       %s | %s | %s $' % (str(file_name),
                                                              str(git_log[0]['commit_date']),
                                                              str(git_log[0]['author_name']))

    else:
        logging.debug('Building empty regex dictionary')

        # Build a empty keyword list if no source data was found
        # Note: the unusual means of building the list is to keep
        #       the code from being modified while using keywords!
        regex_dict['git_hash'] = '$%s$' % 'Hash'
        regex_dict['git_author'] = '$%s$' % 'Author'
        regex_dict['git_date'] = '$%s$' % 'Date'
        regex_dict['git_rev'] = '$%s$' % 'Rev'
        regex_dict['git_revision'] = '$%s$' % 'Revision'
        regex_dict['git_file'] = '$%s$' % 'File'
        regex_dict['git_source'] = '$%s$' % 'Source'
        regex_dict['git_id'] = '$%s$' % 'Id'

    # Log the results of the build regex dictionary operation
    end_time = get_clock()
    logging.info('Elapsed time: %f' % (end_time - start_time))

    return regex_dict


def smudge():
    """Main program.

    Arguments:
        argv: command line arguments

    Returns:
        Nothing
    """

    # Display the parameters passed on the command line
    start_time = get_clock()
    logging.info('Entered function')
    logging.debug('sys.argv parameter count %d' % len(sys.argv))
    logging.debug('sys.argv parameters %s' % sys.argv)

    # Calculate the source file being smudged
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = '<Unknown file>'
    logging.debug('File name parameter %s' % file_name)

    # Define the fields to be extracted from the commit log
    git_field_name = ['hash', 'author_name', 'author_email', 'commit_date', 'short_hash']
    git_field_log = ['%H', '%an', '%ae', '%ci', '%h']

    # Define the various substitution regular expressions
    author_regex = re.compile(r"\$Author: +[.\w@<> ]+ +\$|\$Author\$",
                              re.IGNORECASE)
    id_regex = re.compile(r"\$Id: +.+ \| [-:\d ]+ \| .+ +\$|\$Id\$",
                          re.IGNORECASE)
    date_regex = re.compile(r"\$Date: +[-:\d ]+ +\$|\$Date\$",
                            re.IGNORECASE)
    source_regex = re.compile(r"\$Source: .+[.].+ \$|\$Source\$",
                              re.IGNORECASE)
    file_regex = re.compile(r"\$File: .+[.].+ \$|\$File\$",
                            re.IGNORECASE)
    revision_regex = re.compile(r"\$Revision: +[-:\d ]+ +\$|\$Revision\$",
                                re.IGNORECASE)
    rev_regex = re.compile(r"\$Rev: +[-:\d ]+ +\$|\$Rev\$",
                           re.IGNORECASE)
    hash_regex = re.compile(r"\$Hash: +\w+ +\$|\$Hash\$",
                            re.IGNORECASE)

    regex_dict = {}

    # Process each of the rows found on stdin
    line_count = 0
    try:
        for line in sys.stdin:
            line_count += 1
            if line.count('$') > 1:
                if len(regex_dict) == 0:
                    regex_dict = build_regex_dict(git_field_log=git_field_log,
                                                  file_name=file_name,
                                                  git_field_name=git_field_name)

                line = author_regex.sub(regex_dict['git_author'], line)
                line = id_regex.sub(regex_dict['git_id'], line)
                line = date_regex.sub(regex_dict['git_date'], line)
                line = source_regex.sub(regex_dict['git_source'], line)
                line = file_regex.sub(regex_dict['git_file'], line)
                line = revision_regex.sub(regex_dict['git_revision'], line)
                line = rev_regex.sub(regex_dict['git_rev'], line)
                line = hash_regex.sub(regex_dict['git_hash'], line)
            sys.stdout.write(line)
    except UnicodeDecodeError as err:
        logging.info('UnicodeDecodeError with file %s'
                     % file_name, exc_info=True)
        logging.debug('Generic exception variables: %s' % vars(err))
        logging.error('Unicode error in file %s - Keywords not replaced'
                      % file_name)
        exit(5)
    except Exception as err:
        logging.info('Generic exception smudging file %s'
                     % file_name,
                     exc_info=True)
        logging.debug('Generic exception variables: %s' % vars(err))
        logging.error('Exception smudging file %s - Keywords not replaced'
                      % file_name)
        exit(2)

    end_time = get_clock()
    logging.info('Line count: %d' % line_count)
    logging.info('Elapsed time: %f' % (end_time - start_time))


# Execute the main function
if __name__ == '__main__':
    configure_logging()

    start_time = get_clock()
    logging.debug('Entered module')

    smudge()

    end_time = get_clock()
    logging.info('Elapsed time: %f' % (end_time - start_time))
